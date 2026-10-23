"""Testes do braço MANÔMETRO — offline, stdlib, sem rede."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from core.evidence import verify
from manometro.__main__ import analisar
from manometro.campos import ler
from manometro.carga import carregar_exportacao
from manometro.dedup import deduplicar
from manometro.kpis import calcular
from manometro.matriz import carregar, normalizar
from manometro.relatorio import renderizar

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "manometro" / "fixtures" / "demo-xdome.json"


def doc(aid, upd, status="Unresolved", uid="d1", ts=None):
    return {
        "@timestamp": ts or upd,
        "data_stream": {"dataset": "claroty_xdome.alert"},
        "claroty_xdome": {"alert": {"id": aid, "updated_time": upd, "status": status,
                                    "detected_time": "2026-03-01T00:00:00Z", "category": "Threat",
                                    "device": {"uid": uid, "category": "OT"},
                                    "mitre_technique": {"ics": {"ids": ["T0846"]}}}},
    }


class CatalogoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat = carregar()

    def test_contagens_oficiais_v20(self):
        self.assertEqual(self.cat["attack_version"], "20.0")
        self.assertEqual(self.cat["counts"], {"tactics": 12, "techniques": 78, "subtechniques": 26})
        self.assertEqual(len(self.cat["_subs"]), 26)
        self.assertEqual(self.cat["tactics"][0]["name"], "Initial Access")
        self.assertEqual(self.cat["tactics"][-1]["name"], "Impact")

    def test_revogado_remapeado(self):
        n = normalizar(["T0855", "t0846", "T1059", " "], self.cat)
        self.assertEqual(n["validos"], ["T1692.001", "T0846"])
        self.assertEqual(n["remapeados"], [("T0855", "T1692.001")])
        self.assertEqual(n["fora"], ["T1059"])

    def test_tecnica_multitatica(self):
        self.assertIn("lateral-movement", self.cat["_tecnicas"]["T0866"]["tactics"])
        self.assertIn("initial-access", self.cat["_tecnicas"]["T0866"]["tactics"])


class DedupTest(unittest.TestCase):
    def test_estado_mais_recente_vence(self):
        docs = [doc("a", "2026-03-01T10:00:00Z"), doc("a", "2026-03-02T10:00:00Z", "Resolved"),
                doc("a", "2026-03-01T12:00:00Z")]
        alertas, est = deduplicar(docs)
        self.assertEqual(len(alertas), 1)
        self.assertEqual(alertas[0]["status"], "Resolved")
        self.assertEqual(est["fator_inflacao"], 3.0)

    def test_fanout_de_dispositivos_do_snapshot_vigente(self):
        docs = [doc("a", "2026-03-01T10:00:00Z", uid="velho"),
                doc("a", "2026-03-02T10:00:00Z", uid="d1", ts="2026-03-02T10:01:00Z"),
                doc("a", "2026-03-02T10:00:00Z", uid="d2", ts="2026-03-02T10:01:00Z"),
                doc("a", "2026-03-02T10:00:00Z", uid="d1", ts="2026-03-02T16:00:00Z")]
        alertas, _ = deduplicar(docs)
        self.assertEqual([d["uid"] for d in alertas[0]["dispositivos"]], ["d1", "d2"])

    def test_campo_achatado_e_aninhado(self):
        self.assertEqual(ler({"claroty_xdome.alert.id": "x"}, "alert_id"), "x")
        self.assertEqual(ler({"claroty_xdome": {"alert.id": "y"}}, "alert_id"), "y")
        self.assertIsNone(ler({}, "alert_id"))


class DemoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env = analisar(DEMO, "2026-01", "2026-10")
        cls.k = cls.env["payload"]["kpis"]

    def test_envelope_integro_e_adulteracao(self):
        self.assertTrue(verify(self.env))
        alterado = copy.deepcopy(self.env)
        alterado["payload"]["kpis"]["alertas"]["no_periodo"] = 999
        self.assertFalse(verify(alterado))

    def test_numeros_do_caso_demo(self):
        k = self.k
        self.assertEqual(k["alertas"]["no_periodo"], 17)
        self.assertEqual(k["alertas"]["abertos"], 16)
        self.assertEqual((k["alertas"]["comportamento"], k["alertas"]["exposicao"]), (9, 8))
        self.assertGreater(k["coleta"]["documentos_alerta"], 20 * k["coleta"]["alertas_unicos_total"])
        self.assertEqual(k["dispositivos"]["distintos"], sum(k["dispositivos"]["por_categoria"].values()))
        self.assertGreater(k["dispositivos"]["soma_contagens_fornecedor"], k["dispositivos"]["distintos"])

    def test_matriz_separa_comportamento(self):
        t = self.k["matriz"]["totais"]
        self.assertEqual(t["tecnicas_total"], 78)
        self.assertLess(t["tecnicas_com_comportamento"], t["tecnicas_com_alerta"])
        q = self.k["matriz"]["qualidade"]
        self.assertIn("T0855", {x["de"] for x in q["remapeados"]})
        self.assertEqual({x["id"] for x in q["fora_do_ics"]}, {"T1059"})

    def test_baseline_de_configuracao(self):
        fora = [p for p in self.k["config"]["pares"] if not p["no_baseline"]]
        self.assertEqual({(p["origem"], p["destino"]) for p in fora}, {("PC-17", "PLC-04"), ("SCADA-02", "HMI-07")})
        self.assertFalse(self.k["config"]["pares"][0]["no_baseline"], "pares fora do baseline vêm primeiro")

    def test_saude_da_coleta(self):
        self.assertEqual(self.k["saude"]["status"], "com_erros")
        self.assertEqual(self.k["recomendacoes"][0]["prioridade"], "alta")

    def test_seletor_de_periodo(self):
        k = analisar(DEMO, "2026-10", "2026-10")["payload"]["kpis"]
        self.assertEqual(k["alertas"]["no_periodo"], 2)
        todos = analisar(DEMO)["payload"]["kpis"]
        self.assertEqual(todos["periodo"]["de"], "2025-11")
        self.assertEqual(todos["alertas"]["no_periodo"], 19)

    def test_periodo_invalido(self):
        with self.assertRaises(ValueError):
            analisar(DEMO, "2026-13", None)
        with self.assertRaises(ValueError):
            analisar(DEMO, "2026-10", "2026-01")

    def test_relatorio_html_autocontido(self):
        pagina = renderizar(self.env)
        self.assertIn(self.env["digest"], pagina)
        self.assertNotIn("http://", pagina.replace("http://www.w3.org", ""))
        self.assertNotIn("<script src", pagina)
        self.assertIn("ATT&amp;CK for ICS v20.0", pagina)

    def test_nao_muta_entrada(self):
        exp = carregar_exportacao(DEMO)
        antes = copy.deepcopy(exp["docs"][:50])
        calcular(exp, carregar(), "2026-01", "2026-10")
        self.assertEqual(exp["docs"][:50], antes)


class TravaSinteticaTest(unittest.TestCase):
    def test_rejeita_exportacao_nao_sintetica(self):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = Path(tmp) / "real.json"
            caminho.write_text(json.dumps({"schema": "caldeira.manometro.synthetic.v1", "docs": []}))
            with self.assertRaisesRegex(ValueError, "sintéticas"):
                carregar_exportacao(caminho)


if __name__ == "__main__":
    unittest.main()


class GrafoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from manometro import grafo
        cls.mod = grafo
        cls.g = grafo.carregar()
        cls.env = analisar(DEMO, "2026-01", "2026-10")
        cls.gr = cls.env["payload"]["kpis"]["grafo"]

    def test_grafo_derivado_do_stix_v20(self):
        self.assertEqual(self.g["attack_version"], "20.0")
        self.assertEqual(self.g["contagens"], {"grupo": 14, "campanha": 10, "software": 25, "tecnica": 104})
        self.assertIn(["C0028", "attributed-to", "G0034"], self.g["arestas"])
        self.assertEqual(self.g["source_sha256"], carregar()["source_sha256"])

    def test_atlas_caldeira_ligado_a_campanhas(self):
        casos = self.mod.casos_por_ref()
        self.assertEqual(casos["C0028"][0]["id"], "CAL-CASE-001")
        self.assertEqual(casos["S1045"][0]["id"], "CAL-CASE-004")

    def test_cruzamento_usa_so_comportamento_e_avisa(self):
        self.assertEqual(self.gr["natureza"], "comportamento")
        self.assertIn("não é atribuição", self.gr["aviso"])
        self.assertNotIn("T0866", self.gr["tecnicas_base"], "SMBv1 (exposição) não entra na base")
        topo = self.gr["entidades"][0]
        self.assertEqual(topo["id"], "S1045")
        self.assertEqual(len(topo["tecnicas_comuns"]), len(self.gr["tecnicas_base"]))

    def test_grupo_herda_tecnicas_das_campanhas_atribuidas(self):
        sandworm = next(e for e in self.gr["entidades"] if e["id"] == "G0034")
        self.assertTrue(sandworm["tecnicas_via_campanha"])
        self.assertIn("C0028", sandworm["campanhas"])
        self.assertTrue(any(rel == "uses-via-campaign" for a, rel, b in self.gr["arestas"] if a == "G0034"))

    def test_natureza_todas_amplia_base(self):
        alertas = self.env["payload"]["kpis"]["alertas"]["lista"]
        todas = self.mod.cruzar(alertas, self.g, natureza="todas")
        self.assertIn("T0866", todas["tecnicas_base"])
        self.assertGreater(len(todas["tecnicas_base"]), len(self.gr["tecnicas_base"]))

    def test_graphml_valido(self):
        import xml.etree.ElementTree as ET
        raiz = ET.fromstring(self.mod.graphml(self.gr).split("\n", 1)[1])
        ns = {"g": "http://graphml.graphdrawing.org/xmlns"}
        ids = {n.get("id") for n in raiz.iterfind(".//g:node", ns)}
        self.assertIn("G0034", ids)
        self.assertIn("xd-0043", ids)
        self.assertEqual(len(raiz.findall(".//g:edge", ns)), len(self.gr["arestas"]))

    def test_relatorio_tem_grafo_interativo(self):
        pagina = renderizar(self.env)
        self.assertIn('id="grafo"', pagina)
        self.assertIn('data-id="S1045"', pagina)
        self.assertIn("não é atribuição", pagina)

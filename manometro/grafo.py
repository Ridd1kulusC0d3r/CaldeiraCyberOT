"""Grafo de inteligência: atores, campanhas, software e técnicas do ATT&CK for ICS.

`construir()` deriva nós e arestas do bundle STIX oficial (relações `uses` e
`attributed-to`), sem descrições, só identificadores, nomes, apelidos e
datas. `cruzar()` compara as técnicas dos alertas do período com o que cada
grupo, campanha e software usa e devolve um ranking de *sobreposição*.

Regra editorial: sobreposição de técnicas NÃO é atribuição. Muitos atores
usam as mesmas técnicas comuns (ex.: Remote System Discovery). O ranking
serve para priorizar hipóteses de caça e leitura de relatórios, nunca para
dizer "foi o grupo X".
"""
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

GRAFO_PADRAO = Path(__file__).resolve().parent / "dados" / "attack-ics-v20.0-grafo.json"
CASOS_PADRAO = Path(__file__).resolve().parents[1] / "catalogo" / "casos.json"
TIPOS = {"intrusion-set": "grupo", "campaign": "campanha", "malware": "software", "tool": "software",
         "attack-pattern": "tecnica"}
URL_BASE = {"grupo": "groups", "campanha": "campaigns", "software": "software", "tecnica": "techniques"}
AVISO = "Sobreposição de técnicas não é atribuição: hipóteses para caça e leitura, não conclusão."


def _ext(obj):
    for ref in obj.get("external_references", []):
        if ref.get("source_name") == "mitre-attack":
            return ref.get("external_id")
    return None


def _url(tipo, ident):
    return f"https://attack.mitre.org/{URL_BASE[tipo]}/{ident.replace('.', '/')}/"


def construir(caminho_stix):
    bruto = Path(caminho_stix).read_bytes()
    objs = json.loads(bruto)["objects"]
    por_id = {o["id"]: o for o in objs}
    colecao = next(o for o in objs if o["type"] == "x-mitre-collection")

    def ativo(o):
        return not o.get("revoked") and not o.get("x_mitre_deprecated")

    nos = {}
    for o in objs:
        tipo = TIPOS.get(o["type"])
        if not tipo or not ativo(o) or not _ext(o):
            continue
        ident = _ext(o)
        no = {"id": ident, "tipo": tipo, "nome": o["name"]}
        apelidos = [a for a in o.get("aliases", o.get("x_mitre_aliases", [])) if a != o["name"]]
        if apelidos:
            no["apelidos"] = apelidos
        for campo, chave in (("first_seen", "inicio"), ("last_seen", "fim")):
            if o.get(campo):
                no[chave] = o[campo][:7]
        nos[ident] = no

    arestas = set()
    for r in objs:
        if r["type"] != "relationship" or not ativo(r) or r["relationship_type"] not in ("uses", "attributed-to"):
            continue
        src, dst = por_id.get(r["source_ref"]), por_id.get(r["target_ref"])
        if not src or not dst:
            continue
        a, b = _ext(src), _ext(dst)
        if a in nos and b in nos:
            arestas.add((a, r["relationship_type"], b))

    return {
        "schema": "caldeira.manometro.attack_ics_grafo.v1",
        "attack_version": colecao.get("x_mitre_version"),
        "source_sha256": hashlib.sha256(bruto).hexdigest(),
        "license_note": "Derivado do MITRE ATT&CK(R) for ICS. (c) The MITRE Corporation. Termos de uso: "
                        "https://attack.mitre.org/resources/legal-and-branding/terms-of-use/",
        "contagens": {t: sum(1 for n in nos.values() if n["tipo"] == t) for t in ("grupo", "campanha", "software", "tecnica")},
        "nos": [nos[k] for k in sorted(nos)],
        "arestas": [list(e) for e in sorted(arestas)],
    }


def carregar(caminho=GRAFO_PADRAO):
    g = json.loads(Path(caminho).read_text(encoding="utf-8"))
    if g.get("schema") != "caldeira.manometro.attack_ics_grafo.v1":
        raise ValueError("Grafo ATT&CK em formato desconhecido.")
    return g


def casos_por_ref(caminho=CASOS_PADRAO):
    """ID ATT&CK (C…/S…/G…) -> [casos do atlas do Caldeira]."""
    try:
        dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
    except OSError:
        return {}
    mapa = {}
    for caso in dados.get("cases", []):
        for ref in caso.get("attack_refs", []):
            mapa.setdefault(ref, []).append({"id": caso["id"], "titulo": caso["title"]})
    return mapa


def _pai(t):
    return t.split(".")[0]


def cruzar(alertas, grafo, natureza="comportamento", limite=6, casos=None):
    """Ranking de sobreposição entre técnicas dos alertas e entidades do grafo.

    `alertas`: lista de dicts com id, nome, natureza e ics_normalizados.
    Compara no nível da técnica-mãe (T0846.001 casa com T0846) para não
    depender de o fornecedor ou a MITRE terem descido à subtécnica.
    """
    casos = casos or {}
    nos = {n["id"]: n for n in grafo["nos"]}
    base = [a for a in alertas if natureza == "todas" or a["natureza"] == natureza]
    tec_alertas = {}
    for a in base:
        for t in a["ics_normalizados"]:
            tec_alertas.setdefault(_pai(t), set()).add(a["id"])
    if not tec_alertas:
        return {"natureza": natureza, "aviso": AVISO, "tecnicas_base": [], "entidades": [], "nos": [], "arestas": []}

    usa = {}
    atribuida = {}
    usa_software = {}
    for src, rel, dst in grafo["arestas"]:
        if rel == "attributed-to":
            atribuida.setdefault(dst, set()).add(src)
        elif nos[dst]["tipo"] == "tecnica":
            usa.setdefault(src, set()).add(_pai(dst))
        elif nos[dst]["tipo"] == "software":
            usa_software.setdefault(src, set()).add(dst)

    entidades = []
    for ident, no in nos.items():
        if no["tipo"] == "tecnica":
            continue
        proprias = usa.get(ident, set())
        via = set()
        if no["tipo"] == "grupo":
            for camp in atribuida.get(ident, ()):
                via |= usa.get(camp, set())
        todas = proprias | via
        comuns = sorted(set(tec_alertas) & todas)
        if not comuns:
            continue
        alertas_ligados = sorted(set().union(*(tec_alertas[t] for t in comuns)))
        entidades.append({
            "id": ident, "tipo": no["tipo"], "nome": no["nome"], "apelidos": no.get("apelidos", [])[:3],
            "inicio": no.get("inicio"), "fim": no.get("fim"), "url": _url(no["tipo"], ident),
            "tecnicas_comuns": comuns,
            "tecnicas_via_campanha": sorted(set(comuns) & (via - proprias)),
            "cobertura": round(len(comuns) / len(tec_alertas), 2),
            "especificidade": round(len(comuns) / len(todas), 2) if todas else 0,
            "alertas": alertas_ligados,
            "campanhas": sorted(atribuida.get(ident, ())) if no["tipo"] == "grupo" else [],
            "atribuida_a": sorted(g for g, cs in atribuida.items() if ident in cs) if no["tipo"] == "campanha" else [],
            "software": sorted(usa_software.get(ident, ())),
            "casos_caldeira": casos.get(ident, []),
        })
    entidades.sort(key=lambda e: (-len(e["tecnicas_comuns"]), -e["especificidade"], e["id"]))

    # subgrafo para desenhar: top-N de cada tipo + ligações entre eles
    escolha = []
    for tipo in ("grupo", "campanha", "software"):
        escolha += [e for e in entidades if e["tipo"] == tipo][:limite]
    ids = {e["id"] for e in escolha}
    por_ent = {e["id"]: e for e in escolha}
    arestas = set()
    for e in escolha:
        for c in e["campanhas"]:
            if c in ids:
                arestas.add((e["id"], "attributed-from", c))
        for s in e["software"]:
            if s in ids:
                arestas.add((e["id"], "uses", s))
        for t in e["tecnicas_comuns"]:
            arestas.add((e["id"], "uses-via-campaign" if t in e["tecnicas_via_campanha"] else "uses", t))
    tecnicas = sorted({t for e in escolha for t in e["tecnicas_comuns"]})
    alertas_vistos = sorted({a for t in tecnicas for a in tec_alertas[t]})
    for t in tecnicas:
        for a in sorted(tec_alertas[t]):
            arestas.add((t, "observed-in", a))
    nome_alerta = {a["id"]: a["nome"] for a in base}
    nos_desenho = (
        [{"id": i, "tipo": por_ent[i]["tipo"], "nome": por_ent[i]["nome"],
          "casos": [c["id"] for c in por_ent[i]["casos_caldeira"]]} for i in [e["id"] for e in escolha]]
        + [{"id": t, "tipo": "tecnica", "nome": nos[t]["nome"] if t in nos else t} for t in tecnicas]
        + [{"id": a, "tipo": "alerta", "nome": nome_alerta.get(a, a)} for a in alertas_vistos]
    )
    return {
        "natureza": natureza,
        "aviso": AVISO,
        "tecnicas_base": sorted(tec_alertas),
        "entidades": entidades,
        "nos": nos_desenho,
        "arestas": [list(x) for x in sorted(arestas)],
    }


def graphml(cruzamento):
    """Exporta o subgrafo do cruzamento em GraphML (Gephi, yEd, Maltego, Neo4j)."""
    ET.register_namespace("", "http://graphml.graphdrawing.org/xmlns")
    raiz = ET.Element("graphml", xmlns="http://graphml.graphdrawing.org/xmlns")
    for chave, alvo, nome in (("d0", "node", "tipo"), ("d1", "node", "nome"), ("d2", "edge", "relacao"),
                              ("d3", "node", "casos_caldeira")):
        ET.SubElement(raiz, "key", id=chave, attrib={"for": alvo, "attr.name": nome, "attr.type": "string"})
    g = ET.SubElement(raiz, "graph", id="caldeira-manometro", edgedefault="directed")
    for n in cruzamento["nos"]:
        el = ET.SubElement(g, "node", id=n["id"])
        ET.SubElement(el, "data", key="d0").text = n["tipo"]
        ET.SubElement(el, "data", key="d1").text = n["nome"]
        if n.get("casos"):
            ET.SubElement(el, "data", key="d3").text = ",".join(n["casos"])
    for i, (a, rel, b) in enumerate(cruzamento["arestas"]):
        el = ET.SubElement(g, "edge", id=f"e{i}", source=a, target=b)
        ET.SubElement(el, "data", key="d2").text = rel
    ET.indent(raiz)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(raiz, encoding="unicode") + "\n"


def _main(argv=None):
    import argparse

    p = argparse.ArgumentParser(description="Deriva o grafo compacto do STIX oficial do ATT&CK for ICS (offline).")
    p.add_argument("stix")
    p.add_argument("--saida", default=str(GRAFO_PADRAO))
    a = p.parse_args(argv)
    g = construir(a.stix)
    Path(a.saida).write_text(json.dumps(g, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    print(f"Grafo ATT&CK for ICS v{g['attack_version']}: {g['contagens']} · {len(g['arestas'])} arestas -> {a.saida}")


if __name__ == "__main__":
    _main()

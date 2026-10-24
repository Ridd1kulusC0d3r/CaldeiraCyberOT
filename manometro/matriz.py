"""Catálogo ATT&CK for ICS derivado do bundle STIX oficial da MITRE.

`construir()` lê o arquivo ics-attack.json (baixado manualmente de
https://github.com/mitre-attack/attack-stix-data) e gera um JSON compacto
com táticas na ordem da matriz, técnicas, subtécnicas e o mapa de IDs
revogados -> substitutos. Nada é inventado: o arquivo derivado guarda a
versão da coleção e o SHA-256 do bundle de origem.

`normalizar()` aplica o catálogo aos IDs que vêm do fornecedor e diz o que
aconteceu com cada um (válido, remapeado, descontinuado ou fora do ICS).
"""
import hashlib
import json
from pathlib import Path

CATALOGO_PADRAO = Path(__file__).resolve().parent / "dados" / "attack-ics-v20.0.json"
FONTE_STIX = "https://github.com/mitre-attack/attack-stix-data/blob/master/ics-attack/ics-attack-20.0.json"
AVISO_LICENCA = (
    "Nomes e IDs derivados do MITRE ATT&CK(R) for ICS. (c) The MITRE Corporation. "
    "Reproduzido e distribuído com autorização conforme os Termos de Uso do ATT&CK: "
    "https://attack.mitre.org/resources/legal-and-branding/terms-of-use/"
)


def _ext_id(obj):
    for ref in obj.get("external_references", []):
        if ref.get("source_name") == "mitre-attack":
            return ref.get("external_id")
    return None


def construir(caminho_stix):
    bruto = Path(caminho_stix).read_bytes()
    bundle = json.loads(bruto)
    objs = bundle["objects"]
    por_id = {o["id"]: o for o in objs}
    colecao = next(o for o in objs if o["type"] == "x-mitre-collection")
    matriz = next(o for o in objs if o["type"] == "x-mitre-matrix")

    ativos = [
        o for o in objs
        if o["type"] == "attack-pattern" and not o.get("revoked") and not o.get("x_mitre_deprecated")
    ]
    subs_por_pai = {}
    tecnicas = {}
    for o in ativos:
        tid = _ext_id(o)
        if o.get("x_mitre_is_subtechnique"):
            subs_por_pai.setdefault(tid.split(".")[0], []).append({"id": tid, "name": o["name"]})
        else:
            tecnicas[tid] = {
                "id": tid,
                "name": o["name"],
                "phases": [p["phase_name"] for p in o.get("kill_chain_phases", [])],
            }
    for lista in subs_por_pai.values():
        lista.sort(key=lambda s: s["id"])

    taticas = []
    for ref in matriz["tactic_refs"]:
        t = por_id[ref]
        curto = t["x_mitre_shortname"]
        membros = sorted(
            (x for x in tecnicas.values() if curto in x["phases"]), key=lambda x: x["name"].lower()
        )
        taticas.append({
            "id": _ext_id(t),
            "shortname": curto,
            "name": t["name"],
            "techniques": [
                {"id": m["id"], "name": m["name"], "subtechniques": subs_por_pai.get(m["id"], [])}
                for m in membros
            ],
        })

    revogados, descontinuados = {}, []
    for o in objs:
        if o["type"] != "attack-pattern":
            continue
        tid = _ext_id(o)
        if o.get("revoked") and tid:
            alvo = [
                por_id[r["target_ref"]] for r in objs
                if r["type"] == "relationship" and r.get("relationship_type") == "revoked-by"
                and r["source_ref"] == o["id"]
            ]
            if alvo:
                revogados[tid] = _ext_id(alvo[0])
        elif o.get("x_mitre_deprecated") and tid:
            descontinuados.append(tid)

    return {
        "schema": "caldeira.manometro.attack_ics.v1",
        "attack_version": colecao.get("x_mitre_version"),
        "collection_modified": colecao.get("modified"),
        "source": FONTE_STIX,
        "source_sha256": hashlib.sha256(bruto).hexdigest(),
        "license_note": AVISO_LICENCA,
        "counts": {
            "tactics": len(taticas),
            "techniques": len(tecnicas),
            "subtechniques": sum(len(v) for v in subs_por_pai.values()),
        },
        "tactics": taticas,
        "revoked": dict(sorted(revogados.items())),
        "deprecated": sorted(descontinuados),
    }


def carregar(caminho=CATALOGO_PADRAO):
    cat = json.loads(Path(caminho).read_text(encoding="utf-8"))
    if cat.get("schema") != "caldeira.manometro.attack_ics.v1":
        raise ValueError("Catálogo ATT&CK for ICS em formato desconhecido.")
    tecnicas, subs = {}, {}
    for tatica in cat["tactics"]:
        for t in tatica["techniques"]:
            tecnicas.setdefault(t["id"], {"name": t["name"], "tactics": []})["tactics"].append(tatica["shortname"])
            for s in t["subtechniques"]:
                subs[s["id"]] = {"name": s["name"], "parent": t["id"]}
    cat["_tecnicas"] = tecnicas
    cat["_subs"] = subs
    return cat


def normalizar(ids, catalogo):
    """Classifica cada ID do fornecedor contra o catálogo carregado.

    Retorna dict com:
      validos   -> IDs ativos (técnicas ou subtécnicas) após remapeamento
      remapeados-> [(antigo, novo)] para IDs revogados com substituto
      descont   -> IDs descontinuados sem substituto
      fora      -> IDs que não pertencem ao ATT&CK for ICS (ex.: Enterprise)
    """
    validos, remapeados, descont, fora = [], [], [], []
    for bruto in ids or []:
        tid = str(bruto).strip().upper()
        if not tid:
            continue
        if tid in catalogo["revoked"]:
            novo = catalogo["revoked"][tid]
            remapeados.append((tid, novo))
            tid = novo
        if tid in catalogo["_tecnicas"] or tid in catalogo["_subs"]:
            if tid not in validos:
                validos.append(tid)
        elif tid in catalogo["deprecated"]:
            descont.append(tid)
        else:
            fora.append(tid)
    return {"validos": validos, "remapeados": remapeados, "descont": descont, "fora": fora}


def _main(argv=None):
    import argparse

    p = argparse.ArgumentParser(description="Deriva o catálogo compacto a partir do STIX oficial (offline).")
    p.add_argument("stix", help="caminho do ics-attack.json baixado do repositório oficial da MITRE")
    p.add_argument("--saida", default=str(CATALOGO_PADRAO))
    a = p.parse_args(argv)
    cat = construir(a.stix)
    Path(a.saida).write_text(json.dumps(cat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    c = cat["counts"]
    print(f"ATT&CK for ICS v{cat['attack_version']}: {c['tactics']} táticas, {c['techniques']} técnicas, "
          f"{c['subtechniques']} subtécnicas, {len(cat['revoked'])} IDs revogados mapeados -> {a.saida}")


if __name__ == "__main__":
    _main()

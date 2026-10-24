"""KPIs de OT calculados sobre alertas deduplicados (sem IO, sem rede).

Regras editoriais (as mesmas do Caldeira):
  * "técnica com alerta mapeado" != "técnica executada": o mapeamento vem
    do fornecedor e uma técnica que pertence a N táticas conta nas N;
  * alertas de postura/exposição (ex.: categoria "Risk") são separados de
    alertas de comportamento — firmware antigo não é um adversário;
  * dispositivos são contados por uid distinto, nunca somando contagens
    por alerta;
  * saúde da coleta vem junto: KPI sobre coleta quebrada é subcontagem.
"""
import re
from collections import Counter, defaultdict

from .campos import DATASET_ALERTA, DATASET_EVENTO, campos_supostos, ler
from .dedup import deduplicar, para_data
from .matriz import normalizar

POLITICA_PADRAO = {
    "status_resolvido": ["Resolved"],
    "categorias_exposicao": ["Risk"],
    "categoria_dispositivo": {"OT": "OT", "IT": "IT", "IoT": "IoT", "Medical": "Médico"},
    "eol_estados": ["End-Of-Life"],
    "eol_aviso_estados": ["End-Of-Life Notification"],
    "tipos_firmware_desatualizado": ["Outdated Firmware"],
    "tipos_protocolo_legado": {"SMBv1 Communication": "SMBv1"},
    "niveis_purdue_atencao": ["Level 2", "Level 3"],
    "tipos_evento_config": ["Configuration Download"],
    "baseline_config": [],
    "grafo_natureza": "comportamento",
    "grafo_limite": 6,
}


def _mes(dt):
    return f"{dt.year:04d}-{dt.month:02d}"


def _no_periodo(dt, de, ate):
    return dt is not None and de <= _mes(dt) <= ate


def _meses(de, ate):
    a, m = map(int, de.split("-"))
    fim = tuple(map(int, ate.split("-")))
    out = []
    while (a, m) <= fim:
        out.append(f"{a:04d}-{m:02d}")
        m += 1
        if m == 13:
            a, m = a + 1, 1
    return out


def _tipo_erro(msg):
    texto = re.sub(r"\b[0-9a-f]{8,}\b", "<id>", str(msg), flags=re.I)
    texto = re.sub(r"\d+", "<n>", texto)
    return texto.strip()[:90]


def separar(docs):
    alerta, evento, erro, outros = [], [], [], 0
    for d in docs:
        if ler(d, "erro"):
            erro.append(d)
        ds = ler(d, "dataset")
        if ds == DATASET_ALERTA:
            if not ler(d, "erro"):
                alerta.append(d)
        elif ds == DATASET_EVENTO:
            if not ler(d, "erro"):
                evento.append(d)
        elif not ler(d, "erro"):
            outros += 1
    return alerta, evento, erro, outros


def calcular(exportacao, catalogo, de=None, ate=None, grafo=None, casos=None):
    politica = {**POLITICA_PADRAO, **exportacao.get("policy", {})}
    docs = exportacao["docs"]
    docs_alerta, docs_evento, docs_erro, outros = separar(docs)
    alertas, estat_dedup = deduplicar(docs_alerta)

    datas = [para_data(a["detectado"]) for a in alertas] + [para_data(ler(e, "timestamp")) for e in docs_evento]
    datas = [d for d in datas if d]
    if not datas:
        raise ValueError("Nenhum alerta ou evento com data válida.")
    de = de or _mes(min(datas))
    ate = ate or _mes(max(datas))
    if de > ate:
        raise ValueError("Período inválido: início depois do fim.")
    ultimo_mes = ate

    # ---------------- alertas no período ----------------
    no_periodo = [a for a in alertas if _no_periodo(para_data(a["detectado"]), de, ate)]
    resolvidos = set(politica["status_resolvido"])
    cat_expo = set(politica["categorias_exposicao"])
    for a in no_periodo:
        a["natureza"] = "exposicao" if a["categoria"] in cat_expo else "comportamento"
        a["ultimo_mes"] = _mes(para_data(a["detectado"])) == ultimo_mes
        a["aberto"] = a["status"] not in resolvidos

    # ---------------- dispositivos distintos ----------------
    mapa_cat = politica["categoria_dispositivo"]
    disp = {}
    for a in no_periodo:
        for d in a["dispositivos"]:
            disp.setdefault(d["uid"], d)
    por_cat = Counter(mapa_cat.get(d["categoria"], "Sem categoria") for d in disp.values())
    soma_fornecedor = sum(int(a["fornecedor_qtd_disp"] or 0) for a in no_periodo)

    # ---------------- matriz ATT&CK for ICS ----------------
    qualidade = {"remapeados": [], "fora_do_ics": [], "descontinuados": []}
    alvo_alertas = defaultdict(list)  # técnica/sub -> [ids de alerta]
    for a in no_periodo:
        n = normalizar(a["ics_ids"], catalogo)
        a["ics_normalizados"] = n["validos"]
        for velho, novo in n["remapeados"]:
            qualidade["remapeados"].append({"alerta": a["id"], "de": velho, "para": novo})
        for x in n["fora"]:
            qualidade["fora_do_ics"].append({"alerta": a["id"], "id": x})
        for x in n["descont"]:
            qualidade["descontinuados"].append({"alerta": a["id"], "id": x})
        for tid in n["validos"]:
            if a["id"] not in alvo_alertas[tid]:
                alvo_alertas[tid].append(a["id"])
            if "." in tid:
                pai = tid.split(".")[0]
                if a["id"] not in alvo_alertas[pai]:
                    alvo_alertas[pai].append(a["id"])
    por_id = {a["id"]: a for a in no_periodo}

    def resumo(ids):
        return {
            "alertas": ids,
            "comportamento": sum(1 for i in ids if por_id[i]["natureza"] == "comportamento"),
            "exposicao": sum(1 for i in ids if por_id[i]["natureza"] == "exposicao"),
            "ultimo_mes": any(por_id[i]["ultimo_mes"] for i in ids),
        }

    taticas = []
    for t in catalogo["tactics"]:
        tecs = []
        for tec in t["techniques"]:
            tecs.append({
                "id": tec["id"], "name": tec["name"], **resumo(alvo_alertas.get(tec["id"], [])),
                "subtechniques": [
                    {"id": s["id"], "name": s["name"], **resumo(alvo_alertas.get(s["id"], []))}
                    for s in tec["subtechniques"]
                ],
            })
        com = sum(1 for x in tecs if x["alertas"])
        com_comp = sum(1 for x in tecs if x["comportamento"])
        taticas.append({
            "id": t["id"], "shortname": t["shortname"], "name": t["name"],
            "tecnicas_total": len(tecs), "tecnicas_com_alerta": com,
            "tecnicas_com_comportamento": com_comp, "techniques": tecs,
        })
    tec_com = {k for k in alvo_alertas if "." not in k}
    tec_comp = {k for k in tec_com if any(por_id[i]["natureza"] == "comportamento" for i in alvo_alertas[k])}
    subs_com = {k for k in alvo_alertas if "." in k}
    mapeados = [a for a in no_periodo if a["ics_normalizados"]]
    matriz = {
        "versao": catalogo["attack_version"],
        "fonte_sha256": catalogo["source_sha256"],
        "taticas": taticas,
        "totais": {
            "tecnicas_total": catalogo["counts"]["techniques"],
            "subtecnicas_total": catalogo["counts"]["subtechniques"],
            "taticas_total": catalogo["counts"]["tactics"],
            "tecnicas_com_alerta": len(tec_com),
            "tecnicas_com_comportamento": len(tec_comp),
            "subtecnicas_com_alerta": len(subs_com),
            "taticas_com_alerta": sum(1 for t in taticas if t["tecnicas_com_alerta"]),
            "taticas_com_comportamento": sum(1 for t in taticas if t["tecnicas_com_comportamento"]),
            "alertas_mapeados": len(mapeados),
            "alertas_ultimo_mes": sum(1 for a in no_periodo if a["ultimo_mes"]),
        },
        "qualidade": qualidade,
    }

    # ---------------- exposição de ativos ----------------
    eol = {u for u, d in disp.items() if d["eol"] in set(politica["eol_estados"])}
    eol_aviso = {u for u, d in disp.items() if d["eol"] in set(politica["eol_aviso_estados"])}
    tipos_fw = set(politica["tipos_firmware_desatualizado"])
    fw = {d["uid"] for a in no_periodo if a["tipo"] in tipos_fw for d in a["dispositivos"]}
    legado = defaultdict(lambda: defaultdict(set))
    for a in no_periodo:
        proto = politica["tipos_protocolo_legado"].get(a["tipo"])
        if proto:
            for d in a["dispositivos"]:
                legado[proto][d["purdue"] or "Sem nível"].add(d["uid"])
    atencao = set(politica["niveis_purdue_atencao"])
    ativos = {
        "eol": len(eol),
        "eol_aviso": len(eol_aviso),
        "firmware_desatualizado": len(fw),
        "obsoletos_distintos": len(eol | fw),
        "sobreposicao_eol_firmware": len(eol & fw),
        "eol_em_niveis_atencao": sum(1 for u in eol if disp[u]["purdue"] in atencao),
        "protocolo_legado": {
            p: {nivel: len(u) for nivel, u in sorted(niveis.items())} for p, niveis in sorted(legado.items())
        },
        "lista_obsoletos": sorted(
            ({"uid": u, "nome": disp[u]["nome"], "modelo": disp[u]["modelo"], "firmware": disp[u]["firmware"],
              "eol": disp[u]["eol"], "purdue": disp[u]["purdue"], "categoria": disp[u]["categoria"]}
             for u in eol | fw),
            key=lambda x: (x["purdue"] or "", x["nome"] or ""),
        ),
    }

    # ---------------- Configuration Download x baseline ----------------
    tipos_cfg = set(politica["tipos_evento_config"])
    baseline = {tuple(p) for p in politica["baseline_config"]}
    pares = Counter()
    meta = {}
    por_mes = Counter()
    for e in docs_evento:
        dt = para_data(ler(e, "timestamp"))
        if ler(e, "evt_tipo") not in tipos_cfg or not _no_periodo(dt, de, ate):
            continue
        o = ler(e, "evt_origem_nome") or ler(e, "evt_origem_ip") or "?"
        d = ler(e, "evt_destino_nome") or ler(e, "evt_destino_ip") or "?"
        pares[(o, d)] += 1
        por_mes[_mes(dt)] += 1
        meta.setdefault((o, d), (ler(e, "evt_origem_tipo"), ler(e, "evt_destino_tipo"), ler(e, "evt_protocolo")))
    lista_pares = [
        {"origem": o, "destino": d, "tipo_origem": meta[(o, d)][0], "tipo_destino": meta[(o, d)][1],
         "protocolo": meta[(o, d)][2], "eventos": n, "no_baseline": (o, d) in baseline}
        for (o, d), n in pares.most_common()
    ]
    lista_pares.sort(key=lambda x: (x["no_baseline"], -x["eventos"], x["origem"], x["destino"]))
    config = {
        "eventos": sum(pares.values()),
        "pares": lista_pares,
        "pares_fora_baseline": sum(1 for p in lista_pares if not p["no_baseline"]),
        "eventos_fora_baseline": sum(p["eventos"] for p in lista_pares if not p["no_baseline"]),
        "baseline_declarado": bool(baseline),
        "por_mes": {m: por_mes.get(m, 0) for m in _meses(de, ate)},
    }

    # ---------------- saúde da coleta ----------------
    erros = defaultdict(lambda: {"qtd": 0, "ultimo": None, "dataset": set()})
    for e in docs_erro:
        dt = para_data(ler(e, "timestamp"))
        if not _no_periodo(dt, de, ate):
            continue
        t = erros[_tipo_erro(ler(e, "erro"))]
        t["qtd"] += 1
        t["dataset"].add(ler(e, "dataset") or "?")
        if dt and (t["ultimo"] is None or dt.isoformat() > t["ultimo"]):
            t["ultimo"] = dt.isoformat()
    saude = {
        "erros": sum(v["qtd"] for v in erros.values()),
        "por_tipo": sorted(
            ({"tipo": k, "qtd": v["qtd"], "ultimo": v["ultimo"], "datasets": sorted(v["dataset"])}
             for k, v in erros.items()),
            key=lambda x: -x["qtd"],
        ),
    }
    saude["status"] = "com_erros" if saude["erros"] else "ok"

    resultado = {
        "periodo": {"de": de, "ate": ate, "ultimo_mes": ultimo_mes, "meses": _meses(de, ate)},
        "coleta": {
            "documentos_total": len(docs),
            "documentos_alerta": estat_dedup["documentos_alerta"],
            "documentos_evento": len(docs_evento),
            "documentos_erro": len(docs_erro),
            "documentos_outros": outros,
            "alertas_unicos_total": estat_dedup["alertas_unicos"],
            "fator_inflacao": estat_dedup["fator_inflacao"],
            "documentos_sem_id": estat_dedup["documentos_sem_id"],
        },
        "alertas": {
            "no_periodo": len(no_periodo),
            "abertos": sum(1 for a in no_periodo if a["aberto"]),
            "resolvidos": sum(1 for a in no_periodo if not a["aberto"]),
            "comportamento": sum(1 for a in no_periodo if a["natureza"] == "comportamento"),
            "exposicao": sum(1 for a in no_periodo if a["natureza"] == "exposicao"),
            "sem_mapeamento_ics": sum(1 for a in no_periodo if not a["ics_normalizados"]),
            "ultimo_mes": sum(1 for a in no_periodo if a["ultimo_mes"]),
            "lista": [
                {k: a[k] for k in ("id", "nome", "tipo", "categoria", "status", "historico_status", "detectado",
                                   "natureza", "aberto", "ultimo_mes", "ics_ids", "ics_normalizados",
                                   "enterprise_ids", "documentos", "coletas")}
                | {"dispositivos": len(a["dispositivos"])}
                for a in no_periodo
            ],
        },
        "dispositivos": {
            "distintos": len(disp),
            "por_categoria": dict(sorted(por_cat.items())),
            "soma_contagens_fornecedor": soma_fornecedor,
        },
        "matriz": matriz,
        "ativos": ativos,
        "config": config,
        "saude": saude,
        "campos_supostos": campos_supostos(),
    }
    if grafo is not None:
        from .grafo import cruzar

        resultado["grafo"] = cruzar(resultado["alertas"]["lista"], grafo, politica["grafo_natureza"],
                                    int(politica["grafo_limite"]), casos)
        resultado["grafo"]["attack_version"] = grafo["attack_version"]
        resultado["grafo"]["fonte_sha256"] = grafo["source_sha256"]
    resultado["recomendacoes"] = recomendar(resultado)
    return resultado


def recomendar(r):
    rec = []
    c, m, at, cfg, s = r["coleta"], r["matriz"], r["ativos"], r["config"], r["saude"]
    if s["erros"]:
        rec.append(("alta", f"Corrigir a coleta antes de decidir: {s['erros']} documento(s) com erro no período. "
                            "Os números abaixo podem estar subcontados."))
    if c["fator_inflacao"] and c["fator_inflacao"] > 1.5:
        rec.append(("alta", f"Nunca contar documentos como alertas: {c['documentos_alerta']} documentos de alerta "
                            f"viraram {c['alertas_unicos_total']} alertas únicos (fator {c['fator_inflacao']}x)."))
    q = m["qualidade"]
    if q["remapeados"]:
        ids = sorted({f"{x['de']}→{x['para']}" for x in q["remapeados"]})
        rec.append(("media", "Atualizar mapeamentos com IDs revogados no ATT&CK for ICS v" + m["versao"] + ": "
                             + ", ".join(ids) + "."))
    if q["fora_do_ics"]:
        ids = sorted({x["id"] for x in q["fora_do_ics"]})
        rec.append(("media", "IDs fora do catálogo ICS no campo ics.ids (provável Enterprise ou erro de "
                             "mapeamento): " + ", ".join(ids) + ". Não entram na cobertura."))
    t = m["totais"]
    if t["tecnicas_com_alerta"] > t["tecnicas_com_comportamento"]:
        rec.append(("media", f"Ler a matriz com filtro: {t['tecnicas_com_alerta']} técnicas têm alerta mapeado, "
                             f"mas só {t['tecnicas_com_comportamento']} têm alerta de comportamento; o restante "
                             "vem de alertas de postura/exposição."))
    if r["dispositivos"]["soma_contagens_fornecedor"] > r["dispositivos"]["distintos"]:
        rec.append(("baixa", f"Somar devices_count por alerta dá {r['dispositivos']['soma_contagens_fornecedor']}; "
                             f"dispositivos distintos são {r['dispositivos']['distintos']}. Use o distinto."))
    if at["eol_em_niveis_atencao"]:
        rec.append(("media", f"{at['eol_em_niveis_atencao']} ativo(s) em fim de vida nos níveis Purdue de atenção: "
                             "priorizar segmentação e plano de substituição com Engenharia."))
    for proto, niveis in at["protocolo_legado"].items():
        total = sum(niveis.values())
        rec.append(("media", f"{proto} em {total} dispositivo(s) ({', '.join(f'{k}: {v}' for k, v in niveis.items())}): "
                             "validar dependência operacional antes de desativar."))
    if cfg["eventos"] and not cfg["baseline_declarado"]:
        rec.append(("media", "Declarar o baseline de Configuration Download (origem→destino) com Automação."))
    elif cfg["pares_fora_baseline"]:
        rec.append(("alta", f"{cfg['pares_fora_baseline']} par(es) origem→destino de Configuration Download fora "
                            f"do baseline ({cfg['eventos_fora_baseline']} eventos): validar com Automação."))
    if r["campos_supostos"] and cfg["eventos"]:
        rec.append(("baixa", "Confirmar no índice os campos não documentados usados: " + ", ".join(r["campos_supostos"]) + "."))
    gr = r.get("grafo")
    if gr and gr["entidades"]:
        topo = gr["entidades"][0]
        rec.append(("media", f"Hipótese de caça (não atribuição): {topo['nome']} ({topo['id']}) usa "
                             f"{len(topo['tecnicas_comuns'])} das {len(gr['tecnicas_base'])} técnicas dos alertas de "
                             f"{gr['natureza']}. Revise os relatórios desse {topo['tipo']} e procure as técnicas que faltam."))
    peso = {"alta": 0, "media": 1, "baixa": 2}
    rec.sort(key=lambda x: peso[x[0]])
    return [{"prioridade": p, "texto": txt} for p, txt in rec]

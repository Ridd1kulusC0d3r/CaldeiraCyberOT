"""Relatório HTML estático e autocontido (sem CDN, sem rede, sem cookies).

O HTML é só uma *vista* do envelope selado: todo número vem do payload
JSON e o digest SHA-256 aparece no rodapé para conferência.
"""
import html
import json

E = html.escape

ROTULOS_EN = {
    "titulo": "OT KPI — Executive / Operational",
    "t_sis": "System",
    "t_claro": "Light",
    "t_escuro": "Dark",
    "sintetico": "SYNTHETIC DATA",
    "periodo": "Period",
    "saude_banner": "Collection integration has errors — numbers may be undercounted",
    "ver_saude": "see collection health",
    "k_alertas": "Unique alerts in period",
    "k_alertas_sub": "from {docs} alert documents in the file",
    "k_abertos": "Open",
    "k_abertos_sub": "{n} resolved",
    "k_disp": "Distinct impacted devices",
    "k_taticas": "ICS tactics with a mapped alert",
    "k_taticas_sub": "behaviour only: {n}/12 · {t} techniques",
    "k_obsoletos": "Obsolete OT/IT assets (distinct)",
    "k_obsoletos_sub": "{eol} EoL · {fw} outdated firmware · {ov} in both",
    "k_config": "Configuration Download events",
    "k_config_sub": "{n} out of baseline",
    "s_matriz": "MITRE ATT&CK for ICS — matrix",
    "f_todos": "All alerts",
    "f_comp": "Behaviour",
    "f_expo": "Exposure / posture",
    "f_busca": "Filter by technique, ID or alert",
    "f_expandir": "Expand sub-techniques and alerts",
    "f_mes": "Only alerts of the last month",
    "l_3": "≥3 alerts",
    "l_12": "1–2 alerts",
    "l_0": "No alerts",
    "l_mes": "Alert in last month",
    "m_tec": "ICS techniques with alert",
    "m_sub": "ICS sub-techniques with alert",
    "m_tat": "Tactics with alert",
    "m_map": "Mapped alerts",
    "m_nota": "Vendor mapping, not proof of execution. A technique that belongs to N tactics counts in all N.",
    "s_qualidade": "Mapping quality",
    "s_grafo": "Actors, campaigns and software — overlap with alerts",
    "s_ativos": "Asset exposure",
    "s_config": "Configuration Download × baseline",
    "s_saude": "Collection health",
    "s_rec": "Recommendations",
    "s_alertas": "Deduplicated alerts",
    "rodape": "Static view of a sealed envelope. SHA-256 measures integrity, not authorship.",
}


def _bar(v, m):
    pct = 0 if not m else round(100 * v / m)
    return f'<span class="bar"><i style="width:{pct}%"></i></span>'


def _classe(n):
    return "c3" if n >= 3 else ("c1" if n >= 1 else "c0")


def _tecnica(t, alertas):
    n = len(t["alertas"])
    itens = "".join(
        f'<li data-a="{E(a)}" data-nat="{alertas[a]["natureza"]}" data-mes="{int(alertas[a]["ultimo_mes"])}">'
        f'<b>#{E(a.split("-")[-1])}</b> {E(alertas[a]["nome"] or "")}'
        f'<em class="nat {alertas[a]["natureza"]}">{"C" if alertas[a]["natureza"] == "comportamento" else "E"}</em></li>'
        for a in t["alertas"]
    )
    subs = "".join(
        f'<div class="sub {_classe(len(s["alertas"]))}" data-id="{E(s["id"])}" data-c="{s["comportamento"]}" data-e="{s["exposicao"]}" '
        f'data-busca="{E((s["id"] + " " + s["name"]).lower())}"><span class="sid">{E(s["id"].split(".")[1])}</span> '
        f'{E(s["name"])}<span class="n">{len(s["alertas"]) or ""}</span></div>'
        for s in t["subtechniques"]
    )
    busca = " ".join([t["id"], t["name"]] + [alertas[a]["nome"] or "" for a in t["alertas"]]
                     + [s["id"] + " " + s["name"] for s in t["subtechniques"]]).lower()
    subs_com = sum(1 for s in t["subtechniques"] if s["alertas"])
    contador = f'<span class="subcount">{subs_com}/{len(t["subtechniques"])}</span>' if t["subtechniques"] else ""
    detalhe = ""
    if subs or itens:
        detalhe = f'<div class="det">{subs}' + (f'<p class="lbl">ALERTAS</p><ul>{itens}</ul>' if itens else "") + "</div>"
    return (
        f'<div class="tec {_classe(n)}{" mes" if t["ultimo_mes"] else ""}" data-id="{E(t["id"])}" data-c="{t["comportamento"]}" '
        f'data-e="{t["exposicao"]}" data-busca="{E(busca)}" title="{E(t["id"])}">'
        f'<div class="th"><span class="tn">{E(t["name"])}</span><span class="n">{n or ""}</span>{contador}</div>'
        f'<span class="tid">{E(t["id"])}</span>{detalhe}</div>'
    )


COLUNAS = (("grupo", "Grupos"), ("campanha", "Campanhas"), ("software", "Software"),
           ("tecnica", "Técnicas dos alertas"), ("alerta", "Alertas"))
REPO = "https://github.com/Ridd1kulusC0d3r/CaldeiraCyberOT/blob/main/"


def _marca(tipo, x, y):
    """Forma por tipo (nunca só cor): quadrado, losango, círculo, barra, triângulo."""
    if tipo == "grupo":
        return f'<rect class="mk" x="{x - 6}" y="{y - 6}" width="12" height="12"/>'
    if tipo == "campanha":
        return f'<path class="mk" d="M{x} {y - 7}L{x + 7} {y}L{x} {y + 7}L{x - 7} {y}Z"/>'
    if tipo == "software":
        return f'<circle class="mk" cx="{x}" cy="{y}" r="6"/>'
    if tipo == "tecnica":
        return f'<rect class="mk" x="{x - 8}" y="{y - 3}" width="16" height="6"/>'
    return f'<path class="mk" d="M{x - 6} {y + 5}L{x} {y - 6}L{x + 6} {y + 5}Z"/>'


def grafo_svg(gr):
    if not gr or not gr.get("nos"):
        return '<p class="nota">Sem técnicas de alerta para cruzar no período.</p>'
    largura, passo, topo = 1440, 34, 44
    xs = {"grupo": 24, "campanha": 300, "software": 590, "tecnica": 870, "alerta": 1150}
    pos, por_col = {}, {}
    for n in gr["nos"]:
        por_col.setdefault(n["tipo"], []).append(n)
    altura = topo + passo * max(len(v) for v in por_col.values()) + 20
    for tipo, lista in por_col.items():
        off = topo + (altura - topo - 20 - passo * len(lista)) // 2
        for i, n in enumerate(lista):
            pos[n["id"]] = (xs[tipo], off + i * passo + passo // 2)
    arestas = []
    for a, rel, b in gr["arestas"]:
        if a not in pos or b not in pos:
            continue
        (x1, y1), (x2, y2) = pos[a], pos[b]
        if x1 > x2:
            (x1, y1), (x2, y2), a, b = (x2, y2), (x1, y1), b, a
        mx = (x1 + x2) / 2
        tracejada = " via" if rel == "uses-via-campaign" else ""
        arestas.append(f'<path class="edge{tracejada}" data-a="{E(a)}" data-b="{E(b)}" d="M{x1 + 8} {y1}C{mx} {y1} {mx} {y2} {x2 - 8} {y2}"/>')
    cab = "".join(f'<text class="gcol" x="{xs[t] - 8}" y="22">{E(r.upper())}</text>' for t, r in COLUNAS)
    nos = []
    for n in gr["nos"]:
        x, y = pos[n["id"]]
        rotulo = n["nome"] if n["tipo"] != "alerta" else f'#{n["id"].split("-")[-1]} {n["nome"]}'
        limite = 34 if n["tipo"] == "alerta" else 24
        rotulo = rotulo if len(rotulo) <= limite else rotulo[:limite - 1] + "…"
        sufixo = f' {n["id"]}' if n["tipo"] != "alerta" else ""
        casos = f' ▣{len(n["casos"])}' if n.get("casos") else ""
        nos.append(
            f'<g class="node t-{n["tipo"]}" tabindex="0" data-id="{E(n["id"])}" role="button" '
            f'aria-label="{E(n["tipo"])} {E(n["nome"])}{E(" · atlas " + ", ".join(n["casos"])) if n.get("casos") else ""}"><title>{E(n["nome"])}{E(" · atlas Caldeira: " + ", ".join(n["casos"])) if n.get("casos") else ""}</title>{_marca(n["tipo"], x, y)}'
            f'<text x="{x + 14}" y="{y + 4}">{E(rotulo)}<tspan class="gid">{E(sufixo)}{E(casos)}</tspan></text></g>'
        )
    return (f'<div class="gwrap"><svg id="grafo" viewBox="0 0 {largura} {altura}" role="img" '
            f'aria-label="Grafo de grupos, campanhas e software que usam as técnicas dos alertas">'
            f'{cab}<g>{"".join(arestas)}</g>{"".join(nos)}</svg></div>')


def grafo_tabela(gr):
    linhas = []
    tipos = {"grupo": "grupo", "campanha": "campanha", "software": "software"}
    for e in gr.get("entidades", [])[:15]:
        casos = " ".join(f'<a href="{REPO}docs/casos-ot/README.md">{E(c["id"])}</a>' for c in e["casos_caldeira"]) or "—"
        via = f' <small>({len(e["tecnicas_via_campanha"])} via campanha)</small>' if e["tecnicas_via_campanha"] else ""
        periodo = " → ".join(x for x in (e.get("inicio"), e.get("fim")) if x) or ""
        extra = ""
        if e["atribuida_a"]:
            extra = f'<br><small>atribuída a {E(", ".join(e["atribuida_a"]))} (MITRE)</small>'
        linhas.append(
            f'<tr><td><a href="{E(e["url"])}">{E(e["nome"])}</a> <span class="id">{E(e["id"])}</span>{extra}'
            + (f'<br><small>{E(", ".join(e["apelidos"]))}</small>' if e["apelidos"] else "")
            + f'</td><td>{tipos[e["tipo"]]}</td><td class="num">{len(e["tecnicas_comuns"])}/{len(gr["tecnicas_base"])}{via}'
            f'<br><small>{E(", ".join(e["tecnicas_comuns"]))}</small></td>'
            f'<td class="num">{round(100 * e["especificidade"])}%</td><td class="num">{len(e["alertas"])}</td>'
            f'<td>{E(periodo)}</td><td>{casos}</td></tr>'
        )
    return "".join(linhas) or '<tr><td colspan="7">Nenhuma entidade com técnica em comum.</td></tr>'


def renderizar(env):
    p = env["payload"]
    k = p["kpis"]
    per, co, al, di, ma, at, cf, sa = (k[x] for x in ("periodo", "coleta", "alertas", "dispositivos", "matriz",
                                                      "ativos", "config", "saude"))
    tot = ma["totais"]
    gr = k.get("grafo", {})
    alertas = {a["id"]: a for a in al["lista"]}

    ordem = {"OT": 0, "IT": 1, "IoT": 2, "Médico": 3}
    cats = " · ".join(f"<b>{v}</b> {E(c)}" for c, v in sorted(di["por_categoria"].items(), key=lambda x: (ordem.get(x[0], 9), x[0])))
    soma_cat = sum(di["por_categoria"].values())

    colunas = "".join(
        f'<section class="col" data-total="{t["tecnicas_total"]}"><header><h4>{E(t["name"])}</h4><small class="tc">{t["tecnicas_com_alerta"]}/{t["tecnicas_total"]}'
        f' · {round(100 * t["tecnicas_com_alerta"] / t["tecnicas_total"]) if t["tecnicas_total"] else 0}%</small>'
        f'{_bar(t["tecnicas_com_alerta"], t["tecnicas_total"])}</header>'
        + "".join(_tecnica(x, alertas) for x in t["techniques"]) + "</section>"
        for t in ma["taticas"]
    )

    q = ma["qualidade"]
    linhas_q = "".join(
        f'<tr><td>{E(x["alerta"])}</td><td><code>{E(x["de"])}</code></td><td><code>{E(x["para"])}</code></td>'
        f'<td>revogado no v{E(ma["versao"])}</td></tr>' for x in q["remapeados"]
    ) + "".join(
        f'<tr><td>{E(x["alerta"])}</td><td><code>{E(x["id"])}</code></td><td>—</td><td>fora do catálogo ICS (ignorado)</td></tr>'
        for x in q["fora_do_ics"]
    ) + "".join(
        f'<tr><td>{E(x["alerta"])}</td><td><code>{E(x["id"])}</code></td><td>—</td><td>descontinuado</td></tr>'
        for x in q["descontinuados"]
    ) or '<tr><td colspan="4">Nenhum problema de mapeamento no período.</td></tr>'

    legado = "".join(
        f"<tr><td>{E(proto)}</td><td>{E(nivel)}</td><td>{qtd}</td><td>{_bar(qtd, max(niveis.values()))}</td></tr>"
        for proto, niveis in at["protocolo_legado"].items() for nivel, qtd in niveis.items()
    ) or '<tr><td colspan="4">Sem protocolo legado no período.</td></tr>'
    obsoletos = "".join(
        f'<tr><td>{E(x["nome"] or x["uid"])}</td><td>{E(x["categoria"] or "")}</td><td>{E(x["modelo"] or "")}</td>'
        f'<td><code>{E(x["firmware"] or "")}</code></td><td>{E(x["eol"] or "")}</td><td>{E(x["purdue"] or "")}</td></tr>'
        for x in at["lista_obsoletos"]
    )

    max_mes = max(cf["por_mes"].values() or [0])
    meses = "".join(
        f'<div class="mcol"><span class="mv">{v}</span><i style="height:{round(100 * v / max_mes) if max_mes else 0}%"></i>'
        f'<span class="ml">{E(m[5:])}/{E(m[2:4])}</span></div>' for m, v in cf["por_mes"].items()
    )
    pares = "".join(
        f'<tr class="{"" if x["no_baseline"] else "fora"}"><td>{E(x["origem"])} <small>{E(x["tipo_origem"] or "")}</small></td>'
        f'<td>→ {E(x["destino"])} <small>{E(x["tipo_destino"] or "")}</small></td><td>{E(x["protocolo"] or "")}</td>'
        f'<td>{x["eventos"]}</td><td>{"<span class=ok>no baseline</span>" if x["no_baseline"] else "<span class=bad>FORA do baseline</span>"}</td></tr>'
        for x in cf["pares"]
    ) or '<tr><td colspan="5">Nenhum evento de configuração no período.</td></tr>'

    erros = "".join(
        f'<tr><td>{E(x["tipo"])}</td><td>{x["qtd"]}</td><td>{E(", ".join(x["datasets"]))}</td><td>{E((x["ultimo"] or "")[:16])}</td></tr>'
        for x in sa["por_tipo"]
    ) or '<tr><td colspan="4">Nenhum erro de coleta no período.</td></tr>'

    rec = "".join(f'<li class="p-{E(r["prioridade"])}"><span>{E(r["prioridade"].upper())}</span>{E(r["texto"])}</li>'
                  for r in k["recomendacoes"])
    lista = "".join(
        f'<tr><td>{E(a["id"])}</td><td>{E(a["nome"] or "")}</td><td><em class="nat {a["natureza"]}">'
        f'{"comportamento" if a["natureza"] == "comportamento" else "exposição"}</em></td>'
        f'<td>{E(a["status"] or "")}<br><small>{E(" → ".join(str(s) for s in a["historico_status"]))}</small></td>'
        f'<td>{E((a["detectado"] or "")[:10])}</td><td>{E(", ".join(a["ics_ids"]) or "—")}'
        + (f'<br><small>→ {E(", ".join(a["ics_normalizados"]))}</small>' if a["ics_normalizados"] != a["ics_ids"] else "")
        + f'</td><td>{a["dispositivos"]}</td><td>{a["documentos"]} / {a["coletas"]}</td></tr>'
        for a in al["lista"]
    )

    banner = ""
    if sa["status"] != "ok":
        banner = (f'<a class="banner" href="#saude" data-i18n="saude_banner">⚠ Integração com erros — os números podem '
                  f'estar subcontados</a>')

    i18n = json.dumps(ROTULOS_EN, ensure_ascii=False)
    supostos = ", ".join(k["campos_supostos"]) or "nenhum"

    return f"""<!doctype html>
<html lang="pt-BR" data-theme="system">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%2317150f'/%3E%3Ccircle cx='16' cy='16' r='9' fill='none' stroke='%23f3f0e8' stroke-width='2'/%3E%3Cpath d='M16 16l6-5' stroke='%23e99754' stroke-width='3'/%3E%3C/svg%3E">
<title>Manômetro OT KPI</title>
<style>
/* Família visual LLMInjection · mesa do analista: papel, tinta, uma cor de sinal (cobre). */
:root{{--paper:#f3f0e8;--paper-2:#ebe7dc;--card:#fbf9f3;--ink:#17150f;--ink-2:#4a463c;--ink-3:#68635a;--rule:#cfc9ba;--rule-2:#e0dacb;--signal:#9c4a0c;--signal-ink:#fff;--seq-1:#ecbe92;--seq-3:#9c4a0c;--on-seq-3:#fff;--serif:Georgia,"Iowan Old Style","Times New Roman",serif;--sans:system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;color-scheme:light}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--paper:#131210;--paper-2:#1b1915;--card:#1b1915;--ink:#ece8dd;--ink-2:#b9b4a6;--ink-3:#908b7d;--rule:#37332b;--rule-2:#27241e;--signal:#e99754;--signal-ink:#131210;--seq-1:#6b4224;--seq-3:#e99754;--on-seq-3:#131210;color-scheme:dark}}}}
:root[data-theme="dark"]{{--paper:#131210;--paper-2:#1b1915;--card:#1b1915;--ink:#ece8dd;--ink-2:#b9b4a6;--ink-3:#908b7d;--rule:#37332b;--rule-2:#27241e;--signal:#e99754;--signal-ink:#131210;--seq-1:#6b4224;--seq-3:#e99754;--on-seq-3:#131210;color-scheme:dark}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:14px/1.55 var(--sans)}}
a{{color:var(--ink);text-decoration-color:var(--signal);text-underline-offset:3px}}
.wrap{{max-width:1500px;margin:0 auto;padding:0 24px 24px}}
header.top{{display:flex;flex-wrap:wrap;gap:16px;justify-content:space-between;align-items:end;border-bottom:1px solid var(--ink);padding:22px 0 18px}}
h1{{font:700 clamp(26px,3.4vw,40px)/1.05 var(--serif);letter-spacing:-.01em;margin:0}}h1 small{{display:block;margin-top:10px;font:600 11px var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}}
.tools{{display:flex;gap:8px;flex-wrap:wrap}}.seg{{display:inline-flex;border:1px solid var(--rule)}}
.seg button{{background:none;color:var(--ink-2);border:0;border-left:1px solid var(--rule);padding:6px 10px;cursor:pointer;font:600 11px var(--mono);letter-spacing:.1em;text-transform:uppercase}}.seg button:first-child{{border-left:0}}
.seg button:hover{{color:var(--ink)}}.seg button[aria-pressed="true"]{{background:var(--ink);color:var(--paper)}}
button:focus-visible,input:focus-visible,a:focus-visible{{outline:2px solid var(--signal);outline-offset:2px}}
.chips{{display:flex;gap:6px 18px;flex-wrap:wrap;margin:14px 0 4px;font:600 11px var(--mono);letter-spacing:.06em;color:var(--ink-3)}}.chip code{{font-family:var(--mono)}}
.chip.syn{{color:var(--ink);border:1px solid var(--ink);padding:1px 6px}}
.banner{{display:block;margin:10px 0 0;padding:8px 12px;border-left:3px solid var(--signal);background:var(--paper-2);color:var(--ink);text-decoration:none;font-size:13px}}.banner:hover{{color:var(--signal)}}
.cards{{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));border-top:1px solid var(--ink);border-bottom:1px solid var(--rule);margin:18px 0 0}}
.card{{padding:14px 16px 14px;border-left:1px solid var(--rule)}}.card:first-child{{border-left:0;padding-left:0}}
.card h3{{margin:0;font:600 11px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}}
.card .v{{font:600 34px/1.1 var(--mono);letter-spacing:-.03em;margin-top:6px}}.card .v small{{font-size:15px;color:var(--ink-3)}}
.card p{{margin:4px 0 0;color:var(--ink-2);font-size:12.5px}}.card.r .v{{color:var(--signal)}}
h2{{font:700 22px/1.2 var(--serif);margin:34px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--ink)}}
.box{{padding:4px 0 0;overflow-x:auto;min-width:0}}
.mt{{display:flex;flex-wrap:wrap;gap:0;margin-bottom:12px;border-bottom:1px solid var(--rule)}}.mt div{{padding:6px 22px 10px;border-left:1px solid var(--rule)}}.mt div:first-child{{border-left:0;padding-left:0}}
.mt b{{font:600 26px var(--mono);letter-spacing:-.02em}}.mt small{{display:block;font:600 10.5px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}}
.ctl{{display:flex;flex-wrap:wrap;gap:14px 20px;align-items:center;margin:8px 0 10px}}
.ctl input[type=search]{{font:14px var(--sans);color:var(--ink);background:transparent;border:0;border-bottom:1px solid var(--ink);padding:6px 2px;border-radius:0;min-width:280px}}.ctl input[type=search]:focus{{outline:none;border-bottom-color:var(--signal)}}
.ctl label{{font-size:13px;color:var(--ink-2)}}input[type=checkbox]{{accent-color:var(--signal)}}
.leg{{display:flex;gap:6px 20px;flex-wrap:wrap;font:600 11px var(--mono);letter-spacing:.04em;color:var(--ink-3);margin:6px 0 12px;padding:8px 0;border-top:1px solid var(--rule-2);border-bottom:1px solid var(--rule-2)}}
.leg i{{display:inline-block;width:12px;height:12px;margin-right:6px;vertical-align:-2px;border:1px solid var(--rule)}}
.grid{{display:flex;gap:10px;overflow-x:auto;padding-bottom:10px}}.col{{min-width:170px;max-width:170px;display:flex;flex-direction:column;gap:4px}}
.col header{{border-bottom:1px solid var(--ink);padding:0 0 8px;margin-bottom:4px}}.col h4{{margin:0;font:700 14px/1.2 var(--serif);min-height:34px}}
.col small{{font:600 10.5px var(--mono);color:var(--ink-3);letter-spacing:.06em}}
.bar{{display:block;height:4px;background:var(--rule-2);margin-top:5px;overflow:hidden}}.bar i{{display:block;height:100%;background:var(--seq-3)}}
td .bar{{width:120px;height:8px}}
.tec{{border:1px solid var(--rule);padding:6px 7px;font-size:12px;background:var(--card)}}.tec .th{{display:flex;gap:4px;align-items:flex-start}}.tn{{flex:1}}
.tid,.sid{{font:10.5px var(--mono);color:var(--ink-3)}}.tec .n,.sub .n{{font:700 12px var(--mono)}}.subcount{{font:10px var(--mono);color:var(--ink-3)}}
.tec.c1{{background:var(--seq-1);border-color:var(--seq-3)}}
.tec.c3{{background:var(--seq-3);border-color:var(--seq-3);color:var(--on-seq-3)}}.tec.c3 .tid,.tec.c3 .subcount,.tec.c3>.det>.lbl{{color:var(--on-seq-3);opacity:.85}}
.tec.mes{{position:relative}}.tec.mes:after{{content:"";position:absolute;top:-4px;right:-4px;width:9px;height:9px;background:var(--ink);border:2px solid var(--paper);border-radius:50%}}
.det{{display:none;margin-top:6px}}.open .det{{display:block}}
.sub{{border:1px dashed var(--rule);padding:3px 6px;margin:3px 0;font-size:11px;display:flex;gap:4px;background:var(--card);color:var(--ink)}}.sub .sid{{color:var(--ink-3)}}.sub.c1,.sub.c3{{border-style:solid;border-color:var(--ink)}}
.det .lbl{{margin:6px 0 2px;font:600 10px var(--mono);letter-spacing:.1em;color:var(--ink-3)}}.det ul{{margin:0;padding:0;list-style:none}}
.det li{{background:var(--card);color:var(--ink);border:1px solid var(--rule);padding:3px 5px;margin:3px 0;font-size:11px}}
.nat{{font:700 10px var(--mono);font-style:normal;padding:0 4px;margin-left:4px;border:1px solid var(--ink)}}.nat.comportamento{{background:var(--ink);color:var(--paper)}}.nat.exposicao{{background:transparent;color:var(--ink)}}
.hide{{display:none!important}}.nota{{color:var(--ink-3);font:12px var(--mono);margin:8px 0 0}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}th{{font:600 11px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);text-align:left;padding:8px 12px 8px 0;border-bottom:1px solid var(--ink)}}
td{{padding:9px 12px 9px 0;border-bottom:1px solid var(--rule);vertical-align:top;text-align:left}}td code{{font-family:var(--mono)}}td small{{color:var(--ink-3)}}
tr.fora td{{color:var(--signal);font-weight:600}}.ok{{font:600 11px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}}
.bad{{font:600 10px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--signal);border:1px solid var(--signal);padding:1px 5px;white-space:nowrap}}
.two{{align-items:start;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(380px,100%),1fr));gap:12px 48px}}.two>.box{{min-width:0;overflow-x:auto}}
.meses{{display:flex;gap:6px;align-items:flex-end;height:150px;padding-top:10px;border-bottom:1px solid var(--ink)}}.mcol{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;gap:2px}}
.mcol i{{display:block;width:70%;background:var(--seq-3);min-height:2px}}.mv{{font:11px var(--mono)}}.ml{{font:10px var(--mono);color:var(--ink-3)}}
ol.rec{{margin:0;padding:0;list-style:none;counter-reset:r}}ol.rec li{{counter-increment:r;display:grid;grid-template-columns:28px 64px 1fr;gap:10px;padding:10px 0;border-top:1px solid var(--rule)}}ol.rec li:last-child{{border-bottom:1px solid var(--rule)}}
ol.rec li:before{{content:counter(r,decimal-leading-zero);font:600 12px var(--mono);color:var(--ink-3)}}
ol.rec span{{align-self:start;justify-self:start;font:600 10px var(--mono);letter-spacing:.08em;padding:1px 5px;border:1px solid var(--rule);color:var(--ink-3)}}
ol.rec .p-alta span{{background:var(--signal);border-color:var(--signal);color:var(--signal-ink)}}ol.rec .p-media span{{border-color:var(--ink);color:var(--ink)}}
.gwrap{{overflow:auto;border:1px solid var(--rule);background:var(--paper-2);margin:8px 0 14px}}#grafo{{display:block;min-width:1100px;width:100%;height:auto}}
.gcol{{font:600 10px var(--mono);letter-spacing:.12em;fill:var(--ink-3)}}
.edge{{fill:none;stroke:var(--ink-3);stroke-width:1;opacity:.22}}.edge.via{{stroke-dasharray:4 4}}.edge.on{{stroke:var(--signal);opacity:1;stroke-width:1.8}}
.node{{cursor:pointer;outline:none}}.node text{{font:11.5px var(--sans);fill:var(--ink);paint-order:stroke;stroke:var(--paper-2);stroke-width:4px;stroke-linejoin:round}}.node .gid{{font:10px var(--mono);fill:var(--ink-3)}}
.node .mk{{fill:var(--ink);stroke:var(--ink)}}.node.t-alerta .mk,.node.t-tecnica .mk{{fill:var(--paper-2)}}
.node.dim{{opacity:.2}}.node.on .mk{{fill:var(--signal);stroke:var(--signal)}}.node.on text{{fill:var(--signal)}}.node:focus-visible text{{text-decoration:underline}}
.leg svg{{color:var(--ink);vertical-align:-2px;margin-right:4px}}.gtab .id{{font:11px var(--mono);color:var(--ink-3)}}.gtab td.num{{font-family:var(--mono)}}
footer{{margin:34px 0 10px;color:var(--ink-3);font:12px var(--mono);border-top:1px solid var(--ink);padding-top:12px}}footer code{{font-family:var(--mono);word-break:break-all}}
@media (max-width:1100px){{.cards{{grid-template-columns:repeat(3,minmax(0,1fr))}}.card:nth-child(4){{border-left:0;padding-left:0}}.card{{border-top:1px solid var(--rule)}}}}
@media (max-width:640px){{.wrap{{padding:0 16px 16px}}.cards{{grid-template-columns:repeat(2,minmax(0,1fr))}}.card:nth-child(odd){{border-left:0;padding-left:0}}.card:nth-child(4){{border-left:1px solid var(--rule);padding-left:16px}}.ctl input[type=search]{{min-width:0;width:100%}}.two{{grid-template-columns:1fr}}}}
@media print{{.tools,.ctl{{display:none!important}}body{{background:#fff}}}}
</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <h1 id="titulo"><span data-i18n="titulo">KPI OT — Executivo / Operacional</span>
    <small>CALDEIRA CYBER OT LABS · MANÔMETRO v{E(p["version"])} · <span data-i18n="periodo">Período</span> {E(per["de"])} → {E(per["ate"])}</small></h1>
  <div class="tools">
    <div class="seg" role="group" aria-label="Idioma"><button data-lang="pt" aria-pressed="true">PT</button><button data-lang="en" aria-pressed="false">EN</button></div>
    <div class="seg" role="group" aria-label="Tema"><button data-th="system" aria-pressed="true" data-i18n="t_sis">Sistema</button><button data-th="light" aria-pressed="false" data-i18n="t_claro">Claro</button><button data-th="dark" aria-pressed="false" data-i18n="t_escuro">Escuro</button></div>
  </div>
</header>
<div class="chips" id="chips">
  <span class="chip syn" data-i18n="sintetico">DADOS SINTÉTICOS</span>
  <span class="chip">Claroty xDome → Elastic</span>
  <span class="chip">MITRE ATT&amp;CK for ICS v{E(ma["versao"])}</span>
  <span class="chip">dedup: <code>claroty_xdome.alert.id</code> + último <code>updated_time</code></span>
  <span class="chip">alertas por <code>detected_time</code> · eventos por <code>@timestamp</code></span>
  {banner}
</div>

<div class="cards" id="cards">
  <div class="card"><h3 data-i18n="k_alertas">Alertas únicos no período</h3><div class="v">{al["no_periodo"]}</div>
    <p>de {co["documentos_alerta"]} documentos de alerta no arquivo ({co["fator_inflacao"]}x)</p></div>
  <div class="card r"><h3 data-i18n="k_abertos">Em aberto</h3><div class="v">{al["abertos"]}</div><p>{al["resolvidos"]} resolvido(s) · {al["comportamento"]} comportamento · {al["exposicao"]} exposição</p></div>
  <div class="card a"><h3 data-i18n="k_disp">Dispositivos impactados (distintos)</h3><div class="v">{di["distintos"]}</div>
    <p>{cats}{"" if soma_cat == di["distintos"] else " · ⚠ soma ≠ total"} · soma por alerta seria {di["soma_contagens_fornecedor"]}</p></div>
  <div class="card a"><h3 data-i18n="k_taticas">Táticas ICS com alerta mapeado</h3><div class="v">{tot["taticas_com_alerta"]}<small>/{tot["taticas_total"]}</small></div>
    <p>só comportamento: {tot["taticas_com_comportamento"]}/{tot["taticas_total"]} · {tot["tecnicas_com_alerta"]} técnicas (de {tot["tecnicas_total"]})</p></div>
  <div class="card a"><h3 data-i18n="k_obsoletos">Ativos obsoletos (distintos)</h3><div class="v">{at["obsoletos_distintos"]}</div>
    <p>{at["eol"]} EoL · {at["firmware_desatualizado"]} firmware desatualizado · {at["sobreposicao_eol_firmware"]} nos dois</p></div>
  <div class="card"><h3 data-i18n="k_config">Eventos de Configuration Download</h3><div class="v">{cf["eventos"]}</div>
    <p>{cf["pares_fora_baseline"]} par(es) fora do baseline · {cf["eventos_fora_baseline"]} evento(s)</p></div>
</div>

<h2 data-i18n="s_matriz">MITRE ATT&amp;CK for ICS — matriz</h2>
<div class="box" id="matriz">
  <div class="mt">
    <div><b id="mt-tec">{tot["tecnicas_com_alerta"]}</b>/{tot["tecnicas_total"]}<small data-i18n="m_tec">Técnicas ICS com alerta</small></div>
    <div><b id="mt-sub">{tot["subtecnicas_com_alerta"]}</b>/{tot["subtecnicas_total"]}<small data-i18n="m_sub">Subtécnicas ICS com alerta</small></div>
    <div><b id="mt-tat">{tot["taticas_com_alerta"]}</b>/{tot["taticas_total"]}<small data-i18n="m_tat">Táticas com alerta</small></div>
    <div><b id="mt-map">{tot["alertas_mapeados"]}</b>/<span id="mt-den" data-todos="{al["no_periodo"]}" data-c="{al["comportamento"]}" data-e="{al["exposicao"]}">{al["no_periodo"]}</span><small data-i18n="m_map">Alertas mapeados</small></div>
  </div>
  <div class="ctl">
    <div class="seg" role="group" aria-label="Natureza do alerta">
      <button data-f="todos" aria-pressed="true" data-i18n="f_todos">Todos os alertas</button>
      <button data-f="c" aria-pressed="false" data-i18n="f_comp">Comportamento</button>
      <button data-f="e" aria-pressed="false" data-i18n="f_expo">Exposição / postura</button>
    </div>
    <input type="search" id="busca" placeholder="Filtrar por técnica, ID ou alerta" aria-label="Filtrar matriz">
    <label><input type="checkbox" id="expandir" checked> <span data-i18n="f_expandir">Expandir subtécnicas e alertas</span></label>
    <label><input type="checkbox" id="mes"> <span data-i18n="f_mes">Só alertas do último mês</span> ({E(per["ultimo_mes"])})</label>
  </div>
  <div class="leg"><span><i style="background:var(--seq-3);border-color:var(--seq-3)"></i><span data-i18n="l_3">≥3 alertas</span></span><span><i style="background:var(--seq-1);border-color:var(--seq-3)"></i><span data-i18n="l_12">1–2 alertas</span></span><span><i></i><span data-i18n="l_0">Sem alertas</span></span><span><i style="border-radius:50%;background:var(--ink);width:9px;height:9px"></i><span data-i18n="l_mes">Alerta do último mês</span></span><span><em class="nat comportamento">C</em> comportamento <em class="nat exposicao">E</em> exposição</span></div>
  <div class="grid" id="grade">{colunas}</div>
  <p class="nota" data-i18n="m_nota">Mapeamento do fornecedor, não prova de execução. Uma técnica que pertence a N táticas conta nas N.</p>
</div>

<h2 data-i18n="s_qualidade">Qualidade do mapeamento</h2>
<div class="box"><table><thead><tr><th>Alerta</th><th>ID recebido</th><th>ID usado</th><th>Motivo</th></tr></thead><tbody>{linhas_q}</tbody></table>
<p class="nota">Catálogo derivado do STIX oficial da MITRE (SHA-256 <code>{E(ma["fonte_sha256"][:16])}…</code>). IDs revogados são remapeados para o substituto oficial; IDs de outro domínio não contam cobertura.</p></div>

<h2 data-i18n="s_grafo">Atores, campanhas e software — sobreposição com os alertas</h2>
<div class="box" id="atores">
  <p class="banner" style="cursor:default">{E(gr.get("aviso", ""))} Base: técnicas dos alertas de <b>{E(gr.get("natureza", ""))}</b> ({len(gr.get("tecnicas_base", []))}: {E(", ".join(gr.get("tecnicas_base", [])))}).</p>
  <div class="leg"><span><svg width="12" height="12"><rect x="0" y="0" width="12" height="12" fill="currentColor"/></svg> grupo</span><span><svg width="14" height="14"><path d="M7 0L14 7L7 14L0 7Z" fill="currentColor"/></svg> campanha</span><span><svg width="12" height="12"><circle cx="6" cy="6" r="6" fill="currentColor"/></svg> software</span><span><svg width="16" height="6"><rect width="16" height="6" fill="currentColor"/></svg> técnica</span><span><svg width="12" height="12"><path d="M0 12L6 0L12 12Z" fill="currentColor"/></svg> alerta</span><span>▣n · casos do atlas Caldeira</span><span>- - - técnica via campanha atribuída</span><span>Passe o mouse ou foque um nó para ver as ligações.</span></div>
  {grafo_svg(gr)}
  <table class="gtab"><thead><tr><th>Entidade (MITRE)</th><th>Tipo</th><th>Técnicas em comum</th><th title="parte do repertório da entidade que aparece nos alertas">Especificidade</th><th>Alertas</th><th>Período</th><th>Atlas Caldeira</th></tr></thead><tbody>{grafo_tabela(gr)}</tbody></table>
  <p class="nota">Ordenado por técnicas em comum e, no empate, por especificidade (quanto do repertório da entidade aparece aqui). Ferramentas amplas como INCONTROLLER cobrem muitas técnicas e por isso pontuam alto: leia como “o que procurar”, não como “quem foi”. Fonte: relações <code>uses</code> e <code>attributed-to</code> do STIX oficial v{E(gr.get("attack_version", ""))}.</p>
</div>

<h2 data-i18n="s_ativos">Exposição de ativos</h2>
<div class="two">
  <div class="box"><table><thead><tr><th>Protocolo legado</th><th>Nível Purdue</th><th>Dispositivos</th><th></th></tr></thead><tbody>{legado}</tbody></table>
  <p class="nota">{at["eol"]} em fim de vida ({at["eol_em_niveis_atencao"]} nos níveis de atenção) · {at["eol_aviso"]} com aviso de fim de vida.</p></div>
  <div class="box" style="max-height:340px;overflow:auto"><table><thead><tr><th>Ativo</th><th>Cat.</th><th>Modelo</th><th>Firmware</th><th>Ciclo de vida</th><th>Purdue</th></tr></thead><tbody>{obsoletos}</tbody></table></div>
</div>

<h2 data-i18n="s_config">Configuration Download × baseline</h2>
<div class="two">
  <div class="box"><div class="meses">{meses}</div><p class="nota">Eventos por mês no período (por <code>@timestamp</code>).</p></div>
  <div class="box"><table><thead><tr><th>Origem</th><th>Destino</th><th>Protocolo</th><th>Eventos</th><th>Baseline</th></tr></thead><tbody>{pares}</tbody></table>
  <p class="nota">Confirme com o fornecedor o sentido de “download”/“upload” no seu ambiente antes de tratar como escrita no controlador.</p></div>
</div>

<h2 id="saude" data-i18n="s_saude">Saúde da coleta</h2>
<div class="box"><table><thead><tr><th>Tipo de erro (normalizado)</th><th>Qtd</th><th>Dataset</th><th>Último (UTC)</th></tr></thead><tbody>{erros}</tbody></table></div>

<h2 data-i18n="s_rec">Recomendações</h2>
<div class="box"><ol class="rec">{rec}</ol></div>

<h2 data-i18n="s_alertas">Alertas deduplicados</h2>
<div class="box" style="overflow-x:auto"><table><thead><tr><th>ID</th><th>Alerta</th><th>Natureza</th><th>Status</th><th>Detectado</th><th>ICS (recebido → usado)</th><th>Disp.</th><th>Docs / coletas</th></tr></thead><tbody>{lista}</tbody></table></div>

<footer>
  <p data-i18n="rodape">Vista estática de um envelope selado. SHA-256 mede integridade, não autoria.</p>
  <p>Digest do payload: <code>{E(env["digest"])}</code><br>SHA-256 da exportação: <code>{E(p["input_sha256"])}</code><br>
  Caso: {E(p["case_id"])} · modo {E(p["mode"])} · campos não confirmados na referência pública: <code>{E(supostos)}</code></p>
  <p>MITRE ATT&amp;CK® é marca registrada de The MITRE Corporation. Nomes e IDs reproduzidos conforme os Termos de Uso do ATT&amp;CK. Projeto independente, sem afiliação com MITRE, Claroty ou Elastic.</p>
</footer>
</div>
<script>
(function(){{
  var EN={i18n};
  var PT={{}};
  document.querySelectorAll('[data-i18n]').forEach(function(el){{PT[el.dataset.i18n]=el.textContent;}});
  function seg(sel,attr,fn){{document.querySelectorAll(sel).forEach(function(b){{b.addEventListener('click',function(){{
    b.parentNode.querySelectorAll('button').forEach(function(x){{x.setAttribute('aria-pressed','false')}});b.setAttribute('aria-pressed','true');fn(b.dataset[attr]);}});}});}}
  function lang(l){{document.documentElement.lang=l==='en'?'en':'pt-BR';document.querySelectorAll('[data-i18n]').forEach(function(el){{var k=el.dataset.i18n;var t=(l==='en'?EN:PT)[k];if(t&&!/\\{{/.test(t))el.textContent=t;}});
    try{{localStorage.setItem('manometro-lang',l)}}catch(e){{}}}}
  function theme(t){{document.documentElement.setAttribute('data-theme',t);try{{localStorage.setItem('manometro-theme',t)}}catch(e){{}}}}
  seg('[data-lang]','lang',lang);seg('[data-th]','th',theme);
  try{{var sl=localStorage.getItem('manometro-lang');if(sl)document.querySelector('[data-lang="'+sl+'"]').click();var st=localStorage.getItem('manometro-theme');if(st)document.querySelector('[data-th="'+st+'"]').click();}}catch(e){{}}
  var modo='todos';
  function cls(n){{return n>=3?'c3':(n>=1?'c1':'c0')}}
  function aplicar(){{
    var q=(document.getElementById('busca').value||'').trim().toLowerCase();
    var exp=document.getElementById('expandir').checked, soMes=document.getElementById('mes').checked;
    document.querySelectorAll('.tec,.sub').forEach(function(el){{
      var c=+el.dataset.c,e=+el.dataset.e,n=modo==='c'?c:(modo==='e'?e:c+e);
      el.classList.remove('c0','c1','c3');el.classList.add(cls(n));
      var badge=el.querySelector('.n');if(badge)badge.textContent=n||'';
      if(el.classList.contains('tec')){{el.classList.toggle('open',exp);
        el.classList.toggle('hide',!!q&&el.dataset.busca.indexOf(q)<0);}}
    }});
    document.querySelectorAll('.det li').forEach(function(li){{
      var ok=(modo==='todos'||(modo==='c'?li.dataset.nat==='comportamento':li.dataset.nat==='exposicao'))&&(!soMes||li.dataset.mes==='1');
      li.classList.toggle('hide',!ok);}});
    document.querySelectorAll('.det').forEach(function(d){{var l=d.querySelector('.lbl');if(l)l.classList.toggle('hide',!d.querySelector('li:not(.hide)'));}});
    var tec={{}},sub={{}},tat=0,al={{}};
    document.querySelectorAll('.col').forEach(function(col){{var k=0;
      col.querySelectorAll('.tec').forEach(function(t){{var c=+t.dataset.c,e=+t.dataset.e,n=modo==='c'?c:(modo==='e'?e:c+e);if(n){{k++;tec[t.dataset.id]=1;}}}});
      if(k)tat++;var tot=+col.dataset.total;col.querySelector('.tc').textContent=k+'/'+tot+' · '+(tot?Math.round(100*k/tot):0)+'%';
      col.querySelector('.bar i').style.width=(tot?Math.round(100*k/tot):0)+'%';}});
    document.querySelectorAll('.sub').forEach(function(s){{var c=+s.dataset.c,e=+s.dataset.e,n=modo==='c'?c:(modo==='e'?e:c+e);if(n)sub[s.dataset.id]=1;}});
    document.querySelectorAll('.det li').forEach(function(li){{if(modo==='todos'||(modo==='c'?li.dataset.nat==='comportamento':li.dataset.nat==='exposicao'))al[li.dataset.a]=1;}});
    var den=document.getElementById('mt-den');
    document.getElementById('mt-tec').textContent=Object.keys(tec).length;
    document.getElementById('mt-sub').textContent=Object.keys(sub).length;
    document.getElementById('mt-tat').textContent=tat;
    document.getElementById('mt-map').textContent=Object.keys(al).length;
    den.textContent=den.dataset[modo==='todos'?'todos':modo];
  }}
  var gnodes=[].slice.call(document.querySelectorAll('#grafo .node')),gedges=[].slice.call(document.querySelectorAll('#grafo .edge'));
  function marcar(id){{var viz={{}};viz[id]=1;gedges.forEach(function(e){{var on=e.dataset.a===id||e.dataset.b===id;e.classList.toggle('on',on);if(on){{viz[e.dataset.a]=1;viz[e.dataset.b]=1;}}}});
    gnodes.forEach(function(n){{n.classList.toggle('on',n.dataset.id===id);n.classList.toggle('dim',!viz[n.dataset.id]);}});}}
  function limpar(){{gedges.forEach(function(e){{e.classList.remove('on')}});gnodes.forEach(function(n){{n.classList.remove('on','dim')}});}}
  gnodes.forEach(function(n){{n.addEventListener('mouseenter',function(){{marcar(n.dataset.id)}});n.addEventListener('focus',function(){{marcar(n.dataset.id)}});
    n.addEventListener('mouseleave',limpar);n.addEventListener('blur',limpar);n.addEventListener('keydown',function(ev){{if(ev.key==='Escape'){{n.blur();}}}});}});
  seg('[data-f]','f',function(v){{modo=v;aplicar();}});
  ['busca','expandir','mes'].forEach(function(id){{document.getElementById(id).addEventListener('input',aplicar);}});
  aplicar();
}})();
</script>
</body>
</html>
"""

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


def renderizar(env):
    p = env["payload"]
    k = p["kpis"]
    per, co, al, di, ma, at, cf, sa = (k[x] for x in ("periodo", "coleta", "alertas", "dispositivos", "matriz",
                                                      "ativos", "config", "saude"))
    tot = ma["totais"]
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
<title>Manômetro OT KPI</title>
<style>
:root{{--bg:#f4f8f5;--panel:#ffffff;--panel2:#eaf1ef;--line:#c9d8d5;--ink:#0b2026;--muted:#4d6a6f;--acc:#b8642a;--mint:#1f8a76;--c3:#b8642a;--c3bg:#f6dcc4;--c1bg:#fbeee2;--bad:#b3261e;--font:system-ui,-apple-system,"Segoe UI",Arial,sans-serif;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#07171d;--panel:#0f2a33;--panel2:#0b222a;--line:#244751;--ink:#f4f8f5;--muted:#a9c8c5;--acc:#e99754;--mint:#57c9b2;--c3:#e99754;--c3bg:#8a4b17;--c1bg:#4a2e14;--bad:#ff8a80}}}}
:root[data-theme="dark"]{{--bg:#07171d;--panel:#0f2a33;--panel2:#0b222a;--line:#244751;--ink:#f4f8f5;--muted:#a9c8c5;--acc:#e99754;--mint:#57c9b2;--c3:#e99754;--c3bg:#8a4b17;--c1bg:#4a2e14;--bad:#ff8a80}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font);font-size:14px;line-height:1.5}}
.wrap{{max-width:1500px;margin:0 auto;padding:16px}}
header.top{{display:flex;flex-wrap:wrap;gap:12px;justify-content:space-between;align-items:center;border-bottom:1px solid var(--line);padding-bottom:12px}}
h1{{font-size:20px;margin:0}}h1 small{{display:block;font-size:12px;color:var(--muted);font-weight:400}}
.tools{{display:flex;gap:8px;flex-wrap:wrap}}.seg{{display:inline-flex;border:1px solid var(--line);border-radius:999px;overflow:hidden}}
.seg button{{background:transparent;color:var(--ink);border:0;padding:6px 12px;cursor:pointer;font:inherit}}.seg button[aria-pressed="true"]{{background:var(--mint);color:#04161a;font-weight:700}}
button:focus-visible,input:focus-visible,a:focus-visible{{outline:3px solid var(--acc);outline-offset:2px}}
.chips{{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}}.chip{{border:1px solid var(--line);border-radius:999px;padding:3px 10px;font-size:12px;color:var(--muted)}}.chip code{{font-family:var(--mono)}}.chip.syn{{border-color:var(--mint);color:var(--mint);font-weight:700}}
.banner{{display:inline-block;border:1px solid var(--acc);color:var(--acc);border-radius:999px;padding:4px 12px;text-decoration:none;font-weight:600}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:14px 0}}
.card{{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--mint);border-radius:10px;padding:12px 14px}}.card.a{{border-left-color:var(--acc)}}.card.r{{border-left-color:var(--bad)}}
.card h3{{margin:0;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:600}}.card .v{{font-size:30px;font-weight:800;font-family:var(--mono)}}.card .v small{{font-size:15px;color:var(--muted)}}.card p{{margin:2px 0 0;color:var(--muted);font-size:12.5px}}
h2{{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:26px 0 10px;border-bottom:1px solid var(--line);padding-bottom:6px}}
.box{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px}}
.mt{{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:12px}}.mt div{{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:8px 12px}}.mt b{{font-size:22px;font-family:var(--mono)}}.mt small{{display:block;color:var(--muted);font-size:12px}}
.ctl{{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:8px 0 10px}}.ctl input[type=search]{{background:var(--panel2);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:6px 10px;min-width:260px}}
.leg{{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin:6px 0 10px}}.leg i{{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:5px;vertical-align:-2px;border:1px solid var(--line)}}
.grid{{display:flex;gap:8px;overflow-x:auto;padding-bottom:8px}}.col{{min-width:168px;max-width:168px;display:flex;flex-direction:column;gap:5px}}
.col header{{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:8px;text-align:center}}.col h4{{margin:0;font-size:12.5px}}.col small{{color:var(--muted);font-size:11px}}
.bar{{display:block;height:4px;background:var(--line);border-radius:2px;margin-top:4px;overflow:hidden}}.bar i{{display:block;height:100%;background:var(--acc)}}
td .bar{{width:120px;height:8px}}
.tec{{border:1px solid var(--line);border-radius:6px;padding:6px 7px;font-size:12px;background:var(--panel)}}.tec .th{{display:flex;gap:4px;align-items:flex-start}}.tn{{flex:1}}.tid,.sid{{font-family:var(--mono);font-size:10px;color:var(--muted)}}
.tec .n,.sub .n{{font-family:var(--mono);font-weight:800}}.subcount{{font-family:var(--mono);font-size:10px;color:var(--muted)}}
.tec.c3{{background:var(--c3bg);border-color:var(--c3)}}.tec.c1{{background:var(--c1bg);border-color:var(--c3)}}.tec.mes{{box-shadow:inset 0 0 0 2px var(--mint)}}
.det{{display:none;margin-top:6px}}.open .det{{display:block}}.sub{{border:1px dashed var(--line);border-radius:5px;padding:3px 6px;margin:3px 0;font-size:11px;display:flex;gap:4px}}.sub.c1,.sub.c3{{border-style:solid;border-color:var(--c3)}}
.det .lbl{{margin:6px 0 2px;font-size:10px;letter-spacing:.06em;color:var(--muted)}}.det ul{{margin:0;padding:0;list-style:none}}.det li{{background:var(--panel);border:1px solid var(--line);border-radius:5px;padding:3px 5px;margin:3px 0;font-size:11px}}
.nat{{font-style:normal;font-size:10px;font-weight:800;border-radius:4px;padding:0 4px;margin-left:4px}}.nat.comportamento{{background:var(--mint);color:#04161a}}.nat.exposicao{{background:var(--line);color:var(--ink)}}
.hide{{display:none!important}}.nota{{color:var(--muted);font-size:12.5px;margin:6px 0 0}}
table{{width:100%;border-collapse:collapse;font-size:13px}}th,td{{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top}}th{{font-size:11px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}}td code{{font-family:var(--mono)}}td small{{color:var(--muted)}}
tr.fora td{{color:var(--bad);font-weight:600}}.ok{{color:var(--mint);font-weight:700}}.bad{{color:var(--bad);font-weight:800}}
.two{{align-items:start;display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:12px}}
.meses{{display:flex;gap:6px;align-items:flex-end;height:150px;padding-top:10px}}.mcol{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;gap:2px}}.mcol i{{display:block;width:70%;background:var(--mint);border-radius:3px 3px 0 0;min-height:2px}}.mv{{font-family:var(--mono);font-size:11px}}.ml{{font-size:10px;color:var(--muted)}}
ol.rec{{margin:0;padding-left:18px}}ol.rec li{{margin:6px 0}}ol.rec span{{font-family:var(--mono);font-size:10px;font-weight:800;border-radius:4px;padding:1px 5px;margin-right:8px;background:var(--line)}}ol.rec .p-alta span{{background:var(--bad);color:#fff}}ol.rec .p-media span{{background:var(--acc);color:#04161a}}
footer{{margin:28px 0 10px;color:var(--muted);font-size:12px;border-top:1px solid var(--line);padding-top:10px}}footer code{{font-family:var(--mono);word-break:break-all}}
@media (max-width:640px){{.ctl input[type=search]{{min-width:0;width:100%}}.two{{grid-template-columns:1fr}}}}
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
  <div class="leg"><span><i style="background:var(--c3bg);border-color:var(--c3)"></i><span data-i18n="l_3">≥3 alertas</span></span><span><i style="background:var(--c1bg);border-color:var(--c3)"></i><span data-i18n="l_12">1–2 alertas</span></span><span><i></i><span data-i18n="l_0">Sem alertas</span></span><span><i style="box-shadow:inset 0 0 0 2px var(--mint)"></i><span data-i18n="l_mes">Alerta do último mês</span></span><span><em class="nat comportamento">C</em> comportamento <em class="nat exposicao">E</em> exposição</span></div>
  <div class="grid" id="grade">{colunas}</div>
  <p class="nota" data-i18n="m_nota">Mapeamento do fornecedor, não prova de execução. Uma técnica que pertence a N táticas conta nas N.</p>
</div>

<h2 data-i18n="s_qualidade">Qualidade do mapeamento</h2>
<div class="box"><table><thead><tr><th>Alerta</th><th>ID recebido</th><th>ID usado</th><th>Motivo</th></tr></thead><tbody>{linhas_q}</tbody></table>
<p class="nota">Catálogo derivado do STIX oficial da MITRE (SHA-256 <code>{E(ma["fonte_sha256"][:16])}…</code>). IDs revogados são remapeados para o substituto oficial; IDs de outro domínio não contam cobertura.</p></div>

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
  seg('[data-f]','f',function(v){{modo=v;aplicar();}});
  ['busca','expandir','mes'].forEach(function(id){{document.getElementById(id).addEventListener('input',aplicar);}});
  aplicar();
}})();
</script>
</body>
</html>
"""

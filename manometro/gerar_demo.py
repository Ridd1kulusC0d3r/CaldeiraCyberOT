"""Gera o caso de demonstração 100% sintético (determinístico).

  python -m manometro.gerar_demo            # reescreve manometro/fixtures/demo-xdome.json

Tudo é inventado: planta, nomes, fabricantes ("Vendor-X"), IPs em faixas de
documentação (RFC 5737: 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24).
O formato imita documentos da integração Elastic Claroty xDome para que o
motor seja exercitado com os nomes de campo reais (ver campos.py).

A história embutida no demo, para o analista "encontrar":
  * re-coletas + fan-out por dispositivo inflam os documentos;
  * o fornecedor ainda envia IDs revogados no v20.0 (T0855, T0812, T0857)
    e um ID Enterprise (T1059) no campo de ICS;
  * metade dos alertas é postura (categoria "Risk"), não comportamento;
  * uma estação de TI (PC-17) faz Configuration Download para um PLC;
  * a coleta teve erros de API em agosto e outubro;
  * dois alertas são de nov/dez de 2025 (testam o seletor de período).
"""
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

SAIDA = Path(__file__).resolve().parent / "fixtures" / "demo-xdome.json"
R = random.Random(20261023)
UTC = timezone.utc


def iso(dt):
    return dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def dispositivos():
    d = []

    def add(prefixo, n, cat, tipo, purdue, fab, modelo, fw, eol_fn=lambda i: "Manufacturer-Supported", rede="192.0.2"):
        for i in range(1, n + 1):
            d.append({
                "uid": f"syn-{prefixo.lower()}-{i:03d}",
                "name": f"{prefixo}-{i:02d}" if n < 100 else f"{prefixo}-{i:03d}",
                "category": cat,
                "type": {"family": tipo},
                "manufacturer": fab,
                "model": {"name": modelo},
                "software_or_firmware_version": fw(i) if callable(fw) else fw,
                "end_of": {"life": {"state": eol_fn(i)}},
                "purdue_level": {"value": purdue, "source": "Auto-Assigned"},
                "ip": {"list": [f"{rede}.{len(d) % 250 + 2}"]},
            })

    add("PLC", 12, "OT", "PLC", "Level 1", "Vendor-X", "PLC Series 5",
        lambda i: "2.1.0" if i <= 6 else "4.0.3", lambda i: "End-Of-Life" if i <= 3 else "Manufacturer-Supported")
    add("RTU", 4, "OT", "RTU", "Level 1", "Vendor-Y", "RTU Compact",
        lambda i: "1.0.9" if i <= 2 else "3.2.0")
    add("HMI", 8, "OT", "HMI", "Level 2", "Vendor-Z", "Panel 700",
        "7.4", lambda i: "End-Of-Life" if i <= 5 else ("End-Of-Life Notification" if i == 6 else "Manufacturer-Supported"))
    add("EWS", 3, "OT", "Engineering Station", "Level 2", "Generic", "Workstation", "Win10 LTSC",
        lambda i: "End-Of-Life" if i == 3 else "Manufacturer-Supported")
    add("HIST", 3, "OT", "Historian", "Level 3", "Generic", "Historian Server", "2019",
        lambda i: "End-Of-Life" if i <= 3 else "Manufacturer-Supported")
    add("SCADA", 4, "OT", "SCADA Server", "Level 3", "Generic", "SCADA Server", "2016",
        lambda i: "End-Of-Life" if i <= 4 else "Manufacturer-Supported")
    add("SW", 10, "OT", "Industrial Switch", "Level 2", "Vendor-W", "Ind Switch 8P", "15.2",
        lambda i: "End-Of-Life" if i <= 8 else "Manufacturer-Supported")
    add("PC", 46, "IT", "Workstation", "Level 4", "Generic", "Desktop", "Win10",
        lambda i: "Manufacturer-Supported", rede="198.51.100")
    add("SRV", 6, "IT", "Server", "Level 4", "Generic", "Rack Server", "WS2012R2",
        lambda i: "End-Of-Life" if i <= 2 else "Manufacturer-Supported", rede="198.51.100")
    add("CAM", 2, "IoT", "IP Camera", "Level 3", "Vendor-C", "Cam 2MP", "1.1")
    return d


DISP = dispositivos()
POR_PREFIXO = {}
for _d in DISP:
    POR_PREFIXO.setdefault(_d["name"].split("-")[0], []).append(_d)


def pegar(prefixo, *idx):
    lista = POR_PREFIXO[prefixo]
    return [lista[i - 1] for i in idx] if idx else list(lista)


# (id, nome, tipo, categoria, detectado, ics_ids, enterprise_ids, dispositivos, status final, re-coletas)
ALERTAS = [
    ("xd-0005", "Network Scan: Scanner IP 203.0.113.9", "Network Scan", "Threat", "2025-11-18T03:10:00Z",
     ["T0846"], ["T1046"], pegar("PLC", 1, 2, 3, 4), "Resolved", 3),
    ("xd-0006", "SMBv1 Communication: Legacy NAS", "SMBv1 Communication", "Risk", "2025-12-09T14:00:00Z",
     ["T0866"], [], pegar("SRV", 5), "Unresolved", 4),
    ("xd-0022", "Expired TLS Certificate: historian", "Expired TLS Certificate", "Risk", "2026-01-12T09:30:00Z",
     ["T0859"], ["T1078"], pegar("HIST", 1, 2) + pegar("SCADA", 1, 2, 3), "Unresolved", 6),
    ("xd-0050", "Device End-of-Life: Level 2 assets", "Device End-of-Life", "Risk", "2026-01-20T11:00:00Z",
     [], [], pegar("HMI", 1, 2, 3, 4, 5) + pegar("EWS", 3) + pegar("SW", 1, 2, 3, 4, 5, 6, 7, 8), "Unresolved", 5),
    ("xd-0011", "SMBv1 Communication: Server", "SMBv1 Communication", "Risk", "2026-02-03T16:20:00Z",
     ["T0866", "T0886"], ["T1210", "T1021.002"], pegar("SRV") + pegar("SCADA") + pegar("HIST"), "Unresolved", 7),
    ("xd-0012", "SMBv1 Communication: PC", "SMBv1 Communication", "Risk", "2026-02-03T16:25:00Z",
     ["T0866", "T0886"], ["T1210", "T1021.002"], pegar("PC")[:30] + pegar("EWS"), "Unresolved", 7),
    ("xd-0051", "Device End-of-Life: Level 3 assets", "Device End-of-Life", "Risk", "2026-02-14T10:00:00Z",
     [], [], pegar("HIST", 3) + pegar("SCADA", 4) + pegar("PLC", 1, 2, 3), "Unresolved", 4),
    ("xd-0013", "SMBv1 Communication: HMI", "SMBv1 Communication", "Risk", "2026-03-02T08:05:00Z",
     ["T0866", "T0886"], ["T1210"], pegar("HMI"), "Unresolved", 6),
    ("xd-0021", "Network Scan: Scanner IP 192.0.2.44", "Network Scan", "Threat", "2026-03-27T02:41:00Z",
     ["T0846.001"], ["T1046"], pegar("PLC")[:8] + pegar("HMI")[:4] + pegar("SW")[:4], "Unresolved", 5),
    ("xd-0038", "Scripting Activity on Engineering Station", "Scripting Activity", "Threat", "2026-04-08T19:12:00Z",
     ["T1059"], ["T1059.001"], pegar("EWS", 2), "Unresolved", 3),
    ("xd-0023", "Outdated Firmware: PLC Vendor-X Series 5", "Outdated Firmware", "Risk", "2026-04-16T13:00:00Z",
     ["T0857", "T0820"], [], pegar("PLC", 1, 2, 3, 4, 5, 6), "Unresolved", 5),
    ("xd-0036", "Login with Default Credentials", "Default Credentials", "Threat", "2026-05-21T22:47:00Z",
     ["T0812"], ["T1078.001"], pegar("HMI", 6), "Unresolved", 4),
    ("xd-0032", "Controller Mode Change: PLC-09", "Mode Change", "Threat", "2026-06-11T04:15:00Z",
     ["T0858"], [], pegar("PLC", 9), "Resolved", 4),
    ("xd-0035", "Write Command from Unapproved Source", "Unauthorized Write", "Threat", "2026-07-02T23:58:00Z",
     ["T0855", "T0836"], [], pegar("PLC", 10), "Unresolved", 4),
    ("xd-0024", "Network Scan: Scanner IP 198.51.100.7", "Network Scan", "Threat", "2026-08-19T01:30:00Z",
     ["T0846"], ["T1046"], pegar("PC")[:6] + pegar("SRV")[:2] + pegar("CAM"), "Unresolved", 4),
    ("xd-0041", "Outdated Firmware: RTU Vendor-Y", "Outdated Firmware", "Risk", "2026-09-05T12:00:00Z",
     ["T0857", "T0820"], [], pegar("RTU", 1, 2), "Unresolved", 3),
    ("xd-0037", "Communication with Malicious IP 203.0.113.66", "Malicious IP", "Threat", "2026-09-28T17:40:00Z",
     ["T0869"], ["T1071"], pegar("PC", 17), "Unresolved", 3),
    ("xd-0031", "Configuration Download from Non-Engineering Host", "Configuration Download", "Threat",
     "2026-10-14T21:03:00Z", ["T0843.001"], [], pegar("PLC", 4), "Unresolved", 3),
    ("xd-0043", "Network Scan: Scanner IP 192.0.2.91", "Network Scan", "Threat", "2026-10-20T03:22:00Z",
     ["T0846.001", "T0842"], ["T1046"], pegar("PLC")[8:] + pegar("RTU") + pegar("HMI")[4:], "Unresolved", 2),
]


def _dt(texto):
    return datetime.fromisoformat(texto.replace("Z", "+00:00"))


def doc_alerta(a, disp, atualizado, coletado, status):
    aid, nome, tipo, cat, det, ics, ent, alvos, _, _ = a
    contagem = {"OT": 0, "IT": 0, "IoT": 0}
    for x in alvos:
        contagem[x["category"]] = contagem.get(x["category"], 0) + 1
    return {
        "@timestamp": iso(coletado),
        "event": {"ingested": iso(coletado + timedelta(seconds=R.randint(2, 40))), "kind": "alert"},
        "data_stream": {"dataset": "claroty_xdome.alert", "type": "logs", "namespace": "default"},
        "claroty_xdome": {"alert": {
            "id": aid, "name": nome, "type_name": tipo, "category": cat, "class": "Pre-Defined Alerts",
            "status": status, "detected_time": det, "updated_time": iso(atualizado),
            "devices_count": len(alvos), "ot_devices_count": contagem["OT"], "it_devices_count": contagem["IT"],
            "iot_devices_count": contagem["IoT"], "medical_devices_count": 0,
            "mitre_technique": {"ics": {"ids": ics}, "enterprise": {"ids": ent}},
            "device": disp,
        }},
        "tags": ["synthetic", "caldeira-manometro-demo"],
    }


def montar():
    docs = []
    for a in ALERTAS:
        det, alvos, status_final, coletas = _dt(a[4]), a[7], a[8], a[9]
        atualizado = det
        for c in range(coletas):
            coletado = det + timedelta(hours=6 * (c + 1) + R.randint(0, 3))
            # nem toda re-coleta muda o alerta: só a 1a, a do meio e a última atualizam updated_time
            if c in (0, coletas // 2, coletas - 1):
                atualizado = coletado - timedelta(minutes=R.randint(5, 50))
            ultimo = c == coletas - 1
            status = status_final if ultimo else ("In Progress" if c >= coletas // 2 else "Unresolved")
            if status_final == "Unresolved" and not ultimo and c >= coletas // 2:
                status = "Unresolved"
            for d in alvos:
                docs.append({"_id": f"{a[0]}-{c}-{d['uid']}", "_source": doc_alerta(a, d, atualizado, coletado, status)})

    # eventos OT: Configuration Download (com baseline) e ruído de outros tipos
    ews = {e["name"]: e for e in pegar("EWS")}
    plcs = pegar("PLC")
    baseline = [["EWS-01", p["name"]] for p in plcs[:6]] + [["EWS-02", p["name"]] for p in plcs[6:]] \
        + [["SCADA-01", h["name"]] for h in pegar("HMI")[:4]]
    pares_ok = [(ews["EWS-01"], p) for p in plcs[:6]] + [(ews["EWS-02"], p) for p in plcs[6:]] \
        + [(pegar("SCADA", 1)[0], h) for h in pegar("HMI")[:4]]
    inicio = datetime(2025, 11, 1, tzinfo=UTC)
    n = 0

    def evt(tipo, origem, destino, quando, protocolo="MMS"):
        nonlocal n
        n += 1
        return {"_id": f"evt-{n:05d}", "_source": {
            "@timestamp": iso(quando),
            "data_stream": {"dataset": "claroty_xdome.event", "type": "logs", "namespace": "default"},
            "source": {"ip": origem["ip"]["list"][0]}, "destination": {"ip": destino["ip"]["list"][0]},
            "claroty_xdome": {"event": {
                "type": tipo, "protocol": protocolo, "mode": "Passive",
                "source": {"device": {"name": origem["name"], "type": origem["type"]["family"]}},
                "destination": {"device": {"name": destino["name"], "type": destino["type"]["family"]}},
            }},
            "tags": ["synthetic", "caldeira-manometro-demo"],
        }}

    for dia in range(0, 365):
        quando = inicio + timedelta(days=dia, hours=R.randint(7, 17), minutes=R.randint(0, 59))
        if quando.weekday() < 5:
            for _ in range(R.randint(0, 2)):
                o, d = R.choice(pares_ok)
                docs.append(evt("Configuration Download", o, d, quando + timedelta(minutes=R.randint(0, 300))))
        if dia % 9 == 0:
            o, d = R.choice(pares_ok)
            docs.append(evt("Configuration Upload", o, d, quando))
        if dia % 15 == 0:
            o, d = R.choice(pares_ok)
            docs.append(evt("Online Edit", o, d, quando))
    pc17, plc4 = pegar("PC", 17)[0], pegar("PLC", 4)[0]
    for h in (21, 21, 22):
        docs.append(evt("Configuration Download", pc17, plc4, datetime(2026, 10, 14, h, R.randint(0, 59), tzinfo=UTC)))
    # SCADA-02 -> HMI-07 não declarado no baseline (achado de baixa gravidade para conversar com Automação)
    for dia in (3, 17):
        docs.append(evt("Configuration Download", pegar("SCADA", 2)[0], pegar("HMI", 7)[0],
                        datetime(2026, 9, dia, 10, 15, tzinfo=UTC)))

    # saúde da coleta: erros de API (agosto e outubro)
    erros = [
        ("claroty_xdome.alert", "Request failed: HTTP 429 Too Many Requests (retry after 60s)", datetime(2026, 8, 2, 4, 0)),
        ("claroty_xdome.alert", "Request failed: HTTP 429 Too Many Requests (retry after 120s)", datetime(2026, 8, 2, 10, 0)),
        ("claroty_xdome.alert", "failed to fetch devices for alert 41: timeout after 30s", datetime(2026, 9, 6, 1, 0)),
        ("claroty_xdome.event", "unexpected end of JSON input", datetime(2026, 10, 9, 3, 30)),
        ("claroty_xdome.event", "unexpected end of JSON input", datetime(2026, 10, 9, 9, 30)),
        ("claroty_xdome.alert", "Request failed: HTTP 401 Unauthorized", datetime(2026, 10, 21, 6, 0)),
        ("claroty_xdome.alert", "Request failed: HTTP 401 Unauthorized", datetime(2026, 10, 21, 12, 0)),
        ("claroty_xdome.alert", "Request failed: HTTP 401 Unauthorized", datetime(2026, 10, 21, 18, 0)),
    ]
    for i, (ds, msg, quando) in enumerate(erros):
        docs.append({"_id": f"err-{i:03d}", "_source": {
            "@timestamp": iso(quando.replace(tzinfo=UTC)),
            "data_stream": {"dataset": ds, "type": "logs", "namespace": "default"},
            "error": {"message": msg}, "tags": ["synthetic", "caldeira-manometro-demo"],
        }})

    return {
        "schema": "caldeira.manometro.synthetic.v1",
        "synthetic": True,
        "case_id": "CAL-MAN-DEMO-001",
        "generated_by": "manometro/gerar_demo.py (seed 20261023)",
        "note": "Planta, ativos, IPs e alertas fictícios. IPs em faixas de documentação RFC 5737. "
                "Formato inspirado na integração Elastic Claroty xDome; não é uma exportação real.",
        "policy": {
            "baseline_config": baseline,
            "tipos_evento_config": ["Configuration Download"],
            "categorias_exposicao": ["Risk"],
            "status_resolvido": ["Resolved"],
        },
        "docs": docs,
    }


def main():
    dados = montar()
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps(dados, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"{len(dados['docs'])} documentos sintéticos -> {SAIDA}")


if __name__ == "__main__":
    main()

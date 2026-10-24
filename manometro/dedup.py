"""Deduplicação de alertas re-coletados.

Por que é preciso: a integração consulta a API em intervalos e grava de
novo o estado de cada alerta; além disso, cada alerta é expandido em um
documento por dispositivo afetado. Contar documentos mede *coletas x
dispositivos*, não alertas.

Regra aplicada (determinística e explicável):
  1. agrupa por claroty_xdome.alert.id;
  2. o "estado vigente" é o do maior updated_time; empate -> maior
     @timestamp; empate -> maior event.ingested;
  3. os dispositivos do alerta são os do snapshot vigente (todos os
     documentos com o mesmo updated_time vigente), deduplicados por uid.
"""
from datetime import datetime, timezone

from .campos import ler


def para_data(valor):
    """ISO 8601 -> datetime UTC (aceita sufixo Z também em Python 3.10)."""
    if not valor or not isinstance(valor, str):
        return None
    texto = valor.strip()
    if texto.endswith("Z"):
        texto = texto[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(texto)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


_MINIMO = datetime.min.replace(tzinfo=timezone.utc)


def _ordem(doc):
    return (
        para_data(ler(doc, "alert_atualizado")) or _MINIMO,
        para_data(ler(doc, "timestamp")) or _MINIMO,
        para_data(ler(doc, "ingested")) or _MINIMO,
    )


def _lista(valor):
    if valor is None:
        return []
    return list(valor) if isinstance(valor, (list, tuple)) else [valor]


def deduplicar(docs_alerta):
    """Retorna (alertas_unicos, estatistica)."""
    grupos = {}
    sem_id = 0
    for doc in docs_alerta:
        aid = ler(doc, "alert_id")
        if aid in (None, ""):
            sem_id += 1
            continue
        grupos.setdefault(str(aid), []).append(doc)

    alertas = []
    for aid, docs in grupos.items():
        docs = sorted(docs, key=_ordem)
        vigente = docs[-1]
        chave_vigente = _ordem(vigente)[0]
        snapshot = [d for d in docs if _ordem(d)[0] == chave_vigente]
        dispositivos = {}
        for d in snapshot:
            uid = ler(d, "disp_uid")
            if uid:
                dispositivos[str(uid)] = {
                    "uid": str(uid),
                    "nome": ler(d, "disp_nome"),
                    "categoria": ler(d, "disp_categoria"),
                    "fabricante": ler(d, "disp_fabricante"),
                    "modelo": ler(d, "disp_modelo"),
                    "firmware": ler(d, "disp_firmware"),
                    "eol": ler(d, "disp_eol"),
                    "purdue": ler(d, "disp_purdue"),
                }
        estados = []
        for d in docs:
            s = ler(d, "alert_status")
            if not estados or estados[-1] != s:
                estados.append(s)
        alertas.append({
            "id": aid,
            "nome": ler(vigente, "alert_nome"),
            "tipo": ler(vigente, "alert_tipo"),
            "categoria": ler(vigente, "alert_categoria"),
            "classe": ler(vigente, "alert_classe"),
            "status": ler(vigente, "alert_status"),
            "historico_status": estados,
            "detectado": ler(vigente, "alert_detectado"),
            "atualizado": ler(vigente, "alert_atualizado"),
            "ics_ids": _lista(ler(vigente, "alert_ics_ids")),
            "enterprise_ids": _lista(ler(vigente, "alert_ent_ids")),
            "fornecedor_qtd_disp": ler(vigente, "alert_qtd_disp"),
            "fornecedor_qtd_ot": ler(vigente, "alert_qtd_ot"),
            "fornecedor_qtd_it": ler(vigente, "alert_qtd_it"),
            "dispositivos": sorted(dispositivos.values(), key=lambda x: x["uid"]),
            "documentos": len(docs),
            "coletas": len({_ordem(d)[0] for d in docs}),
        })
    alertas.sort(key=lambda a: (para_data(a["detectado"]) or _MINIMO, a["id"]))
    estat = {
        "documentos_alerta": len(docs_alerta),
        "documentos_sem_id": sem_id,
        "alertas_unicos": len(alertas),
        "fator_inflacao": round(len(docs_alerta) / len(alertas), 1) if alertas else None,
    }
    return alertas, estat

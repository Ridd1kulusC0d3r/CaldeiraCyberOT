"""Mapa de campos: o único lugar onde o MANÔMETRO conhece nomes de campo.

Status de cada caminho:
  "doc"     -> listado na referência pública da integração Elastic Claroty xDome
               (https://www.elastic.co/docs/reference/integrations/claroty_xdome)
  "ecs"     -> campo padrão do Elastic Common Schema
  "suposto" -> nome plausível NÃO confirmado na referência; confira no seu
               índice (Discover > campo) antes de confiar no KPI que depende dele.

Para adaptar a outro mapeamento, altere só este arquivo.
"""

CAMPOS = {
    # --- roteamento de documentos ---
    "dataset": ("data_stream.dataset", "ecs"),
    "timestamp": ("@timestamp", "ecs"),
    "ingested": ("event.ingested", "ecs"),
    "erro": ("error.message", "ecs"),
    # --- alertas (claroty_xdome.alert) ---
    "alert_id": ("claroty_xdome.alert.id", "doc"),
    "alert_nome": ("claroty_xdome.alert.name", "doc"),
    "alert_tipo": ("claroty_xdome.alert.type_name", "doc"),
    "alert_categoria": ("claroty_xdome.alert.category", "doc"),
    "alert_classe": ("claroty_xdome.alert.class", "doc"),
    "alert_status": ("claroty_xdome.alert.status", "doc"),
    "alert_detectado": ("claroty_xdome.alert.detected_time", "doc"),
    "alert_atualizado": ("claroty_xdome.alert.updated_time", "doc"),
    "alert_qtd_disp": ("claroty_xdome.alert.devices_count", "doc"),
    "alert_qtd_ot": ("claroty_xdome.alert.ot_devices_count", "doc"),
    "alert_qtd_it": ("claroty_xdome.alert.it_devices_count", "doc"),
    "alert_ics_ids": ("claroty_xdome.alert.mitre_technique.ics.ids", "doc"),
    "alert_ent_ids": ("claroty_xdome.alert.mitre_technique.enterprise.ids", "doc"),
    # --- dispositivo afetado (fan-out: 1 documento por alerta x dispositivo) ---
    "disp_uid": ("claroty_xdome.alert.device.uid", "doc"),
    "disp_nome": ("claroty_xdome.alert.device.name", "doc"),
    "disp_categoria": ("claroty_xdome.alert.device.category", "doc"),
    "disp_fabricante": ("claroty_xdome.alert.device.manufacturer", "doc"),
    "disp_modelo": ("claroty_xdome.alert.device.model.name", "doc"),
    "disp_firmware": ("claroty_xdome.alert.device.software_or_firmware_version", "doc"),
    "disp_eol": ("claroty_xdome.alert.device.end_of.life.state", "doc"),
    "disp_purdue": ("claroty_xdome.alert.device.purdue_level.value", "doc"),
    # --- eventos OT (claroty_xdome.event) ---
    "evt_tipo": ("claroty_xdome.event.type", "doc"),
    "evt_protocolo": ("claroty_xdome.event.protocol", "doc"),
    "evt_origem_tipo": ("claroty_xdome.event.source.device.type", "doc"),
    "evt_destino_tipo": ("claroty_xdome.event.destination.device.type", "doc"),
    "evt_origem_nome": ("claroty_xdome.event.source.device.name", "suposto"),
    "evt_destino_nome": ("claroty_xdome.event.destination.device.name", "suposto"),
    "evt_origem_ip": ("source.ip", "ecs"),
    "evt_destino_ip": ("destination.ip", "ecs"),
}

DATASET_ALERTA = "claroty_xdome.alert"
DATASET_EVENTO = "claroty_xdome.event"

_FALTA = object()


def ler(doc, chave):
    """Lê um campo por nome lógico, aceitando _source aninhado ou achatado."""
    caminho = CAMPOS[chave][0]
    if caminho in doc:
        return doc[caminho]
    atual = doc
    for parte in caminho.split("."):
        if isinstance(atual, dict) and parte in atual:
            atual = atual[parte]
        else:
            # tentativa mista: resto do caminho achatado dentro do nível atual
            resto = caminho.split(".")
            for i in range(1, len(resto)):
                prefixo, sufixo = resto[:i], ".".join(resto[i:])
                no = doc
                for p in prefixo:
                    no = no.get(p, _FALTA) if isinstance(no, dict) else _FALTA
                    if no is _FALTA:
                        break
                if isinstance(no, dict) and sufixo in no:
                    return no[sufixo]
            return None
    return atual


def campos_supostos():
    """Campos não confirmados na referência pública (para o relatório)."""
    return sorted(c[0] for c in CAMPOS.values() if c[1] == "suposto")

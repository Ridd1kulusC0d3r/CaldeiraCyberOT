"""Detecção ilustrativa em eventos normalizados. Nenhum tráfego de rede é gerado."""


def detect_unapproved_modbus_write(event, policy):
    """Identifica escrita declarada fora da lista de origens autorizadas.

    Este é um detector sobre **metadados sintéticos**, não um parser ou
    validador Modbus e não confirma alteração física nem intenção maliciosa.
    """
    if event.get("protocol") != "modbus" or event.get("operation") != "write":
        return None
    target, source = event.get("target"), event.get("source")
    allowed = policy.get("modbus_approved_sources", {}).get(target, [])
    if source in allowed:
        return None
    return {
        "rule_id": "CAL-DET-OT-001",
        "event_id": event["event_id"],
        "severity": "high",
        "title": "Solicitação de escrita fora da política OT",
        "reason": "Origem ausente da lista autorizada para o destino simulado.",
        "techniques": ["T1692.001"],
        "confidence": "contextual",
        "requires_corrob": True,
        "source": source,
        "target": target,
    }

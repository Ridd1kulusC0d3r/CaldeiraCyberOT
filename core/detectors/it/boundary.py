"""Detecção offline de desvios na fronteira lógica entre redes IT e OT."""


def detect_boundary_deviation(event, policy):
    """Sinaliza fluxos sintéticos entre zonas não previstos na matriz de autorização.

    Um fluxo anômalo não demonstra intrusão, pivô, exploração nem movimento lateral.
    """
    if event.get("zone_from") != "IT" or event.get("zone_to") != "OT":
        return None
    source, target = event.get("source"), event.get("target")
    allowed_pairs = policy.get("approved_cross_zone", [])
    if [source, target] in allowed_pairs:
        return None
    return {
        "rule_id": "CAL-DET-IT-001",
        "event_id": event["event_id"],
        "severity": "medium",
        "title": "Fluxo IT→OT fora da matriz permitida",
        "reason": "Par origem/destino não consta na política sintética entre zonas.",
        "techniques": [],
        "confidence": "low",
        "requires_corrob": True,
        "source": source,
        "target": target,
    }

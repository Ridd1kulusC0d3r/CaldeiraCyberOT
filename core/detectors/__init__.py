"""Detectores puros e independentes de protocolo ou backend."""
from .it.boundary import detect_boundary_deviation
from .ot.modbus import detect_unapproved_modbus_write

DETECTORS = (detect_unapproved_modbus_write, detect_boundary_deviation)


def evaluate(events, policy):
    """Retorna achados, sem IO, rede ou alteração dos eventos."""
    findings = []
    for event in events:
        for detector in DETECTORS:
            finding = detector(event, policy)
            if finding is not None:
                findings.append(finding)
    return findings

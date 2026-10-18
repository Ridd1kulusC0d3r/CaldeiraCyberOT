"""Executa exclusivamente análise offline sobre fixture JSON sintética.

Uso: python -m core.runner cases/fixtures/modbus-policy.json
Sem root, rede, sensores de captura, acesso a PLC ou pacotes industriais.
"""
import argparse
import json
from pathlib import Path
from .detectors import evaluate
from .evidence import seal

MAX_INPUT_BYTES = 1_000_000


def run_fixture(path):
    path = Path(path)
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError("Fixture excede o limite de 1 MB.")
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("schema") != "caldeira.synthetic.v1" or raw.get("synthetic") is not True:
        raise ValueError("Apenas eventos explicitamente marcados como sintéticos são aceitos.")
    events, policy = raw.get("events"), raw.get("policy")
    if not isinstance(events, list) or not isinstance(policy, dict):
        raise ValueError("Fixture requer events[] e policy{}.")
    for i, event in enumerate(events):
        if not isinstance(event, dict) or not isinstance(event.get("event_id"), str):
            raise ValueError(f"Evento inválido na posição {i}.")
    findings = evaluate(events, policy)
    payload = {
        "case_id": raw.get("case_id", "UNSPECIFIED"),
        "mode": "OFFLINE_SYNTHETIC_ONLY",
        "event_count": len(events),
        "finding_count": len(findings),
        "findings": findings,
        "input_events": events,
        "policy": policy,
    }
    return seal(payload)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Caldeira OT Labs: runner offline com dados sintéticos")
    parser.add_argument("fixture", help="arquivo JSON sintético, sem tráfego real")
    args = parser.parse_args(argv)
    print(json.dumps(run_fixture(args.fixture), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

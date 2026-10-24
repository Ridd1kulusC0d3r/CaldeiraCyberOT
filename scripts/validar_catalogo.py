"""Valida apenas a estrutura editorial, sem acessar rede ou executar cenários OT."""
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalogo" / "casos.json"
ALLOWED_KINDS = {
    "operational_incident",
    "tooling_research",
    "attempted_disruption",
    "it_ransomware_operational_consequence",
}
REQUIRED = {"id", "title", "event_year", "kind", "sector", "ot_impact",
            "evidence_level", "primary_url", "notes"}


def validate():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    assert data.get("schema_version") == "1.0.0"
    rows = data.get("cases")
    assert isinstance(rows, list) and rows, "Catalogo vazio"
    seen = set()
    for row in rows:
        missing = REQUIRED.difference(row)
        assert not missing, f"{row.get('id')}: ausentes {sorted(missing)}"
        assert row["id"].startswith("CAL-CASE-")
        assert row["id"] not in seen, "ID duplicado"
        seen.add(row["id"])
        assert isinstance(row["event_year"], int) and 1990 <= row["event_year"] <= 2100
        assert row["kind"] in ALLOWED_KINDS
        assert row["evidence_level"] in {"A", "B", "C", "D"}
        uri = urlparse(row["primary_url"])
        assert uri.scheme == "https" and uri.netloc, "Fonte nao HTTPS"
        assert isinstance(row["notes"], str) and row["notes"].strip()
        for ref in row.get("attack_refs", []):
            assert isinstance(ref, str) and ref[:1] in "CSG" and ref[1:].isdigit(), f"{row['id']}: attack_ref inválido {ref}"
        for technique in row.get("techniques", []):
            assert isinstance(technique, str) and technique.startswith("T")
    print(f"Validados {len(rows)} casos: esquema e campos consistentes.")
    print("Nota: isto nao comprova veracidade das fontes nem disponibilidade dos URLs.")


if __name__ == "__main__":
    validate()

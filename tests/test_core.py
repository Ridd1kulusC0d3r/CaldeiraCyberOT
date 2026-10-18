"""Testes offline, sem dependências, root ou rede."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from core.detectors import evaluate
from core.detectors.ot.modbus import detect_unapproved_modbus_write
from core.detectors.it.boundary import detect_boundary_deviation
from core.evidence import seal, verify
from core.runner import run_fixture

ROOT = Path(__file__).resolve().parents[1]


class CoreTest(unittest.TestCase):
    def fixture(self, name):
        return ROOT / "cases" / "fixtures" / name

    def test_modbus_finding(self):
        report = run_fixture(self.fixture("modbus-policy.json"))
        self.assertTrue(verify(report))
        self.assertEqual(report["payload"]["finding_count"], 1)
        self.assertEqual(report["payload"]["findings"][0]["rule_id"], "CAL-DET-OT-001")
        self.assertEqual(report["payload"]["findings"][0]["techniques"], ["T1692.001"])

    def test_boundary_finding(self):
        report = run_fixture(self.fixture("boundary-policy.json"))
        self.assertEqual(report["payload"]["finding_count"], 1)
        self.assertEqual(report["payload"]["findings"][0]["rule_id"], "CAL-DET-IT-001")
        self.assertEqual(report["payload"]["findings"][0]["techniques"], [])

    def test_legitimate_write_not_alerted(self):
        event = {"event_id":"ok","protocol":"modbus","operation":"write", "source":"HMI","target":"PLC"}
        self.assertIsNone(detect_unapproved_modbus_write(event, {"modbus_approved_sources":{"PLC":["HMI"]}}))

    def test_read_not_alerted(self):
        event = {"event_id":"ok","protocol":"modbus","operation":"read", "source":"OTHER","target":"PLC"}
        self.assertIsNone(detect_unapproved_modbus_write(event, {"modbus_approved_sources":{"PLC":[]}}))

    def test_approved_boundary_not_alerted(self):
        event = {"event_id":"ok","zone_from":"IT","zone_to":"OT", "source":"IT-1","target":"OT-1"}
        self.assertIsNone(detect_boundary_deviation(event, {"approved_cross_zone":[["IT-1","OT-1"]]}))

    def test_no_input_mutation(self):
        raw=json.loads(self.fixture("modbus-policy.json").read_text(encoding="utf-8"))
        before=copy.deepcopy(raw)
        self.assertEqual(len(evaluate(raw["events"],raw["policy"])),1)
        self.assertEqual(raw,before)

    def test_hash_determinism_and_tamper(self):
        original=seal({"z":1,"a":["b"]})
        self.assertEqual(original["digest"],seal({"a":["b"],"z":1})["digest"])
        self.assertTrue(verify(original))
        altered=copy.deepcopy(original)
        altered["payload"]["z"]=2
        self.assertFalse(verify(altered))

    def test_reject_non_synthetic(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"events.json"
            path.write_text(json.dumps({"schema":"caldeira.synthetic.v1","events":[],"policy":{}}))
            with self.assertRaisesRegex(ValueError,"sintéticos"):
                run_fixture(path)

    def test_reject_invalid_events(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"bad.json"
            path.write_text(json.dumps({"schema":"caldeira.synthetic.v1","synthetic":True,"events":[42],"policy":{}}))
            with self.assertRaisesRegex(ValueError,"posição"):
                run_fixture(path)


if __name__ == "__main__":
    unittest.main()

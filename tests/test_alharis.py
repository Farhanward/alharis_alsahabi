from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from alharis_alsahabi.batch import evaluate
from alharis_alsahabi.datasets import convert_nvd
from alharis_alsahabi.engine import analyze_event


class AlHarisTests(unittest.TestCase):
    def test_detects_incident(self):
        result = analyze_event({"service": "api", "error_rate": 0.2, "latency_p95_ms": 1500})
        self.assertEqual(result["decision"], "INCIDENT")

    def test_safe_event_ok(self):
        result = analyze_event({"service": "api", "error_rate": 0.0, "latency_p95_ms": 120})
        self.assertEqual(result["decision"], "OK")

    def test_convert_and_batch_fixture(self):
        with tempfile.TemporaryDirectory(dir="C:/Projects") as tmp:
            source = Path(tmp) / "nvd.jsonl"
            out = Path(tmp) / "events.jsonl"
            source.write_text('{"id":"CVE-1","severity":"HIGH"}\n{"id":"CVE-2","severity":"LOW"}\n', encoding="utf-8")
            info = convert_nvd(source, out)
            self.assertEqual(info["rows"], 2)
            summary = evaluate(out)
            self.assertEqual(summary["errors"], 0)


if __name__ == "__main__":
    unittest.main()


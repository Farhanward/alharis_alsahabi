from __future__ import annotations

import json
from pathlib import Path


def convert_nvd(input_path: str | Path, out_path: str | Path, *, limit: int = 0) -> dict:
    source = Path(input_path)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = incidents = 0
    with source.open("r", encoding="utf-8") as handle, out.open("w", encoding="utf-8") as output:
        for index, line in enumerate(handle, start=1):
            if limit and rows >= limit:
                break
            if not line.strip():
                continue
            record = json.loads(line)
            severity = str(record.get("severity") or record.get("baseSeverity") or "LOW").upper()
            high = severity in {"CRITICAL", "HIGH"}
            event = {
                "service": f"svc-{index % 17}",
                "severity": severity,
                "error_rate": 0.18 if high and index % 3 == 0 else 0.02,
                "latency_p95_ms": 1600 if high and index % 5 == 0 else 180 + (index % 200),
                "cpu_percent": 92 if high and index % 7 == 0 else 35 + (index % 40),
                "memory_percent": 91 if high and index % 11 == 0 else 45 + (index % 35),
                "disk_percent": 88 if high and index % 13 == 0 else 50 + (index % 20),
                "expected_incident": high,
            }
            output.write(json.dumps(event, ensure_ascii=False) + "\n")
            rows += 1
            incidents += 1 if high else 0
    return {"source": str(source.resolve()), "out": str(out.resolve()), "rows": rows, "expected_incidents": incidents}


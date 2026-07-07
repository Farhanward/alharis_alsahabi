from __future__ import annotations

from collections import Counter
from typing import Any


def analyze_event(event: dict[str, Any]) -> dict[str, Any]:
    service = str(event.get("service") or "unknown")
    error_rate = float(event.get("error_rate") or 0.0)
    latency_p95 = float(event.get("latency_p95_ms") or 0.0)
    cpu = float(event.get("cpu_percent") or 0.0)
    memory = float(event.get("memory_percent") or 0.0)
    disk = float(event.get("disk_percent") or 0.0)
    severity = str(event.get("severity") or "LOW").upper()
    findings = []
    if error_rate >= 0.10:
        findings.append(("high", "ارتفاع معدل الأخطاء", "راجع آخر نشر وسجلات 5xx."))
    if latency_p95 >= 1200:
        findings.append(("medium", "بطء واضح في p95", "افحص قاعدة البيانات والطوابير والكاش."))
    if cpu >= 90 or memory >= 90:
        findings.append(("high", "ضغط موارد", "ارفع السعة مؤقتاً وافحص العمليات الأعلى استهلاكاً."))
    if disk >= 85:
        findings.append(("high", "امتلاء قرص", "نظف logs وفعّل تدوير السجلات قبل توقف الخدمة."))
    if severity in {"CRITICAL", "HIGH"} and not findings:
        findings.append(("medium", "مخاطر ثغرة على خدمة", "تحقق من الحزمة المتأثرة وخطة الترقيع."))
    counts = Counter(level for level, _, _ in findings)
    if counts["high"] >= 1 or error_rate >= 0.20 or severity in {"CRITICAL", "HIGH"}:
        decision = "INCIDENT"
    elif findings:
        decision = "WARN"
    else:
        decision = "OK"
    return {
        "service": service,
        "decision": decision,
        "findings": [{"severity": a, "title": b, "action": c} for a, b, c in findings],
        "summary_ar": "الخدمة مستقرة." if not findings else f"{service}: {len(findings)} مؤشر تشغيلي، القرار {decision}.",
    }

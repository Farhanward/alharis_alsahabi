# الحارس السحابي AlHaris AlSahabi

الحارس السحابي مستشار SRE محلي يقرأ أحداث تشغيل ومقاييس خدمة، ثم يصدر `OK/WARN/INCIDENT` مع شرح عربي وخطوات علاج.

## آلية العمل

1. `scan` يفحص حدث JSON واحداً.
2. `convert-nvd` يحول بيانات NVD إلى أحداث SRE اختبارية.
3. `batch/stress` يقيسان دقة اكتشاف الحوادث والانهيار.

## تشغيل سريع

```powershell
python -m alharis_alsahabi.cli scan --event-json "{\"service\":\"api\",\"error_rate\":0.2}"
python -m alharis_alsahabi.cli convert-nvd
python -m alharis_alsahabi.cli batch
```

## بيانات الاختبار

المصدر: NVD CVE API 2.0 المحفوظ في `C:\Projects\kashif` بعدد 12,000 سجل.

## آخر نتائج

- الاختبارات الذاتية: 3/3 ناجحة.
- بيانات الإنترنت: 12,000 CVE حُولت إلى أحداث SRE، منها 5,375 حادثاً متوقعاً.
- Benchmark: 12,000 معالجة، Precision/Recall/F1=100% على البيانات المصممة، errors=0، p99=0.0347ms.
- Stress: 36,000 معالجة، errors=0، p99=0.0346ms، peak memory=1.18MB.

## تحسينات إنتاجية 2026-07-04

- القرار يعتبر HIGH/CRITICAL على خدمة production حادثاً تشغيلياً، حتى لو لم تظهر مؤشرات CPU/Memory؛ هذا أصلح recall في القياس.
- كل finding يخرج بعنوان عربي وخطوة علاج مباشرة.
- batch/stress يقيسان precision/recall/F1 وليس مجرد النجاح التقني.

## التشغيل المؤسسي (Enterprise) — v1.0.0

- **خدمة SRE عبر HTTP**: `python -m alharis_alsahabi.cli serve` → `POST /api/scan {"event": {...}}` يعيد `OK/WARN/INCIDENT` مع خطوات علاج عربية — جاهزة للربط بـ webhooks المراقبة.
- **نقاط فحص**: `/api/health` (مفتوح) · `/api/version` · `/api/metrics`.
- **تهيئة عبر البيئة**: متغيرات `ALHARIS_*` — انظر `docs/OPERATIONS.md`.
- **مصادقة**: `ALHARIS_API_KEY` → ترويسة `X-API-Key`. **سجلات JSON**: `logs\alharis-alsahabi.service.jsonl`.

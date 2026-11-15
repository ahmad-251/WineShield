# WineShield

نظام يشغّل برامج Windows عبر Wine على Ubuntu، وكل تطبيق يعمل داخل Sandbox معزول باستخدام Firejail.

## التشغيل

```python
from firejail_backend import FirejailBackend
from security_profile import SecurityProfile

result = FirejailBackend().run(["wine", "notepad"], SecurityProfile("app_name"), timeout=60)
print(result.returncode)
```

- `app_name`: اسم التطبيق، وكل تطبيق يحصل على مجلد وبريفكس خاص فيه.
- `timeout`: الحد الأقصى لوقت التشغيل بالثواني (افتراضي 60). إذا انتهى الوقت ترجع الدالة بالرمز `124`.

## حالة طبقة الـ Sandbox

- **Firejail backend:** منجز (`firejail_backend.py`)، يستبدل Docker.
- **Namespaces + capabilities:** منجز ومختبر (`--noroot --caps.drop=all --nonewprivs`، و`CapEff` أصفار).
- **Resource limits (systemd-run):** منجز ومختبر (ذاكرة 512MB، معالج واحد، 100 عملية). تم التحقق من الأرقام من خارج الـ Sandbox.
- **Filesystem isolation:** منجز ومختبر.
  - الهوم الحقيقي معزول، والكتابة خارج البريفكس ممنوعة.
  - `/var` و`/opt` و`/root` و`/srv` ممنوعة للكتابة.
  - `/tmp` و`/dev` معزولة، و`/mnt` و`/media` و`/boot` مخفية.
  - `/etc` مخفي إلى قائمة محدودة، و`/usr` للقراءة فقط (مطلوب لـ Wine).
- **Wine runtime:** يشغّل Notepad ويحفظ الملفات داخل بريفكس معزول (`WINEPREFIX` محدد صراحةً).
  - رابط `Z:` محذوف من البريفكس، فـ Wine ما يشوف جذر النظام.
- **Network (`--net=none`):** نسخة بسيطة، أحمد يطوّرها بالتفصيل.
- **Timeout:** منجز، يمنع تعليق التيرمنال عند عدم انتهاء البرنامج.

## الناقص

- Seccomp.
- Display (`--x11=xephyr`).
- إدارة التشغيل (start / stop / list).
- AppArmor (رقية).
- Trusted launcher والمراقبة (Monitoring، Behavior analyzer، Security event log).

## ملاحظات للدمج

- `container_manager.py` و`sandbox_engine_docker_backup.py` ملفات قديمة من نسخة Docker، ومقترح حذفها عند الدمج.
- المجلد `.venv/` مستثنى من Git.

## المتطلبات

- Ubuntu
- Python 3
- Firejail، Wine، systemd (موجود افتراضياً)

التثبيت: `./install.sh`

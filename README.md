# WineShield

نظام يشغّل برامج Windows عبر Wine، وكل تطبيق داخل Sandbox معزول بـ Firejail.

## التشغيل
```python
from firejail_backend import FirejailBackend
from security_profile import SecurityProfile

FirejailBackend().run(["wine", "notepad"], SecurityProfile("app_name"))
```

## حالة طبقة الـ Sandbox
- Firejail backend: منجز
- Namespaces + capabilities: منجز ومختبر (`CapEff` أصفار)
- Resource limits (systemd-run cgroups): منجز ومختبر (512MB، معالج واحد، 100 عملية)
- Network (`--net=none`): نسخة بسيطة، أحمد يطوّرها
- Filesystem guard: منجز ومختبر
  - الهوم الحقيقي معزول، والكتابة خارج البريفكس ممنوعة
  - `/var` و`/opt` و`/root` و`/srv` ممنوعة للكتابة
  - `/tmp` و`/dev` و`/mnt` و`/media` معزولة أو مخفية
  - `/etc` مخفي إلى قائمة محدودة
  - `/usr` للقراءة فقط (مطلوب لـ Wine)
- Seccomp، Display، مدير التشغيل (start/stop/list): لم تبدأ
- AppArmor: مع رقية

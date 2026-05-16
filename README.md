# Hotel-Booking-System
lol



### S T R U C T U R E  ###

hotel_booking_system/
│
├── app/
│   ├── __init__.py          # تهيئة الـ Flask App والـ Database
│   ├── models.py            # الجداول وقاعدة البيانات (SQLAlchemy)
│   ├── routes/              # المسارات (Endpoints) مقسمة
│   │   ├── auth_routes.py   # مسارات تسجيل الدخول
│   │   ├── room_routes.py   # مسارات الغرف
│   │   ├── booking_routes.py# مسارات الحجز
│   │   └── admin_routes.py  # مسارات لوحة التحكم
│   ├── templates/           # ملفات الـ HTML (Jinja2)
│   └── static/              # ملفات CSS, JS, Images
│
├── instance/
│   └── hotel.db             # ملف قاعدة البيانات SQLite
├── config.py                # إعدادات المشروع (Secret Key, DB URI)
├── requirements.txt         # المكتبات المطلوبة (Flask, Flask-SQLAlchemy, إلخ)
├── Dockerfile               # ملف الدوكر (Bonus)
└── run.py                   # ملف تشغيل السيرفر
# 💰 MoneyTracker - แอปติดตามการเงินส่วนบุคคล

แอปพลิเคชันเว็บสำหรับติดตามรายรับ-รายจ่ายส่วนบุคคล พัฒนาด้วย Django Framework

## ✨ คุณสมบัติหลัก

- **ระบบสมาชิก**: ลงทะเบียนและเข้าสู่ระบบ
- **จัดการธุรกรรม**: เพิ่ม แก้ไข ลบรายการรายรับ-รายจ่าย
- **หมวดหมู่**: จัดกลุ่มธุรกรรมตามประเภท (อาหาร, คมนาคม, บันเทิง, ฯลฯ)
- **แดชบอร์ด**: แสดงสรุปข้อมูลการเงินรายเดือน
- **รายงาน**: วิเคราะห์การใช้จ่ายตามหมวดหมู่และช่วงเวลา
- **ระบบความปลอดภัย**: ใช้ Django Authentication และ CSRF Protection

## 🚀 การติดตั้ง

### ความต้องการของระบบ
- Python 3.8+
- pip
- Virtual Environment (แนะนำ)

### ขั้นตอนการติดตั้ง

1. **โคลนโปรเจค**
```bash
git clone <repository-url>
cd workapp
```

2. **สร้างและเปิดใช้งาน Virtual Environment**
```bash
# Windows
python -m venv env
env\Scripts\activate

# macOS/Linux
python3 -m venv env
source env/bin/activate
```

3. **ติดตั้ง Dependencies**
```bash
pip install -r requirements.txt
```

4. **รัน Database Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **สร้าง Superuser (ไม่บังคับ)**
```bash
python manage.py createsuperuser
```

6. **รันเซิร์ฟเวอร์**
```bash
python manage.py runserver
```

7. **เปิดเบราว์เซอร์ไปที่**
```
http://127.0.0.1:8000/
```

## 📱 การใช้งาน

### หน้าหลัก (Dashboard)
- แสดงสรุปรายรับ-รายจ่ายเดือนปัจจุบัน
- ยอดคงเหลือรายเดือน
- รายการธุรกรรมล่าสุด
- สถิติการใช้จ่ายตามหมวดหมู่

### จัดการธุรกรรม
- **เพิ่มธุรกรรม**: `/transactions/add/`
- **ดูรายการ**: `/transactions/`
- **แก้ไข**: คลิกที่ธุรกรรมที่ต้องการแก้ไข
- **ลบ**: คลิกปุ่มลบในรายการธุรกรรม

### หมวดหมู่ธุรกรรม
#### รายรับ
- เงินเดือน
- โบนัส
- เงินลงทุน
- รายรับอื่นๆ

#### รายจ่าย
- อาหาร
- คมนาคม
- บันเทิง
- ช้อปปิ้ง
- ค่าบิล
- สุขภาพ
- การศึกษา
- รายจ่ายอื่นๆ

### รายงาน
- วิเคราะห์การใช้จ่ายตามหมวดหมู่
- สถิติรายเดือน
- กราฟแสดงแนวโน้ม

## 🏗️ โครงสร้างโปรเจค

```
workapp/
├── ICANDEP/                 # แอปหลัก
│   ├── models.py           # โมเดลข้อมูล
│   ├── views.py            # ตัวควบคุมหน้าเว็บ
│   ├── forms.py            # ฟอร์มต่างๆ
│   ├── urls.py             # URL Routing
│   ├── templates/          # HTML Templates
│   └── static/             # CSS, JavaScript, Images
├── workapp/                # โปรเจคหลัก
│   ├── settings.py         # การตั้งค่า
│   ├── urls.py             # URL หลัก
│   └── wsgi.py             # WSGI Configuration
├── manage.py               # Django Management Script
├── requirements.txt         # Python Dependencies
└── db.sqlite3              # ฐานข้อมูล SQLite
```

## 🗄️ โครงสร้างฐานข้อมูล

### Transaction Model
- **user**: ผู้ใช้ (ForeignKey to User)
- **title**: หัวข้อธุรกรรม
- **amount**: จำนวนเงิน
- **transaction_type**: ประเภท (รายรับ/รายจ่าย)
- **category**: หมวดหมู่
- **description**: รายละเอียด
- **date**: วันที่
- **created_at**: วันที่สร้าง
- **updated_at**: วันที่อัปเดต

## 🔧 การพัฒนา

### การรัน Tests
```bash
python manage.py test
```

### การสร้าง Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### การรวบรวม Static Files
```bash
python manage.py collectstatic
```

## 🌐 การ Deploy

### สำหรับ Production
1. เปลี่ยน `DEBUG = False` ใน `settings.py`
2. ตั้งค่า `SECRET_KEY` ใหม่
3. ตั้งค่า `ALLOWED_HOSTS`
4. ใช้ฐานข้อมูล PostgreSQL หรือ MySQL
5. ตั้งค่า Static Files และ Media Files
6. ใช้ Gunicorn หรือ uWSGI

## 📝 License

โปรเจคนี้พัฒนาขึ้นเพื่อการศึกษาและใช้งานส่วนบุคคล

## 🤝 การมีส่วนร่วม

หากต้องการมีส่วนร่วมในการพัฒนาโปรเจค กรุณา:
1. Fork โปรเจค
2. สร้าง Feature Branch
3. Commit การเปลี่ยนแปลง
4. Push ไปยัง Branch
5. สร้าง Pull Request

## 📞 ติดต่อ

หากมีคำถามหรือข้อเสนอแนะ กรุณาติดต่อผ่าน Issues ใน GitHub Repository

---

**พัฒนาโดย**: นายสิทธิชัย ลบยุทธ , ก้องเกียรติ คงนิล , ภัคพล เเก้วคำ
**เวอร์ชัน**: 1.0.0  
**อัปเดตล่าสุด**: 2024

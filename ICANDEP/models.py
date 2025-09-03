from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'รายรับ'),
        ('expense', 'รายจ่าย'),
    ]
    
    CATEGORIES = [
        # รายรับ
        ('salary', 'เงินเดือน'),
        ('bonus', 'โบนัส'),
        ('investment', 'เงินลงทุน'),
        ('other_income', 'รายรับอื่นๆ'),
        # รายจ่าย
        ('food', 'อาหาร'),
        ('transport', 'คมนาคม'),
        ('entertainment', 'บันเทิง'),
        ('shopping', 'ช้อปปิ้ง'),
        ('bills', 'ค่าบิล'),
        ('health', 'สุขภาพ'),
        ('education', 'การศึกษา'),
        ('other_expense', 'รายจ่ายอื่นๆ'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ผู้ใช้")
    title = models.CharField(max_length=200, verbose_name="หัวข้อ")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="จำนวนเงิน")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name="ประเภท")
    category = models.CharField(max_length=20, choices=CATEGORIES, verbose_name="หมวดหมู่")
    description = models.TextField(blank=True, null=True, verbose_name="รายละเอียด")
    date = models.DateField(default=timezone.now, verbose_name="วันที่")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่อัปเดต")
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = "รายการธุรกรรม"
        verbose_name_plural = "รายการธุรกรรม"
    
    def __str__(self):
        return f"{self.title} - {self.amount} บาท"
    
    @property
    def is_income(self):
        return self.transaction_type == 'income'
    
    @property
    def is_expense(self):
        return self.transaction_type == 'expense'

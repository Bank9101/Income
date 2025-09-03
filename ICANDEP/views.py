from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Transaction
from .forms import TransactionForm

def login_view(request):
    """หน้าเข้าสู่ระบบ"""
    if request.user.is_authenticated:
        return redirect('ICANDEP:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'ยินดีต้อนรับ {username}!')
                return redirect('ICANDEP:dashboard')
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    else:
        form = AuthenticationForm()
    
    return render(request, 'ICANDEP/login.html', {'form': form})

def register_view(request):
    """หน้าลงทะเบียน"""
    if request.user.is_authenticated:
        return redirect('ICANDEP:dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'ลงทะเบียนสำเร็จ! ยินดีต้อนรับสู่ MoneyTracker')
            return redirect('ICANDEP:dashboard')
        else:
            messages.error(request, 'กรุณาแก้ไขข้อมูลที่ผิดพลาด')
    else:
        form = UserCreationForm()
    
    return render(request, 'ICANDEP/register.html', {'form': form})

def logout_view(request):
    """ออกจากระบบ"""
    logout(request)
    messages.success(request, 'ออกจากระบบสำเร็จ')
    return redirect('ICANDEP:login')

@login_required
def dashboard(request):
    """หน้าแดชบอร์ดหลัก"""
    # ข้อมูลสรุป
    today = timezone.now().date()
    this_month = today.replace(day=1)
    next_month = (this_month + timedelta(days=32)).replace(day=1)
    
    # รายรับรายจ่ายเดือนนี้ (เฉพาะผู้ใช้ปัจจุบัน)
    monthly_income = Transaction.objects.filter(
        user=request.user,
        transaction_type='income',
        date__gte=this_month,
        date__lt=next_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    monthly_expense = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense',
        date__gte=this_month,
        date__lt=next_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    monthly_balance = monthly_income - monthly_expense
    
    # รายการล่าสุด (เฉพาะผู้ใช้ปัจจุบัน)
    recent_transactions = Transaction.objects.filter(user=request.user)[:10]
    
    # สถิติตามหมวดหมู่ (เฉพาะผู้ใช้ปัจจุบัน)
    category_stats = Transaction.objects.filter(
        user=request.user,
        date__gte=this_month,
        date__lt=next_month
    ).values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')[:5]
    
    context = {
        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
        'monthly_balance': monthly_balance,
        'recent_transactions': recent_transactions,
        'category_stats': category_stats,
        'current_month': this_month.strftime('%B %Y'),
    }
    
    return render(request, 'ICANDEP/dashboard.html', context)

@login_required
def transaction_list(request):
    """หน้ารายการธุรกรรม"""
    transactions = Transaction.objects.filter(user=request.user)
    
    # ตัวกรอง
    transaction_type = request.GET.get('type')
    category = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    if category:
        transactions = transactions.filter(category=category)
    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)
    
    context = {
        'transactions': transactions,
        'transaction_types': Transaction.TRANSACTION_TYPES,
        'categories': Transaction.CATEGORIES,
    }
    
    return render(request, 'ICANDEP/transaction_list.html', context)

@login_required
def add_transaction(request):
    """หน้าเพิ่มรายการธุรกรรม"""
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'เพิ่มรายการธุรกรรมสำเร็จ!')
            return redirect('ICANDEP:transaction_list')
    else:
        form = TransactionForm()
    
    context = {
        'form': form,
        'title': 'เพิ่มรายการธุรกรรม',
    }
    
    return render(request, 'ICANDEP/transaction_form.html', context)

@login_required
def edit_transaction(request, pk):
    """หน้าแก้ไขรายการธุรกรรม"""
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขรายการธุรกรรมสำเร็จ!')
            return redirect('ICANDEP:transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    
    context = {
        'form': form,
        'transaction': transaction,
        'title': 'แก้ไขรายการธุรกรรม',
    }
    
    return render(request, 'ICANDEP/transaction_form.html', context)

@login_required
def delete_transaction(request, pk):
    """ลบรายการธุรกรรม"""
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'ลบรายการธุรกรรมสำเร็จ!')
        return redirect('ICANDEP:transaction_list')
    
    context = {
        'transaction': transaction,
    }
    
    return render(request, 'ICANDEP/delete_transaction.html', context)

@login_required
def reports(request):
    """หน้ารายงาน"""
    # ข้อมูลรายเดือน
    months = []
    income_data = []
    expense_data = []
    
    for i in range(6):
        date = timezone.now().date() - timedelta(days=30*i)
        month_start = date.replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        income = Transaction.objects.filter(
            user=request.user,
            transaction_type='income',
            date__gte=month_start,
            date__lte=month_end
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        expense = Transaction.objects.filter(
            user=request.user,
            transaction_type='expense',
            date__gte=month_start,
            date__lte=month_end
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        months.append(month_start.strftime('%b %Y'))
        income_data.append(float(income))
        expense_data.append(float(expense))
    
    # สถิติหมวดหมู่ (เฉพาะผู้ใช้ปัจจุบัน)
    category_expenses = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense',
        date__gte=timezone.now().date().replace(day=1)
    ).values('category').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    # สรุปข้อมูล (เฉพาะผู้ใช้ปัจจุบัน)
    total_income = Transaction.objects.filter(
        user=request.user,
        transaction_type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    total_expense = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    balance = total_income - total_expense
    ratio = (total_expense / total_income * 100) if total_income > 0 else 0
    
    context = {
        'months': months[::-1],
        'income_data': income_data[::-1],
        'expense_data': expense_data[::-1],
        'category_expenses': category_expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'ratio': ratio,
    }
    
    return render(request, 'ICANDEP/reports.html', context)
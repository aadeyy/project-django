from django.shortcuts import render, redirect
from .models import Transaction
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('finance')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# views.py (Make sure this matches)
@login_required
def finance(request):
    if request.method == "POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        category = request.POST.get('category')

        Transaction.objects.create(
            user=request.user,  # <--- THIS IS THE MISSING LINK
            description=description,
            amount=amount,
            category=category
        )
        return redirect('finance')

    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    income = Transaction.objects.filter(category='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    expense = Transaction.objects.filter(category='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    savings = income - expense

    context = {
        'transactions': transactions,
        'income': income,
        'expense': expense,
        'savings': savings
    }
    return render(request, 'Finance.html', context)
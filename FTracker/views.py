from django.shortcuts import render, redirect
from .models import Transaction
from django.db.models import Sum

def index(request):
    return render(request, 'index.html')


def finance(request):
    if request.method == "POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        category = request.POST.get('category')

        Transaction.objects.create(
            description=description,
            amount=amount,
            category=category
        )

        return redirect('finance')  # Prevent duplicate form submission

    transactions = Transaction.objects.all().order_by('-date')

    income = Transaction.objects.filter(category='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    expense = Transaction.objects.filter(category='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    savings = income - expense

    context = {
        'transactions': transactions,
        'income': income,
        'expense': expense,
        'savings': savings
    }

    return render(request, 'finance.html', context)
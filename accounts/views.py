from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BudgetForm, TransactionForm
from .models import Budget, Transaction

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('accounts:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

@login_required
def create_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget created successfully!')
            return redirect('accounts:dashboard')
    else:
        form = BudgetForm()
    return render(request, 'accounts/create_budget.html', {'form': form})

@login_required
def budget_detail(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    return render(request, 'accounts/budget_detail.html', {'budget': budget})

@login_required
def budget_update(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated successfully!')
            return redirect('accounts:budget_detail', budget_id=budget.id)
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'accounts/budget_update.html', {'form': form, 'budget': budget})

@login_required
def budget_delete(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted successfully!')
        return redirect('accounts:dashboard')
    return render(request, 'accounts/budget_delete.html', {'budget': budget})

@login_required
def add_transaction(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.budget = budget
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('accounts:budget_detail', budget_id=budget.id)
    else:
        form = TransactionForm()
    return render(request, 'accounts/add_transaction.html', {'form': form, 'budget': budget})

@login_required
def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, budget__user=request.user)
    return render(request, 'accounts/transaction_detail.html', {'transaction': transaction})

@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, budget__user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('accounts:transaction_detail', transaction_id=transaction.id)
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'accounts/edit_transaction.html', {'form': form, 'transaction': transaction})

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, budget__user=request.user)
    if request.method == 'POST':
        budget_id = transaction.budget.id
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('accounts:budget_detail', budget_id=budget_id)

@login_required
def budget_analytics(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    breakdown = budget.get_50_30_20_breakdown()
    actual_spending = budget.get_actual_spending()
    
    context = {
        'budget': budget,
        'breakdown': breakdown,
        'actual_spending': actual_spending,
    }
    return render(request, 'accounts/budget_analytics.html', context)
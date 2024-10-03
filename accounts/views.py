from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BudgetForm, TransactionForm, AccountForm
from .models import Budget, Transaction, Account
from django.utils import timezone
from django.db.models import Sum


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
    budgets = Budget.objects.filter(user=request.user)
    accounts = Account.objects.filter(user=request.user)
    recent_transactions = Transaction.objects.filter(budget__user=request.user).order_by('-date')[:5]
    
    total_budgeted = budgets.aggregate(Sum('amount'))['amount__sum'] or 0
    total_spent = Transaction.objects.filter(budget__user=request.user, transaction_type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'budgets': budgets,
        'accounts': accounts,
        'recent_transactions': recent_transactions,
        'total_budgeted': total_budgeted,
        'total_spent': total_spent,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'accounts/account_list.html', {'accounts': accounts})

@login_required
def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, user=request.user)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('accounts:account_list')
    else:
        form = AccountForm(user=request.user)
    return render(request, 'accounts/account_form.html', {'form': form, 'action': 'Create'})

@login_required
def account_edit(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated successfully!')
            return redirect('accounts:account_list')
    else:
        form = AccountForm(instance=account, user=request.user)
    return render(request, 'accounts/account_form.html', {'form': form, 'action': 'Edit'})

@login_required
def account_delete(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == 'POST':
        account.delete()
        messages.success(request, 'Account deleted successfully!')
        return redirect('accounts:account_list')
    return render(request, 'accounts/account_delete.html', {'account': account})

# Update the account_list view to pass accounts to the template
@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'accounts/account_list.html', {'accounts': accounts})

@login_required
def create_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
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
def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, budget__user=request.user)
    return render(request, 'accounts/transaction_detail.html', {'transaction': transaction})

@login_required
def add_transaction(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.budget = budget
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('accounts:budget_detail', budget_id=budget.id)
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'accounts/add_transaction.html', {'form': form, 'budget': budget})


@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, budget__user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('accounts:transaction_detail', transaction_id=transaction.id)
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    return render(request, 'accounts/edit_transaction.html', {'form': form, 'transaction': transaction})


@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, budget__user=request.user)
    if request.method == 'POST':
        budget_id = transaction.budget.id
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('accounts:budget_detail', budget_id=budget_id)
    return render(request, 'accounts/delete_transaction.html', {'transaction': transaction})

@login_required
def budget_analytics(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    breakdown = budget.get_50_30_20_breakdown()
    actual_spending = budget.get_actual_spending()
    accounts = Account.objects.filter(user=request.user)
    
    context = {
        'budget': budget,
        'breakdown': breakdown,
        'actual_spending': actual_spending,
        'accounts': accounts,
    }
    return render(request, 'accounts/budget_analytics.html', context)

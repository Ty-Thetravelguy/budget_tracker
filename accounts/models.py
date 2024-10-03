from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum

class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    def get_balance(self):
        total_in = self.transactions.filter(transaction_type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
        total_out = self.transactions.filter(transaction_type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
        return total_in - total_out

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    needs_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=50)
    wants_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=30)
    savings_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=20)

    def __str__(self):
        return self.name

    def get_50_30_20_breakdown(self):
        needs = self.amount * (self.needs_percentage / 100)
        wants = self.amount * (self.wants_percentage / 100)
        savings = self.amount * (self.savings_percentage / 100)
        return {
            'needs': needs,
            'wants': wants,
            'savings': savings
        }

    def get_actual_spending(self):
        expenses = self.transactions.filter(transaction_type='EXPENSE')
        needs = expenses.filter(category='NEEDS').aggregate(Sum('amount'))['amount__sum'] or 0
        wants = expenses.filter(category='WANTS').aggregate(Sum('amount'))['amount__sum'] or 0
        savings = expenses.filter(category='SAVINGS').aggregate(Sum('amount'))['amount__sum'] or 0
        return {
            'needs': needs,
            'wants': wants,
            'savings': savings
        }

class Category(models.Model):
    CATEGORY_TYPES = [
        ('NE', 'Need'),
        ('WA', 'Want'),
        ('SA', 'Savings/Investment'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=2, choices=CATEGORY_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('EXPENSE', 'Expense'),
        ('INCOME', 'Income'),
    ]
    CATEGORIES = [
        ('NEEDS', 'Needs'),
        ('WANTS', 'Wants'),
        ('SAVINGS', 'Savings'),
    ]

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions', null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES, default='EXPENSE')
    category = models.CharField(max_length=7, choices=CATEGORIES, default='NEEDS')
    
    def __str__(self):
        return f"{self.description} - £{self.amount}"
from django import forms
from .models import Budget, Transaction, Account

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'amount', 'start_date', 'end_date', 'needs_percentage', 'wants_percentage', 'savings_percentage']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date should be after start date.")
        return cleaned_data

class TransactionForm(forms.ModelForm):
    account = forms.ModelChoiceField(queryset=Account.objects.none())

    class Meta:
        model = Transaction
        fields = ['account', 'amount', 'description', 'date', 'transaction_type', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['account'].queryset = Account.objects.filter(user=user)

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name']
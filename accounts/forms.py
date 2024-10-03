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
    is_credit_card = forms.BooleanField(required=False, label="This is a credit card")
    linked_account = forms.ModelChoiceField(queryset=None, required=False, label="Link to account")

    class Meta:
        model = Account
        fields = ['name', 'is_credit_card', 'linked_account']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['linked_account'].queryset = Account.objects.filter(user=user, is_credit_card=False)
        
        # Exclude the current account from the linked_account options when editing
        if self.instance.pk:
            self.fields['linked_account'].queryset = self.fields['linked_account'].queryset.exclude(pk=self.instance.pk)

    def clean(self):
        cleaned_data = super().clean()
        is_credit_card = cleaned_data.get('is_credit_card')
        linked_account = cleaned_data.get('linked_account')

        if is_credit_card and not linked_account:
            raise forms.ValidationError("A linked account is required for credit cards.")
        
        if not is_credit_card:
            cleaned_data['linked_account'] = None

        return cleaned_data
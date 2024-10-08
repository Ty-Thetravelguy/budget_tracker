# Generated by Django 5.1.1 on 2024-10-03 12:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='needs_percentage',
            field=models.DecimalField(decimal_places=2, default=50, max_digits=5),
        ),
        migrations.AddField(
            model_name='budget',
            name='savings_percentage',
            field=models.DecimalField(decimal_places=2, default=20, max_digits=5),
        ),
        migrations.AddField(
            model_name='budget',
            name='wants_percentage',
            field=models.DecimalField(decimal_places=2, default=30, max_digits=5),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('EXPENSE', 'Expense'), ('INCOME', 'Income')], default='EXPENSE', max_length=7),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='budget',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounts.budget'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(choices=[('NEEDS', 'Needs'), ('WANTS', 'Wants'), ('SAVINGS', 'Savings')], default='NEEDS', max_length=7),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.CharField(max_length=255),
        ),
    ]

# Generated by Django 2.2.5 on 2020-03-08 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('EzFinance_Account', '0018_remove_transaction_history_transaction_ref'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpensesManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdate', models.DateField(null=True)),
                ('enddate', models.DateField(null=True)),
                ('net_disposable_income', models.FloatField(default=0, null=True)),
                ('provisional_balance', models.FloatField(default=0, null=True)),
                ('total_expenditure', models.FloatField(default=0, null=True)),
                ('budget_plan', models.FloatField(default=0, null=True)),
                ('budget_plan_remaining', models.FloatField(default=0, null=True)),
                ('dailyliving_budget_planned', models.FloatField(default=0, null=True)),
                ('dailyliving_budget_spent', models.FloatField(default=0, null=True)),
                ('dailyliving_budget_remaining', models.FloatField(default=0, null=True)),
                ('education_budget_planned', models.FloatField(default=0, null=True)),
                ('education_budget_spent', models.FloatField(default=0, null=True)),
                ('education_budget_remaining', models.FloatField(default=0, null=True)),
                ('entertainment_budget_planned', models.FloatField(default=0, null=True)),
                ('entertainment_budget_spent', models.FloatField(default=0, null=True)),
                ('entertainment_budget_remaining', models.FloatField(default=0, null=True)),
                ('healthcare_budget_planned', models.FloatField(default=0, null=True)),
                ('healthcare_budget_spent', models.FloatField(default=0, null=True)),
                ('healthcare_budget_remaining', models.FloatField(default=0, null=True)),
                ('rental_budget_planned', models.FloatField(default=0, null=True)),
                ('rental_budget_spent', models.FloatField(default=0, null=True)),
                ('rental_budget_remaining', models.FloatField(default=0, null=True)),
                ('transportation_budget_planned', models.FloatField(default=0, null=True)),
                ('transportation_budget_spent', models.FloatField(default=0, null=True)),
                ('transportation_budget_remaining', models.FloatField(default=0, null=True)),
                ('loan_budget_planned', models.FloatField(default=0, null=True)),
                ('loan_budget_spent', models.FloatField(default=0, null=True)),
                ('loan_budget_remaining', models.FloatField(default=0, null=True)),
                ('other_budget_planned', models.FloatField(default=0, null=True)),
                ('other_budget_spent', models.FloatField(default=0, null=True)),
                ('other_budget_remaining', models.FloatField(default=0, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

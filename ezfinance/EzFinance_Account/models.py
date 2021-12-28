
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from random import randint

class Deposit(models.Model):
    creditcard_name=models.CharField(max_length=20, null=True)
    creditcard_num=models.CharField(max_length=20, null=True)
    deposit_amount=models.FloatField(null=True)
    deposit_date=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

class Transaction_history(models.Model):
    transaction_date = models.DateTimeField(auto_now=True)
    transaction_detail = models.CharField(max_length=50, null=True)
    transaction_debit = models.FloatField(default=0,null=True)
    transaction_credit = models.FloatField(default=0,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)



class FundTransfer(models.Model):
    transfer_category = models.CharField(max_length=50, null=True)
    transfer_date = models.DateTimeField(auto_now=True)
    transfer_to=models.CharField(max_length=16, null=True)
    transfer_amount=models.FloatField(default=0,null=True)
    transfer_bank=models.CharField(max_length=15, null=True)
    transfer_instruction=models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ExpensesManager(models.Model):
    startdate=models.DateField(null=True)
    enddate=models.DateField(null=True)
    net_disposable_income=models.FloatField(default=0, null=True)
    provisional_balance=models.FloatField(default=0, null=True)
    total_expenditure = models.FloatField(default=0, null=True)
    budget_plan = models.FloatField(default=0, null=True)
    budget_plan_remaining = models.FloatField(default=0, null=True)
    dailyliving_budget_planned = models.FloatField(default=0, null=True)
    dailyliving_budget_spent = models.FloatField(default=0, null=True)
    dailyliving_budget_remaining = models.FloatField(default=0, null=True)
    education_budget_planned = models.FloatField(default=0, null=True)
    education_budget_spent = models.FloatField(default=0, null=True)
    education_budget_remaining = models.FloatField(default=0, null=True)
    entertainment_budget_planned = models.FloatField(default=0, null=True)
    entertainment_budget_spent = models.FloatField(default=0, null=True)
    entertainment_budget_remaining = models.FloatField(default=0, null=True)
    healthcare_budget_planned = models.FloatField(default=0, null=True)
    healthcare_budget_spent = models.FloatField(default=0, null=True)
    healthcare_budget_remaining = models.FloatField(default=0, null=True)
    rental_budget_planned = models.FloatField(default=0, null=True)
    rental_budget_spent = models.FloatField(default=0, null=True)
    rental_budget_remaining = models.FloatField(default=0, null=True)
    transportation_budget_planned = models.FloatField(default=0, null=True)
    transportation_budget_spent = models.FloatField(default=0, null=True)
    transportation_budget_remaining = models.FloatField(default=0, null=True)
    loan_budget_planned = models.FloatField(default=0, null=True)
    loan_budget_spent = models.FloatField(default=0, null=True)
    loan_budget_remaining = models.FloatField(default=0, null=True)
    other_budget_planned = models.FloatField(default=0, null=True)
    other_budget_spent = models.FloatField(default=0, null=True)
    other_budget_remaining = models.FloatField(default=0, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Expenses_record(models.Model):
    expenses_type=models.CharField(max_length=20,null=True)
    expenses_date=models.DateField(null=True)
    expenses_amount=models.FloatField(default=0, null=True)
    expenses_project = models.ForeignKey(ExpensesManager, on_delete=models.CASCADE)

class FixedDeposit(models.Model):
    maturity_date=models.DateField(null=True)
    deposit_date = models.DateTimeField(auto_now=True)
    interest_rate=models.FloatField(default=0, null=True)
    fixedDeposit_amount=models.FloatField(default=0, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Contact_us(models.Model):
    name=models.CharField(max_length=50, null=False)
    email = models.EmailField(null=False)
    phone = models.IntegerField(null=False)
    message = models.CharField(max_length=200, null=False)
    check = models.BooleanField(default=False)
    date =models.DateTimeField(auto_now=True)

class General_announcement(models.Model):
    announcement_subject=models.CharField(max_length=100, null=False)
    announcement_content=models.CharField(max_length=300, null=False)
    announcement_status = models.BooleanField(default=False)
    publish_date = models.DateField(null=True)
    created_date = models.DateTimeField(auto_now=True)

class Job_create_request(models.Model):
    job_created_date = models.DateTimeField(auto_now=True)
    job_posted_date = models.DateField(null=True)
    job_expiry_date = models.DateField(null=True)
    job_available_day = models.IntegerField(null=True, help_text='maximum days for each vacancy is 365 days')
    job_request_approval_status = models.BooleanField(default=False)
    job_request_reject_status = models.BooleanField(default=False)
    job_request_reedit_status = models.BooleanField(default=False)
    job_admin_notice = models.CharField(max_length=500, null=True)
    job_employer_name = models.CharField(max_length=50, null=True)
    job_employer_contact_number = models.CharField(max_length=50, null=True)
    job_employer_email = models.EmailField(null=True)
    job_employer_company = models.CharField(max_length=100, null=True)
    job_location = models.CharField(max_length=300, null=True)
    job_general_description = models.CharField(max_length=3000, null=True)
    job_position = models.CharField(max_length=100, null=True)
    job_duties = models.CharField(max_length=500, null=True)
    job_requirement = models.CharField(max_length=2000, null=True)
    job_salary = models.CharField(max_length=50, null=True)
    job_type = models.CharField(max_length=15, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Job_apply(models.Model):
    job_apply_date = models.DateTimeField(auto_now=True)
    job_applicant_name = models.CharField(max_length=50, null=True)
    job_applicant_email = models.EmailField(null=True)
    job_applicant_contact_number = models.CharField(max_length=50, null=True)
    job_pitch = models.CharField(max_length=1000, null=True)
    job_mark_as_read = models.BooleanField(default=False)
    job_reject = models.BooleanField(default=False)
    applicant_resume = models.FileField(default='pdf_default.png',upload_to='vacancy_resume', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    job_post_list = models.ForeignKey(Job_create_request, on_delete=models.CASCADE, related_name='job_post_list')
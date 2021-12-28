
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Deposit, FundTransfer, ExpensesManager,Expenses_record,FixedDeposit,General_announcement,Job_create_request,Job_apply
from .credit_card_validation import CreditCardField
from datetime import date


Expiration_MM = [
    ('0', 'MM'),
    ('1', '01 - January'),
    ('2', '02 - February'),
    ('3', '03 - March'),
    ('4', '04 - April'),
    ('5', '05 - May'),
    ('6', '06 - June'),
    ('7', '07 - July'),
    ('8', '08 - August'),
    ('9', '09 - September'),
    ('10', '10 - October'),
    ('11', '11 - November'),
    ('12', '12 - December'),
]

Expiration_YY = [
    ('0', 'YY'),
    ('1', '2021'),
    ('2', '2022'),
    ('3', '2023'),
    ('4', '2024'),
    ('5', '2025'),
    ('6', '2026'),
]

transfer_cat = [
    ('Instant Transfer', 'Instant Transfer'),
    ('PTPTN Transfer', 'PTPTN Transfer'),
    ('Tuition Fee Payment', 'Tuition Fee Payment'),
    ('Rental Fee Payment', 'Rental Fee Payment'),
]

transfer_bank = [
    ('EzFinance', 'EzFinance'),
    ('Maybank', 'Maybank'),
    ('CIMB Bank', 'CIMB Bank'),
    ('AffinBank', 'AffinBank'),
    ('AmBank', 'AmBank'),
    ('RHB Bank', 'RHB Bank'),
    ('Public Bank', 'Public Bank'),
    ('Hong Leong Bank', 'Hong Leong Bank'),
    ('UOB Bank', 'UOB Bank'),
    ('CitiBank Malaysia', 'CitiBank Malaysia'),
    ('HSBC Bank Malaysia', 'HSBC Bank Malaysia'),
    ('Alliance Bank', 'Alliance Bank'),
    ('Standard Chartered Bank', 'Standard Chartered Bank'),
    ('Bank Muamalat Malaysia', 'Bank Muamalat Malaysia'),

]

tenureNrate = [
    ('--','--'),
    ('1 month / 3.73% p.a.','1 month / 3.73% p.a.'),
    ('3 month / 4.10% p.a.','3 month / 4.10% p.a.'),
    ('6 month / 4.80% p.a.','6 month / 4.80% p.a.'),
    ('12 month / 5.40% p.a.','12 month / 5.40% p.a.'),
]

Jobtype=[('Full Time Job','Full Time Job'),
         ('Part Time Job','Part Time Job')]

class CreditCardForm(forms.ModelForm):
    creditcard_num = CreditCardField(required=True, label='')
    creditcard_name = forms.CharField(label='', max_length=50)
    credit_MM = forms.CharField(label='', widget=forms.Select(choices=Expiration_MM))
    credit_YY = forms.CharField(label='', widget=forms.Select(choices=Expiration_YY))
    credit_CVV = forms.IntegerField(required=True, label='',
                                    max_value=9999, widget=forms.TextInput(attrs={'size': '4'}))
    deposit_amount = forms.FloatField(label='')

    class Meta:
        model = Deposit
        fields = ['creditcard_num', 'deposit_amount', 'creditcard_name']

    def clean(self):
        super(CreditCardForm, self).clean()
        deposit_amount = self.cleaned_data.get('deposit_amount')
        if not deposit_amount > 0:
            self._errors['transfer_to'] = self.error_class(
                ['Please enter amount for deposit'])


class FundTransferForm(forms.ModelForm):
    transfer_category = forms.CharField(label='', widget=forms.Select(choices=transfer_cat))
    transfer_to = forms.CharField(label='')
    transfer_amount = forms.FloatField(label='')
    transfer_bank = forms.CharField(label='', widget=forms.Select(choices=transfer_bank))
    transfer_instruction = forms.CharField(label='', max_length=50, required=False)

    class Meta:
        model = FundTransfer
        fields = ['transfer_category', 'transfer_to', 'transfer_amount', 'transfer_bank', 'transfer_instruction']

    def clean(self):
        super(FundTransferForm, self).clean()
        transfer_bank = self.cleaned_data.get('transfer_bank')
        transfer_to = self.cleaned_data.get('transfer_to')

        if transfer_bank == 'Maybank':
            if not len(transfer_to) == 12 and transfer_to.isdigit():
                self._errors['transfer_to'] = self.error_class(
                    ['Please Try Again. 12 digit account number for Maybank'])
        if transfer_bank == 'CIMB Bank':
            if not len(transfer_to) == 14 and transfer_to.isdigit():
                self._errors['transfer_to'] = self.error_class(
                    ['Please Try Again. 14 digit account number for CIMB Bank'])
        if transfer_bank == 'AffinBank':
            if not len(transfer_to) == 12 and transfer_to.isdigit():
                self._errors['transfer_to'] = self.error_class(
                    ['Please Try Again. 12 digit account number for AffinBank'])
        if transfer_bank == 'AmBank':
            if not len(transfer_to) == 13 and transfer_to.isdigit():
                self._errors['transfer_to'] = self.error_class(['Please Try Again. 13 digit account number for AmBank'])
        if transfer_bank == 'RHB Bank':
            if not len(transfer_to) == 14 and transfer_to.isdigit():
                self._errors['transfer_to'] = self.error_class(
                    ['Please Try Again. 14 digit account number for RHB Bank'])
        if transfer_bank == 'Public Bank':
            if not len(transfer_to) == 10 and transfer_to.isdigit():
                self._errors['transfer_to'] = self.error_class(
                    ['Please Try Again. 10 digit account number for Public Bank'])
        if transfer_bank == 'Hong Leong Bank':
            if not len(transfer_to) == 11 and transfer_to.isdigit():
                self._errors['transfer_to'] = self.error_class(
                    ['Please Try Again. 11 digit account number for Hong Leong Bank'])
        if transfer_bank == 'UOB Bank':
            if not len(transfer_to) == 11 and transfer_to.isdigit():
                self._errors['transfer_to'] = self.error_class(
                    ['Please Try Again. 11 digit account number for UOB Bank'])
        if transfer_bank == 'CitiBank Malaysia':
            if not len(transfer_to) == 10 and transfer_to.isdigit():
                self._errors['transfer_to'] = self.error_class(
                    ['Please Try Again. 10 digit account number for CitiBank Malaysia'])
        if transfer_bank == 'HSBC Bank Malaysia':
            if not len(transfer_to) == 12 and transfer_to.isdigit():
                self._errors['transfer_to'] = self.error_class(
                    ['Please Try Again. 12 digit account number for HSBC Bank Malaysia'])
        if transfer_bank == 'Alliance Bank':
            if not len(transfer_to) == 15 and transfer_to.isdigit():
                self._errors['transfer_to'] = self.error_class(
                    ['Please Try Again. 15 digit account number for Alliance Bank'])
        if transfer_bank == 'Standard Chartered Bank':
            if not len(transfer_to) == 12 and transfer_to.isdigit():
                self._errors['transfer_to'] = self.error_class(
                    ['Please Try Again. 12 digit account number for Standard Chartered Bank'])
        if transfer_bank == 'Bank Muamalat Malaysia':
            if not len(transfer_to) == 14 and transfer_to.isdigit():
                self._errors['transfer_to'] = self.error_class(
                    ['Please Try Again. 14 digit account number for Bank Muamalat Malaysia'])
        if transfer_bank == 'EzFinance':
            if not len(transfer_to) == 10 and transfer_to.isdigit():
                self._errors['transfer_to'] = self.error_class(
                    ['Please Try Again. 10 digit account number for EzFinance'])

        return self.cleaned_data


class ExpensesManagerForm(forms.ModelForm):
    startdate = forms.DateTimeField(label='Start Date', widget=forms.TextInput(
        attrs={'type': 'date'}
    ))
    enddate = forms.DateTimeField(label='End Date', widget=forms.TextInput(
        attrs={'type': 'date'}
    ))
    net_disposable_income = forms.FloatField(label='Net Disposable Income')
    budget_plan = forms.FloatField(label='Budget in Plan')
    dailyliving_budget_planned = forms.FloatField(label='Daily Living Budget Planned')
    education_budget_planned = forms.FloatField(label='Education Budget Planned')
    entertainment_budget_planned = forms.FloatField(label='Entertainment Budget Planned')
    healthcare_budget_planned = forms.FloatField(label='Healthcare Budget Planned')
    rental_budget_planned = forms.FloatField(label='Home/Rent Budget Planned')
    transportation_budget_planned = forms.FloatField(label='Transportation Budget Planned')
    loan_budget_planned = forms.FloatField(label='Loan Payment Budget Planned')
    other_budget_planned = forms.FloatField(label='Others Budget Planned')

    class Meta:
        model = ExpensesManager
        fields = ['startdate', 'enddate', 'net_disposable_income', 'budget_plan', 'dailyliving_budget_planned',
                  'education_budget_planned', 'entertainment_budget_planned',
                  'healthcare_budget_planned', 'rental_budget_planned', 'transportation_budget_planned',
                  'loan_budget_planned', 'other_budget_planned']

    def clean(self):
        super(ExpensesManagerForm, self).clean()
        startdate = self.cleaned_data.get('startdate')
        enddate = self.cleaned_data.get('enddate')
        budget_plan = self.cleaned_data.get('budget_plan')
        net_disposable_income = self.cleaned_data.get('net_disposable_income')
        dailyliving_budget_planned = self.cleaned_data.get('dailyliving_budget_planned')
        education_budget_planned = self.cleaned_data.get('education_budget_planned')
        entertainment_budget_planned = self.cleaned_data.get('entertainment_budget_planned')
        healthcare_budget_planned = self.cleaned_data.get('healthcare_budget_planned')
        rental_budget_planned = self.cleaned_data.get('rental_budget_planned')
        transportation_budget_planned = self.cleaned_data.get('transportation_budget_planned')
        loan_budget_planned = self.cleaned_data.get('loan_budget_planned')
        other_budget_planned = self.cleaned_data.get('other_budget_planned')
        total = dailyliving_budget_planned + education_budget_planned + entertainment_budget_planned + healthcare_budget_planned \
                + rental_budget_planned + transportation_budget_planned + loan_budget_planned + other_budget_planned

        if  enddate < startdate:
            self._errors['enddate'] = self.error_class(
                ['End date should be greater than start date.'])

        if not budget_plan < net_disposable_income:
            self._errors['budget_plan'] = self.error_class(
                ['Your budget expenses had exceeded income.'])

        if not total < budget_plan:
            self._errors['budget_plan'] = self.error_class(
                ['Total of your category budget expenses had exceeded your budget plan.'])

class DailyLivingExpensesRecordForm(forms.ModelForm):
    expenses_date = forms.DateField(label='Expenses Date', widget=forms.TextInput(
        attrs={'type': 'date'}
    ))
    expenses_amount=forms.FloatField(label='Expenses Amount')

    class Meta:
        model = Expenses_record
        fields = ['expenses_date', 'expenses_amount']

class EducationExpensesRecordForm(forms.ModelForm):
    expenses_date = forms.DateField(label='Expenses Date', widget=forms.TextInput(
        attrs={'type': 'date'}
    ))
    expenses_amount=forms.FloatField(label='Expenses Amount')

    class Meta:
        model = Expenses_record
        fields = ['expenses_date', 'expenses_amount']

class EntertainmentExpensesRecordForm(forms.ModelForm):
    expenses_date = forms.DateField(label='Expenses Date', widget=forms.TextInput(
        attrs={'type': 'date'}
    ))
    expenses_amount=forms.FloatField(label='Expenses Amount')

    class Meta:
        model = Expenses_record
        fields = ['expenses_date', 'expenses_amount']

class HealthcareExpensesRecordForm(forms.ModelForm):
    expenses_date = forms.DateField(label='Expenses Date', widget=forms.TextInput(
        attrs={'type': 'date'}
    ))
    expenses_amount=forms.FloatField(label='Expenses Amount')

    class Meta:
        model = Expenses_record
        fields = ['expenses_date', 'expenses_amount']

class HomerentalExpensesRecordForm(forms.ModelForm):
    expenses_date = forms.DateField(label='Expenses Date', widget=forms.TextInput(
        attrs={'type': 'date'}
    ))
    expenses_amount=forms.FloatField(label='Expenses Amount')

    class Meta:
        model = Expenses_record
        fields = ['expenses_date', 'expenses_amount']

class TransportationExpensesRecordForm(forms.ModelForm):
    expenses_date = forms.DateField(label='Expenses Date', widget=forms.TextInput(
        attrs={'type': 'date'}
    ))
    expenses_amount=forms.FloatField(label='Expenses Amount')

    class Meta:
        model = Expenses_record
        fields = ['expenses_date', 'expenses_amount']

class LoanExpensesRecordForm(forms.ModelForm):
    expenses_date = forms.DateField(label='Expenses Date', widget=forms.TextInput(
        attrs={'type': 'date'}
    ))
    expenses_amount=forms.FloatField(label='Expenses Amount')

    class Meta:
        model = Expenses_record
        fields = ['expenses_date', 'expenses_amount']

class OtherExpensesRecordForm(forms.ModelForm):
    expenses_type = forms.CharField(label='Expenses Type', max_length=50)
    expenses_date = forms.DateField(label='Expenses Date', widget=forms.TextInput(
        attrs={'type': 'date'}
    ))
    expenses_amount=forms.FloatField(label='Expenses Amount')


    class Meta:
        model = Expenses_record
        fields = ['expenses_date', 'expenses_amount', 'expenses_type']

class FixedDepositForm(forms.ModelForm):
    tenure_rate = forms.CharField(label='', widget=forms.Select(choices=tenureNrate))
    fixedDeposit_amount = forms.FloatField(label="")

    class Meta:
        model = FixedDeposit
        fields = ['fixedDeposit_amount']

class AnnouncementForm(forms.ModelForm):
    announcement_subject = forms.CharField(label='Announcement Subject', max_length=100)
    announcement_content = forms.CharField(label='Announcement Body', max_length=300, widget=forms.Textarea)
    publish_date = forms.DateField(label='Publish Date', widget=forms.TextInput(
        attrs={'type': 'date'}
    ))
    class Meta:
        model = General_announcement
        fields = ['announcement_subject','announcement_content','publish_date']

    def clean(self):
        super(AnnouncementForm, self).clean()
        publish_date = self.cleaned_data.get('publish_date')
        if not publish_date >= date.today():
            self._errors['publish_date'] = self.error_class(
                ['Announcement publish date should be greater than today date.'])


class JobcreationForm(forms.ModelForm):
    job_available_day = forms.IntegerField(min_value=0,max_value=365,label="")
    job_employer_name = forms.CharField(max_length=50, label="")
    job_employer_contact_number = forms.CharField(max_length=50, label="")
    job_employer_email = forms.EmailField(label="")
    job_employer_company = forms.CharField(max_length=100, label="", widget=forms.TextInput(attrs={'placeholder': 'e.g. Thermotronic Industrial Sdn. Bhd.'}))
    job_location = forms.CharField(max_length=300, label="", widget=forms.TextInput(attrs={'placeholder': 'e.g. Bukit Mertajam (Penang) - Lembah Permai, Bukit Mertajam'}))
    job_general_description = forms.CharField(max_length=3000, label="", widget=forms.Textarea(attrs={'rows': 5,'style': 'padding:0.5%; width: 100%; border: 1px solid rgba(5, 0, 0, 0.17); border-radius: 4px;'}))
    job_position = forms.CharField(max_length=100, label="", widget=forms.TextInput(attrs={'placeholder': 'e.g. Front Office Assistant'}))
    job_duties = forms.CharField(max_length=500, label="", widget=forms.Textarea(attrs={'rows': 3,'style': 'padding:0.5%; width: 100%; border: 1px solid rgba(5, 0, 0, 0.17); border-radius: 4px;'}))
    job_requirement = forms.CharField(max_length=2000, label="", widget=forms.Textarea(attrs={'rows': 4,'style': 'padding:0.5%; width: 100%; border: 1px solid rgba(5, 0, 0, 0.17); border-radius: 4px;',}))
    job_salary = forms.CharField(max_length=50, label="",widget=forms.TextInput(attrs={'placeholder': 'e.g. RM 8 per hour'}))
    job_type = forms.ChoiceField(choices=Jobtype, widget=forms.RadioSelect(),label="" )

    class Meta:
        model = Job_create_request
        fields = ['job_available_day', 'job_employer_name', 'job_employer_contact_number','job_employer_email', 'job_employer_company', 'job_location',
                  'job_general_description', 'job_position', 'job_duties','job_requirement', 'job_salary', 'job_type',]


    def clean(self):
        super(JobcreationForm, self).clean()
        job_employer_contact_number = self.cleaned_data.get('job_employer_contact_number')

        if not job_employer_contact_number.isdigit() and len(job_employer_contact_number) < 13:
            self._errors['job_employer_contact_number'] = self.error_class([
                'Please enter a valid phone number'])



class VacancyForm(forms.ModelForm):
    ALLOWED_TYPES = ['pdf']
    job_applicant_name = forms.CharField(max_length=50, label="")
    job_applicant_email = forms.EmailField(label="")
    job_applicant_contact_number = forms.CharField(max_length=50, label="")
    job_pitch = forms.CharField(label="",max_length=1000, widget=forms.Textarea(attrs={'rows': 4,'style': 'padding:0.5%; width: 100%; border: 1px solid rgba(5, 0, 0, 0.17); border-radius: 4px;',
                                                                                       'placeholder': 'Tell the employer why you are the best suited for this role. Highlight'
                                                                                                      ' specific skills and how you can contribute. Avoid generic pitches e.g. I am responsible'}))
    applicant_resume = forms.FileField(label="")

    class Meta:
        model = Job_apply
        fields = ['job_applicant_name','job_applicant_email','job_applicant_contact_number','job_pitch','applicant_resume']



    def clean(self):
        super(VacancyForm, self).clean()
        job_applicant_contact_number = self.cleaned_data.get('job_applicant_contact_number')

        if not job_applicant_contact_number.isdigit() and len(job_applicant_contact_number) < 13:
            self._errors['job_employer_contact_number'] = self.error_class([
                'Please enter a valid phone number'])



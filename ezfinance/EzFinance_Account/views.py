from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from users.models import Account
from .forms import CreditCardForm, FundTransferForm, ExpensesManagerForm, DailyLivingExpensesRecordForm, \
    EducationExpensesRecordForm, EntertainmentExpensesRecordForm, HealthcareExpensesRecordForm, \
    HomerentalExpensesRecordForm, TransportationExpensesRecordForm, LoanExpensesRecordForm, OtherExpensesRecordForm, \
    FixedDepositForm,AnnouncementForm,JobcreationForm,VacancyForm
from django.contrib.auth.models import User
from users.forms import AccountUpdateForm, UserUpdateForm
from django.contrib import messages
from .models import Deposit, Transaction_history, FundTransfer, ExpensesManager, Expenses_record, FixedDeposit, \
    Contact_us,General_announcement,Job_create_request,Job_apply
from django.template.loader import render_to_string
from django.http import JsonResponse
import datetime
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mortgage import Loan
from django.views.decorators.clickjacking import xframe_options_sameorigin
import random
from datetime import date
from django.contrib.admin.views.decorators import staff_member_required

@xframe_options_sameorigin
def contact_us(request):
    if 'btnSubmit' in request.POST:
        cname = request.POST.get("txtName")
        cemail = request.POST.get("txtEmail")
        cphone = request.POST.get("txtPhone")
        cmessage = request.POST.get("txtMsg")
        if cname != '' and cemail != '' and cphone != '' and cmessage != '':
            contact_us_save = Contact_us(
                name=cname,
                email=cemail,
                phone=cphone,
                message=cmessage
            )
            contact_us_save.save()
            messages.success(request, f'Your message had successfully send to our customer service.')
        else:
            messages.warning(request, f'Your message failed to send. Please try again')

    return render(request, 'EzFinance_Account/contact_us.html')


@xframe_options_sameorigin
def about_us(request):
    return render(request, 'EzFinance_Account/about_us.html')


@xframe_options_sameorigin
def landing_page(request):
    return render(request, 'EzFinance_Account/landing_page.html')

@login_required
@xframe_options_sameorigin
def home(request):
    if request.user.is_authenticated:
        current_user_id = request.user.id
        account_num = int(current_user_id) + 6067071528
    else:
        account_num = 'none'

    latest_history = Transaction_history.objects.filter(user=request.user).last()
    latest_fixeddepositdate = FixedDeposit.objects.filter(user=request.user).last()
    fixedDepositObject = FixedDeposit.objects.filter(user=request.user)

    last_three_day_date=date.today() - relativedelta(days=3)
    general_announcement_today = General_announcement.objects.filter(publish_date=date.today()).filter(announcement_status=True)
    general_announcement_last_three_day = General_announcement.objects.filter(publish_date__gte=last_three_day_date, publish_date__lt=date.today()).filter(announcement_status=True)
    annoucement_count=general_announcement_today.count()+general_announcement_last_three_day.count()
    general_announcement_overall = General_announcement.objects.filter(announcement_status=True).order_by('-publish_date')[:10]
    general_announcement_all = General_announcement.objects.filter(announcement_status=True).order_by(
        '-publish_date')
    context = {
        "account_num": account_num,
        'latest_history': latest_history,
        'latest_fixeddepositdate': latest_fixeddepositdate,
        'fixedDepositObject': fixedDepositObject,
        'general_announcement_today':general_announcement_today,
        'general_announcement_last_three_day': general_announcement_last_three_day,
        'general_announcement_last_three_day_count': general_announcement_last_three_day.count(),
        'general_announcement_today_count': general_announcement_today.count(),
        'annoucement_count': annoucement_count,
        'general_announcement_overall':general_announcement_overall,
        'general_announcement_overall_count': general_announcement_overall.count(),
        'general_announcement_all':general_announcement_all,
    }
    profile = Account.objects.get(user=request.user)
    if profile.mykad is None or profile.phone is None:
        messages.warning(request, f'Please update your profile information accordingly.')

    return render(request, 'EzFinance_Account/home.html', context)


@login_required
@xframe_options_sameorigin
def fixedDeposit_claim(request, pk):
    current_fixedDepositAcc = get_object_or_404(FixedDeposit, pk=pk)
    account_balance_deduct = Account.objects.get(user=request.user)
    if request.method == 'POST':
        if current_fixedDepositAcc.maturity_date <= datetime.date.today():
            amount_after = (current_fixedDepositAcc.fixedDeposit_amount * (current_fixedDepositAcc.interest_rate / 100)) \
                           + current_fixedDepositAcc.fixedDeposit_amount
            # update account balance
            account_balance_deduct.account_balance += round(amount_after, 2)
            account_balance_deduct.save()
            acc_id = 4045219663 + current_fixedDepositAcc.id
            transaction_detail = 'Fixed Deposit Claim #' + str(acc_id)
            transfer_history_save = Transaction_history(transaction_detail=transaction_detail,
                                                        transaction_debit=round(amount_after, 2),
                                                        user=request.user)
            transfer_history_save.save()
            current_fixedDepositAcc.delete()
            profile = Account.objects.get(user=request.user)
            if profile.mykad is None or profile.phone is None:
                messages.warning(request, f'Please update your profile information accordingly.')
            messages.success(request, f'Your Fixed Deposit account has succesfully claimed')
            return redirect('EzFinance-Account-home')
        else:
            acc_id = 4045219663 + current_fixedDepositAcc.id
            messages.warning(request, f'Account #{acc_id} has not reach it maturity date yet.')
            return redirect('EzFinance-Account-home')

    return render(request, 'EzFinance_Account/home.html')


@login_required
@xframe_options_sameorigin
def profile(request):
    if request.user.is_authenticated:
        current_user_id = request.user.id
        account_num = int(current_user_id) + 6067071528
    else:
        account_num = 'none'

    context = {
        "account_num": account_num
    }

    if 'btnAddMore' in request.POST:
        return redirect('EzFinance-Account-profile-update')
    return render(request, 'EzFinance_Account/profile.html', context)


@login_required
@xframe_options_sameorigin
def profile_update(request):
    if 'UpdateProfile' in request.POST:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = AccountUpdateForm(request.POST, request.FILES, instance=request.user.account)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('EzFinance-Account-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = AccountUpdateForm(instance=request.user.account)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'EzFinance_Account/profile_update.html', context)


@login_required
@xframe_options_sameorigin
def transaction(request):
    # deposit action
    if 'deposit_confirm' in request.POST:
        form = CreditCardForm(request.POST)
        if form.is_valid():
            # insert into transaction model
            creditcard_name = form.cleaned_data['creditcard_name']
            creditcard_num = form.cleaned_data['creditcard_num']
            deposit_amount = form.cleaned_data['deposit_amount']
            Deposit_save = Deposit(creditcard_name=creditcard_name, creditcard_num=creditcard_num,
                                   deposit_amount=deposit_amount, user=request.user)
            Deposit_save.save()

            # update account balance
            account_balance_update = Account.objects.get(user=request.user)
            account_balance_update.account_balance += deposit_amount
            account_balance_update.save()

            # update transaction history
            History_save = Transaction_history(transaction_detail="Deposit", transaction_debit=deposit_amount,
                                               user=request.user)
            History_save.save()
            balance = round(account_balance_update.account_balance, 2)
            messages.success(request,
                             f'Your deposit has been successfully made. Your current balance is RM {balance}')
            return redirect('EzFinance-Account-transaction')
        else:
            messages.warning(request, f'Transaction failed. Please Try Again')

    else:
        form = CreditCardForm()

    # transfer action
    if 'transfer_confirm' in request.POST:
        transfer_form = FundTransferForm(request.POST)
        if transfer_form.is_valid():
            account_balance_deduct = Account.objects.get(user=request.user)
            transfer_amount = transfer_form.cleaned_data['transfer_amount']
            transfer_bank = transfer_form.cleaned_data['transfer_bank']
            transfer_category = transfer_form.cleaned_data['transfer_category']
            transfer_to = transfer_form.cleaned_data['transfer_to']
            transfer_instruction = transfer_form.cleaned_data['transfer_instruction']
            transaction_check = False;
            if transfer_amount < account_balance_deduct.account_balance:

                # update other ezfinance account if ezfinance is selected
                if transfer_bank == "EzFinance":
                    try:
                        account_id = int(transfer_to) - 6067071528
                        user_id = User.objects.get(id=account_id)
                        account_balance_add_from_transaction = Account.objects.get(user=user_id)
                        account_balance_add_from_transaction.account_balance += transfer_amount
                        account_balance_add_from_transaction.save()
                        payment_history_save = Transaction_history(transaction_detail=transfer_category,
                                                                    transaction_debit=transfer_amount,
                                                                    user=user_id)
                        payment_history_save.save()
                        transaction_check = True
                    except User.DoesNotExist:
                        messages.warning(request,
                                         f'This EzFinance Account does not exist.')
                        return redirect('EzFinance-Account-transaction')
                else:
                    # insert into FundTransfer model
                    Transfer_save = FundTransfer(transfer_category=transfer_category, transfer_to=transfer_to,
                                                 transfer_bank=transfer_bank, transfer_amount=transfer_amount,
                                                 transfer_instruction=transfer_instruction, user=request.user)
                    Transfer_save.save()
                    # update transaction history
                    transfer_history_save = Transaction_history(transaction_detail=transfer_category,
                                                                transaction_credit=transfer_amount,
                                                                user=request.user)
                    transfer_history_save.save()

                    # update account balance
                    account_balance_deduct.account_balance -= transfer_amount
                    account_balance_deduct.save()
                    balance = round(account_balance_deduct.account_balance, 2)
                    messages.success(request,
                                     f'Your transfer has been successfully made. Your current balance is RM {balance}')
                    return redirect('EzFinance-Account-transaction')

                if transaction_check == True:
                    # insert into FundTransfer model
                    Transfer_save = FundTransfer(transfer_category=transfer_category, transfer_to=transfer_to,
                                                 transfer_bank=transfer_bank, transfer_amount=transfer_amount,
                                                 transfer_instruction=transfer_instruction, user=request.user)
                    Transfer_save.save()
                    # update transaction history
                    transfer_history_save = Transaction_history(transaction_detail=transfer_category,
                                                                transaction_credit=transfer_amount,
                                                                user=request.user)
                    transfer_history_save.save()

                    # update account balance
                    account_balance_deduct.account_balance -= transfer_amount
                    account_balance_deduct.save()
                    balance = round(account_balance_deduct.account_balance, 2)
                    messages.success(request,
                                     f'Your transfer has been successfully made. Your current balance is RM {balance}')
                    return redirect('EzFinance-Account-transaction')



            else:
                messages.warning(request,
                                 f'You have no enough credit to transfer')
                return redirect('EzFinance-Account-transaction')
        else:
            messages.warning(request, f'Transaction failed. Please Try Again')
    else:
        transfer_form = FundTransferForm()

    return render(request, 'EzFinance_Account/transaction.html', {'deposit': form, 'transfer': transfer_form})


@login_required
@xframe_options_sameorigin
def history(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        history_list = Transaction_history.objects.filter(user=request.user).filter(
            Q(transaction_detail__icontains=query) | Q(transaction_date__icontains=query))
        page = request.GET.get('page', 1)

        paginator = Paginator(history_list, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    else:
        history_list = Transaction_history.objects.filter(user=request.user)
        page = request.GET.get('page', 1)

        paginator = Paginator(history_list, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

    context = {
        'history_list': history_list,
        'users': users

    }

    return render(request, "EzFinance_Account/history.html", context)


@login_required
@xframe_options_sameorigin
def fixed_deposit(request):
    if 'deposit_submit' in request.POST:
        fixed_deposit_form = FixedDepositForm(request.POST)
        account_balance_deduct = Account.objects.get(user=request.user)
        if fixed_deposit_form.is_valid():
            tenureWithrate = fixed_deposit_form.cleaned_data['tenure_rate']
            fixed_deposit_amount = fixed_deposit_form.cleaned_data['fixedDeposit_amount']
            if fixed_deposit_amount <= account_balance_deduct.account_balance:
                if tenureWithrate == '1 month / 3.73% p.a.':
                    d1 = datetime.date.today()
                    maturitydate = d1 + relativedelta(months=1)
                    interestrate = 3.73
                    FixedDeposit_save = FixedDeposit(
                        maturity_date=maturitydate,
                        interest_rate=interestrate,
                        fixedDeposit_amount=fixed_deposit_amount,
                        user=request.user
                    )
                    FixedDeposit_save.save()
                    # update account balance
                    account_balance_deduct.account_balance -= fixed_deposit_amount
                    account_balance_deduct.save()
                    # update transaction history
                    transfer_history_save = Transaction_history(transaction_detail='Fixed Deposit-1 month/3.73% p.a.',
                                                                transaction_credit=fixed_deposit_amount,
                                                                user=request.user)
                    transfer_history_save.save()
                    balance = round(account_balance_deduct.account_balance, 2)
                    messages.success(request,
                                     f'Your Fixed Deposit account has succesfully created. Your current balance is RM {balance}')
                    return redirect('EzFinance-Account-fixed-deposit')

                elif tenureWithrate == '3 month / 4.10% p.a.':
                    d1 = datetime.date.today()
                    maturitydate = d1 + relativedelta(months=3)
                    interestrate = 4.10
                    FixedDeposit_save = FixedDeposit(
                        maturity_date=maturitydate,
                        interest_rate=interestrate,
                        fixedDeposit_amount=fixed_deposit_amount,
                        user=request.user
                    )
                    FixedDeposit_save.save()
                    # update account balance
                    account_balance_deduct.account_balance -= fixed_deposit_amount
                    account_balance_deduct.save()
                    # update transaction history
                    transfer_history_save = Transaction_history(transaction_detail='Fixed Deposit-3 month/4.10% p.a.',
                                                                transaction_credit=fixed_deposit_amount,
                                                                user=request.user)
                    transfer_history_save.save()
                    balance = round(account_balance_deduct.account_balance, 2)
                    messages.success(request,
                                     f'Your Fixed Deposit account has succesfully created. Your current balance is RM {balance}')
                    return redirect('EzFinance-Account-fixed-deposit')

                elif tenureWithrate == '6 month / 4.80% p.a.':
                    d1 = datetime.date.today()
                    maturitydate = d1 + relativedelta(months=6)
                    interestrate = 4.80
                    FixedDeposit_save = FixedDeposit(
                        maturity_date=maturitydate,
                        interest_rate=interestrate,
                        fixedDeposit_amount=fixed_deposit_amount,
                        user=request.user
                    )
                    FixedDeposit_save.save()
                    # update account balance
                    account_balance_deduct.account_balance -= fixed_deposit_amount
                    account_balance_deduct.save()
                    # update transaction history
                    transfer_history_save = Transaction_history(transaction_detail='Fixed Deposit-6 month/4.80% p.a.',
                                                                transaction_credit=fixed_deposit_amount,
                                                                user=request.user)
                    transfer_history_save.save()
                    balance = round(account_balance_deduct.account_balance, 2)
                    messages.success(request,
                                     f'Your Fixed Deposit account has succesfully created. Your current balance is RM {balance}')
                    return redirect('EzFinance-Account-fixed-deposit')
                elif tenureWithrate == '12 month / 5.40% p.a.':
                    d1 = datetime.date.today()
                    maturitydate = d1 + relativedelta(months=12)
                    interestrate = 5.40
                    FixedDeposit_save = FixedDeposit(
                        maturity_date=maturitydate,
                        interest_rate=interestrate,
                        fixedDeposit_amount=fixed_deposit_amount,
                        user=request.user
                    )
                    FixedDeposit_save.save()
                    # update account balance
                    account_balance_deduct.account_balance -= fixed_deposit_amount
                    account_balance_deduct.save()
                    # update transaction history
                    transfer_history_save = Transaction_history(transaction_detail='Fixed Deposit-12 month/5.40% p.a.',
                                                                transaction_credit=fixed_deposit_amount,
                                                                user=request.user)
                    transfer_history_save.save()
                    balance = round(account_balance_deduct.account_balance, 2)
                    messages.success(request,
                                     f'Your Fixed Deposit account has succesfully created. Your current balance is RM {balance}')
                    return redirect('EzFinance-Account-fixed-deposit')
                else:
                    messages.warning(request, f'Please select Tenure & Rate before submission')
            else:
                messages.warning(request, f'Fixed Deposit amount has exceeded your account balance.')


        else:
            messages.warning(request, f'Fixed Deposit account create failed. Please Try Again')
    else:
        fixed_deposit_form = FixedDepositForm()
    return render(request, 'EzFinance_Account/fixed_deposit.html', {'fixed_deposit_form': fixed_deposit_form})


@login_required
@xframe_options_sameorigin
def expenses_manager(request, pk):
    expenses_list = get_object_or_404(ExpensesManager, pk=pk)
    expenses_record = Expenses_record.objects.filter(expenses_project=expenses_list.pk)
    # data
    net_saving_percentage = (expenses_list.total_expenditure / expenses_list.net_disposable_income) * 100
    budget_plan_percentage = (expenses_list.budget_plan_remaining / expenses_list.budget_plan) * 100
    saving_plan_percentage = (expenses_list.provisional_balance / expenses_list.net_disposable_income) * 100
    budget_spent = ((expenses_list.budget_plan - expenses_list.budget_plan_remaining) / expenses_list.budget_plan) * 100
    dailyliving_used = (expenses_list.dailyliving_budget_spent / expenses_list.dailyliving_budget_planned) * 100
    education_used = (expenses_list.education_budget_spent / expenses_list.education_budget_planned) * 100
    entertainment_used = (expenses_list.entertainment_budget_spent / expenses_list.entertainment_budget_planned) * 100
    healthcare_used = (expenses_list.healthcare_budget_spent / expenses_list.healthcare_budget_planned) * 100
    homerental_used = (expenses_list.rental_budget_spent / expenses_list.rental_budget_planned) * 100
    transportation_used = (
                                  expenses_list.transportation_budget_spent / expenses_list.transportation_budget_planned) * 100
    loan_used = (expenses_list.loan_budget_spent / expenses_list.loan_budget_planned) * 100
    other_used = (expenses_list.other_budget_spent / expenses_list.other_budget_planned) * 100

    context = {
        'expenses_list': expenses_list,
        'net_saving_percentage': net_saving_percentage,
        'budget_plan_percentage': budget_plan_percentage,
        'saving_plan_percentage': saving_plan_percentage,
        'budget_spent': budget_spent,
        'dailyliving_used': dailyliving_used,
        'education_used': education_used,
        'entertainment_used': entertainment_used,
        'healthcare_used': healthcare_used,
        'homerental_used': homerental_used,
        'transportation_used': transportation_used,
        'loan_used': loan_used,
        'other_used': other_used,
        'expenses_record': expenses_record,
    }
    if expenses_list.total_expenditure > expenses_list.budget_plan:
        messages.warning(request, f'Warning: Your total expenditure had exceeded your budget plan')
    if expenses_list.total_expenditure > expenses_list.net_disposable_income:
        messages.warning(request, f'Warning: Your total expenditure had exceeded your net disposable income')
    return render(request, 'EzFinance_Account/expenses_manager.html', context)


@login_required
@xframe_options_sameorigin
def expenses_manager_menu(request):
    if 'budgetcreate' in request.POST:
        return redirect('EzFinance-Account-expenses-manager-form')

    ExpensesManagerList = ExpensesManager.objects.filter(user=request.user)
    context = {
        'ExpensesManagerList': ExpensesManagerList
    }
    return render(request, 'EzFinance_Account/expenses_manager_menu.html', context)


@login_required
@xframe_options_sameorigin
def expenses_delete(request, pk):
    expenses_list = get_object_or_404(ExpensesManager, pk=pk)  # Get your current cat

    if request.method == 'POST':  # If method is POST,
        expenses_list.delete()  # delete the cat.
        return redirect('EzFinance-Account-expenses-manager-menu')
    # Finally, redirect to the homepage.
    ExpensesManagerList = ExpensesManager.objects.filter(user=request.user)
    context = {
        'ExpensesManagerList': ExpensesManagerList
    }
    return render(request, 'EzFinance_Account/expenses_manager_menu.html', context)


@login_required
@xframe_options_sameorigin
def expenses_manager_form(request):
    if 'expenses_manager_create' in request.POST:
        exp_form = ExpensesManagerForm(request.POST)
        if exp_form.is_valid():

            startdate = exp_form.cleaned_data['startdate']
            enddate = exp_form.cleaned_data['enddate']
            budget_plan = exp_form.cleaned_data['budget_plan']
            net_disposable_income = exp_form.cleaned_data['net_disposable_income']
            dailyliving_budget_planned = exp_form.cleaned_data['dailyliving_budget_planned']
            education_budget_planned = exp_form.cleaned_data['education_budget_planned']
            entertainment_budget_planned = exp_form.cleaned_data['entertainment_budget_planned']
            healthcare_budget_planned = exp_form.cleaned_data['healthcare_budget_planned']
            rental_budget_planned = exp_form.cleaned_data['rental_budget_planned']
            transportation_budget_planned = exp_form.cleaned_data['transportation_budget_planned']
            loan_budget_planned = exp_form.cleaned_data['loan_budget_planned']
            other_budget_planned = exp_form.cleaned_data['other_budget_planned']
            ExpensesManager_save = ExpensesManager(
                startdate=startdate,
                enddate=enddate,
                net_disposable_income=net_disposable_income,
                provisional_balance=net_disposable_income - budget_plan,
                budget_plan=budget_plan,
                budget_plan_remaining=budget_plan,
                dailyliving_budget_planned=dailyliving_budget_planned,
                dailyliving_budget_remaining=dailyliving_budget_planned,
                education_budget_planned=education_budget_planned,
                education_budget_remaining=education_budget_planned,
                entertainment_budget_planned=entertainment_budget_planned,
                entertainment_budget_remaining=entertainment_budget_planned,
                healthcare_budget_planned=healthcare_budget_planned,
                healthcare_budget_remaining=healthcare_budget_planned,
                rental_budget_planned=rental_budget_planned,
                rental_budget_remaining=rental_budget_planned,
                transportation_budget_planned=transportation_budget_planned,
                transportation_budget_remaining=transportation_budget_planned,
                loan_budget_planned=loan_budget_planned,
                loan_budget_remaining=loan_budget_planned,
                other_budget_planned=other_budget_planned,
                other_budget_remaining=other_budget_planned,
                user=request.user
            )
            ExpensesManager_save.save()
            messages.success(request, f'New expenses plan has been successfully created')
            return redirect('EzFinance-Account-expenses-manager-menu')
        else:
            messages.warning(request, f'Wrong Information. Please Try Again')
    else:
        exp_form = ExpensesManagerForm()

    context = {
        'exp_form': exp_form
    }
    return render(request, 'EzFinance_Account/create_expenses_form.html', context)


@login_required
@xframe_options_sameorigin
def dailyliving_expenses(request, pk):
    expenses_list = get_object_or_404(ExpensesManager, pk=pk)
    dailyliving_used = (expenses_list.dailyliving_budget_spent / expenses_list.dailyliving_budget_planned) * 100
    if 'dl_expenses_submit' in request.POST:
        DailyLivingExpensesRecord_form = DailyLivingExpensesRecordForm(request.POST)
        if DailyLivingExpensesRecord_form.is_valid():
            amount = DailyLivingExpensesRecord_form.cleaned_data['expenses_amount']
            date = DailyLivingExpensesRecord_form.cleaned_data['expenses_date']

            if date > expenses_list.enddate or date < expenses_list.startdate:
                messages.warning(request, f'Wrong Information: Expenses date must between start date and end date')
                return redirect('dailyliving_expenses', expenses_list.pk)
            else:
                Expenses_record_save = Expenses_record(
                    expenses_type='Daily Living Expenses',
                    expenses_date=date,
                    expenses_amount=amount,
                    expenses_project=expenses_list)

                Expenses_record_save.save()
                expenses_list.dailyliving_budget_spent += amount
                expenses_list.dailyliving_budget_remaining -= amount
                expenses_list.total_expenditure += amount
                expenses_list.budget_plan_remaining -= amount
                expenses_list.save()
                messages.success(request, f'Your expenses plan has been successfully updated')
                return redirect('expenses_manager', expenses_list.pk)


        else:
            messages.warning(request, f'Wrong Information. Please Try Again')
    else:
        DailyLivingExpensesRecord_form = DailyLivingExpensesRecordForm()

    context = {
        'DailyLivingExpensesRecord_form': DailyLivingExpensesRecord_form,
        'expenses_list': expenses_list,
        'dailyliving_used': dailyliving_used
    }
    return render(request, 'EzFinance_Account/dailyliving_expense_update.html', context)


@login_required
@xframe_options_sameorigin
def education_expenses(request, pk):
    expenses_list = get_object_or_404(ExpensesManager, pk=pk)
    education_used = (expenses_list.education_budget_spent / expenses_list.education_budget_planned) * 100
    if 'dl_expenses_submit' in request.POST:
        EducationExpensesRecord_form = EducationExpensesRecordForm(request.POST)
        if EducationExpensesRecord_form.is_valid():
            amount = EducationExpensesRecord_form.cleaned_data['expenses_amount']
            date = EducationExpensesRecord_form.cleaned_data['expenses_date']

            if date > expenses_list.enddate or date < expenses_list.startdate:
                messages.warning(request, f'Wrong Information: Expenses date must between start date and end date')
                return redirect('education_expenses', expenses_list.pk)
            else:
                Expenses_record_save = Expenses_record(
                    expenses_type='Education',
                    expenses_date=date,
                    expenses_amount=amount,
                    expenses_project=expenses_list)

                Expenses_record_save.save()
                expenses_list.education_budget_spent += amount
                expenses_list.education_budget_remaining -= amount
                expenses_list.total_expenditure += amount
                expenses_list.budget_plan_remaining -= amount
                expenses_list.save()
                messages.success(request, f'Your expenses plan has been successfully updated')
                return redirect('expenses_manager', expenses_list.pk)


        else:
            messages.warning(request, f'Wrong Information. Please Try Again')
    else:
        EducationExpensesRecord_form = EducationExpensesRecordForm()

    context = {
        'EducationExpensesRecord_form': EducationExpensesRecord_form,
        'expenses_list': expenses_list,
        'education_used': education_used
    }
    return render(request, 'EzFinance_Account/education_expense_update.html', context)


@login_required
@xframe_options_sameorigin
def entertainment_expenses(request, pk):
    expenses_list = get_object_or_404(ExpensesManager, pk=pk)
    entertainment_used = (expenses_list.entertainment_budget_spent / expenses_list.entertainment_budget_planned) * 100
    if 'dl_expenses_submit' in request.POST:
        EntertainmentExpensesRecord_form = EntertainmentExpensesRecordForm(request.POST)
        if EntertainmentExpensesRecord_form.is_valid():
            amount = EntertainmentExpensesRecord_form.cleaned_data['expenses_amount']
            date = EntertainmentExpensesRecord_form.cleaned_data['expenses_date']

            if date > expenses_list.enddate or date < expenses_list.startdate:
                messages.warning(request, f'Wrong Information: Expenses date must between start date and end date')
                return redirect('entertainment_expenses', expenses_list.pk)
            else:
                Expenses_record_save = Expenses_record(
                    expenses_type='Entertainment',
                    expenses_date=date,
                    expenses_amount=amount,
                    expenses_project=expenses_list)

                Expenses_record_save.save()
                expenses_list.entertainment_budget_spent += amount
                expenses_list.entertainment_budget_remaining -= amount
                expenses_list.total_expenditure += amount
                expenses_list.budget_plan_remaining -= amount
                expenses_list.save()
                messages.success(request, f'Your expenses plan has been successfully updated')
                return redirect('expenses_manager', expenses_list.pk)


        else:
            messages.warning(request, f'Wrong Information. Please Try Again')
    else:
        EntertainmentExpensesRecord_form = EntertainmentExpensesRecordForm()

    context = {
        'EntertainmentExpensesRecord_form': EntertainmentExpensesRecord_form,
        'expenses_list': expenses_list,
        'entertainment_used': entertainment_used
    }
    return render(request, 'EzFinance_Account/entertainment_expense_update.html', context)


@login_required
@xframe_options_sameorigin
def healthcare_expenses(request, pk):
    expenses_list = get_object_or_404(ExpensesManager, pk=pk)
    healthcare_used = (expenses_list.healthcare_budget_spent / expenses_list.healthcare_budget_planned) * 100
    if 'dl_expenses_submit' in request.POST:
        HealthcareExpensesRecord_form = HealthcareExpensesRecordForm(request.POST)
        if HealthcareExpensesRecord_form.is_valid():
            amount = HealthcareExpensesRecord_form.cleaned_data['expenses_amount']
            date = HealthcareExpensesRecord_form.cleaned_data['expenses_date']

            if date > expenses_list.enddate or date < expenses_list.startdate:
                messages.warning(request, f'Wrong Information: Expenses date must between start date and end date')
                return redirect('healthcare_expenses', expenses_list.pk)
            else:
                Expenses_record_save = Expenses_record(
                    expenses_type='Health care',
                    expenses_date=date,
                    expenses_amount=amount,
                    expenses_project=expenses_list)

                Expenses_record_save.save()
                expenses_list.healthcare_budget_spent += amount
                expenses_list.healthcare_budget_remaining -= amount
                expenses_list.total_expenditure += amount
                expenses_list.budget_plan_remaining -= amount
                expenses_list.save()
                messages.success(request, f'Your expenses plan has been successfully updated')
                return redirect('expenses_manager', expenses_list.pk)


        else:
            messages.warning(request, f'Wrong Information. Please Try Again')
    else:
        HealthcareExpensesRecord_form = HealthcareExpensesRecordForm()

    context = {
        'HealthcareExpensesRecord_form': HealthcareExpensesRecord_form,
        'expenses_list': expenses_list,
        'healthcare_used': healthcare_used
    }
    return render(request, 'EzFinance_Account/healthcare_expense_update.html', context)


@login_required
@xframe_options_sameorigin
def homerental_expenses(request, pk):
    expenses_list = get_object_or_404(ExpensesManager, pk=pk)
    homerental_used = (expenses_list.rental_budget_spent / expenses_list.rental_budget_planned) * 100
    if 'dl_expenses_submit' in request.POST:
        HomerentalExpensesRecord_form = HomerentalExpensesRecordForm(request.POST)
        if HomerentalExpensesRecord_form.is_valid():
            amount = HomerentalExpensesRecord_form.cleaned_data['expenses_amount']
            date = HomerentalExpensesRecord_form.cleaned_data['expenses_date']

            if date > expenses_list.enddate or date < expenses_list.startdate:
                messages.warning(request, f'Wrong Information: Expenses date must between start date and end date')
                return redirect('homerental_expenses', expenses_list.pk)
            else:
                Expenses_record_save = Expenses_record(
                    expenses_type='Home Rental',
                    expenses_date=date,
                    expenses_amount=amount,
                    expenses_project=expenses_list)

                Expenses_record_save.save()
                expenses_list.rental_budget_spent += amount
                expenses_list.rental_budget_remaining -= amount
                expenses_list.total_expenditure += amount
                expenses_list.budget_plan_remaining -= amount
                expenses_list.save()
                messages.success(request, f'Your expenses plan has been successfully updated')
                return redirect('expenses_manager', expenses_list.pk)


        else:
            messages.warning(request, f'Wrong Information. Please Try Again')
    else:
        HomerentalExpensesRecord_form = HomerentalExpensesRecordForm()

    context = {
        'HomerentalExpensesRecord_form': HomerentalExpensesRecord_form,
        'expenses_list': expenses_list,
        'homerental_used': homerental_used
    }
    return render(request, 'EzFinance_Account/homerental_expense_update.html', context)


@login_required
@xframe_options_sameorigin
def transportation_expenses(request, pk):
    expenses_list = get_object_or_404(ExpensesManager, pk=pk)
    transportation_used = (
                                  expenses_list.transportation_budget_spent / expenses_list.transportation_budget_planned) * 100
    if 'dl_expenses_submit' in request.POST:
        TransportationExpensesRecord_form = TransportationExpensesRecordForm(request.POST)
        if TransportationExpensesRecord_form.is_valid():
            amount = TransportationExpensesRecord_form.cleaned_data['expenses_amount']
            date = TransportationExpensesRecord_form.cleaned_data['expenses_date']

            if date > expenses_list.enddate or date < expenses_list.startdate:
                messages.warning(request, f'Wrong Information: Expenses date must between start date and end date')
                return redirect('transportation_expenses', expenses_list.pk)
            else:
                Expenses_record_save = Expenses_record(
                    expenses_type='Health care',
                    expenses_date=date,
                    expenses_amount=amount,
                    expenses_project=expenses_list)

                Expenses_record_save.save()
                expenses_list.transportation_budget_spent += amount
                expenses_list.transportation_budget_remaining -= amount
                expenses_list.total_expenditure += amount
                expenses_list.budget_plan_remaining -= amount
                expenses_list.save()
                messages.success(request, f'Your expenses plan has been successfully updated')
                return redirect('expenses_manager', expenses_list.pk)


        else:
            messages.warning(request, f'Wrong Information. Please Try Again')
    else:
        TransportationExpensesRecord_form = TransportationExpensesRecordForm()

    context = {
        'TransportationExpensesRecord_form': TransportationExpensesRecord_form,
        'expenses_list': expenses_list,
        'transportation_used': transportation_used
    }
    return render(request, 'EzFinance_Account/transportation_expense_update.html', context)


@login_required
@xframe_options_sameorigin
def loan_expenses(request, pk):
    expenses_list = get_object_or_404(ExpensesManager, pk=pk)
    loan_used = (expenses_list.loan_budget_spent / expenses_list.loan_budget_planned) * 100
    if 'dl_expenses_submit' in request.POST:
        LoanExpensesRecord_form = LoanExpensesRecordForm(request.POST)
        if LoanExpensesRecord_form.is_valid():
            amount = LoanExpensesRecord_form.cleaned_data['expenses_amount']
            date = LoanExpensesRecord_form.cleaned_data['expenses_date']

            if date > expenses_list.enddate or date < expenses_list.startdate:
                messages.warning(request, f'Wrong Information: Expenses date must between start date and end date')
                return redirect('loan_expenses', expenses_list.pk)
            else:
                Expenses_record_save = Expenses_record(
                    expenses_type='Loan Payment',
                    expenses_date=date,
                    expenses_amount=amount,
                    expenses_project=expenses_list)

                Expenses_record_save.save()
                expenses_list.loan_budget_spent += amount
                expenses_list.loan_budget_remaining -= amount
                expenses_list.total_expenditure += amount
                expenses_list.budget_plan_remaining -= amount
                expenses_list.save()
                messages.success(request, f'Your expenses plan has been successfully updated')
                return redirect('expenses_manager', expenses_list.pk)


        else:
            messages.warning(request, f'Wrong Information. Please Try Again')
    else:
        LoanExpensesRecord_form = LoanExpensesRecordForm()

    context = {
        'LoanExpensesRecord_form': LoanExpensesRecord_form,
        'expenses_list': expenses_list,
        'loan_used': loan_used
    }
    return render(request, 'EzFinance_Account/loan_expense_update.html', context)


@login_required
@xframe_options_sameorigin
def other_expenses(request, pk):
    expenses_list = get_object_or_404(ExpensesManager, pk=pk)
    other_used = (expenses_list.other_budget_spent / expenses_list.other_budget_planned) * 100
    if 'dl_expenses_submit' in request.POST:
        OtherExpensesRecord_form = OtherExpensesRecordForm(request.POST)
        if OtherExpensesRecord_form.is_valid():
            amount = OtherExpensesRecord_form.cleaned_data['expenses_amount']
            date = OtherExpensesRecord_form.cleaned_data['expenses_date']
            type = OtherExpensesRecord_form.cleaned_data['expenses_type']
            if date > expenses_list.enddate or date < expenses_list.startdate:
                messages.warning(request, f'Wrong Information: Expenses date must between start date and end date')
                return redirect('other_expenses', expenses_list.pk)
            else:
                Expenses_record_save = Expenses_record(
                    expenses_type=type,
                    expenses_date=date,
                    expenses_amount=amount,
                    expenses_project=expenses_list)

                Expenses_record_save.save()
                expenses_list.other_budget_spent += amount
                expenses_list.other_budget_remaining -= amount
                expenses_list.total_expenditure += amount
                expenses_list.budget_plan_remaining -= amount
                expenses_list.save()
                messages.success(request, f'Your expenses plan has been successfully updated')
                return redirect('expenses_manager', expenses_list.pk)


        else:
            messages.warning(request, f'Wrong Information. Please Try Again')
    else:
        OtherExpensesRecord_form = OtherExpensesRecordForm()

    context = {
        'OtherExpensesRecord_form': OtherExpensesRecord_form,
        'expenses_list': expenses_list,
        'other_used': other_used
    }
    return render(request, 'EzFinance_Account/other_expense_update.html', context)


@login_required
@xframe_options_sameorigin
def loan_calculator(request):
    if 'loan_calculate' in request.POST:
        loan_amount = request.POST.get("loan_amount")
        loan_period = request.POST.get("loan_period")
        selected_loan = request.POST.get("loan_provider")
        if selected_loan == 'Alliance Bank@8.88%':
            loan_rate = 8.88
        elif selected_loan == 'Kuwait Finance House@6.88%':
            loan_rate = 6.88
        elif selected_loan == 'Hong Leong @ 9%':
            loan_rate = 9
        elif selected_loan == 'Standard Chartered @ 6.88%':
            loan_rate = 6.88
        elif selected_loan == 'JCL @ 18%':
            loan_rate = 18
        elif selected_loan == 'HSBC @ 6.88%':
            loan_rate = 6.88
        elif selected_loan == 'UOB @ 9.96%':
            loan_rate = 9.96
        elif selected_loan == 'AmBank @ 9.99%':
            loan_rate = 9.99
        elif selected_loan == 'CIMB @ 6.88%':
            loan_rate = 6.88
        elif selected_loan == 'Maybank @ 6.5%':
            loan_rate = 6.5
        elif selected_loan == 'Bank Rakyat (Private Sector) @ 5.09%':
            loan_rate = 5.09
        elif selected_loan == 'Bank Rakyat (Public Sector) @ 4.54%':
            loan_rate = 4.54
        elif selected_loan == 'Bank Islam @ 4.99%':
            loan_rate = 4.99
        elif selected_loan == 'Al Rajhi @ 6.99%':
            loan_rate = 6.99
        elif selected_loan == 'MBSB (Private Sector) @ 6.58%':
            loan_rate = 6.58
        elif selected_loan == 'Citibank @ 5.88%':
            loan_rate = 5.88
        else:
            messages.warning(request, f'Please choose either interest rate as per Loan Provider')
            return redirect('loan_calculator')
        if loan_rate:
            rate = float(loan_rate) / 100
        loan = Loan(principal=float(loan_amount), interest=float(rate), term=int(loan_period))
        context = {
            'credit_balance': loan_amount,
            'annual_interest_rate': loan_rate,
            'tenure': loan_period,
            'total_paid': loan.total_paid,
            'total_interest_paid': loan.total_interest,
            'monthly_paid': loan.monthly_payment,
            'monthtopayoff': int(loan_period) * 12,
        }
        messages.success(request, f'Your loan has successfully calculated. Please refer to Your Monthly Payments.')
    else:
        context = {
            'credit_balance': 0,
            'annual_interest_rate': 0,
            'tenure': 0,
            'total_paid': 0,
            'total_interest_paid': 0,
            'monthly_paid': 0,
            'monthtopayoff': 0,
        }

    return render(request, 'EzFinance_Account/simple_loan_calculator.html', context)


# admin-site
@login_required
@staff_member_required
@xframe_options_sameorigin
def admin_site_home(request):
    # line graph
    """
        lineChart page
        """
    currentYear = date.today().year

    month = ["Jan", "Feb", "Mar","Apr", "May", "Jun","Jul", "Aug", "Sept","Oct", "Nov", "Dec"]
    data = []
    for x in range(12):
        if x==11:
            start = date(currentYear, int(x) + 1, 1)
            end = date(currentYear, int(x) + 1, 31)
            user_login = User.objects.filter(is_staff=False).filter(is_superuser=False).filter(date_joined__gte=start, date_joined__lt=end).count()
        else:
            start = date(currentYear, int(x)+1, 1)
            end = date(currentYear, int(x)+2, 1)
            user_login = User.objects.filter(is_staff=False).filter(is_superuser=False).filter(date_joined__gte=start,date_joined__lt=end).count()
        data.append([month[x], user_login])

    # line graph end
    staff = User.objects.filter(is_staff=True)
    # user
    if 'q' in request.GET:
        query = request.GET.get('q')
        if query == "":
            user = User.objects.filter(is_staff=False).filter(is_superuser=False)
        elif query.isdigit():
            user = User.objects.filter(is_staff=False).filter(is_superuser=False).filter(
                Q(pk__icontains=str(int(query) - 6067071528)))
        else:
            user = User.objects.filter(is_staff=False).filter(is_superuser=False).filter(
                Q(email__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
                | Q(username__icontains=query))

        page = request.GET.get('page', 1)

        paginator = Paginator(user, 5)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    else:
        user = User.objects.filter(is_staff=False).filter(is_superuser=False)
        page = request.GET.get('page', 1)

        paginator = Paginator(user, 5)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    case_check=Contact_us.objects.filter(check=False).count()
    announcement_check = General_announcement.objects.filter(publish_date=date.today()).filter(
        announcement_status=False).count()
    application_check=Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=False).count()+Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=True).count()

    context = {
        'all_user': user,
        'all_staff': staff,
        'users': users,
        'data': data,
        'currentYear':currentYear,
        'case_check':case_check,
        'announcement_check': announcement_check,
        'application_check': application_check,
    }
    return render(request, 'EzFinance_Account/admin_site_home.html', context)


@login_required
@staff_member_required
@xframe_options_sameorigin
def admin_site_profile(request):
    if request.user.is_authenticated:
        current_user_id = request.user.id
        account_num = int(current_user_id) + 771522553
    else:
        account_num = 'none'
    case_check = Contact_us.objects.filter(check=False).count()
    announcement_check = General_announcement.objects.filter(publish_date=date.today()).filter(
        announcement_status=False).count()
    application_check=Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=False).count()+Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=True).count()

    context = {
        "account_num": account_num,
        'case_check':case_check,
        'announcement_check': announcement_check,
        'application_check': application_check,
    }

    if 'btnAddMore' in request.POST:
        return redirect('admin_site_profile_update')
    return render(request, 'EzFinance_Account/admin_profile.html', context)


@login_required
@staff_member_required
@xframe_options_sameorigin
def admin_site_profile_update(request):
    if 'UpdateProfile' in request.POST:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = AccountUpdateForm(request.POST, request.FILES, instance=request.user.account)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('admin_site_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = AccountUpdateForm(instance=request.user.account)
    case_check = Contact_us.objects.filter(check=False).count()
    announcement_check = General_announcement.objects.filter(publish_date=date.today()).filter(
        announcement_status=False).count()
    application_check=Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=False).count()+Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=True).count()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'case_check': case_check,
        'announcement_check': announcement_check,
        'application_check': application_check,
    }
    return render(request, 'EzFinance_Account/admin_profile_update.html', context)

@login_required
@staff_member_required
@xframe_options_sameorigin
def user_detail(request, pk):
    user_detail_list = get_object_or_404(User, pk=pk)
    if 'q' in request.GET:
        query = request.GET.get('q')
        history_list = Transaction_history.objects.filter(user=user_detail_list).filter(
            Q(transaction_detail__icontains=query) | Q(transaction_date__icontains=query))
        page = request.GET.get('page', 1)

        paginator = Paginator(history_list, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    else:
        history_list = Transaction_history.objects.filter(user=user_detail_list)
        page = request.GET.get('page', 1)

        paginator = Paginator(history_list, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

    fixedDepositObject = FixedDeposit.objects.filter(user=user_detail_list)
    current_user_id = request.user.id
    account_num = int(current_user_id) + 771522553

    # set active & inactive
    if 'active_lock' in request.POST:
        user_detail_list.is_active = False
        user_detail_list.save()
        messages.success(request, f'Account {account_num} has successfully been locked.')
    elif 'active_unlock' in request.POST:
        user_detail_list.is_active = True
        user_detail_list.save()
        messages.success(request, f'Account {account_num} has successfully been unlocked.')
    case_check = Contact_us.objects.filter(check=False).count()
    announcement_check = General_announcement.objects.filter(publish_date=date.today()).filter(
        announcement_status=False).count()
    application_check=Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=False).count()+Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=True).count()

    context = {
        'user_detail_list': user_detail_list,
        'history_list': history_list,
        'users': users,
        'fixedDepositObject': fixedDepositObject,
        'account_num': account_num,
        'case_check': case_check,
        'announcement_check': announcement_check,
        'application_check': application_check,
    }

    return render(request, 'EzFinance_Account/user_detail.html',context )

@login_required
@staff_member_required
@xframe_options_sameorigin
def fixedDeposit_refund(request, pk):
    current_fixedDepositAcc = get_object_or_404(FixedDeposit, pk=pk)
    account_balance_deduct = Account.objects.get(user=current_fixedDepositAcc.user)
    if request.method == 'POST':
        amount_after = current_fixedDepositAcc.fixedDeposit_amount
        # update account balance
        account_balance_deduct.account_balance += round(amount_after, 2)
        account_balance_deduct.save()
        acc_id = 4045219663 + current_fixedDepositAcc.id
        transaction_detail = 'Fixed Deposit REFUND #' + str(acc_id)
        transfer_history_save = Transaction_history(transaction_detail=transaction_detail,
                                                    transaction_debit=round(amount_after, 2),
                                                    user=current_fixedDepositAcc.user)
        transfer_history_save.save()
        current_fixedDepositAcc.delete()
        messages.success(request, f'Refund has successfully been done for account number {acc_id}.')
        return redirect('user_detail', current_fixedDepositAcc.user.pk)

    return render(request, 'EzFinance_Account/user_detail.html')

@login_required
@staff_member_required
@xframe_options_sameorigin
def admin_transaction_analysis(request):
# credit transaction
    if 'q' in request.GET:
        query = request.GET.get('q')
        transaction_credit = FundTransfer.objects.all().filter(
            Q(transfer_date__icontains=query) | Q(transfer_category__icontains=query) | Q(transfer_to__icontains=query)
            | Q(transfer_bank__icontains=query) | Q(transfer_instruction__icontains=query))
        page = request.GET.get('page', 1)

        paginator = Paginator(transaction_credit, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    else:
        transaction_credit = FundTransfer.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(transaction_credit, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

# debit transaction
        transaction_debit=Deposit.objects.all()

    if 'p' in request.GET:
        query = request.GET.get('p')
        transaction_debit = Deposit.objects.all().filter(
            Q(creditcard_name__icontains=query) | Q(creditcard_num__icontains=query) | Q(deposit_date__icontains=query))
        page = request.GET.get('deposit_page', 1)

        paginator = Paginator(transaction_debit, 10)
        try:
            deposit_users = paginator.page(page)
        except PageNotAnInteger:
            deposit_users = paginator.page(1)
        except EmptyPage:
            deposit_users = paginator.page(paginator.num_pages)
    else:
        transaction_debit = Deposit.objects.all()
        page = request.GET.get('deposit_page', 1)

        paginator = Paginator(transaction_debit, 10)
        try:
            deposit_users = paginator.page(page)
        except PageNotAnInteger:
            deposit_users = paginator.page(1)
        except EmptyPage:
            deposit_users = paginator.page(paginator.num_pages)

#graph
    currentYear = date.today().year
    month = ["Jan", "Feb", "Mar","Apr", "May", "Jun","Jul", "Aug", "Sept","Oct", "Nov", "Dec"]
    data = []
    for x in range(12):
        if x==11:
            start = date(currentYear, int(x) + 1, 1)
            end = date(currentYear, int(x) + 1, 31)
            user_credit = FundTransfer.objects.filter(transfer_date__gte=start, transfer_date__lt=end).count()
            user_debit = Deposit.objects.filter(deposit_date__gte=start, deposit_date__lt=end).count()
        else:
            start = date(currentYear, int(x)+1, 1)
            end = date(currentYear, int(x)+2, 1)
            user_credit = FundTransfer.objects.filter(transfer_date__gte=start,transfer_date__lt=end).count()
            user_debit = Deposit.objects.filter(deposit_date__gte=start, deposit_date__lt=end).count()
        data.append([month[x], user_credit, user_debit])
    case_check = Contact_us.objects.filter(check=False).count()
    announcement_check = General_announcement.objects.filter(publish_date=date.today()).filter(announcement_status=False).count()
    application_check = Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=False).count() + Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=True).count()

    context = {
            'transaction_debit':transaction_debit,
            'transaction_credit': transaction_credit,
            'users': users,
            'deposit_users': deposit_users,
            'data':data,
            'currentYear':currentYear,
            'case_check':case_check,
            'announcement_check':announcement_check,
            'application_check':application_check,
    }

    return render(request, 'EzFinance_Account/admin_transaction_analysis.html', context)

@login_required
@staff_member_required
@xframe_options_sameorigin
def admin_fixed_deposit_analysis(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        transaction_fixeddeposit = FixedDeposit.objects.all().order_by('maturity_date').filter(
            Q(maturity_date__icontains=query) | Q(deposit_date__icontains=query) | Q(interest_rate__icontains=query) )
        page = request.GET.get('page', 1)

        paginator = Paginator(transaction_fixeddeposit, 15)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    else:
        transaction_fixeddeposit = FixedDeposit.objects.order_by('maturity_date').all()
        page = request.GET.get('page', 1)

        paginator = Paginator(transaction_fixeddeposit, 15)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

    # graph
    currentYear = date.today().year
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
    data = []
    for x in range(12):
        if x == 11:
            start = date(currentYear, int(x) + 1, 1)
            end = date(currentYear, int(x) + 1, 31)
            user_fixeddeposit = Transaction_history.objects.filter(Q(transaction_detail='Fixed Deposit-1 month/3.73% p.a.')|Q(transaction_detail='Fixed Deposit-3 month/4.10% p.a.')|Q(transaction_detail='Fixed Deposit-6 month/4.80% p.a.')|Q(transaction_detail='Fixed Deposit-12 month/5.40% p.a.')).filter(transaction_date__gte=start, transaction_date__lt=end).count()
            fixed_deposit_refund=Transaction_history.objects.filter(Q(transaction_detail__icontains='Fixed Deposit REFUND #')).filter(transaction_date__gte=start, transaction_date__lt=end).count()
            fixed_deposit_claim=Transaction_history.objects.filter(Q(transaction_detail__icontains='Fixed Deposit Claim #')).filter(transaction_date__gte=start, transaction_date__lt=end).count()
        else:
            start = date(currentYear, int(x) + 1, 1)
            end = date(currentYear, int(x) + 2, 1)
            user_fixeddeposit = Transaction_history.objects.filter(Q(transaction_detail='Fixed Deposit-1 month/3.73% p.a.')|Q(transaction_detail='Fixed Deposit-3 month/4.10% p.a.')|Q(transaction_detail='Fixed Deposit-6 month/4.80% p.a.')|Q(transaction_detail='Fixed Deposit-12 month/5.40% p.a.')).filter(transaction_date__gte=start, transaction_date__lt=end).count()
            fixed_deposit_refund = Transaction_history.objects.filter(Q(transaction_detail__icontains='Fixed Deposit REFUND #')).filter(transaction_date__gte=start,transaction_date__lt=end).count()
            fixed_deposit_claim = Transaction_history.objects.filter(Q(transaction_detail__icontains='Fixed Deposit Claim #')).filter(transaction_date__gte=start,transaction_date__lt=end).count()
        data.append([month[x], user_fixeddeposit, fixed_deposit_refund, fixed_deposit_claim])
    case_check = Contact_us.objects.filter(check=False).count()
    announcement_check = General_announcement.objects.filter(publish_date=date.today()).filter(
        announcement_status=False).count()
    application_check=Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=False).count()+Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=True).count()

    context={
        'transaction_fixeddeposit':transaction_fixeddeposit,
        'users':users,
        'today_date':datetime.date.today(),
        'data': data,
        'currentYear': date.today().year,
        'case_check': case_check,
        'announcement_check': announcement_check,
        'application_check': application_check,
    }
    return render(request, 'EzFinance_Account/admin_fixed_deposit_analysis.html', context)

@login_required
@staff_member_required
@xframe_options_sameorigin
def admin_customer_service(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        customer_feedback = Contact_us.objects.all().order_by('date').filter(
            Q(date__icontains=query) | Q(message__icontains=query) | Q(phone__icontains=query) | Q(email__icontains=query) | Q(name__icontains=query))
        page = request.GET.get('page', 1)

        paginator = Paginator(customer_feedback, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    else:
        customer_feedback = Contact_us.objects.order_by('date').all()
        page = request.GET.get('page', 1)

        paginator = Paginator(customer_feedback, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
            # graph
        currentYear = date.today().year
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
        data = []
        for x in range(12):
            if x == 11:
                start = date(currentYear, int(x) + 1, 1)
                end = date(currentYear, int(x) + 1, 31)
                issue_amt = Contact_us.objects.filter(date__gte=start, date__lt=end).count()

            else:
                start = date(currentYear, int(x) + 1, 1)
                end = date(currentYear, int(x) + 2, 1)
                issue_amt = Contact_us.objects.filter(date__gte=start, date__lt=end).count()

            data.append([month[x], issue_amt])

    case_check = Contact_us.objects.filter(check=False).count()
    announcement_check = General_announcement.objects.filter(publish_date=date.today()).filter(
        announcement_status=False).count()
    application_check=Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=False).count()+Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=True).count()

    context={
        'customer_feedback':customer_feedback,
        'users': users,
        'data':data,
        'currentYear':currentYear,
        'case_check': case_check,
        'announcement_check': announcement_check,
        'application_check': application_check,
    }
    return render(request, 'EzFinance_Account/admin_customer_service.html', context)

@login_required
@staff_member_required
@xframe_options_sameorigin
def customer_service_case(request, pk):
    current_case = get_object_or_404(Contact_us, pk=pk)
    issue_id=int(current_case.id)+1140
    if 'issue_solved' in request.POST:
        current_case.check = True
        current_case.save()
        messages.success(request, f'Issue #(ID:{issue_id}) had successfully solved and closed.')
    elif 'issue_activate' in request.POST:
        current_case.check = False
        current_case.save()
        messages.success(request, f'Issue (ID:#{issue_id}) had successfully been activated.')
    case_check = Contact_us.objects.filter(check=False).count()
    announcement_check = General_announcement.objects.filter(publish_date=date.today()).filter(
        announcement_status=False).count()
    application_check=Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=False).count()+Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=True).count()

    context={
        'current_case':current_case,
        'case_check':case_check,
        'announcement_check': announcement_check,
        'application_check': application_check,
    }
    return render(request, 'EzFinance_Account/customer_service_case.html', context)

@login_required
@staff_member_required
@xframe_options_sameorigin
def admin_announcement(request):
# form
    if 'announcement_save' in request.POST:
        announcement_form=AnnouncementForm(request.POST)
        if announcement_form.is_valid():
            announcement_form.save()
            messages.success(request, f'Announcement had succesfully saved')
            return redirect('admin_announcement')
        else:
            messages.warning(request, f'Announcement failed to save. Please try again')
    else:
        announcement_form = AnnouncementForm()
# table
    if 'q' in request.GET:
        query = request.GET.get('q')
        announcement_list = General_announcement.objects.all().order_by('publish_date').filter(
            Q(announcement_subject__icontains=query) | Q(announcement_content__icontains=query) )
        page = request.GET.get('page', 1)

        paginator = Paginator(announcement_list, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    else:
        announcement_list = General_announcement.objects.order_by('publish_date').all()
        page = request.GET.get('page', 1)

        paginator = Paginator(announcement_list, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

    case_check = Contact_us.objects.filter(check=False).count()
    announcement_check = General_announcement.objects.filter(publish_date=date.today()).filter(announcement_status=False).count()
    application_check = Job_create_request.objects.filter(job_request_approval_status=False,job_request_reject_status=False,job_request_reedit_status=False).count() + Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=True).count()

    context={
            'announcement_form':announcement_form,
            'announcement_list':announcement_list,
            'users': users,
            'case_check':case_check,
            'today':date.today(),
            'announcement_check':announcement_check,
            'application_check':application_check,
        }
    return render(request, 'EzFinance_Account/admin_announcement.html', context)

@login_required
@staff_member_required
@xframe_options_sameorigin
def announcement_delete(request, pk):
    announcement_selected = get_object_or_404(General_announcement, pk=pk)
    if request.method == 'GET':
        announcement_selected.delete()
        messages.success(request, f'Announcement selected had successfully deleted')
        return redirect('admin_announcement')
    return render(request, 'EzFinance_Account/admin_announcement.html')

@login_required
@staff_member_required
@xframe_options_sameorigin
def announcement_publish(request, pk):
    announcement_selected = get_object_or_404(General_announcement, pk=pk)
    if request.method == 'GET':
        announcement_selected.announcement_status=True
        announcement_selected.save()
        messages.success(request, f'Selected announcement had successfully published')
        return redirect('admin_announcement')
    return render(request, 'EzFinance_Account/admin_announcement.html')

@login_required
@staff_member_required
@xframe_options_sameorigin
def announcement_undo(request, pk):
    announcement_selected = get_object_or_404(General_announcement, pk=pk)
    if request.method == 'GET':
        announcement_selected.announcement_status=False
        announcement_selected.save()
        messages.success(request, f'Selected announcement had successfully retrieved')
        return redirect('admin_announcement')
    return render(request, 'EzFinance_Account/admin_announcement.html')

@login_required
@staff_member_required
@xframe_options_sameorigin
def admin_job_vacancy(request):

    # Job Pending
    job_application_list_pending = Job_create_request.objects.filter(job_request_approval_status=False,
                                                                     job_request_reject_status=False,
                                                                     job_request_reedit_status=False).order_by('job_created_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(job_application_list_pending, 5)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    # Job Approve
    job_application_list_approve = Job_create_request.objects.filter(job_request_approval_status=True,
                                                                     job_request_reject_status=False,
                                                                     job_request_reedit_status=False).order_by('job_expiry_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(job_application_list_approve, 5)
    try:
        approve_users = paginator.page(page)
    except PageNotAnInteger:
        approve_users = paginator.page(1)
    except EmptyPage:
        approve_users = paginator.page(paginator.num_pages)

    # Job Edit
    job_application_list_edit = Job_create_request.objects.filter(job_request_approval_status=False, job_request_reedit_status=True).order_by('job_created_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(job_application_list_edit, 5)
    try:
        rejected_users = paginator.page(page)
    except PageNotAnInteger:
        rejected_users = paginator.page(1)
    except EmptyPage:
        rejected_users = paginator.page(paginator.num_pages)

    case_check = Contact_us.objects.filter(check=False).count()
    announcement_check = General_announcement.objects.filter(publish_date=date.today()).filter(
        announcement_status=False).count()

    application_check=Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=False).count()+Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=True).count()
    context={
        'case_check': case_check,
        'announcement_check': announcement_check,
        'job_application_list_pending': job_application_list_pending,
        'job_application_list_approve': job_application_list_approve,
        'job_application_list_edit': job_application_list_edit,
        'users':users,
        'approve_users':approve_users,
        'today_date':date.today(),
        'job_application_list_pending_total': job_application_list_pending.count(),
        'job_application_list_approve_total': job_application_list_approve.count(),
        'job_application_list_edit_total': job_application_list_edit.count(),
        'rejected_users':rejected_users,
        'application_check':application_check,
    }
    return render(request, 'EzFinance_Account/admin_job_vacancy.html',context)

@login_required
@staff_member_required
@xframe_options_sameorigin
def admin_job_vacancy_resubmit_process(request, pk):
    job_create_form = get_object_or_404(Job_create_request, pk=pk)
    job_id = int(job_create_form.pk) + 886457
    # approval
    if 'ApproveJobApplication' in request.POST:
        exp_date = date.today() + relativedelta(days=job_create_form.job_available_day)
        Job_create_request.objects.filter(pk=job_create_form.pk).update(
            job_request_approval_status=True,
            job_request_reject_status=False,
            job_request_reedit_status=False,
            job_posted_date=date.today(),
            job_expiry_date=exp_date,
        )
        vacancy = "Vacancy for " + job_create_form.job_position
        annoucement_vacancy_post = General_announcement(
            announcement_subject=job_create_form.job_employer_company,
            announcement_content=vacancy,
            announcement_status=True,
            publish_date=date.today()
        )
        annoucement_vacancy_post.save()
        messages.success(request, f'Job application ID #J{job_id} has approved.')
        return redirect('admin_job_vacancy')
    # reject
    if 'admin_reject_btn' in request.POST:
        admin_message = request.POST['admin_comment']
        Job_create_request.objects.filter(pk=job_create_form.pk).update(
            job_request_approval_status=False,
            job_request_reject_status=True,
            job_request_reedit_status=True,
            job_admin_notice=admin_message,
        )
        messages.warning(request, f'Job application ID #J{job_id} has rejected.')
        return redirect('admin_job_vacancy')

    case_check = Contact_us.objects.filter(check=False).count()
    announcement_check = General_announcement.objects.filter(publish_date=date.today()).filter(
        announcement_status=False).count()
    application_check=Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=False).count()+Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=True).count()

    context = {
        'job_create_form': job_create_form,
        'case_check': case_check,
        'announcement_check': announcement_check,
        'application_check': application_check,
    }
    return render(request, 'EzFinance_Account/admin_job_vacancy_resubmit_process.html', context)

@login_required
@staff_member_required
@xframe_options_sameorigin
def admin_job_vacancy_delete(request, pk):
    job_selected = get_object_or_404(Job_create_request, pk=pk)
    job_id = int(job_selected.pk) + 886457
    if request.method == 'GET':
        job_selected.delete()
        messages.success(request, f'Job Applcation [ ID: #J{job_id} ] had successfully deleted')
        return redirect('admin_job_vacancy')
    return render(request, 'EzFinance_Account/admin_job_vacancy.html')

@login_required
@staff_member_required
@xframe_options_sameorigin
def approved_job_vacancy_detail(request, pk):
    job_create_form = get_object_or_404(Job_create_request, pk=pk)
    job_id = int(job_create_form.pk) + 886457

    if 'DeleteJobApplication' in request.POST:
        job_create_form.delete()
        messages.success(request, f'Job Applcation [ ID: #J{job_id} ] had successfully deleted')
        return redirect('admin_job_vacancy')

    case_check = Contact_us.objects.filter(check=False).count()
    announcement_check = General_announcement.objects.filter(publish_date=date.today()).filter(
        announcement_status=False).count()
    application_check=Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=False).count()+Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=True).count()

    context = {
        'job_create_form': job_create_form,
        'case_check': case_check,
        'announcement_check': announcement_check,
        'application_check': application_check,
    }
    return render(request, 'EzFinance_Account/approved_job_vacancy_detail.html', context)

@login_required
@staff_member_required
@xframe_options_sameorigin
def admin_job_vacancy_process(request, pk):
    job_create_form = get_object_or_404(Job_create_request, pk=pk)
    job_id = int(job_create_form.pk) + 886457
    # approval
    if 'ApproveJobApplication' in request.POST:
        exp_date = date.today() + relativedelta(days=job_create_form.job_available_day)
        Job_create_request.objects.filter(pk=job_create_form.pk).update(
            job_request_approval_status=True,
            job_posted_date=date.today(),
            job_expiry_date=exp_date,
        )
        vacancy="Vacancy for "+ job_create_form.job_position
        annoucement_vacancy_post=General_announcement(
            announcement_subject=job_create_form.job_employer_company,
            announcement_content=vacancy,
            announcement_status=True,
            publish_date=date.today()
        )
        annoucement_vacancy_post.save()
        messages.success(request, f'Job application ID #J{job_id} has approved.')
        return redirect('admin_job_vacancy')
    # reject
    if 'admin_reject_btn' in request.POST:
        admin_message=request.POST['admin_comment']
        Job_create_request.objects.filter(pk=job_create_form.pk).update(
            job_request_approval_status=False,
            job_request_reject_status=True,
            job_request_reedit_status=True,
            job_admin_notice=admin_message,
        )
        messages.warning(request, f'Job application ID #J{job_id} has rejected.')
        return redirect('admin_job_vacancy')

    case_check = Contact_us.objects.filter(check=False).count()
    announcement_check = General_announcement.objects.filter(publish_date=date.today()).filter(
        announcement_status=False).count()
    application_check=Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=False).count()+Job_create_request.objects.filter(job_request_approval_status=False, job_request_reject_status=False, job_request_reedit_status=True).count()

    context={
        'job_create_form': job_create_form,
        'case_check': case_check,
        'announcement_check': announcement_check,
        'application_check': application_check,
    }
    return render(request, 'EzFinance_Account/admin_job_vacancy_process.html',context)
# Part Time Job

@login_required
@xframe_options_sameorigin
def user_job_create(request):
    if 'job_create_btn' in request.POST:
        job_create_form = JobcreationForm(request.POST)
        if job_create_form.is_valid():
            # get input data
            job_available_day = job_create_form.cleaned_data['job_available_day']
            job_employer_name = job_create_form.cleaned_data['job_employer_name']
            job_employer_contact_number = job_create_form.cleaned_data['job_employer_contact_number']
            job_employer_email = job_create_form.cleaned_data['job_employer_email']
            job_employer_company = job_create_form.cleaned_data['job_employer_company']
            job_location = job_create_form.cleaned_data['job_location']
            job_general_description = job_create_form.cleaned_data['job_general_description']
            job_position = job_create_form.cleaned_data['job_position']
            job_duties = job_create_form.cleaned_data['job_duties']
            job_requirement = job_create_form.cleaned_data['job_requirement']
            job_salary = job_create_form.cleaned_data['job_salary']
            job_type = job_create_form.cleaned_data['job_type']
            Job_create_request_save=Job_create_request(
                job_available_day=job_available_day,
                job_employer_name=job_employer_name,
                job_employer_contact_number=job_employer_contact_number,
                job_employer_email=job_employer_email,
                job_employer_company=job_employer_company,
                job_location=job_location,
                job_general_description=job_general_description,
                job_position=job_position,
                job_duties=job_duties,
                job_requirement=job_requirement,
                job_salary=job_salary,
                job_type=job_type,
                user=request.user,
            )
            Job_create_request_save.save()
            # get input data end
            messages.success(request, f'Your new job request has successfully submitted and currently processing')
            return redirect('user_job_create')
        else:
            messages.warning(request, f'Request failed. Please Try Again')
    else:
        job_create_form = JobcreationForm()

    job_request_list=Job_create_request.objects.filter(user=request.user).order_by('job_created_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(job_request_list, 5)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context={
        'job_create_form':job_create_form,
        'job_request_list':job_request_list,
        'today': date.today(),
        'users':users,
    }
    return render(request, 'EzFinance_Account/user_job_create.html',context)

@login_required
@xframe_options_sameorigin
def job_application_modify(request, pk):
    job_application_selected = get_object_or_404(Job_create_request, pk=pk)
    job_id = int(job_application_selected.pk) + 886457
    if 'ModifyJobApplication' in request.POST:
        job_create_form = JobcreationForm(request.POST, instance=job_application_selected)
        if job_create_form.is_valid():
            job_available_day = job_create_form.cleaned_data['job_available_day']
            job_employer_name = job_create_form.cleaned_data['job_employer_name']
            job_employer_contact_number = job_create_form.cleaned_data['job_employer_contact_number']
            job_employer_email = job_create_form.cleaned_data['job_employer_email']
            job_employer_company = job_create_form.cleaned_data['job_employer_company']
            job_location = job_create_form.cleaned_data['job_location']
            job_general_description = job_create_form.cleaned_data['job_general_description']
            job_position = job_create_form.cleaned_data['job_position']
            job_duties = job_create_form.cleaned_data['job_duties']
            job_requirement = job_create_form.cleaned_data['job_requirement']
            job_salary = job_create_form.cleaned_data['job_salary']
            job_type = job_create_form.cleaned_data['job_type']

            Job_create_request.objects.filter(pk=job_application_selected.pk).update(
                job_available_day=job_available_day,
                job_employer_name=job_employer_name,
                job_employer_contact_number=job_employer_contact_number,
                job_employer_email=job_employer_email,
                job_employer_company=job_employer_company,
                job_location=job_location,
                job_general_description=job_general_description,
                job_position=job_position,
                job_duties=job_duties,
                job_requirement=job_requirement,
                job_salary=job_salary,
                job_type=job_type,
                job_request_reject_status=False,
            )

            messages.success(request, f'Job application ID #J{job_id} has successfully modified.')
            return redirect('user_job_create')
    else:
        job_create_form = JobcreationForm(instance=job_application_selected)
    context={
        'job_create_form': job_create_form,
        'job_application_selected':job_application_selected,
    }
    return render(request, 'EzFinance_Account/job_application_modify.html', context)

# Part Time Job End

# Apply Job
@login_required
@xframe_options_sameorigin
def job_vacancy_list(request):
    vacancy_list=Job_create_request.objects.filter(job_request_approval_status=True, job_request_reject_status=False, job_request_reedit_status=False).exclude(user=request.user)
    page = request.GET.get('page', 1)

    paginator = Paginator(vacancy_list, 5)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    # vacancy form
    if 'vacancy_submit_btn' in request.POST:
        vacancyform = VacancyForm(request.POST, request.FILES)
        vacancy_pk = request.POST['vacancy_pk']
        vacancy_apply = Job_create_request.objects.get(pk=vacancy_pk)
        if vacancyform.is_valid():
            Job_apply_save=Job_apply(
                job_applicant_name=vacancyform.cleaned_data['job_applicant_name'],
                job_applicant_email = vacancyform.cleaned_data['job_applicant_email'],
                job_applicant_contact_number = vacancyform.cleaned_data['job_applicant_contact_number'],
                job_pitch = vacancyform.cleaned_data['job_pitch'],
                applicant_resume =vacancyform.cleaned_data['applicant_resume'],
                user = request.user,
                job_post_list = vacancy_apply,
            )
            Job_apply_save.save()
        messages.success(request, f'Your job application has successfully send to employer')
    else:
        vacancyform = VacancyForm()

    # my vacancy list
    my_apply_list=Job_apply.objects.filter(user=request.user)
    page = request.GET.get('page', 1)

    paginator = Paginator(my_apply_list, 10)
    try:
        users_apply_list = paginator.page(page)
    except PageNotAnInteger:
        users_apply_list = paginator.page(1)
    except EmptyPage:
        users_apply_list = paginator.page(paginator.num_pages)

    context={
        'vacancy_list':vacancy_list,
        'users':users,
        'vacancyForm':vacancyform,
        'my_apply_list': my_apply_list,
        'users_apply_list':users_apply_list,
        'my_apply_list_count': my_apply_list.count(),
    }
    return render(request, 'EzFinance_Account/job_vacancy_list.html', context)

@login_required
@xframe_options_sameorigin
def job_vacancy_list_detail(request, pk):
    job_vacancy_list_detail_selected = get_object_or_404(Job_create_request, pk=pk)
    # submit application
    if 'vacancy_submit_btn' in request.POST:
        vacancyform = VacancyForm(request.POST, request.FILES)
        vacancy_pk = request.POST['vacancy_pk']
        vacancy_apply = Job_create_request.objects.get(pk=vacancy_pk)
        if vacancyform.is_valid():
            Job_apply_save = Job_apply(
                job_applicant_name=vacancyform.cleaned_data['job_applicant_name'],
                job_applicant_email=vacancyform.cleaned_data['job_applicant_email'],
                job_applicant_contact_number=vacancyform.cleaned_data['job_applicant_contact_number'],
                job_pitch=vacancyform.cleaned_data['job_pitch'],
                applicant_resume=vacancyform.cleaned_data['applicant_resume'],
                user=request.user,
                job_post_list=vacancy_apply,
            )
            Job_apply_save.save()
        messages.success(request, f'Your job application has successfully send to employer')
        return redirect('job_vacancy_list_detail', job_vacancy_list_detail_selected.pk)
    else:
        vacancyform = VacancyForm()
    context={
        'job_vacancy_list_detail_selected': job_vacancy_list_detail_selected,
        'vacancyForm':vacancyform,
    }
    return render(request, 'EzFinance_Account/job_vacancy_list_detail.html', context)
# Apply Job

# delete Job
@login_required
@xframe_options_sameorigin
def job_vacancy_list_delete(request, pk):
    job_vacancy_list_delete_selected = get_object_or_404(Job_apply, pk=pk)
    if request.method == 'GET':
        job_vacancy_list_delete_selected.delete()
        messages.success(request, f'Your job application had successfully deleted')
        return redirect('job_vacancy_list')

    return render(request, 'EzFinance_Account/job_vacancy_list.html')

#review applied job detail
@login_required
@xframe_options_sameorigin
def job_vacancy_list_selected_review(request, pk):
    job_vacancy_list_detail_selected = get_object_or_404(Job_create_request, pk=pk)
    context = {
        'job_vacancy_list_detail_selected': job_vacancy_list_detail_selected,
        }
    return render(request, 'EzFinance_Account/job_vacancy_list_selected_review.html',context)

#employer review application
@login_required
@xframe_options_sameorigin
def job_vacancy_applied_list(request, pk):
    job_vacancy_list_detail_selected = get_object_or_404(Job_create_request, pk=pk)
    applied_list=Job_apply.objects.filter(job_post_list=job_vacancy_list_detail_selected).order_by('job_apply_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(applied_list, 5)
    try:
        users_applied_list = paginator.page(page)
    except PageNotAnInteger:
        users_applied_list = paginator.page(1)
    except EmptyPage:
        users_applied_list = paginator.page(paginator.num_pages)

    if 'vacancy_accept' in request.POST:
        vacancy_pk = request.POST['applied_list_pk']
        vacancy_name = request.POST['applied_list_name']
        Job_apply.objects.filter(pk=vacancy_pk).update(
            job_mark_as_read=True,
            job_reject=False,
        )
        messages.success(request, f'You had accepted {vacancy_name} application' )
        return redirect('job_vacancy_applied_list', job_vacancy_list_detail_selected.pk)

    if 'vacancy_reject' in request.POST:
        vacancy_pk = request.POST['applied_list_pk']
        vacancy_name = request.POST['applied_list_name']
        Job_apply.objects.filter(pk=vacancy_pk).update(
            job_mark_as_read=False,
            job_reject=True,
        )
        messages.success(request, f'You had rejected {vacancy_name} application' )
        return redirect('job_vacancy_applied_list', job_vacancy_list_detail_selected.pk)

    context={
        'applied_list':applied_list,
        'users_applied_list':users_applied_list,
        'job_vacancy_list_detail_selected':job_vacancy_list_detail_selected,
        'applied_list_count': applied_list.count(),
    }
    return render(request, 'EzFinance_Account/job_vacancy_applied_list.html', context)




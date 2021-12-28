from django.contrib import admin
from .models import Deposit
from .models import FundTransfer, Transaction_history, ExpensesManager,Expenses_record,FixedDeposit,Contact_us,General_announcement,Job_create_request,Job_apply

admin.site.register(Deposit)
admin.site.register(FundTransfer)
admin.site.register(Transaction_history)
admin.site.register(ExpensesManager)
admin.site.register(Expenses_record)
admin.site.register(FixedDeposit)
admin.site.register(Contact_us)
admin.site.register(General_announcement)
admin.site.register(Job_create_request)
admin.site.register(Job_apply)
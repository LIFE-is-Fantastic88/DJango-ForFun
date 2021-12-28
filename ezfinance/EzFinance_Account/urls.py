from django.urls import path
from .import views
urlpatterns = [
    path('home', views.home, name='EzFinance-Account-home'),
    path('profile', views.profile, name='EzFinance-Account-profile'),
    path('transaction', views.transaction, name='EzFinance-Account-transaction'),
    path('transaction-history', views.history, name='EzFinance-transaction-history'),
    path('fixed-deposit', views.fixed_deposit, name='EzFinance-Account-fixed-deposit'),
    path('profile-update', views.profile_update, name='EzFinance-Account-profile-update'),
    path('expenses-manager/?P<pk>\d+', views.expenses_manager, name='expenses_manager'),
    path('expenses-manager-menu', views.expenses_manager_menu, name='EzFinance-Account-expenses-manager-menu'),
    path('expenses-manager-form', views.expenses_manager_form, name='EzFinance-Account-expenses-manager-form'),
    path('expenses-dailylivingexpense/?P<pk>\d+', views.dailyliving_expenses, name='dailyliving_expenses'),
    path('expenses-educationexpense/?P<pk>\d+', views.education_expenses, name='education_expenses'),
    path('expenses-entertainmentexpense/?P<pk>\d+', views.entertainment_expenses, name='entertainment_expenses'),
    path('expenses-healthcareexpense/?P<pk>\d+', views.healthcare_expenses, name='healthcare_expenses'),
    path('expenses-homerentalexpense/?P<pk>\d+', views.homerental_expenses, name='homerental_expenses'),
    path('expenses-transportationexpense/?P<pk>\d+', views.transportation_expenses, name='transportation_expenses'),
    path('expenses-loanexpense/?P<pk>\d+', views.loan_expenses, name='loan_expenses'),
    path('expenses-otherexpense/?P<pk>\d+', views.other_expenses, name='other_expenses'),
    path('expenses-deleteexpense/?P<pk>\d+', views.expenses_delete, name='expenses_delete'),
    path('fixed_deposit_claim_process/?P<pk>\d+', views.fixedDeposit_claim, name='fixedDeposit_claim'),
    path('expenses-loan-calculator', views.loan_calculator, name='loan_calculator'),
    path('administrator-site', views.admin_site_home, name='admin_site_home'),
    path('admin-profile', views.admin_site_profile, name='admin_site_profile'),
    path('admin-profile-update', views.admin_site_profile_update, name='admin_site_profile_update'),
    path('adminsite_userdetail/?P<pk>\d+', views.user_detail, name='user_detail'),
    path('fixed_deposit_refund_process/?P<pk>\d+', views.fixedDeposit_refund, name='fixedDeposit_refund'),
    path('admin-transaction-analysis', views.admin_transaction_analysis, name='admin_transaction_analysis'),
    path('admin-fixed-deposit-analysis', views.admin_fixed_deposit_analysis, name='admin_fixed_deposit_analysis'),
    path('admin-customer-service', views.admin_customer_service, name='admin_customer_service'),
    path('admin_service_case/?P<pk>\d+', views.customer_service_case, name='customer_service_case'),
    path('admin_announcement', views.admin_announcement, name='admin_announcement'),
    path('admin_announcement_delete/?P<pk>\d+', views.announcement_delete, name='announcement_delete'),
    path('admin_announcement_publish/?P<pk>\d+', views.announcement_publish, name='announcement_publish'),
    path('admin_announcement_restore/?P<pk>\d+', views.announcement_undo, name='announcement_undo'),
    path('job_create_post', views.user_job_create, name='user_job_create'),
    path('job_application_modify/?P<pk>\d+', views.job_application_modify, name='job_application_modify'),
    path('admin_job_vacancy', views.admin_job_vacancy, name='admin_job_vacancy'),
    path('admin_job_vacancy_process/?P<pk>\d+', views.admin_job_vacancy_process, name='admin_job_vacancy_process'),
    path('admin_job_vacancy_delete/?P<pk>\d+', views.admin_job_vacancy_delete, name='admin_job_vacancy_delete'),
    path('approved_job_vacancy_detail/?P<pk>\d+', views.approved_job_vacancy_detail, name='approved_job_vacancy_detail'),
    path('admin_job_vacancy_resubmit_process/?P<pk>\d+', views.admin_job_vacancy_resubmit_process, name='admin_job_vacancy_resubmit_process'),
    path('job_vacancy_list', views.job_vacancy_list, name='job_vacancy_list'),
    path('job_vacancy_list_detail/?P<pk>\d+', views.job_vacancy_list_detail, name='job_vacancy_list_detail'),
    path('job_vacancy_list_delete/?P<pk>\d+', views.job_vacancy_list_delete, name='job_vacancy_list_delete'),
    path('job_vacancy_list_selected_review/?P<pk>\d+', views.job_vacancy_list_selected_review, name='job_vacancy_list_selected_review'),
    path('job_vacancy_applied_list/?P<pk>\d+', views.job_vacancy_applied_list, name='job_vacancy_applied_list'),
]
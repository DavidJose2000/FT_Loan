from django.contrib import admin
from .models import Referral, Loan, BankInfo, Profile, Additional_assets, Additional_liabilities, Verification, Contact, Business
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
import os

admin.site.unregister(User)
@admin.register(User)
class UserAdminCoustoms(UserAdmin):
    actions = ['download_csv']
    list_display = ('username','email','first_name','last_name', 'is_superuser')
    

    def download_csv(self, request, queryset):
        
        import csv
        from django.http import HttpResponse

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'w+')
        writer = csv.writer(f)

        writer.writerow(['id','username','email','first_name','last_name', 'superuser'])

        for s in queryset:
            writer.writerow([s.id, s.username, s.email, s.first_name, s.last_name, s.is_superuser])

        f.close()

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'r+')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=User.csv'
        return response

    download_csv.short_description = "export csv"
    


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ('user', 'fullname', 'signature','pdf', 'phonenum','emailid', 'status', 'created_on')
    search_fields = ['user__username']
    def phonenum(self, obj):
        u = obj.user
        p = Profile.objects.get(user=u)
        phone = p.phnumber
        # obj.phone_no=Profile.phnumber
        return phone
    def emailid(self, obj):
        e = obj.user.email
        return e


    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'w+')
        writer = csv.writer(f)

        writer.writerow(['id','user', 'fullname', 'signature', 'pdf', 'status', 'created_on','phonenum','emailid'])

        for s in queryset:
            writer.writerow([s.id, s.user, s.fullname, s.signature, s.pdf, s.status, s.created_on,s.user.profile.phnumber,s.user.email])

        f.close()

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'r+')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Bizpartner-data.csv'
        return response

    download_csv.short_description = "export csv"

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ('referred_by', 'user', 'status', 'commission_status',  'commissions')
    search_fields = ['referred_by__username']
    
    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'w+')
        writer = csv.writer(f)

        writer.writerow(['id','referred_by','user','status','commission_status', 'commissions','created_on'])

        for s in queryset:
            writer.writerow([s.id, s.referred_by, s.user, s.status, s.commission_status, s.commissions, s.created_on])

        f.close()

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'r+')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=referral-info.csv'
        return response

    download_csv.short_description = "export csv"


class Additional_assetsInline(admin.TabularInline):
    model = Additional_assets
    extra = 0

class Additional_liabilitiesInline(admin.TabularInline):
    model = Additional_liabilities
    extra = 0



@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id','user_id', 'Username', 'First_name', 'Last_name',  'Phone_Number', 'Email', 'loan_type','loan_wname','loan_wphone','loan_wemail','vehicle','vehicle_worth','vehicle_money','carloan_pay','accounts','superannuation','credit_card','loans','employment_type','annual_salary','monthly_expense', 'created_on')
    
    def Phone_Number(self, obj):
        u = obj.user
        p = Profile.objects.get(user=u)
        phone = p.phnumber
        return phone
        
    def Email(self, obj):
        e = obj.user.email
        return e

    def Username(self, obj):
        e = obj.user.username
        return e    
    
    def First_name(self, obj):
        e = obj.user.first_name
        return e    

    def Last_name(self, obj):
        e = obj.user.last_name
        return e    
    
    inlines = [
        Additional_assetsInline,
        Additional_liabilitiesInline
    ]
    actions = ['download_csv']
    search_fields = ['user_id__username']

    list_filter = (
        'user_id',
    )

    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'w+')
        writer = csv.writer(f)
        writer.writerow(['id','user_id', 'Username', 'First_name', 'Last_name',  'Phone_Number', 'Email', 'Do you want to buy a new house or refinance existing loan ?','loan_wname','loan_wphone','loan_wemail','Do you have car or any other type of vehicle ?','Car Market Value','Car Loan','If required, Can you pay off car loan immediately?','$ in Saving Accounts ?','$ in Superannuation', 'Do you have any additional assets ?','Term Deposit Description', 'Term Deposit Total Value','Shares Description', 'Shares Total Value','Managed Funds Description', 'Managed Funds Total Value','Gift Cards Description', 'Gift Cards Total Value','Approximate value of total home contains you may have ?', 'Do you have any Credit Card ?', 'Credit Limit', 'Do you have any other additional liabilities ?', 'Tax Debt Owned', 'Tax Debt Description','other lines of credit owned','other lines of credit Description', 'How much existing Mortgage loan you have currently?','employment_type','Annual Salary  (Indicate Combined Family Income)','Monthly Expense (Indicate Combined Family Expense)', 'created_on'])

        for s in queryset:
            try:
                term_Deposit = Additional_assets.objects.get(loan=s, types="Term Deposit")
                term_desc = term_Deposit.description
                term_Depo = term_Deposit.total_value
            except Additional_assets.DoesNotExist:
                term_Deposit=None
                term_Depo="-"
                term_desc="-"
            
            try:
                shares = Additional_assets.objects.get(loan=s, types="Shares")
                shar_desc = shares.description
                shar = shares.total_value
            except Additional_assets.DoesNotExist:
                shares=None
                shar="-"
                shar_desc="-"
            
            try:    
                mf = Additional_assets.objects.get(loan=s, types="Managed Funds")
                mf_desc = mf.description
                mf_value=mf.total_value
            except Additional_assets.DoesNotExist:
                mf=None
                mf_value="-"
                mf_desc="-"
            
            try:    
                gift = Additional_assets.objects.get(loan=s, types="Gifts")
                gif_desc = gift.description
                gif=gift.total_value
            except Additional_assets.DoesNotExist:
                gift=None
                gif="-"
                gif_desc="-"
            
            try:
                tax_loan = Additional_liabilities.objects.get(loan=s, types = "tax debt")
                t_desc= tax_loan.description
                t= tax_loan.owned
            except Additional_liabilities.DoesNotExist:
                tax_loan=None
                t="-"
                t_desc="-"
            
            try:
                credit_loan = Additional_liabilities.objects.get(loan=s, types = "other lines of credit")
                cred_desc= credit_loan.description
                cred = credit_loan.owned
            except Additional_liabilities.DoesNotExist:
                credit_loan= None
                cred="-"
                cred_desc="-"
            writer.writerow([s.id, s.user_id, s.user.username, s.user.first_name, s.user.last_name, s.user.profile.phnumber, s.user.email, s.loan_type, s.loan_wname, s.loan_wphone, s.loan_wemail, s.vehicle, s.vehicle_worth, s.vehicle_money, s.carloan_pay, s.accounts, s.superannuation,s.additional_asset,term_desc, term_Depo,shar_desc,shar, mf_desc,mf_value,gif_desc,gif,s.home_content, s.credit_card, s.credit_limit, s.liability_loan,t,t_desc, cred, cred_desc, s.loans, s.employment_type, s.annual_salary, s.monthly_expense, s.created_on])

        f.close()

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'r+')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=loan-info.csv'
        return response

    download_csv.short_description = "export csv"
    
@admin.register(BankInfo)
class BankInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'bankname','acname', 'acno', 'bankisc')
    search_fields = ['user_id__username']
    actions =['download_csv']

    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'w+')
        writer = csv.writer(f)
        writer.writerow(['id','user_id','bankname','acname','acno','bankisc','created_on'])

        for s in queryset:
            writer.writerow([s.id, s.user_id, s.bankname, s.acname, s.acno, s.bankisc, s.created_on])

        f.close()

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'r+')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=bank-info.csv'
        return response

    download_csv.short_description = "export csv"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phnumber', 'email_confirmed')
    search_fields = ['user__username']
    actions =['download_csv']

    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

    
        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'w+')
        writer = csv.writer(f)
        writer.writerow(['id','user','phnumber','email_confirmed'])

        for s in queryset:
            writer.writerow([s.id, s.user, s.phnumber, s.email_confirmed])

        f.close()

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'r+')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=profile-info.csv'
        return response

    download_csv.short_description = "export csv"

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):

    # def is_bizpartner(self):
    #     return self.is_bizpartner=1
    # is_bizpartner = "Yes"

    list_display = ('user', 'is_Bizpartner')

    search_fields = ['user__username']
    actions =['download_csv']

    def is_Bizpartner(self, obj):
        if obj.is_bizpartner=="1":
            is_Bizpartner = "yes "
            return is_Bizpartner
        elif obj.is_bizpartner=="0":
            is_Bizpartner="No"
            return is_Bizpartner
   

    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        
        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'w+')
        writer = csv.writer(f)
        writer.writerow(['id','user', 'is_bizpartner'])

        for s in queryset:
            writer.writerow([s.id, s.user, s.is_bizpartner])

        f.close()

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'r+')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=vrification-info.csv'
        return response

    download_csv.short_description = "export csv"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name',
            'email',
            'number',
            'subject',
            'message',
            'created_on')
    actions =['download_csv']
    search_fields = ['name']

    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'w+')
        writer = csv.writer(f)
        writer.writerow(['id','name','email','number','subject','message', 'created_on'])

        for s in queryset:
            writer.writerow([s.id, s.name, s.email, s.number, s.subject, s.message])

        f.close()

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'r+')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=inbox-info.csv'
        return response

    download_csv.short_description = "export csv"

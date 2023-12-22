from django.utils.http import urlsafe_base64_decode
# Change this line
# from django.utils.encoding import force_text

# to
from django.utils.encoding import force_str

from django.contrib.auth import login
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View, UpdateView
from user.forms import SignUpForm, ProfileForm, BusinessForm, BankInfoForm, LoanForm, AdditionalAssetsForm, \
    AdditionalLiabilitiesForm, ProfileForms, ContactForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from user.tokens import account_activation_token
from user.models import Referral, Business, Verification, BankInfo, Loan, Profile, Additional_assets, \
    Additional_liabilities, Contact, Underprocess_loans
from django_tables2 import SingleTableView
from .tables import ReferralTable
from django import forms
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
import requests
from .utils import render_to_pdf


# ===== Landing page views ====#


class home(View):
    def get(self, request):
        user = self.request.user
        if request.user.is_anonymous:
            val = 0
        else:
            verify = Verification.objects.filter(user=user)
            val = verify.values('is_bizpartner')
            if len(val) != 0:
                val = val[0]['is_bizpartner']
            else:
                val = 0

        return render(request, 'home/index.html', {'val': val})


def agreement(request):
    return render(request, 'commons/agreement.html', {})


class loan(SingleTableView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'dashboard/loan.html'

    def get(self, request, *args, **kwargs):
        template_name = 'dashboard/loan.html'
        user = self.request.user
        table = Loan.objects.all().filter(user=user)

        return render(request, template_name, {'table': table})


def about(request):
    return render(request, 'home/about.html')


def home_loan(request):
    return render(request, 'home/home_loan.html')


def ts(request):
    return render(request, 'home/Terms.html', {})


def PrivacyPolicy(request):
    return render(request, 'home/PrivacyPolicy.html', {})


# ===== Dashboard views ====#


class dashboard(View):
    login_url = '/login/'
    template_name = 'dashboard/index.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user

        if request.user.is_anonymous:
            val = 0
            return render(request, self.template_name)
        else:
            pr = Profile.objects.get(user=user)
            if pr.kyc_done:
                verify = Verification.objects.filter(user=user)
                val = verify.values('is_bizpartner')
                if len(val) != 0:
                    val = val[0]['is_bizpartner']
                else:
                    val = 0
                return render(request, self.template_name)
            else:
                return redirect('kycForm')


def KycForm(request):
    user = request.user
    try:
        r = Referral.objects.get(user=user)
    except Referral.DoesNotExit:
        r = None
    if r is None:
        return HttpResponse('Form for user who came by google search')
    else:
        u = r.referred_by
        pr = Profile.objects.get(user=u)
        if pr.is_agent:
            return HttpResponse('Form for user who came by refer of agent')
        if pr.is_bizpartner:
            return HttpResponse('Form for user who came by refer of customer')


class SignUpView(View):
    form_class = SignUpForm

    template_name = 'account/signup.html'

    @classmethod
    def ref(self, request, uid, *args, **kwargs):
        form = self.form_class()
        # link = request.GET.get('ref=', None)
        return render(request, self.template_name, {'form': form, 'uid': uid})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(User.objects.all())
        return render(request, self.template_name, {'form': form})

    def post(self, request, uid, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            emaill = form.cleaned_data['email']
            if User.objects.filter(email=emaill).exists():

                return HttpResponse('User with same email already exists, Please try again with different Username!!')
            else:
                user = form.save(commit=False)
                user.is_active = False  # Deactivate account till it is confirmed
                user.save()
                u = User.objects.get(id=uid)
                pr = Profile.objects.get(user=u)
                if pr.is_agent:
                    comm = 0
                    comm_status = "done"
                    reff = Referral(referred_by_id=uid, user_id=user.pk, commissions=comm,
                                    commission_status=comm_status)
                else:
                    reff = Referral(referred_by_id=uid, user_id=user.pk)
                reff.save()
                ph = list(form.cleaned_data['phnumber'])
                if ph[0] is "+":
                    phnumber = ''.join(map(str, ph))
                else:
                    if ph[0] is "0":
                        ph.pop(0)
                        ph.insert(0, "1")
                        ph.insert(0, "6")
                        ph.insert(0, "+")
                        phnumber = ''.join(map(str, ph))
                    else:
                        ph.insert(0, "1")
                        ph.insert(0, "6")
                        ph.insert(0, "+")
                        phnumber = ''.join(map(str, ph))
                new_profile = Profile(
                    user=user, phnumber=phnumber, email_confirmed=False)
                new_profile.save()
                current_site = get_current_site(request)
                subject = 'Activate Your FinTop Account'
                message = render_to_string('emails/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
                messages.success(
                    request, ('Please check your mail for complete registration.'))
                # return redirect('login')
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True

            pr = Profile.objects.get(user=user)
            pr.email_confirmed = True
            pr.save()
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('dashboard_home')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('dashboard_home')


# Edit Profile View
# @login_required(login_url='/login/')


class ProfileViews(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    form2 = BusinessForm
    success_url = reverse_lazy('home')
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'dashboard/my-profile.html'


@login_required(login_url='/login/')
def ProfileView(request, pk):
    profile = Profile.objects.get(user=User.objects.get(id=pk))
    if request.method == 'POST':
        form1 = ProfileForm(request.POST, instance=User.objects.get(id=pk))
        if form1.is_valid():

            form1.save()
            form2 = ProfileForms(request.POST, instance=profile)

            if form2.is_valid():
                ph = list(form2.cleaned_data['phnumber'])
                if ph[0] is "+":
                    phnumber = ''.join(map(str, ph))
                else:
                    if ph[0] is "0":
                        ph.pop(0)
                        ph.insert(0, "1")
                        ph.insert(0, "6")
                        ph.insert(0, "+")
                        phnumber = ''.join(map(str, ph))
                    else:
                        ph.insert(0, "1")
                        ph.insert(0, "6")
                        ph.insert(0, "+")
                        phnumber = ''.join(map(str, ph))

                form2.save()
                profile.phnumber = phnumber
                profile.save()

    form = ProfileForm(instance=User.objects.get(id=pk))
    form2 = ProfileForms(instance=profile)
    return render(request, 'dashboard/my-profile.html', {"form": form, 'form2': form2})


def prf(request):
    #     query_results = Referral.objects.all()
    return render(request, 'commons/profile1.html', {})


def success(request):
    return render(request, 'dashboard/success.html', {})


class SignUpVieww(View):
    form_class = SignUpForm

    template_name = 'account/signup.html'

    @classmethod
    def ref(self, request, uid, *args, **kwargs):
        form = self.form_class()
        # link = request.GET.get('ref=', None)
        return render(request, self.template_name, {'form': form, 'uid': uid})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():

            emaill = form.cleaned_data['email']
            if User.objects.filter(email=emaill).exists():

                return HttpResponse('User with same email already exists, Please try again with different Username!!')
            else:

                user = form.save(commit=False)
                ph = list(form.cleaned_data['phnumber'])
                if ph[0] is "+":
                    phnumber = ''.join(map(str, ph))
                else:
                    if ph[0] is "0":
                        ph.pop(0)
                        ph.insert(0, "1")
                        ph.insert(0, "6")
                        ph.insert(0, "+")
                        phnumber = ''.join(map(str, ph))
                    else:
                        ph.insert(0, "1")
                        ph.insert(0, "6")
                        ph.insert(0, "+")
                        phnumber = ''.join(map(str, ph))
                user.is_active = False  # Deactivate account till it is confirmed
                user.save()
                new_profile = Profile(
                    user=user, phnumber=phnumber, email_confirmed=False)
                new_profile.save()
                current_site = get_current_site(request)
                subject = 'Activate Your FinTop Account'
                message = render_to_string('emails/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)

                messages.success(
                    request, ('Please check your mail for complete registration.'))

                # return redirect('login')

                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})


class write_pdf_view(LoginRequiredMixin, View):
    model = Business
    form_class = BusinessForm
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'dashboard/business.html'

    # def write_pdf_vieww(request):

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        template_path = 'commons/agreement.html'
        form = self.form_class(request.POST)
        user = self.request.user

        #

        if form.is_valid():
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            if Business.objects.filter(user=user).exists():

                return messages.success(request, 'You are already a BizPartner !!')
            else:
                bn = form.save(commit=False)

                bn.user = user
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'filename="agreement.pdf"'
                fname = request.POST["fullname"]
                sign = request.POST["signature"]
                bn = Business(user=user, fullname=fname, signature=sign)

                bn.save()
                bn = Business.objects.get(user=user)
                bn.generate_obj_pdf()
                fil = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), f"agreement/{user.username}.pdf"),
                           'w+b')

                context = {'fname': fname, 'sign': sign, 'ip': ip}
                template = get_template(template_path)
                html = template.render(context)
                pisa_status = pisa.CreatePDF(html, dest=response)
                pisa_status = pisa.CreatePDF(html, dest=fil)
                fil.close()
                fil = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), f"agreement/{user.username}.pdf"),
                           'r+')
                urll = (os.path.realpath(fil.name))
                to_emails = [user.email, settings.EMAIL_HOST_USER]
                subject = "FinTop Agreement"

                email = EmailMessage(
                    subject, "Congratulations You are Successfully Registered as a BizPartner.",
                    from_email=settings.EMAIL_HOST_USER, to=to_emails)
                email.attach_file(urll)

                email.send()
                fil.close()
                if Verification.objects.filter(user=user, is_bizpartner=1).exists():
                    return render(request, 'dashboard/success.html', {'status': 1})
                else:
                    Verification.objects.create(user=user, is_bizpartner=1)
                return render(request, 'dashboard/success.html', {'status': 1})


class ReferralListView(SingleTableView):
    model = Referral
    table_class = ReferralTable
    model = BankInfo
    form_class = BankInfoForm
    template_name = 'dashboard/ref.html'

    def get(self, request):
        user = self.request.user
        if request.user.is_anonymous:
            val = 0
        else:
            verify = Verification.objects.filter(user=user)
            val = verify.values('is_bizpartner')
            if len(val) != 0:
                val = val[0]['is_bizpartner']
            else:
                val = 0
        try:
            formdetails = BankInfo.objects.get(user_id=self.request.user)
        except BankInfo.DoesNotExist:
            formdetails = None

        form = BankInfoForm(instance=formdetails)
        contextt = {
            'form': form,
            'formdetails': formdetails
        }

        table = Referral.objects.all().filter(referred_by=user)
        return render(request, 'dashboard/comingsoon.html',
                      {'val': val, 'table': table, 'form': form, 'formdetails': formdetails})

    def post(self, request, *args, **kwargs):
        template_path = 'dashboard/ref.html'

        try:
            formdetails = BankInfo.objects.get(user_id=self.request.user)
            form = self.form_class(request.POST, instance=formdetails)
        except BankInfo.DoesNotExist:
            form = self.form_class(request.POST)
        user = self.request.user
        if form.is_valid():
            bn = form.save(commit=False)
            bn.user_id = user
            bn.save()

        return render(request, template_path, {'form': form})


class bank(View):
    model = BankInfo
    form_class = BankInfoForm
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'dashboard/bank.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        user = self.request.user
        if request.user.is_anonymous:
            val = 0
        else:
            verify = Verification.objects.filter(user=user)
            val = verify.values('is_bizpartner')
            if len(val) != 0:
                val = val[0]['is_bizpartner']
            else:
                val = 0
        return render(request, self.template_name, {'form': form, 'val': val})

    def post(self, request, *args, **kwargs):
        template_path = 'dashboard/bank.html'
        form = self.form_class(request.POST)
        user = self.request.user

        if form.is_valid():
            bn = form.save(commit=False)
            bn.user_id = user
            bn.save()

        return render(request, 'dashboard/bank.html', {'form': form})


class applyloan(View):
    model = Loan
    form_class = LoanForm
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'dashboard/applyloan.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        user = self.request.user

        return render(request, self.template_name,
                      {'loan': LoanForm, 'asset': AdditionalAssetsForm, 'liability': AdditionalLiabilitiesForm})

    def post(self, request, *args, **kwargs):
        template_path = 'dashboard/loan.html'
        form = self.form_class(request.POST)
        user = self.request.user

        if form.is_valid():

            bn = form.save(commit=False)
            bn.user_id = user.pk

            bn.save()

            td = request.POST.get('td', None)
            share = request.POST.get('share', None)
            mf = request.POST.get('mf', None)
            gifts = request.POST.get('gifts', None)

            liabilitys = request.POST.get('liability_loan', None)
            print("liabilitys", liabilitys)
            if td:
                td_description = request.POST['td_description']
                td_total = request.POST['td_total_value']
                a_a = Additional_assets(
                    loan=bn, types="Term Deposit", description=td_description, total_value=td_total)
                a_a.save()
            if share:
                td_description = request.POST['share_description']
                td_total = request.POST['share_total_value']
                a_a = Additional_assets(
                    loan=bn, types="Shares", description=td_description, total_value=td_total)
                a_a.save()
            if mf:
                td_description = request.POST['mf_description']
                td_total = request.POST['mf_total_value']
                a_a = Additional_assets(
                    loan=bn, types="Managed Funds", description=td_description, total_value=td_total)
                a_a.save()

            if gifts:
                td_description = request.POST['gift_description']
                td_total = request.POST['gift_total_value']
                a_a = Additional_assets(
                    loan=bn, types="Gifts", description=td_description, total_value=td_total)
                a_a.save()
            if liabilitys != 'No':
                get_type = request.POST['types']
                get_owned = request.POST['owned']
                get_description = request.POST['description']
                add_liabilities = Additional_liabilities(
                    loan=bn, types=get_type, owned=get_owned, description=get_description)
                add_liabilities.save()
            print('===>', td)
            td_total_value = request.POST['td_total_value']
            r = Referral.objects.get(user=user)
            pr = r.referred_by
            if pr.is_agent:
                Underprocess_loans.objects.create(loan_id=bn.pk, agent=pr.pk).save()
            # AdditionalAssets()
        # table = Loan.objects.all().filter(user=user)
        # return render(request, 'dashboard/loan.html', {'loan':LoanForm, 'asset': AdditionalAssetsForm, 'liability': AdditionalLiabilitiesForm, 'table': table})
        return redirect('loan')


class contact(View):
    model = Contact
    form_class = ContactForm
    template_name = 'home/contact_us.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            #         data = {}
            #         secret_key = settings.RECAPTCHA_SECRET_KEY

            # # captcha verification
            #         data = {
            #             'response': data.get('g-recaptcha-response'),
            #             'secret': secret_key
            #         }
            #         resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            #         result_json = resp.json()
            #     if not result_json.get('success'):
            #         return HttpResponseRedirect(reverse('contact_us'))
            #     else :
            bn = form.save(commit=False)
            # to_emails =  [settings.EMAIL_HOST_USER]
            # message = [request.POST["email"], request.POST["message"]]
            # subject = request.POST["subject"]
            # email = EmailMessage(
            #     subject, message ,  from_email=settings.EMAIL_HOST_USER, to=to_emails)
            # email.encoding = 'utf-8'
            # email.send()
            ph = list(form.cleaned_data['number'])
            if ph[0] is "+":
                phnumber = ''.join(map(str, ph))
            else:
                if ph[0] is "0":
                    ph.pop(0)
                    ph.insert(0, "1")
                    ph.insert(0, "6")
                    ph.insert(0, "+")
                    phnumber = ''.join(map(str, ph))
                else:
                    ph.insert(0, "1")
                    ph.insert(0, "6")
                    ph.insert(0, "+")
                    phnumber = ''.join(map(str, ph))

            bn.save(number=phnumber)

        return HttpResponseRedirect(reverse('contact_us'))

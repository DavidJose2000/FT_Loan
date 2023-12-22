from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.views.generic import View, UpdateView
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from user.tokens import account_activation_token
from user.models import Referral, Profile
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
# Change this line
# from django.utils.encoding import force_text

# to
from django.utils.encoding import force_str

from django.contrib.auth import login, authenticate


# Create your views here.

class SignUpVieww(View):
    form_class = SignUpForm

    template_name = 'account/signup_agent.html'

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


class SignUpView(View):
    form_class = SignUpForm

    template_name = 'account/signup_agent.html'

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
                user.is_agent = True
                user.save()

                comm = 0
                comm_status = "done"
                reff = Referral(referred_by_id=uid, user_id=user.pk, commissions=comm,
                                commission_status=comm_status)

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
            return HttpResponse('Your account have been confirmed.')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            # return redirect('dashboard_home')
            return HttpResponse('The confirmation link was invalid, possibly because it has already been used.')


def login_agent(request):
    pr = Profile.objects.get(user=request.user)
    if request.user.is_authenticated and pr.is_agent:
        print(request.user)
        return redirect('jobseeker:jobseeker_home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('pass')

            # print(username)
            # print(password)
            user = authenticate(request, username=username, password=password)

            if user is not None:
                pr = Profile.objects.get(user=user)
                if pr.is_agent:
                    login(request, user)
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        return redirect('agent:agent_home')
                else:
                    messages.info(request, 'This Agent Login')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}

        return render(request, 'account/login_agent.html', context)


def agent_dashboard(request):
    user = request.user
    pr = Profile.objects.get(user=user)
    if pr.kyc_done:
        return HttpResponse('hello world')
    else:
        return redirect('kycForm')


def KycForm(request):
    return HttpResponse('kycForm for agent ')

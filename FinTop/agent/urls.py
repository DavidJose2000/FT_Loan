from django.urls import include, path
from .views import SignUpView, SignUpVieww, login_agent, agent_dashboard, KycForm
from . import views
from django.contrib.auth import views as auth_views  # import this

app_name = 'agent'
urlpatterns = [
    path('signup', SignUpVieww.as_view(), name='signup'),
    path('signup/ref=<uid>', SignUpView.as_view(), name='ref'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="account/password_reset_confirm.html"), name='password_reset_confirm'),
    path('account/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('login/', login_agent, name='login_agent'),
    path('/', agent_dashboard, name='agent_home'),
    path('kyc/', KycForm, name='kyc'),
]

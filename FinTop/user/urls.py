from django.urls import include, path
from user.views import SignUpView, ProfileView, ActivateAccount, ReferralListView, SignUpVieww, ts, PrivacyPolicy, write_pdf_view, loan, prf, bank, success, dashboard, agreement, applyloan, contact
from . import views
from django.contrib.auth import views as auth_views  # import this
urlpatterns = [
    ##=== home routes ===##

    path('about-us', views.about, name='about'),
    path('contact-us', contact.as_view(), name='contact_us'),
    path('home-loan', views.home_loan, name='home_loan'),
    path('terms-and-conditions', views.ts, name='Terms'),
    path('privacy-policy', views.PrivacyPolicy, name='PrivacyPolicy'),
    path('agreement', views.agreement, name='agreement'),

    ##=== account routes ===##

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

    ##=== dashboard routes ===##

    path('dashboard/', include([
        path('', dashboard.as_view(), name='dashboard_home'),

        path('ref', ReferralListView.as_view(), name='referral'),

        path('profile/<int:pk>/', ProfileView,
             name='profile'),  # here I changed

        path('activate/<uidb64>/<token>/',
             ActivateAccount.as_view(), name='activate'),

        path('Business', write_pdf_view.as_view(), name='Business'),

        path('loan', loan.as_view(), name='loan'),

        path('biz/<int:pk>', ProfileView, name='biz'),

        path('agreement', views.agreement, name='agreement'), 

        # path('profile', views.prf, name='profile1'),

        path('bank', bank.as_view(), name='bank'),

        path('success', views.success, name='success'),
        path('applyloan', applyloan.as_view(), name='applyloan'),
    ])),
]

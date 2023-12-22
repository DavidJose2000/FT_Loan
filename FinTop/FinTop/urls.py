"""django_user URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views

from django.views.generic import TemplateView

from user import urls as core_urls
from agent import urls as a_urls
from user.views import home
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include(core_urls)),
    path('agent/', include(core_urls)),
    re_path(r'^static/(?:.*)$', serve,
            {'document_root': settings.STATIC_ROOT, }),
    # re_path(r'^media/(?:.*)$', serve,
    #         {'document_root': settings.MEDIA_ROOT, }),
    
    
    
    # Login and Logout
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True,
                                               template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Main Page
    path('', home.as_view(), name='home'),

    # Change Password
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='account/change-password.html',
            success_url='/'
        ),
        name='change_password'
    ),

    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='account/password-reset/password_reset.html',
             subject_template_name='account/password-reset/password_reset_subject.txt',
             email_template_name='account/password-reset/password_reset_email.html',
             success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password_reset_complete.html'
         ),
         name='password_reset_complete'),
  
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)


admin.sites.AdminSite.site_header = 'FINTOP Admin Panel'
admin.sites.AdminSite.site_title = 'FINTOP Admin'
admin.sites.AdminSite.index_title = 'Tables'
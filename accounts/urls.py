from django.urls import re_path, include

from accounts import views

app_name = 'accouts'

urlpatterns = [
    re_path(r'^upload/$', views.FileUploadAPI.as_view()),

    re_path(r'^driver-register/$', views.DriverRegisterAPI.as_view(),),
    re_path(r'^driver-login/$', views.DriverLoginAPI.as_view(),),
    re_path(r'^driver-profile/$', views.DriverProfileAPI.as_view()),
    re_path(r'^^(?P<pk>\d+)/get-driver-profile/$', views.GetDriverProfileAPI.as_view()),
    re_path(r'^driver-reset-password/$', views.DriverResetPasswordAPI.as_view()),

    re_path(r'^customer-register/$', views.CustomerRegisterAPI.as_view(),),
    re_path(r'^customer-otp-verify/$', views.CustomerOtpVerifyLoginAPI.as_view(),),
    re_path(r'^customer-profile/$', views.CustomerProfileAPI.as_view()),
    re_path(r'^customer-login-with-phone/$',views.LoginCustomerwithPhoneNumberApi.as_view()),
    
    
    # re_path(r'^profile/(?P<pk>\d+)/$', views.DriverProfileAPI.as_view())
]
from django.urls import re_path, include, path

from cab_booking_api import views

app_name = 'cab_booking_api'

urlpatterns = [
    path('cab-class-price-list/', views.CabClassPriceList.as_view(),),
    path('valide-coupon-code-list/', views.ValideCouponCodeList.as_view(),),
    path('apply-coupon/', views.ApplyCouponView.as_view(), name='apply-coupon'),
    path('message-support/', views.MessageSupportListCreateView.as_view(), name='message-support-list'),
    path('customer-support/', views.CustomerSupportAPIView.as_view(), name='customer-support-api'),
]
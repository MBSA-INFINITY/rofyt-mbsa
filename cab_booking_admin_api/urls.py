from django.urls import re_path, include, path

from cab_booking_admin_api import views

app_name = 'cab_booking_admin_api'

urlpatterns = [
    path('drivers/', views.DriverListCreateAPIView.as_view(),),
    path('drivers/<int:pk>/', views.DriverDetailsView.as_view(),),
    path('passengers/', views.PassengerListView.as_view(),),
    path('passengers/<int:pk>/', views.PassengerDetailsView.as_view(),),
    # Trip urls
    path('active-trip/', views.ActiveTripListView.as_view(),),
    path('booked-trip/', views.BookedTripListView.as_view(),),
    path('completed-trip/', views.CompletedTripListView.as_view(),),
    # price urls 
    path('price-settings/', views.CabBookingPriceSettingList.as_view(), name='cab-booking-price-settings-list'),
    path('price-settings/<int:pk>/', views.CabBookingPriceSettingDetail.as_view(), name='cab-booking-price-settings-detail'),

    path('vehicles/', views.VehicleListCreateAPIView.as_view(),),
    path('vehicles/<int:pk>/', views.VehicleUpdateDestroyAPIView.as_view(), name='vehicle-update'),
    path('coupon-code-setting/', views.CabBookingCouponCodeSettingListCreateAPIView.as_view(), name='coupon-code-setting-list'),
    path('coupon-code-setting/<int:pk>/', views.CabBookingCouponCodeSettingRetrieveUpdateDestroyAPIView.as_view(), name='coupon-code-setting-detail'),
    path('support-message-list/', views.MessageSupportListView.as_view(), name="support-message-list" ),
    path('customer-support-message-list/', views.CutomerSupportListView.as_view(), name="cutomer-support-message-list" ),
    
]
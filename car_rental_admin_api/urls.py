from django.urls import re_path, include, path

from car_rental_admin_api import views

app_name = 'car_rental_admin_api'

urlpatterns = [
    path('price-settings/', views.VehicleRentePriceSettingList.as_view(), name='vehicle-rente-price-settings-list'),
    path('price-settings/<int:pk>/', views.VehicleRentePriceSettingDetail.as_view(), name='vehicle-rente-price-settings-detail'),
    path('city-setting/', views.CityListCreateAPIView.as_view(), name='city-setting-list'),
    path('city-settings/<int:pk>/', views.CityRetrieveUpdateDestroyAPIView.as_view(), name='city-setting-detail'),
    path('location-setting/', views.LocationsListCreateAPIView.as_view(), name='location-setting-list'),
    path('location-settings/<int:pk>/', views.LocationsRetrieveUpdateDestroyAPIView.as_view(), name='location-setting-detail'),
    path('coupon-code-setting/', views.CouponCodeSettingListCreateAPIView.as_view(), name='coupon-code-setting-list'),
    path('coupon-code-setting/<int:pk>/', views.CouponCodeSettingRetrieveUpdateDestroyAPIView.as_view(), name='coupon-code-setting-detail'),
    path('car-owner/', views.CarOwnerListView.as_view(), name='car-owner-list'),
]
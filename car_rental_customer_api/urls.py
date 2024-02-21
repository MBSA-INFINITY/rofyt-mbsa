from django.urls import re_path, include, path

from car_rental_customer_api import views

app_name = 'car_rental_customer_api'

urlpatterns = [
    path('active-city-list/',views.ActiveCityListAPIView.as_view(), name='active-city-list'),
    path('locations/by-city/<int:city_id>/',views.LocationByCityAPIView.as_view(), name='locations-by-city'),
    path('vehicles/',views.VehicleListForCutomerAPIView.as_view(),),
    path('vehicle/',views.VehicleDetailsForCutomerAPIView.as_view(),),
    path('car-booking/', views.CreateCarBooking.as_view(),),
    path('payment/', views.CarBookingPayment.as_view(),),
    re_path('razorpay/webhook/', views.razorpay_webhook, name='razorpay-webhook'),
    
   
]
from django.urls import re_path, include, path

from admin_api import views

app_name = 'admin_api'

urlpatterns = [
    path('login', views.AdminLoginView.as_view(),),
    path('logout', views.LogoutView.as_view(),),
    path('profile', views.AdminProfileView.as_view(),),
    path('profile/update',views.AdminProfileUpdateView.as_view()),
    
    # vehicle urls 
    path('vehicle-type', views.VehicleTypeView.as_view(),),
    path('vehicle-type/<int:pk>/', views.VehicleTypeDetailsView.as_view(),),
    path('vehicle-class', views.VehicleClassView.as_view(),),
    path('vehicle-class/<int:pk>/', views.VehicleClassDetailsView.as_view(),),
    path('vehicle-maker', views.VehicleMakerView.as_view(),),
    path('vehicle-maker/<int:pk>/', views.VehicleMakerDetailsVeiw.as_view(),),
    path('vehicle-model', views.VehicleModelView.as_view(),),
    path('vehicle-model/<int:pk>/', views.VehicleModelDetailsVeiw.as_view(),),
    path('vehicle-manufacturer/', views.VehicleManufacturerDetailsView.as_view(),),
   
]
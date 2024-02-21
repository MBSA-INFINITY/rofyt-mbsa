from django.urls import re_path, include, path

from car_owners_api import views

app_name = 'car_owners_api'

urlpatterns = [
    re_path(r'^register-car-owner/$', views.CarOwnerRegisterAPI.as_view(),),
    re_path(r'^verify-car-owner-phone-with-otp/$', views.VerifyCarOwnerPhoneWithOtpAPI.as_view(),),
    re_path(r'^send-otp-to-alternative-number/$', views.SendOTPtoAlternativeNumberApi.as_view(),),
    re_path(r'^save-car-owner-and-vehicle-detail/$', views.SaveCarOwnerAndVehicleDetailApi.as_view(),),
    re_path(r'^agree-tearm-and-condition/$', views.AgreeTearmAndConditionApi.as_view(),),
    re_path(r'^login-car-owner-with-phone-number/$', views.LoginCarOwnerwithPhoneNumberApi.as_view(),),
    re_path(r'^verify-login-phone-number-with-otp/$', views.VerifyLoginPhoneNumerApi.as_view(),),
    path('profile/<int:id>/', views.CarOwnerProfileApi.as_view(),),
    path('<int:user_id>/vehicles/', views.CarOwnerVehicleListApi.as_view(),),
    path('vehicle/<int:id>', views.CarOwnerVehicleDetialsApi.as_view(),),
    path('<int:user_id>/vehicle/', views.CarOwnerVehicleCreateApi.as_view(),),
    # re_path(r'^send-otp/$', views.SendOtpApi.as_view(),),
    # re_path(r'^user-sign-in/$', views.UserSignInApi.as_view(),)
    # re_path(r'^profile/(?P<pk>\d+)/$', views.Ref.as_view())
    re_path(r'^save-car-owner-details/$', views.SaveCarOwnerDetailsApi.as_view(),),
    re_path(r'^save-car-owner-vehicle-details/$', views.SaveCarOwnerVehicleDetailsApi.as_view(),),
    re_path(r'^save-car-owner-vehicle-certificated/$', views.SaveCarOwnerVehicleCertificatedApi.as_view(),),
    re_path(r'^carowner-profile/$', views.CarOwnerProfileAndUpdateAPI.as_view()),
    re_path(r'^get-carowner-profile/$', views.GetCarOwnerProfileAPI.as_view()),
    path('change-vehicle-status/<int:vehicle_id>/',views.VehicleActiveStatusView.as_view()),
    path('get-carbooking-status/',views.CarBookingRequestView.as_view()),
    path('change-carbooking-status/<int:carbooking_id>/',views.AcceptCarBookingView.as_view()),
    path('save-images-before-delivery/<int:carbooking_id>/',views.SaveImagesBeforeDeliveryView.as_view()),
    path('save-images-after-delivery/<int:carbooking_id>/',views.SaveImagesAfterDeliveryView.as_view()),
    path('completed-carbooking-list/',views.CarBookingCompletedView.as_view()),
    path('last-carbooking-status/<int:vehicle_id>/',views.LastCarBookingView.as_view()),
    re_path(r'^create-accident-support/$', views.AccidentSupportView.as_view(),),
    path('upload-aadhar/<int:user_id>/', views.CarOwnerUpdateAadharApi.as_view(),),
    path('upload-insurance/<int:vehicle_id>/', views.CarOwnerUpdateInsuranceApi.as_view(),),
    path('vehicle-trip-count/<int:user_id>/',views.CarOwnerProfileDetailsApi.as_view(),),
    path('upload-profile-photo/<int:user_id>/', views.CarOwnerUpdateProfilePictureApi.as_view(),),
    path('upload-documents/<int:user_id>/', views.CarOwnerUpdateDocumentsApi.as_view(),),
]
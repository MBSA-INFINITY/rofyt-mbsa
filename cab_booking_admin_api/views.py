from django.shortcuts import render
import pyotp
from django.conf import settings
from accounts import serializers
from rest_framework import views , permissions, status, generics
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from utility.otp import send_otp
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from accounts.models import *
from accounts.serializers import CustomerProfileSerializer
from trips.models import Trip
from cabs.models import *
from cab_booking_admin_api.models import *
from cab_booking_admin_api.serializers import *
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from cab_booking_api.models import Message_Support, Customer_Suppport
from cab_booking_api.serializers import MessageSupportSerializer, CustomerSupportSerializer

class CustomPagination(PageNumberPagination):
    page_size = 10  # Set your desired page size
    page_size_query_param = 'page_size'
    max_page_size = 100

# Create your views here.
class DriverListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    pagination_class = CustomPagination
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', None)
        first_name=request.data.get('first_name', None)
        last_name=request.data.get('last_name', None)
        email=request.data.get('email', None)
        full_address=request.data.get('full_address', None)
        pincode=request.data.get('pincode', None)
        state=request.data.get('state', None)
        city=request.data.get('city', None)
        house_or_building=request.data.get('city', None)
        road_or_area=request.data.get('road_or_area',None)
        alternate_number=request.data.get('alternate_number',None)
        aadhar_number=request.data.get('aadhar_number')
        aadhar_upload_front=request.data.get('aadhar_upload_front',None)
        aadhar_upload_back=request.data.get('aadhar_upload_back', None)
        pan_number=request.data.get('pan_number', None)
        pan_upload=request.data.get('pan_upload',None)
        license_number=request.data.get('license_number',None)
        license_upload_front=request.data.get('license_upload_front',None)
        license_upload_back=request.data.get('license_upload_back',None)
        photo_upload=request.data.get('photo_upload',None)
        if not phone:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            driver = Driver.objects.get(phone=phone)
            if first_name:
                driver.first_name=first_name
            if last_name:
                driver.last_name=last_name
            if email:
                driver.email=email
            if full_address:
                driver.full_address=full_address
            if pincode:
                driver.pincode=pincode
            if state:
                driver.state=state
            if city:
                driver.city=city
            if house_or_building:
                driver.house_or_building=house_or_building
            if road_or_area:
                driver.road_or_area=road_or_area
            if alternate_number:
                driver.alternate_number=alternate_number
            if aadhar_number:
                driver.aadhar_number=aadhar_number
            if aadhar_upload_front:
                driver.aadhar_upload_front=aadhar_upload_front
            if aadhar_upload_back:
                driver.aadhar_upload_back=aadhar_upload_back
            if pan_number:
                driver.pan_number=pan_number
            if pan_upload:
                driver.pan_upload=pan_upload
            if license_number:
                driver.license_number=license_number
            if license_upload_front:
                driver.license_upload_front=license_upload_front
            if license_upload_back:
                driver.license_upload_back=license_upload_back
            if photo_upload:
                driver.photo_upload=photo_upload
            driver.terms_policy=True
            driver.myride_insurance=True
            driver.save()
            serializer = DriverListSerializer(driver)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Driver.DoesNotExist:
            return Response({'error': 'Driver not found.'}, status=status.HTTP_404_NOT_FOUND)
    def get(self, request, *args, **kwargs):
        driver = Driver.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(driver, request)
        serializer =DriverListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

# class DriverListView(generics.ListAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated & IsAdminUser]
#     parser_classes = (MultiPartParser,FormParser,JSONParser)
#     queryset = User.objects.filter(type="DRIVER", is_driver=True)  # Adjust the queryset based on your actual model structure
#     serializer_class = DriverListSerializer
#     pagination_class = CustomPagination

class DriverDetailsView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    queryset = User.objects.filter(type="DRIVER", is_driver=True)  # Adjust the queryset based on your actual model structure
    serializer_class = DriverListSerializer
  


class PassengerListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    queryset = User.objects.filter(Q(is_customer=1) & Q(type="CUSTOMER")) # Adjust the queryset based on your actual model structure
    serializer_class = PassengersListSerializer
    pagination_class = CustomPagination

class PassengerDetailsView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    queryset = User.objects.filter(Q(is_customer=1) & Q(type="CUSTOMER")) # Adjust the queryset based on your actual model structure
    serializer_class = PassengersListSerializer


#  Trip API 
class ActiveTripListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset=Trip.objects.filter(Q(status="ACCEPTED") | Q(status="ON_TRIP"))
    serializer_class = TripListSerializer
    pagination_class = CustomPagination

class BookedTripListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset=Trip.objects.filter(status="BOOKED")
    serializer_class = TripListSerializer
    pagination_class = CustomPagination

class CompletedTripListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset=Trip.objects.filter(status="COMPLETED")
    serializer_class = TripListSerializer
    pagination_class = CustomPagination
    
# Price Settings 
class CabBookingPriceSettingList(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = CabBookingPriceSetting.objects.all()
    serializer_class = CabBookingPriceSettingSerializer

class CabBookingPriceSettingDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = CabBookingPriceSetting.objects.all()
    serializer_class = CabBookingPriceSettingSerializer


class VehicleListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    pagination_class = CustomPagination
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', None)
        number_plate=request.data.get('number_plate')
        insurance_certiifcate=request.data.get('insurance_certiifcate')
        registration_certiifcate=request.data.get('registration_certiifcate')
        mot_certiifcate=request.data.get('mot_certiifcate')
        addtional_document=request.data.get('addtional_document')
        insurance_certiifcate=request.data.get('insurance_certiifcate')

        front=request.data.get('front')
        back=request.data.get('back')
        left=request.data.get('left')
        right=request.data.get('right')
        inside_driver_seat=request.data.get('inside_driver_seat')
        inside_passanger_seat=request.data.get('inside_passanger_seat')
        front_head_light=request.data.get('front_head_light')
        back_head_light=request.data.get('back_head_light')
        sound=request.data.get('sound')
        pollution=request.data.get('pollution')
        cab_type_id=request.data.get('cab_type_id')
        # cab_class_id=request.data.get('cab_class_id')
        maker_id=request.data.get('maker_id')
        model_id=request.data.get('model_id')
        if not phone:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            driver = Driver.objects.get(phone=phone)
        except Driver.DoesNotExist:
            return Response({'error': 'Driver not found.'}, status=status.HTTP_404_NOT_FOUND)
        if not CabType.objects.filter(id=cab_type_id).exists():
            return Response({'error': 'Cab type not found.'}, status=status.HTTP_404_NOT_FOUND)
        cab_type=CabType.objects.get(id=cab_type_id)
        if not VehicleMaker.objects.filter(id=maker_id).exists():
            return Response({'error': 'Vehicle Maker not found.'}, status=status.HTTP_404_NOT_FOUND)
        maker=VehicleMaker.objects.get(id=maker_id)
        if not VehicleModel.objects.filter(Q(id=model_id) and Q(maker_id=maker_id)).exists():
            return Response({'error': 'Vehicle Model not found.'}, status=status.HTTP_404_NOT_FOUND)
        model=VehicleModel.objects.get(id=model_id)
        if not CabClass.objects.filter(id=model.cab_class.id).exists():
            return Response({'error': 'Cab class not found.'}, status=status.HTTP_404_NOT_FOUND)
        cab_class=CabClass.objects.get(id=model.cab_class.id)
        vehicle=Vehicle.objects.create(driver=driver, number_plate=number_plate, insurance_certiifcate=insurance_certiifcate,
                                       registration_certiifcate=registration_certiifcate,mot_certiifcate=mot_certiifcate, addtional_document=addtional_document,
                                       front=front, back=back, right=right, left=left, inside_driver_seat=inside_driver_seat, inside_passanger_seat=inside_passanger_seat,
                                       front_head_light=front_head_light, back_head_light=back_head_light, sound=sound, pollution=pollution,
                                       maker=maker, model=model, cab_type=cab_type, cab_class=cab_class, is_active=True,is_approved=True)
      

        serializer = CabBookingVehicleSerializer(vehicle)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def get(self, request, *args, **kwargs):
        vehicle = Vehicle.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(vehicle, request)
        serializer =CabBookingVehicleSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
       

class VehicleUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = Vehicle.objects.all()
    serializer_class = CabBookingVehicleSerializer

class CabBookingCouponCodeSettingListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = CabBookingCouponCodeSetting.objects.all()
    serializer_class =  CabBookingCouponCodeSettingSerializer


class CabBookingCouponCodeSettingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = CabBookingCouponCodeSetting.objects.all()
    serializer_class =  CabBookingCouponCodeSettingSerializer


class MessageSupportListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset=Message_Support.objects.all().order_by('-created_at')
    serializer_class = MessageSupportSerializer
    pagination_class = CustomPagination


class CutomerSupportListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset=Customer_Suppport.objects.all().order_by('-created_at')
    serializer_class = MessageSupportSerializer
    pagination_class = CustomPagination



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
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.db.models import Q

from car_rental_admin_api.models import *
from car_rental_admin_api.serializers import *
from accounts.models import CarOwner
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
import json




class VehicleRentePriceSettingList(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = VehicleRentePriceSetting.objects.all()
    serializer_class = VehicleRentePriceSettingSerializer

class VehicleRentePriceSettingDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = VehicleRentePriceSetting.objects.all()
    serializer_class = VehicleRentePriceSettingSerializer


class CityListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = CitySetting.objects.all()
    serializer_class = CitySettingSerializer


class CityRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = CitySetting.objects.all()
    serializer_class = CitySettingSerializer

class LocationsListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = LocationsSetting.objects.all()
    serializer_class = LocationsSettingSerializer


class LocationsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = LocationsSetting.objects.all()
    serializer_class = LocationsSettingSerializer



class CouponCodeSettingListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = CouponCodeSetting.objects.all()
    serializer_class =  CouponCodeSettingSerializer


class CouponCodeSettingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = CouponCodeSetting.objects.all()
    serializer_class =  CouponCodeSettingSerializer


class CarOwnerListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CarOwnerDetailsSerializer
    def get_queryset(self):
        # Filter coupons that are not expired
        current_date = timezone.now().date()
        return CarOwner.objects.filter(is_active=True, is_carowner=True)

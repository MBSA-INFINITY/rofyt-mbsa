from django.shortcuts import render
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
# Create your views here.


class CabClassPriceList(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CabBookingPriceSetting.objects.all()
    serializer_class = CabBookingPriceSettingSerializer

class ValideCouponCodeList(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CabBookingCouponCodeSettingSerializer
    def get_queryset(self):
        # Filter coupons that are not expired
        current_date = timezone.now().date()
        return CabBookingCouponCodeSetting.objects.filter(expire_date__gte=current_date, is_active=True)

class ApplyCouponView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        coupon_code = request.data.get('coupon_code', '')
        try:
            customer=User.objects.get(id=request.user.id)
            if not Trip.objects.filter(customer=customer, applied_coupon=coupon_code).exists():
                coupon = CabBookingCouponCodeSetting.objects.get(coupon_code=coupon_code, expire_date__gte=timezone.now(), is_active=True)
            else:
                return Response({'error': 'The coupon code are expired for you.'}, status=status.HTTP_400_BAD_REQUEST)
        except CabBookingCouponCodeSetting.DoesNotExist:
            return Response({'error': 'Invalid coupon code or expired.'}, status=status.HTTP_400_BAD_REQUEST)
        # Perform your logic to apply the coupon, e.g., calculate discounted price
        # Return a response with applied coupon details
        serializer = CabBookingCouponCodeSettingSerializer(coupon)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class PassengerListView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    queryset = User.objects.filter(Q(is_customer=1) & Q(type="CUSTOMER")) # Adjust the queryset based on your actual model structure
    serializer_class = PassengersListSerializer

class MessageSupportListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        subject=request.data.get('subject', None)
        message=request.data.get('message', None)  #.order_by('-created_at')
        print(request.user.id, "request.user.id", subject, message, "request.user.id")
        user=User.objects.get(id=request.user.id)
        response=Message_Support.objects.create(user=user, subject=subject, message=message)
        serializer=MessageSupportSerializer(response)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def get(self, request):
        data=Message_Support.objects.filter(user=request.user.id).order_by('-created_at')
        serializer = MessageSupportSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerSupportAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Assuming you have the user associated with the request
        user = request.user
        # Combine user and request data to create a new Customer_Support instance
        data = {**request.data, 'cutomer': user.id}
        # Serialize the data
        serializer = CustomerSupportSerializer(data=data)
        if serializer.is_valid():
            # Save the instance
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        data=Customer_Suppport.objects.filter(cutomer=request.user.id).order_by('-created_at')
        serializer = MessageSupportSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

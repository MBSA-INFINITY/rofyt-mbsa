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
from car_owners_api.models import *
from cabs.models import *
from admin_api.serializers import *
from car_rental_admin_api.serializers import *
from car_rental_customer_api.serializers import *
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
import json

import googlemaps
import os
import requests
from django.db.models import Min, Max
import ast
from car_owners_api.models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


class ActiveCityListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = CitySetting.objects.filter(is_active=True)
    serializer_class = CitySettingSerializer


class LocationByCityAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LocationsSettingSerializer
    def get_queryset(self):
        city_id = self.kwargs['city_id']
        return LocationsSetting.objects.filter(city_id=city_id)


class VehicleListForCutomerAPIView(APIView):
    permission_classes = [permissions.AllowAny]
   
    def post(self, request):
        # Get pickup and drop locations from request parameters
        pickup_location = request.data.get('pickup_location')
        drop_location = request.data.get('drop_location')
        city=request.data.get('city')
        pickup_date=request.data.get('pickup_date')
        drop_date=request.data.get('drop_date')
        vehicle_type=request.data.get('vehicle_type')
        price_by=request.data.get('price_by')
        cab_class_id=request.data.get('cab_class_list', [])
        try:
            if cab_class_id:
                cab_class_list = ast.literal_eval(cab_class_id)
            else:
                cab_class_list=[]
        except Exception as e:
            cab_class_list=cab_class_id
        print(pickup_date)
        # Parse the string into a datetime object
        pickup_date_object = datetime.strptime(pickup_date, "%Y-%m-%d %H:%M:%S")
        drop_date_object = datetime.strptime(drop_date, "%Y-%m-%d %H:%M:%S")
        time_difference = drop_date_object - pickup_date_object
        hours_difference = time_difference.total_seconds() / 3600  # convert seconds to hours
        total_hours=round(hours_difference, 2)
        # # endpoint = os.getenv('GOOGLE_MAPS_GEOCODING_ENDPOINT')
        # # google_map_key = os.getenv('GOOGLE_MAPS_API_KEY')
        # endpoint='https://maps.googleapis.com/maps/api/geocode/json'
        # google_map_key="AIzaSyCYwHNeqOW-oeSSex-b-vqUyZb3vWcWxVA"
        # print(endpoint, "endpoint", google_map_key)
        # params1 = {
        #         'address':  pickup_location,
        #         'key': google_map_key,}
        # params2 = {
        #         'address':  drop_location,
        #         'key': google_map_key,}   
        # # Make the API request
        # response1 = requests.get(endpoint, params=params1) 
        # response2 = requests.get(endpoint, params=params2) 
        # # Parse the JSON response
        # data1 = response1.json()
        # data2 = response2.json()
        # if data1['status'] == 'OK':
        #     # Extract latitude and longitude
        #     pickup_coordinates = data1['results'][0]['geometry']['location'] 
        # else:
        #     print(f"Geocoding API error: {data1['status']}")
        #     return Response({'error': f"Geocoding API error: {data1['status']}"}, status=status.HTTP_400_BAD_REQUEST)
        
        # if data2['status']=="OK":
        #     # Extract latitude and longitude
        #     drop_coordinates = data1['results'][0]['geometry']['location'] 
        # else:
        #     print(f"Geocoding API error: {data2['status']}")
        #     return Response({'error': f"Geocoding API error: {data2['status']}"}, status=status.HTTP_400_BAD_REQUEST)
        bookings_within_date_range = Car_Booking.objects.filter(Q(pick_up_data_time__range=(pickup_date_object, drop_date_object)) | Q(drop_up_date_time__range=(pickup_date_object, drop_date_object)))
        # Extract the unique vehicle IDs from the filtered bookings
        vehicle_ids = bookings_within_date_range.values_list('vehicle_id', flat=True).distinct()
        print(vehicle_ids,"vehicle_ids")
        if vehicle_type=="Bike" :
            vehicle_type_ids=CabType.objects.filter(cab_type=vehicle_type).values_list('id', flat=True).distinct()
        elif vehicle_type=="Cab":
            vehicle_type_ids=CabType.objects.filter(cab_type="Cab").values_list('id', flat=True).distinct()
            vehicle_type_class=CabClass.objects.filter(cab_type_id__in=vehicle_type_ids)
            vehicle_class_serializer=SaveVehicleClassSerializer(vehicle_type_class, many=True)
        vehicles = (Car_Owner_Vehicle.objects.exclude(id__in=vehicle_ids).filter(user__city=city)).filter(vehicle_type_id__in=vehicle_type_ids, is_active=True)
        if cab_class_list:
            vehicles=vehicles.filter(vehicle_class_id__in=cab_class_list)
        if price_by == "Low to High":
            vehicles=vehicles.annotate(min_price=Min('vehicle_model__vehiclerentepricesetting__with_fuel_price'))
            vehicles=vehicles.order_by('min_price')
        elif price_by == "High to Low":
            vehicles=vehicles.annotate(max_price=Max('vehicle_model__vehiclerentepricesetting__with_fuel_price'))
            vehicles=vehicles.order_by('-max_price')
        else:
            vehicles=vehicles.annotate(min_price=Min('vehicle_model__vehiclerentepricesetting__with_fuel_price'))
            vehicles=vehicles.order_by('min_price')
        vehicles_serializer=VehicleListForCutomerSerializer(vehicles, many=True)
        fast_kms=int(5)*int(total_hours),
        second_kms= int(10)*int(total_hours),
        third_kms=int(20)*int(total_hours),
        response={
            "pickup_location":pickup_location,
            "drop_location":drop_location,
            "pickup_date":pickup_date,
            "drop_date":drop_date,
            "total_hours":total_hours,
            # "vehicle_class": vehicle_class_serializer.data,
            "vehicles":vehicles_serializer.data,
            "fast_kms":fast_kms,
            "second_kms":second_kms,
            "third_kms":third_kms,
        }
        
        return Response(response, status=status.HTTP_200_OK)


class VehicleDetailsForCutomerAPIView(APIView):
    permission_classes = [permissions.AllowAny]
   
    def post(self, request):
        vehicle_id = request.data.get('vehicle_id')
        price_type=request.data.get('price_type') #without_fuel_price
        kms_type=request.data.get('kms_type')
        total_hours=request.data.get('total_hours')
        vehicle=Car_Owner_Vehicle.objects.get(id=vehicle_id)
        vehicle_serializer=VehicleDetailsForCutomerSerializer(vehicle,context={"price_type": price_type,})
        if kms_type == "fast_kms":
            total_kms=int(5)*float(total_hours),
        elif kms_type == "second_kms":
            total_kms=int(10)*float(total_hours)
        elif kms_type == "third_kms":
            total_kms=int(20)*float(total_hours)
   
        response={
            "price_type":price_type,
            "kms_type":kms_type,
            "total_hours":total_hours,
            "vehicle":vehicle_serializer.data,
            "total_kms":total_kms,
            "delivery_charge":int(2000)
        }
        return Response(response, status=status.HTTP_200_OK)


class CreateCarBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        vehicle_id=request.data.get('vehicle_id')
        pickup_location = request.data.get('pickup_location')
        drop_location = request.data.get('drop_location')
        pickup_date=request.data.get('pickup_date')
        drop_date=request.data.get('drop_date')
        duration=request.data.get('duration')
        applied_coupon=request.data.get('applied_coupon', None)
        coupon_discount_amount=request.data.get('coupon_discount_amount', None)
        basic_price=request.data.get('basic_fare')
        delivery_charge=request.data.get('delivery_charge')
        tax_amount=request.data.get('tax_amount')
        payment_price=request.data.get('payment_price')
        if Car_Owner_Vehicle.objects.filter(id=vehicle_id).exists():
            vehicle=Car_Owner_Vehicle.objects.get(id=vehicle_id)
            car_owner_id=vehicle.user.id
            car_owner=User.objects.get(id=car_owner_id)
            customer=User.objects.get(id=request.user.id)
            if customer.first_name and customer.last_name and customer.email:
                if customer.license_upload_front and customer.license_upload_back:
                    carbooking=Car_Booking(car_owner=car_owner, customer=customer, vehicle=vehicle, pick_up_locations=pickup_location, drop_off_locations=drop_location, pick_up_data_time=pickup_date, drop_up_date_time=drop_date, booking_status='Pending', basic_price=basic_price, tax_amount=tax_amount, payment_price=payment_price, duration=duration).save()
                    if applied_coupon and coupon_discount_amount:
                        carbooking.applied_coupon=applied_coupon
                        carbooking.coupon_discount_amount=coupon_discount_amount
                        carbooking.save()
                    return Response({"car_booking_id": carbooking.id, "payment_price": carbooking.payment_price, 'vehicle_id':vehicle.id}, status=status.HTTP_201_CREATED)
                         
                else:
                    return Response({'message':f"Hello {customer['first_name'] + ' ' +customer['last_name']}, Please Upload you Driving Licence", "status":"UploadDrivingLicence"}, status=status.HTTP_200_OK)
            else:
                return Response({'message':"Dear Customer you profile Incomplete, please update your profile", "status":"UpdateProfile"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "Vehicle dose not exist"}, status=status.HTTP_400_BAD_REQUEST)

class CarBookingPayment(APIView):
    def post(self, request, *args, **kwargs):
        car_booking_id=request.data.get('car_booking_id')
        payment_price = request.data.get('payment_price')
        client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
        booking_amount = payment_price * 100  # Amount in paise
        booking_currency = 'INR'
        booking_receipt = f'booking_{car_booking_id}'
        params = {
        'amount': booking_amount,
        'currency': booking_currency,
        'receipt': booking_receipt,
        'payment_capture': 1  # Auto-capture payment
        }
        razorpay_order = client.order.create(params)
        razorpay_order_id = razorpay_order.get('id')
        car_booking=Car_Booking.objects.get(id=car_booking_id)
        car_booking.razorpay_order_id=razorpay_order_id
        car_booking.save()
        return Response({'razorpay_order_id': car_booking.razorpay_order_id}, status=status.HTTP_200_OK)



@csrf_exempt
@api_view(['POST'])
def razorpay_webhook(request):
    if request.method == 'POST':
        data = request.POST
        try:
            # Verify the webhook signature
            razorpay_client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
            rzp_res =razorpay_client.utility.verify_webhook_signature(
                data.get('razorpay_signature'),
                data.get('razorpay_order_id'),
                data.get('razorpay_payment_id'),
                request.body.decode('utf-8')
            )
            if rzp_res == True :
                # Update payment status in the database
                booking = Car_Booking.objects.get(razorpay_order_id=data.get('razorpay_order_id'))
                booking.payment_status = 'Paid'
                booking.booking_status='Confirmed'
                booking.save()
                return Response({'status':'Payment Successful'}, status=status.HTTP_200_OK)
            else:
                booking = Car_Booking.objects.get(razorpay_order_id=data.get('razorpay_order_id'))
                booking.payment_status = 'Failed'
                booking.save()
                return Response({'status':'Payment Failed'},  status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Handle verification failure or other exceptions
            print(f"Webhook verification failed: {str(e)}")
            return Response({'status':f"Webhook verification failed: {str(e)}"})
          
# class UploadDrivingLicence(APIView):
#     pass
   


        

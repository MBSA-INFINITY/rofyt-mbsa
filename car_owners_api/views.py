import pyotp
from django.shortcuts import render
from django.conf import settings
from accounts import serializers
from rest_framework import views , permissions, status, generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from accounts.models import *
from rest_framework.authtoken.models import Token
from utility.otp import send_otp
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from car_owners_api.models import Car_Booking, Car_Owner_Vehicle, Car_Owner_Vehicle_Certificate, Car_Owner_Vehicle_Image,Accident_Support
# from car_owners_api.serializers import UserSerializer,UserDetailsSerializer, CarOwnerVehicleSerializer, CarOwnerVehicleImageSerializer, CarOwnerVehicleCertificateSerializer, UserAndCarOwnerVehicleSerializer
import os
import requests
from cabs.models import CabType, CabClass, VehicleMaker, VehicleModel
from rest_framework.exceptions import NotFound
from django.core.files.storage import FileSystemStorage
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from car_owners_api.car_owner_utility import car_owner_vehicle_utility, get_car_owner_utility
from car_owners_api.serializers import CarOwnerProfileSerializer, GetCarBookingStatusSerializer, GetCarOwnerProfileSerializer
# Create your views here.

class CarOwnerRegisterAPI(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone", None)
        if User.objects.filter(phone=phone).exists():
            return Response(data={"status": False, 'data': "Number already registered"}, status=status.HTTP_400_BAD_REQUEST)
        car_owner = CarOwner.objects.create(phone=phone, code=create_ref_code())
        hotp = pyotp.HOTP(car_owner.hash(), 4)
        send_otp(hotp.at(car_owner.carownerphoneverify.count), car_owner.phone)
        return Response(data={"status": True, "phone":car_owner.phone}, status=status.HTTP_201_CREATED)

class VerifyCarOwnerPhoneWithOtpAPI(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone", None)
        otp = request.data.get("otp", None)
        try:
            if not User.objects.filter(phone=phone).exists():
                return Response(data={"status": False, 'data': "Phone Number not registered"}, status=status.HTTP_400_BAD_REQUEST)
            carowner = CarOwner.objects.filter(phone=phone).first()
           
            hotp = pyotp.HOTP(carowner.hash(), 4)
            phone_obj = carowner.carownerphoneverify
            if otp and phone:
                print("otp", otp, "exit opt",hotp.at(phone_obj.count) )
                if str(otp) == hotp.at(phone_obj.count):
                    phone_obj.count += 1
                    phone_obj.save()
                    return Response(data={"status": True, "phone":carowner.phone, "data":"OTP IS CORRECT"}, status=status.HTTP_200_OK)
                else:
                    return Response(data={"status": False, 'data': "Phone OTP is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendOTPtoAlternativeNumberApi(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone", None)
        alternate_number=request.data.get('alternate_number', None)
        try:
            if not User.objects.filter(phone=phone).exists():
                return Response(data={"status": False, 'data': "Phone Number not registered"}, status=status.HTTP_400_BAD_REQUEST)
            carowner = CarOwner.objects.filter(phone=phone).first()
            hotp = pyotp.HOTP(carowner.hash(), 4)
            send_otp(hotp.at(carowner.carownerphoneverify.count), alternate_number)
            return Response(data={"status": True, "phone":carowner.phone}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
class SaveCarOwnerAndVehicleDetailApi(views.APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request, *args, **kwargs):
        try:
            phone=request.data.get('phone', None)
            first_name=request.data.get('first_name', None)
            last_name=request.data.get('last_name', None)
            alternate_number=request.data.get('alternate_number', None)
            email=request.data.get('email', None)
            carowner_address=request.data.get('address', None)
            carowner_aadhar_no=request.data.get('aadhar_no', None)
            carowner_aadhar_front=request.data.get('aadhar_front', None)
            carowner_aadhar_back=request.data.get('aadhar_back', None)
            carowner_pan_no=request.data.get('pan_no', None)
            carowner_pan_photo=request.data.get('pan_photo', None)
            carowner_photo=request.data.get('photo', None)
            if User.objects.filter(email=email).exists():
                return Response(data={"status": False, 'data': "Email Id already Exist"}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(phone=phone).first():
                carowner=User.objects.get(phone=phone)
                carowner.first_name=first_name
                carowner.last_name=last_name
                carowner.alternate_number=alternate_number
                carowner.email=email
                carowner.aadhar_number=carowner_aadhar_no
                carowner.full_address=carowner_address
                carowner.aadhar_upload_front=carowner_aadhar_front
                carowner.aadhar_upload_back=carowner_aadhar_back
                carowner.pan_number=carowner_pan_no
                carowner.pan_upload=carowner_pan_photo
                carowner.photo_upload=carowner_photo
                carowner.save()
        
            folder_name= first_name + "_" + last_name + "_" + str(phone[-4:])
        
            media_folder = os.path.join(settings.MEDIA_ROOT, folder_name)
            os.makedirs(media_folder, exist_ok=True)
            storage = FileSystemStorage(location=media_folder)
            if carowner_aadhar_front:
                storage.save(carowner_aadhar_front.name, carowner_aadhar_front)
            if carowner_aadhar_back:
                storage.save(carowner_aadhar_back.name, carowner_aadhar_back)
            if carowner_pan_photo:
                storage.save(carowner_pan_photo.name, carowner_pan_photo)
            if carowner_photo:
                storage.save(carowner_photo.name, carowner_photo)
        

            vehicle_maker_id=request.data.get('vehicle_maker_id', None)
            vehicle_model_id=request.data.get('vehicle_model_id', None)
            vehicle_plate_no=request.data.get('vehicle_plate_no', None)
            if Car_Owner_Vehicle.objects.filter(vehicle_plate_no=vehicle_plate_no).exists():
                return Response(data={"status": False, 'data': "Vehicle already exist"}, status=status.HTTP_400_BAD_REQUEST)
            car_owner_vehicle=Car_Owner_Vehicle.objects.create(
                user_id=carowner.id,
                vehicle_maker_id=vehicle_maker_id,
                vehicle_model_id=vehicle_model_id,
                vehicle_plate_no=vehicle_plate_no,
            )
            vehicle_front_image=request.data.get('vehicle_front_image', None)
            vehicle_back_image=request.data.get('vehicle_back_image', None)
            vehicle_left_image=request.data.get('vehicle_left_image', None)
            vehicle_right_image=request.data.get('vehicle_right_image', None)
            driver_seat_image=request.data.get('driver_seat_image', None)
            passager_seat_image=request.data.get('passager_seat_image', None)
            front_head_light_image=request.data.get('front_head_light_image', None)
            back_head_light_image=request.data.get('back_head_light_image', None)
            Car_Owner_Vehicle_Image.objects.create(
                user_id=carowner.id,
                car_owner_vehicle_id= car_owner_vehicle.id,
                vehicle_front_image=vehicle_front_image,
                vehicle_back_image=vehicle_back_image,
                vehicle_left_image=vehicle_left_image,
                vehicle_right_image=vehicle_right_image,
                driver_seat_image=driver_seat_image,
                passager_seat_image=passager_seat_image,
                front_head_light_image=front_head_light_image,
                back_head_light_image=back_head_light_image
            )
            if vehicle_front_image:
                storage.save(vehicle_front_image.name, vehicle_front_image)
            if vehicle_back_image:
                storage.save(vehicle_back_image.name, vehicle_back_image)
            if vehicle_left_image:
                storage.save(vehicle_left_image.name, vehicle_left_image)
            if vehicle_right_image:
                storage.save(vehicle_right_image.name, vehicle_right_image)
            if driver_seat_image:
                storage.save(driver_seat_image.name, driver_seat_image)
            if passager_seat_image:
                storage.save(passager_seat_image.name, passager_seat_image)
            if front_head_light_image:
                storage.save(front_head_light_image.name, front_head_light_image)
            if back_head_light_image:
                storage.save(back_head_light_image.name, back_head_light_image)
            insurance=request.data.get('insurance', None)
            rc_book=request.data.get('RC_book', None)
            c_book=request.data.get('C_book', None)

            Car_Owner_Vehicle_Certificate.objects.create(
                user_id=carowner.id,
                car_owner_vehicle_id= car_owner_vehicle.id,
                insurance=insurance,
                RC_book=rc_book,
                C_book=c_book,  
            )
            if insurance:
                storage.save(insurance.name, insurance)
            if rc_book:
                storage.save(rc_book.name, rc_book)
            if c_book:
                storage.save(c_book.name, c_book)
            return Response(data={"status": True, "phone":carowner.phone}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
class AgreeTearmAndConditionApi(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            phone = request.data.get("phone", None)
            terms_policy=request.data.get("terms_policy", None)
            myride_insurance=request.data.get("myride_insurance", None)
            if not User.objects.filter(phone=phone).exists():
                return Response(data={"status": False, 'data': "Phone Number not registered"}, status=status.HTTP_400_BAD_REQUEST)
            if terms_policy and myride_insurance:
                car_owner=User.objects.get(phone=phone)
                car_owner.terms_policy=terms_policy
                car_owner.myride_insurance=myride_insurance
                car_owner.save()
                return Response(data={"status": True,}, status=status.HTTP_200_OK)
            else:
                return Response(data={"status": False, 'data': "Please fill the field"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

class LoginCarOwnerwithPhoneNumberApi(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            phone = request.data.get("phone", None)
            if phone:
                if not User.objects.filter(phone=phone).exists():
                    car_owner = CarOwner.objects.create(phone=phone, code=create_ref_code())
                    hotp = pyotp.HOTP(car_owner.hash(), 4)
                    send_otp(hotp.at(car_owner.carownerphoneverify.count), car_owner.phone)
                    return Response(data={"status": True, "phone":car_owner.phone,"msg":"New user created."}, status=status.HTTP_201_CREATED)
                    # return Response(data={"status": False, 'data': "User not exist"}, status=status.HTTP_400_BAD_REQUEST)
                carowner = CarOwner.objects.get(phone=phone)
                hotp = pyotp.HOTP(carowner.hash(), 4)
                send_otp(hotp.at(carowner.carownerphoneverify.count), carowner.phone)
                return Response(data={"status": True, "phone":carowner.phone}, status=status.HTTP_200_OK)
            
            else:
                return Response(data={"status": False, 'data': "Login Failed"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
class VerifyLoginPhoneNumerApi(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone", None)
        otp = request.data.get("otp", None)
        try:
            if not User.objects.filter(phone=phone).exists():
                return Response(data={"status": False, 'data': "Phone Number not registered"}, status=status.HTTP_400_BAD_REQUEST)
            carowner = CarOwner.objects.filter(phone=phone).first()
           
            hotp = pyotp.HOTP(carowner.hash(), 4)
            phone_obj = carowner.carownerphoneverify
            if otp and phone:
                print("otp", otp, "exit opt",hotp.at(phone_obj.count) )
                if str(otp) == hotp.at(phone_obj.count):
                    token, _ = Token.objects.get_or_create(user=carowner)
                    phone_obj.count += 1
                    phone_obj.save()
                    return Response(data={"status": True, "user_id":carowner.id, "token": token.key}, status=status.HTTP_200_OK)
                else:
                    return Response(data={"status": False, 'data': "Phone OTP is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CarOwnerProfileApi(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def get(self, request, id):

        try:
            if id:
                car_owner=User.objects.get(id=id)
                print(car_owner, "EEEEEEEEEEEEEEEEE")
                data=get_car_owner_utility.get_car_owner_profile_detials(car_owner)
                return Response(data={"status": True, "user_data":data}, status=status.HTTP_200_OK)
            else:
                return Response(data={"status": False, 'user_data': "User Not Exist."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"status": False, 'user_data': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class CarOwnerVehicleListApi(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def get(self, request, user_id):
        try:
            if user_id:
                vehicle_obj=Car_Owner_Vehicle.objects.filter(user_id=user_id)
                vehicle=car_owner_vehicle_utility.get_car_owner_vehicle_list(vehicle_obj)
                if vehicle:
                    return Response(data={"status": True, "vehicles":vehicle}, status=status.HTTP_200_OK)
                else:
                    return Response(data={"status": False, "vehicles":"No Data Found"}, status=status.HTTP_404_NOT_FOUND)

            else:
                return Response(data={"status": False, 'vehicles': []}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response(data={"status": False, 'vehicle': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CarOwnerVehicleDetialsApi(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def get(self, request, id):
        try:
            if id:
                vehicle_obj=Car_Owner_Vehicle.objects.get(id=id)
                vehicle=car_owner_vehicle_utility.get_car_owner_vehicle_details(vehicle_obj)
                return Response(data={"status": True, "vehicle":vehicle}, status=status.HTTP_200_OK)
            else:
                return Response(data={"status": False, 'vehicle': []}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response(data={"status": False, 'vehicle': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class CarOwnerVehicleCreateApi(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request, user_id):
        try:
            vehicle=car_owner_vehicle_utility.create_vehicle(request.data, user_id)
            print(vehicle, "EEEEE")
            if vehicle==True:
                return Response(data={"status": True, "data":"Success"}, status=status.HTTP_201_CREATED)
            else:
                return vehicle
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)




class SaveCarOwnerDetailsApi(views.APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request, *args, **kwargs):
        try:
            phone=request.data.get('phone', None)
            first_name=request.data.get('first_name', None)
            last_name=request.data.get('last_name', None)
            alternate_number=request.data.get('alternate_number', None)
            email=request.data.get('email', None)
            carowner_address=request.data.get('address', None)
            carowner_city=request.data.get('city', None)
            carowner_state=request.data.get('state', None)
            carowner_pincode=request.data.get('pincode', None)
            carowner_house_no=request.data.get('house_no', None)
            carowner_landmark=request.data.get('landmark', None)
            carowner_aadhar_no=request.data.get('aadhar_no', None)
            carowner_aadhar_front=request.data.get('aadhar_front', None)
            carowner_aadhar_back=request.data.get('aadhar_back', None)
            carowner_pan_no=request.data.get('pan_no', None)
            carowner_pan_photo=request.data.get('pan_photo', None)
            carowner_photo=request.data.get('photo', None)
            carowner_license_number=request.data.get('license_number', None)
            carowner_license_upload_front=request.data.get('license_upload_front', None)
            carowner_license_upload_back=request.data.get('license_upload_back', None)
            
            
            carowner_latitude = None
            carowner_longitude = None
            if User.objects.filter(email=email).exists():
                return Response(data={"status": False, 'data': "Email Id already Exist"}, status=status.HTTP_400_BAD_REQUEST)
            
            endpoint = os.getenv('GOOGLE_MAPS_GEOCODING_ENDPOINT')
            google_map_key = os.getenv('GOOGLE_MAPS_API_KEY')

            params = {
                'address': carowner_address,
                'key': google_map_key,}
            
            # Make the API request
            response = requests.get(endpoint, params=params)
            
            # Parse the JSON response
            data = response.json()
            if data['status'] == 'OK':
                # Extract latitude and longitude
                location = data['results'][0]['geometry']['location']
                carowner_latitude = location['lat']
                carowner_longitude = location['lng']
            else:
                print(f"Geocoding API error: {data['status']}")
            
            if User.objects.filter(phone=phone).first():
                carowner=User.objects.get(phone=phone)
                carowner.first_name=first_name
                carowner.last_name=last_name
                carowner.alternate_number=alternate_number
                carowner.email=email
                carowner.aadhar_number=carowner_aadhar_no
                carowner.city=carowner_city
                carowner.state=carowner_state
                carowner.house_or_building=carowner_house_no
                carowner.road_or_area=carowner_landmark
                carowner.pincode=carowner_pincode
                carowner.full_address=carowner_address
                carowner.aadhar_upload_front=carowner_aadhar_front
                carowner.aadhar_upload_back=carowner_aadhar_back
                carowner.pan_number=carowner_pan_no
                carowner.pan_upload=carowner_pan_photo
                carowner.photo_upload=carowner_photo
                carowner.latitude=carowner_latitude
                carowner.longitude=carowner_longitude
                carowner.license_number = carowner_license_number
                carowner.license_upload_front = carowner_license_upload_front
                carowner.license_upload_back = carowner_license_upload_back
                carowner.save()
        
            # last_phone_digit = str(phone)

            # folder_name= first_name + "_" + last_name + "_" + last_phone_digit[-4:]

        
            # media_folder = os.path.join(settings.MEDIA_ROOT, folder_name)
            # os.makedirs(media_folder, exist_ok=True)
            # storage = FileSystemStorage(location=media_folder)
            # if carowner_aadhar_front:
            #     storage.save(carowner_aadhar_front.name, carowner_aadhar_front)
            # if carowner_aadhar_back:
            #     storage.save(carowner_aadhar_back.name, carowner_aadhar_back)
            # if carowner_pan_photo:
            #     storage.save(carowner_pan_photo.name, carowner_pan_photo)
            # if carowner_photo:
            #     storage.save(carowner_photo.name, carowner_photo)
                
            return Response(data={"status": True, "phone":carowner.phone}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST) 


class SaveCarOwnerVehicleDetailsApi(views.APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request, *args, **kwargs):
        try:
            phone=request.data.get('phone', None)
            vehicle_type_id=request.data.get('vehicle_type_id', None)
            vehicle_maker_id=request.data.get('vehicle_maker_id', None)
            vehicle_model_id=request.data.get('vehicle_model_id', None)
            vehicle_plate_no=request.data.get('vehicle_plate_no', None)

            if not User.objects.filter(phone=phone).exists():
                return Response(data={"status": False, 'data': "User not exist"}, status=status.HTTP_400_BAD_REQUEST)

            if Car_Owner_Vehicle.objects.filter(vehicle_plate_no=vehicle_plate_no).exists():
                return Response(data={"status": False, 'data': "Vehicle already exist"}, status=status.HTTP_400_BAD_REQUEST)
            carowner = User.objects.get(phone=phone)
            cab_type_instance = CabType.objects.get(pk=vehicle_type_id)
            vehicle_model_instance=VehicleModel.objects.get(pk=vehicle_model_id)
            cab_class_instance=CabClass.objects.get(pk=vehicle_model_instance.cab_class.id)
            car_owner_vehicle=Car_Owner_Vehicle.objects.create(
                user_id=carowner.id,
                vehicle_maker_id=vehicle_maker_id,
                vehicle_model_id=vehicle_model_id,
                vehicle_plate_no=vehicle_plate_no,
                vehicle_type=cab_type_instance,
                vehicle_class=cab_class_instance

            )
            vehicle_front_image=request.data.get('vehicle_front_image', None)
            vehicle_back_image=request.data.get('vehicle_back_image', None)
            vehicle_left_image=request.data.get('vehicle_left_image', None)
            vehicle_right_image=request.data.get('vehicle_right_image', None)
            driver_seat_image=request.data.get('driver_seat_image', None)
            passager_seat_image=request.data.get('passager_seat_image', None)
            front_head_light_image=request.data.get('front_head_light_image', None)
            back_head_light_image=request.data.get('back_head_light_image', None)
            
            Car_Owner_Vehicle_Image.objects.create(
                user_id=carowner.id,
                vehicle_id= car_owner_vehicle.id,
                vehicle_front_image=vehicle_front_image,
                vehicle_back_image=vehicle_back_image,
                vehicle_left_image=vehicle_left_image,
                vehicle_right_image=vehicle_right_image,
                driver_seat_image=driver_seat_image,
                passager_seat_image=passager_seat_image,
                front_head_light_image=front_head_light_image,
                back_head_light_image=back_head_light_image
            )
            # last_phone_digit = str(phone)

            # folder_name= carowner.first_name + "_" + carowner.last_name + "_" + last_phone_digit[-4:]
            # media_folder = os.path.join(settings.MEDIA_ROOT, folder_name)
            # os.makedirs(media_folder, exist_ok=True)
            # storage = FileSystemStorage(location=media_folder)
            # if vehicle_front_image:
            #     storage.save(vehicle_front_image.name, vehicle_front_image)
            # if vehicle_back_image:
            #     storage.save(vehicle_back_image.name, vehicle_back_image)
            # if vehicle_left_image:
            #     storage.save(vehicle_left_image.name, vehicle_left_image)
            # if vehicle_right_image:
            #     storage.save(vehicle_right_image.name, vehicle_right_image)
            # if driver_seat_image:
            #     storage.save(driver_seat_image.name, driver_seat_image)
            # if passager_seat_image:
            #     storage.save(passager_seat_image.name, passager_seat_image)
            # if front_head_light_image:
            #     storage.save(front_head_light_image.name, front_head_light_image)
            # if back_head_light_image:
            #     storage.save(back_head_light_image.name, back_head_light_image)
            
            
            return Response(data={"status": True, "phone":carowner.phone,"vehicle_id":car_owner_vehicle.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST) 



class SaveCarOwnerVehicleCertificatedApi(views.APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request, *args, **kwargs):
        try:
            phone=request.data.get('phone', None)
            vehicle_id=request.data.get('vehicle_id', None)

            if not User.objects.filter(phone=phone).exists():
                return Response(data={"status": False, 'data': "User not exist"}, status=status.HTTP_400_BAD_REQUEST)

            carowner = User.objects.get(phone=phone)
            car_owner_vehicle = Car_Owner_Vehicle.objects.get(id=vehicle_id)
           
            
            
            # last_phone_digit = str(phone)

            # folder_name= carowner.first_name + "_" + carowner.last_name + "_" + last_phone_digit[-4:]
            # media_folder = os.path.join(settings.MEDIA_ROOT, folder_name)
            # os.makedirs(media_folder, exist_ok=True)
            # storage = FileSystemStorage(location=media_folder)
            
            insurance=request.data.get('insurance', None)
            rc_book=request.data.get('RC_book', None)
            c_book=request.data.get('C_book', None)

            Car_Owner_Vehicle_Certificate.objects.create(
                user_id=carowner.id,
                vehicle_id= car_owner_vehicle.id,
                insurance=insurance,
                RC_book=rc_book,
                C_book=c_book,  
            )
            # if insurance:
            #     storage.save(insurance.name, insurance)
            # if rc_book:
            #     storage.save(rc_book.name, rc_book)
            # if c_book:
            #     storage.save(c_book.name, c_book)
            return Response(data={"status": True, "phone":carowner.phone,"vehicle_id":car_owner_vehicle.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST) 


class CarOwnerProfileAndUpdateAPI(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CarOwnerProfileSerializer

    def get_object(self):
        return self.request.user
class VehicleActiveStatusView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request, vehicle_id):
        try:
            statu=request.data.get('status', None)
            car_vehcle = Car_Owner_Vehicle.objects.get(id=vehicle_id)
            car_vehcle.is_active = statu
            car_vehcle.save()
            return Response(data={"status": True, "message":"Vehicle Status change successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

class GetCarOwnerProfileAPI(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GetCarOwnerProfileSerializer

    def get_object(self):
        return self.request.user
    
class CarBookingRequestView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GetCarBookingStatusSerializer
    def get_queryset(self):
        return Car_Booking.objects.filter(booking_status="Pending", car_owner=self.request.user)
    

class AcceptCarBookingView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request, carbooking_id):
        try:
            booking_status = request.data.get('booking_status', None)
            car_booking = Car_Booking.objects.get(id=carbooking_id)
            car_booking.booking_status = booking_status
            car_booking.save()
            return Response(data={"status": True, "message":"Request approved successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

class SaveImagesBeforeDeliveryView(views.APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request,booking_id):
        try:
            car_booking = Car_Booking.objects.get(id=booking_id)
            vehicle_front_image=request.data.get('vehicle_front_image', None)
            vehicle_back_image=request.data.get('vehicle_back_image', None)
            vehicle_left_image=request.data.get('vehicle_left_image', None)
            vehicle_right_image=request.data.get('vehicle_right_image', None)
            speedo_meter_image=request.data.get('speedo_meter', None)
            vehicle_inside_image=request.data.get('vehicle_inside', None)
            
            
            car_booking.before_front=vehicle_front_image,
            car_booking.before_back=vehicle_back_image,
            car_booking.before_right=vehicle_left_image,
            car_booking.before_left=vehicle_right_image,
            car_booking.before_speedo_meter=speedo_meter_image,
            car_booking.before_inside_car=vehicle_inside_image,

            car_booking.save()
           
            return Response(data={"status": True, "message":"Images uploaded successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

class SaveImagesAfterDeliveryView(views.APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request,booking_id):
        try:
            car_booking = Car_Booking.objects.get(id=booking_id)
            vehicle_front_image=request.data.get('vehicle_front_image', None)
            vehicle_back_image=request.data.get('vehicle_back_image', None)
            vehicle_left_image=request.data.get('vehicle_left_image', None)
            vehicle_right_image=request.data.get('vehicle_right_image', None)
            speedo_meter_image=request.data.get('speedo_meter', None)
            vehicle_inside_image=request.data.get('vehicle_inside', None)
            
            
            car_booking.after_front=vehicle_front_image,
            car_booking.after_back=vehicle_back_image,
            car_booking.after_right=vehicle_left_image,
            car_booking.after_left=vehicle_right_image,
            car_booking.after_speedo_meter=speedo_meter_image,
            car_booking.after_inside_car=vehicle_inside_image,
            car_booking.booking_status = 'Completed'

            car_booking.save()
           
            return Response(data={"status": True, "message":"Images uploaded successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

class CarBookingCompletedView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GetCarBookingStatusSerializer
    def get_queryset(self):
        return Car_Booking.objects.filter(booking_status="Completed", car_owner=self.request.user)

class LastCarBookingView(generics.RetrieveAPIView):
    serializer_class = GetCarBookingStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        user = self.request.user
        try:
            car_booking = Car_Booking.objects.filter(car_owner=user, vehicle=vehicle_id,booking_status='Completed').latest('modified_at')
            car_booking.duration = self.calculate_total_duration(car_booking)
            return car_booking
        except Car_Booking.DoesNotExist:
            raise NotFound("Car Booking not found")
    
    def calculate_total_duration(self, car_booking):
        pick_up_time = car_booking.pick_up_data_time
        drop_off_time = car_booking.drop_up_date_time

        if pick_up_time and drop_off_time:
            duration = drop_off_time - pick_up_time
            total_seconds = duration.total_seconds()
            hours, remainder = divmod(total_seconds, 3600)
            minutes, _ = divmod(remainder, 60)

            if hours == 1:
                hours_str = "1h"
            else:
                hours_str = f"{int(hours)}h"

            if minutes == 1:
                minutes_str = "1min"
            else:
                minutes_str = f"{int(minutes)}min"

            return f"{hours_str}:{minutes_str}"

        return None

class AccidentSupportView(views.APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request):
        try:
            vehicle_id=request.data.get('vehicle_id', None)
            vehicle_image=request.data.get('vehicle_image', None)
            vehicle_video=request.data.get('vehicle_video', None)
            description=request.data.get('description', None)
            car_owner = Car_Owner_Vehicle.objects.get(id=vehicle_id)
            if not car_owner:
                return Response(data={"status": False, "message":"Vehicle id not found"}, status=status.HTTP_400_BAD_REQUEST)
                
            
            Accident_Support.objects.create(vehicle=car_owner,vehicle_image=vehicle_image,
                                   vehicle_video=vehicle_video, description=description)
            
           
            return Response(data={"status": True, "message":"Accident support created successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST) 


class CarOwnerUpdateAadharApi(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request, user_id):
        try:
            car_owner = User.objects.get(id=user_id)
            
            aadhar_front=request.data.get('aadhar_front', None)
            aadhar_back=request.data.get('aadhar_back', None)
            
            car_owner.aadhar_upload_front = aadhar_front
            car_owner.aadhar_upload_back = aadhar_back

            car_owner.save()
                
            return Response(data={"status": True, "data":"Aadhar uploaded successfully"}, status=status.HTTP_200_OK)
           
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CarOwnerUpdateInsuranceApi(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request, vehicle_id):
        try:
            car_owner = Car_Owner_Vehicle_Certificate.objects.get(vehicle_id=vehicle_id)
            
            
            insurance=request.data.get('insurance', None)
            
            car_owner.insurance = insurance

            car_owner.save()
                
            return Response(data={"status": True, "data":"Insurance uploaded successfully"}, status=status.HTTP_200_OK)
           
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CarOwnerProfileDetailsApi(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def get(self, request, user_id):
        try:
            vehicle_count = Car_Owner_Vehicle.objects.filter(user_id=user_id).count()
            trip_count = Car_Booking.objects.filter(car_owner=user_id,booking_status="Completed").count()
            duration_counts = Car_Booking.objects.filter(car_owner=user_id)

            total_duration = 0

            for booking in duration_counts:
                duration_str = booking.duration
                if duration_str.endswith("KM") or duration_str.endswith("km") :
                    duration_str = duration_str[:-2]
                try:
                    duration_as_int = int(duration_str)
                    total_duration += duration_as_int
                except Exception as f:
                    return Response(data={"status": False, 'vehicle': str(f)}, status=status.HTTP_400_BAD_REQUEST)

            return Response(data={"status": True, "vehicles_count":vehicle_count,"trip_count":trip_count,"km_count":total_duration}, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response(data={"status": False, 'vehicle': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CarOwnerUpdateProfilePictureApi(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request, user_id):
        try:
            car_owner = User.objects.get(id=user_id)
            
            profile_picture=request.data.get('profile_photo', None)
            
            car_owner.photo_upload = profile_picture

            car_owner.save()
                
            return Response(data={"status": True, "data":"Profile Picture uploaded successfully"}, status=status.HTTP_200_OK)
           
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CarOwnerUpdateDocumentsApi(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request, user_id):
        try:
            car_owner = User.objects.get(id=user_id)
            
            aadhar_front=request.data.get('aadhar_front', None)
            aadhar_back=request.data.get('aadhar_back', None)
            pan_upload = request.data.get('pan_upload', None)
            insurance=request.data.get('insurance', None)
            rc_book=request.data.get('rc_book', None)
            license_upload_front = request.data.get('license_upload_front', None)
            license_upload_back = request.data.get('license_upload_back', None)


            if aadhar_front is not None:
                car_owner.aadhar_upload_front = aadhar_front
            if aadhar_back is not None:
                car_owner.aadhar_upload_back = aadhar_back
            if pan_upload is not None:
                car_owner.pan_upload = pan_upload
            if license_upload_front is not None:
                car_owner.license_upload_front = license_upload_front
            if license_upload_back is not None:
                car_owner.license_upload_back = license_upload_back

            if insurance or rc_book:
                car_owner_certificate = Car_Owner_Vehicle_Certificate.objects.filter(user=user_id).first()
                if insurance is not None:
                    car_owner_certificate.insurance = insurance
                if rc_book is not None:
                    car_owner_certificate.RC_book = rc_book

                car_owner_certificate.save()


            car_owner.save()
                
            return Response(data={"status": True, "data":"Document uploaded successfully"}, status=status.HTTP_200_OK)
           
        except Exception as e:
            return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)

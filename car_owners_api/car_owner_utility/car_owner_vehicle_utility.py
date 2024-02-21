
from car_owners_api.models import Car_Owner_Vehicle_Image, Car_Owner_Vehicle_Certificate, Car_Owner_Vehicle
from accounts.models import *
import os
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import FileSystemStorage
def get_car_owner_vehicle_list(vehicle_obj):
    vehicle_list =[]
    for vehicle in vehicle_obj:
        vehicle_dict= get_car_owner_vehicle_details(vehicle)
        vehicle_list.append(vehicle_dict)
    return vehicle_list
def get_car_owner_vehicle_details(vehicle):
    vehicle_dict={}
    vehicle_dict['user_id']=vehicle.user_id
    vehicle_dict['id']=vehicle.id
    vehicle_dict['vehicle_maker']=vehicle.vehicle_maker.maker
    vehicle_dict["vehicle_model"]=vehicle.vehicle_model.model
    vehicle_dict['vehicle_plate_no']=vehicle.vehicle_plate_no
    vehicle_dict['is_active']=vehicle.is_active

    if not CarOwner.objects.filter(id=vehicle.user_id).exists():
        return Response(data={"status": False, 'data': "User not exist"}, status=status.HTTP_400_BAD_REQUEST)
    car_owner=CarOwner.objects.get(id=vehicle.user_id)
    folder_name=car_owner.first_name + "_" + car_owner.last_name + "_" + str(car_owner.phone[-4:]) 
    file_path = os.path.join(settings.MEDIA_URL, folder_name)
    if Car_Owner_Vehicle_Image.objects.filter(vehicle_id=vehicle.id).exists():
        vehicle_image_obj=Car_Owner_Vehicle_Image.objects.get(vehicle_id=vehicle.id)
        vehicle_image_dict={}
        if vehicle_image_obj.vehicle_front_image:
            vehicle_image_dict["vehicle_front_image"]= vehicle_image_obj.vehicle_front_image
        if vehicle_image_obj.vehicle_back_image:
            vehicle_image_dict["vehicle_back_image"]= vehicle_image_obj.vehicle_back_image
        if vehicle_image_obj.vehicle_left_image:
            vehicle_image_dict["vehicle_left_image"]= vehicle_image_obj.vehicle_left_image
        if vehicle_image_obj.vehicle_back_image:
            vehicle_image_dict["vehicle_right_image"]= vehicle_image_obj.vehicle_back_image
        if vehicle_image_obj.driver_seat_image:
            vehicle_image_dict["driver_seat_image"]= vehicle_image_obj.driver_seat_image
        if vehicle_image_obj.passager_seat_image:
            vehicle_image_dict["passager_seat_image"]= vehicle_image_obj.passager_seat_image
        if vehicle_image_obj.front_head_light_image:
            vehicle_image_dict["front_head_light_image"]= vehicle_image_obj.front_head_light_image
        if vehicle_image_obj.back_head_light_image:
            vehicle_image_dict["back_head_light_image"]= vehicle_image_obj.back_head_light_image
        vehicle_dict["vehicle_image"]=vehicle_image_dict
    if Car_Owner_Vehicle_Certificate.objects.filter(vehicle_id=vehicle.id).exists():
        vehicle_certificate_obj=Car_Owner_Vehicle_Certificate.objects.filter(vehicle_id=vehicle.id).first()
        vehicle_certificate_dict={}
        if vehicle_certificate_obj.insurance:
            vehicle_certificate_dict['insurance']= vehicle_certificate_obj.insurance
        if vehicle_certificate_obj.RC_book:
            vehicle_certificate_dict['RC_book']= vehicle_certificate_obj.RC_book
        if vehicle_certificate_obj.C_book:
            vehicle_certificate_dict['C_book']= vehicle_certificate_obj.C_book
        vehicle_dict["vehicle_certificate"]=vehicle_certificate_dict
    return vehicle_dict
    
def create_vehicle(data, user_id):
    try:
        vehicle_maker_id=data.get('vehicle_maker_id', None)
        vehicle_model_id=data.get('vehicle_model_id', None)
        vehicle_plate_no=data.get('vehicle_plate_no', None)
        print(vehicle_plate_no, "odododododood")
        if not CarOwner.objects.filter(id=user_id).exists():
            return Response(data={"status": False, 'data': "User not exist"}, status=status.HTTP_400_BAD_REQUEST)
        car_owner=CarOwner.objects.get(id=user_id)
        folder_name= car_owner.first_name + "_" + car_owner.last_name + "_" + str(car_owner.phone[-4:])
        media_folder = os.path.join(settings.MEDIA_ROOT, folder_name)
        os.makedirs(media_folder, exist_ok=True)
        storage = FileSystemStorage(location=media_folder)
        if Car_Owner_Vehicle.objects.filter(vehicle_plate_no=vehicle_plate_no).exists():
            return Response(data={"status": False, 'data': "Vehicle already exist"}, status=status.HTTP_400_BAD_REQUEST)
        car_owner_vehicle=Car_Owner_Vehicle.objects.create(
            user_id=user_id,
            vehicle_maker_id=vehicle_maker_id,
            vehicle_model_id=vehicle_model_id,
            vehicle_plate_no=vehicle_plate_no,
        )
        vehicle_front_image=data.get('vehicle_front_image', None)
        vehicle_back_image=data.get('vehicle_back_image', None)
        vehicle_left_image=data.get('vehicle_left_image', None)
        vehicle_right_image=data.get('vehicle_right_image', None)
        driver_seat_image=data.get('driver_seat_image', None)
        passager_seat_image=data.get('passager_seat_image', None)
        front_head_light_image=data.get('front_head_light_image', None)
        back_head_light_image=data.get('back_head_light_image', None)
        Car_Owner_Vehicle_Image.objects.create(
            user_id=user_id,
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
        insurance=data.get('insurance', None)
        rc_book=data.get('RC_book', None)
        c_book=data.get('C_book', None)

        Car_Owner_Vehicle_Certificate.objects.create(
            user_id=user_id,
            vehicle_id= car_owner_vehicle.id,
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
        return True
    except Exception as e:
        return Response(data={"status": False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)




import os
from django.conf import settings

def get_car_owner_profile_detials(car_owner):
    car_owner_dict={}
    car_owner_dict['user_id']=car_owner.id
    car_owner_dict['first_name']=car_owner.first_name
    car_owner_dict['last_name']=car_owner.last_name
    car_owner_dict['phone']=car_owner.phone
    car_owner_dict['email']=car_owner.email
    car_owner_dict['address']=car_owner.full_address
    car_owner_dict['aadhar_number']=car_owner.aadhar_number
    car_owner_dict['pan_number']=car_owner.pan_number
    car_owner_dict['profile_photo']=car_owner.photo_upload
        
    car_owner_dict['aadhar_front']=car_owner.aadhar_upload_front
    car_owner_dict['aadhar_back']=car_owner.aadhar_upload_back
    car_owner_dict['pan_image']=car_owner.pan_upload
    car_owner_dict['license_number']=car_owner.license_number
    car_owner_dict['license_front']=car_owner.license_upload_front
    car_owner_dict['license_back']=car_owner.license_upload_back

    # if car_owner.photo_upload:
    #     folder_name=car_owner.first_name + "_" + car_owner.last_name + "_" + str(car_owner.phone[-4:]) + "/" + car_owner.photo_upload
    #     photo = os.path.join(settings.MEDIA_URL, folder_name)
    #     car_owner_dict['photo']=photo
    return car_owner_dict

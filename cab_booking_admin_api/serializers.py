from rest_framework import serializers
from django.db.models import Q
from datetime import datetime
from accounts.models import User
from trips.models import Trip
from accounts.models import User, Driver
from cabs.models import *
from cab_booking_admin_api.models import *


class CabBookingPriceSettingSerializer(serializers.ModelSerializer):
    cab_class_name = serializers.SerializerMethodField()
    cab_class_icon=serializers.SerializerMethodField()
    class Meta:
        model = CabBookingPriceSetting
        fields = ['id','price', 'cab_class', 'cab_class_name','cab_class_icon', 'platform_charge',]
    def get_cab_class_name(self, obj):
        return obj.cab_class.cab_class
    def get_cab_class_icon(self, obj):
        return obj.cab_class.icon
    def validate(self, data):
        # Check if a car with the same name already exists
        cab_class = data.get('cab_class')
        existing_cab_class = CabBookingPriceSetting.objects.filter(cab_class=cab_class).exclude(pk=self.instance.pk if self.instance else None).first()

        if existing_cab_class:
            raise serializers.ValidationError(f'A coupon code with the name "{ cab_class }" already exists.')
        return data
    


class TripListSerializer(serializers.ModelSerializer):
    # vehicle_name = serializers.CharField(source='cab.model.model', read_only=True)
    customer_first_name = serializers.CharField(source='customer.first_name', read_only=True)
    customer_last_name = serializers.CharField(source='customer.last_name', read_only=True)
    driver_first_name = serializers.CharField(source='driver.first_name', read_only=True)
    driver_last_name = serializers.CharField(source='driver.last_name', read_only=True)


    class Meta:
        model = Trip
        fields = ('id', 'customer','customer_first_name', 'customer_last_name','driver', 'driver_first_name','driver_last_name', 'status', 'source', 'destination', 'distance', 'timing', 'ride_type', 'otp_count')
       

    def get_customer_first_name(self, obj):
        return obj.customer.first_name
    def get_customer_last_name(self, obj):
        return obj.customer.last_name
    def get_driver_first_name(self, obj):
        return obj.driver.first_name if obj.driver else None
    def get_driver_last_name(self, obj):
        return obj.driver.last_name if obj.driver else None
    




class DriverListSerializer(serializers.ModelSerializer):
    total_trips = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name','last_name', 'email','phone', 'full_address','date_joined','photo_upload','status', 'total_trips', 'birth_day', 'gender', 'state', 'city', 'pincode', 'house_or_building','road_or_area', 'alternate_number', 'aadhar_number', 'aadhar_upload_front', 'aadhar_upload_back', 'pan_number','pan_upload', 'license_number', 'license_upload_front', 'license_upload_back')

    def get_total_trips(self, obj):
        return Trip.objects.filter(driver_id=obj.id).count()

    def get_status(self, user):
        if user.type == "DRIVER" and user.is_driver:
            if Trip.objects.filter(driver_id=user.id, status="ON_TRIP").exists():
                return "ON_TRIP"
            elif user.driver_duty:
                return "AVAILABLE"
            else:
                return "LEAVE"

class PassengersListSerializer(serializers.ModelSerializer):
    total_trips = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name','last_name', 'email','phone', 'full_address','date_joined','photo_upload','status', 'total_trips', 'birth_day', 'gender','state', 'city', 'pincode', 'house_or_building','road_or_area', 'alternate_number')

    def get_total_trips(self, obj):
        return Trip.objects.filter(customer_id=obj.id).count()

    def get_status(self, user):
        if user.type == "CUSTOMER" and user.is_customer:
            if user.is_active:
                return "ACTIVE"
            else:
                return "DEACTIVE"



class CabBookingVehicleSerializer(serializers.ModelSerializer):
    driver_first_name = serializers.SerializerMethodField()
    driver_last_name = serializers.SerializerMethodField()
    maker_name=serializers.SerializerMethodField()
    model_name=serializers.SerializerMethodField()
    cab_type_name=serializers.SerializerMethodField()
    cab_class_name=serializers.SerializerMethodField()
    class Meta:
        model=Vehicle
        fields = ['id', 'number_plate', 'insurance_certiifcate', 'registration_certiifcate', 'mot_certiifcate','addtional_document','front','back','right','left','inside_driver_seat','inside_passanger_seat','front_head_light','back_head_light','sound', 'pollution', 'last_location','is_approved','is_active','driver', 'driver_first_name','driver_last_name','cab_type','cab_type_name', 'cab_class', 'cab_class_name','maker','maker_name','model','model_name']
    def get_driver_first_name(self, obj):
        return obj.driver.first_name if obj.driver else None
    def get_driver_last_name(self, obj):
        return obj.driver.last_name if obj.driver else None
    def get_maker_name(self, obj):
        return obj.maker.maker if obj.maker else None
    def get_model_name(self, obj):
        return obj.model.model if obj.model else None
    def get_cab_type_name(self, obj):
        return obj.cab_type.cab_type if obj.cab_type else None
    def get_cab_class_name(self, obj):
        return obj.cab_class.cab_class if obj.cab_class else None
    
class CabBookingCouponCodeSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model=CabBookingCouponCodeSetting
        fields=['id', 'coupon_code','coupon_discount', 'is_active', 'expire_date', 'image']
    def validate(self, data):
        # Check if a car with the same name already exists
        coupon_code = data.get('coupon_code')
        existing_coupon_code =  CabBookingCouponCodeSetting.objects.filter(coupon_code=coupon_code).exclude(pk=self.instance.pk if self.instance else None).first()

        if existing_coupon_code:
            raise serializers.ValidationError(f'A coupon code with the name "{ coupon_code }" already exists.')
        return data
    
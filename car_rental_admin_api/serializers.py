from rest_framework import serializers
from django.db.models import Q
from datetime import datetime
from accounts.models import User
from trips.models import Trip
from accounts.models import User, Driver, CarOwner
from cabs.models import *
from car_rental_admin_api.models import *
class VehicleRentePriceSettingSerializer(serializers.ModelSerializer):
    model_name = serializers.SerializerMethodField()
    class Meta:
        model = VehicleRentePriceSetting
        fields = ['id','without_fuel_price','with_fuel_price', 'model', 'model_name', 'platform_charge', "tax_percentage", 'extra_kms_charge']
    def get_model_name(self, obj):
        return obj.model.model
    def validate(self, data):
        # Check if a car with the same name already exists
        model = data.get('model')
        existing_model =  VehicleRentePriceSetting.objects.filter(model=model).exclude(pk=self.instance.pk if self.instance else None).first()

        if existing_model:
            raise serializers.ValidationError(f' Vehicle Rental Price with the name "{ model }" already exists.')
        return data
    

class CitySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model=CitySetting
        fields = '__all__'
        # fields=['id','city_name']

class LocationsSettingSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField()
    class Meta:
        model=LocationsSetting
        fields=['id', 'location', 'city', 'city_name', 'is_active']
    def get_city_name(self, obj):
        return obj.city.city_name

class CouponCodeSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model=CouponCodeSetting
        fields=['id', 'coupon_code','coupon_discount', 'is_active']
    def validate(self, data):
        # Check if a car with the same name already exists
        coupon_code = data.get('coupon_code')
        existing_coupon_code =  CouponCodeSetting.objects.filter(coupon_code=coupon_code).exclude(pk=self.instance.pk if self.instance else None).first()

        if existing_coupon_code:
            raise serializers.ValidationError(f'A coupon code with the name "{ coupon_code }" already exists.')
        return data



class CarOwnerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=CarOwner
        fields='__all__'
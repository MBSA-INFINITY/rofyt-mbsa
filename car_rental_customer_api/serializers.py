from rest_framework import serializers
from django.db.models import Q
from datetime import datetime
from accounts.models import User
from trips.models import Trip
from accounts.models import User, Driver
from cabs.models import *
from car_rental_admin_api.models import *
from car_owners_api.models import *
from admin_api.serializers import *

class VehicleListForCutomerSerializer(serializers.ModelSerializer):
    vehicle_rental_price=serializers.SerializerMethodField()
    class Meta:
        model = Car_Owner_Vehicle
        fields=['id','vehicle_plate_no', 'vehicle_type','vehicle_class','vehicle_maker', 'vehicle_model', 'user', 'is_active', 'vehicle_rental_price']
    def to_representation(self, instance):
     
        self.fields['vehicle_class'] = SaveVehicleClassSerializer(read_only=True)
        self.fields['vehicle_type'] = VehicleTypeSerializer(read_only=True)
        self.fields['vehicle_maker'] = VehicleMakerSerializers(read_only=True)
        self.fields['vehicle_model'] = SaveVehicleModelSerializer(read_only=True)
        return super(VehicleListForCutomerSerializer, self).to_representation(instance)
    def get_vehicle_rental_price(self, obj): 
        try:
           
            vehicle_model_obj=VehicleModel.objects.get(id=obj.vehicle_model.id)
            vehicle_price_obj=VehicleRentePriceSetting.objects.get(model=vehicle_model_obj)
            data={'id':vehicle_price_obj.id,
                   "without_fuel_price": vehicle_price_obj.without_fuel_price,
                   "with_fuel_price": vehicle_price_obj.with_fuel_price,
                   "model": vehicle_price_obj.model.id,
                   "platform_charge": vehicle_price_obj.platform_charge,
                   "tax_percentage": vehicle_price_obj.tax_percentage,
                   "extra_kms_charge": vehicle_price_obj.extra_kms_charge
                   }
            return data
        except Exception as e:
            print(e)
            return None
      
class VehicleDetailsForCutomerSerializer(serializers.ModelSerializer):
    vehicle_rental_price=serializers.SerializerMethodField()
    class Meta:
        model = Car_Owner_Vehicle
        fields=['id','vehicle_plate_no', 'vehicle_type','vehicle_class','vehicle_maker', 'vehicle_model', 'user', 'is_active', 'vehicle_rental_price']
    def to_representation(self, instance):
     
        self.fields['vehicle_class'] = SaveVehicleClassSerializer(read_only=True)
        self.fields['vehicle_type'] = VehicleTypeSerializer(read_only=True)
        self.fields['vehicle_maker'] = VehicleMakerSerializers(read_only=True)
        self.fields['vehicle_model'] = SaveVehicleModelSerializer(read_only=True)
        return super(VehicleDetailsForCutomerSerializer, self).to_representation(instance)
    def get_vehicle_rental_price(self, obj): 
        try:
            print(self.context.get("price_type"), "self.context.get('date_from')")
            vehicle_model_obj=VehicleModel.objects.get(id=obj.vehicle_model.id)
            vehicle_price_obj=VehicleRentePriceSetting.objects.get(model=vehicle_model_obj)
            price_type=self.context.get("price_type")
           
            data={'id':vehicle_price_obj.id,
                   "model": vehicle_price_obj.model.id,
                   "platform_charge": vehicle_price_obj.platform_charge,
                   "tax_percentage": vehicle_price_obj.tax_percentage,
                   "extra_kms_charge": vehicle_price_obj.extra_kms_charge
                   }
            if price_type =="without_fuel_price":
                data["without_fuel_price"]= vehicle_price_obj.without_fuel_price,
            elif price_type == "with_fuel_price":
               data["with_fuel_price"]= vehicle_price_obj.with_fuel_price,
            return data
        except Exception as e:
            print(e)
            return None
       
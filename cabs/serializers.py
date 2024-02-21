from rest_framework import serializers
from cabs.models import *
from cab_booking_admin_api.serializers import CabBookingPriceSettingSerializer
from cab_booking_admin_api.serializers import CabBookingPriceSetting
class CabTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CabType
        fields = ('id', 'cab_type')
    

class CabClassSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    class Meta:
        model = CabClass
        fields = ['id', 'cab_type', 'cab_class', 'icon', 'price']
    
    def to_representation(self, instance):
        self.fields['cab_type'] = CabTypeSerializer(read_only=True)
        return super(CabClassSerializer, self).to_representation(instance)
    def get_price(self, obj):
        cab_id=obj.id
        cab_class_obj=CabClass.objects.get(id=cab_id)
        price=CabBookingPriceSetting.objects.filter(cab_class=cab_class_obj).values('id', 'price','platform_charge','cab_class')[0]
        return price

class VehicleLocationUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ['id', 'last_location','updated_at']


class VehicleMakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleMaker
        fields = ['id', 'maker', 'cab_type']
    def to_representation(self, instance):
        self.fields['cab_type'] = CabTypeSerializer(read_only=True)
        return super(VehicleMakerSerializer, self).to_representation(instance)

class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = ['id', 'maker', 'model', 'cab_class', 'model_image']
    
    def to_representation(self, instance):
        self.fields['maker'] = VehicleMakerSerializer(read_only=True)
        return super(VehicleModelSerializer, self).to_representation(instance)

class VehicaleDetailsSerializer(serializers.ModelSerializer):
    driver = serializers.HiddenField(
    default=serializers.CurrentUserDefault())
    # price = serializers.SerializerMethodField()
    class Meta:
        model = Vehicle
        exclude = ['is_approved',]
        include=['price',]

    def to_representation(self, instance):
        self.fields['maker'] = VehicleMakerSerializer(read_only=True)
        self.fields['model'] = VehicleModelSerializer(read_only=True)
        self.fields['cab_type'] = CabTypeSerializer(read_only=True)
        self.fields['cab_class'] = CabClassSerializer(read_only=True)
        # self.fields['price']=CabBookingPriceSettingSerializer(read_only=True)
        return super(VehicaleDetailsSerializer, self).to_representation(instance)
    
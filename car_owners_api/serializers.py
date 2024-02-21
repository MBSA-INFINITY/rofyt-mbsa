from rest_framework import serializers
from accounts.models import *
from car_owners_api.models import Car_Booking, Car_Owner_Vehicle, Car_Owner_Vehicle_Certificate, Car_Owner_Vehicle_Image
class UserOptAuthSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.filter(phone=data["phone"], is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")
        data["user"] = user
        return data


# class CarOwnerVehicleImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Car_Owner_Vehicle_Image
#         fields = '__all__'

# class CarOwnerVehicleCertificateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Car_Owner_Vehicle_Certificate
#         fields = '__all__'
# class CarOwnerVehicleSerializer(serializers.ModelSerializer):
#     vehicle_image=CarOwnerVehicleImageSerializer()
#     vehicle_certificate=CarOwnerVehicleCertificateSerializer()
#     class Meta:
#         model = Car_Owner_Vehicle
#         fields = ('id', 'vehicle_maker_id', 'vehicle_model_id', 'vehicle_plate_no', "vehicle_image", "vehicle_certificate")

# class CarOwnerProfileSerializer(serializers.ModelSerializer):


class CarOwnerProfileSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField()

    # def validate_email(self, value):
    #     lower_email = value.lower()
    #     instance = self.instance

    #     queryset = CarOwner.objects.filter(email__iexact=lower_email).exclude(pk=instance.pk if instance else None)
    #     if queryset.exists():
    #         raise serializers.ValidationError("Email ID already used!")
    #     return lower_email
    class Meta:
        model = CarOwner
        fields = ('id','first_name', 'last_name', 'photo_upload')


class GetCarOwnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarOwner
        fields = ['id','first_name', 'last_name', 'phone', 'email', 'birth_day', 'gender', 'photo_upload']


class GetCarBookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car_Booking
        fields = '__all__'
from django.db import models
from cabs.models import VehicleModel
from utility.model import BaseModel
# Create your models here.


class VehicleRentePriceSetting(BaseModel):
    model = models.ForeignKey(VehicleModel, on_delete=models.PROTECT)
    without_fuel_price = models.FloatField(default=0.0, verbose_name="without fuel vehicle rente price for per kms",)
    with_fuel_price = models.FloatField(default=0.0, verbose_name="with fuel vehicle rente price for per kms",)
    platform_charge=models.IntegerField(default=0, verbose_name="platform charge pasentage")
    tax_percentage=models.IntegerField(default=0, verbose_name="Tax Percentage")
    extra_kms_charge=models.IntegerField(default=0, verbose_name="Extra Charge for per kms",)
    class Meta:
        db_table = 'vehicle_rente_Price_setting'
    objects=models.Manager()
    def __str__(self):
        return self.model_name

class CitySetting(BaseModel):
    city_name=models.CharField(max_length=500, null=False, blank=False, unique=True)
    city_image=models.TextField(default="https://www.shutterstock.com/image-vector/indian-city-icon-bangalorevidhan-soudha-karnataka-1455972629")
    class Meta:
        db_table = 'city_setting'
    objects=models.Manager()
    def __str__(self):
        return self.city_name
    

class LocationsSetting(BaseModel):
    city=models.ForeignKey(CitySetting, on_delete=models.PROTECT)
    location=models.CharField(max_length=1000, null=False, blank=False)
    class Meta:
        db_table = 'locations_setting'
    objects=models.Manager()
    def __str__(self):
        return self.location


class CouponCodeSetting(BaseModel):
    coupon_code=models.CharField(max_length=15)
    coupon_discount=models.IntegerField()
    class Meta:
        db_table = 'car_rental_coupon_code_setting'
    objects=models.Manager()
    def __str__(self):
        return self.coupon_code
    

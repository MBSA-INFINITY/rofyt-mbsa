from django.db import models
from cabs.models import CabClass
from utility.model import BaseModel
from django.utils import timezone
# Create your models here.


class CabBookingPriceSetting(BaseModel):
    cab_class = models.ForeignKey(CabClass, on_delete=models.PROTECT,  blank=True, null=True)
    # model_name=models.CharField(max_length=500, blank=True,null=True)
    price = models.FloatField(default=0.0, verbose_name="cab booking price base on per kms")
    platform_charge=models.IntegerField(default=0)
    class Meta:
        db_table = 'cab_booking_price_setting'
    objects=models.Manager()
    def __str__(self):
        return self.price

def defualt_expire_date():
    return timezone.now() + timezone.timedelta(days=5)

class CabBookingCouponCodeSetting(BaseModel):
    coupon_code=models.CharField(max_length=15)
    coupon_discount=models.IntegerField()
    expire_date=models.DateTimeField(default=defualt_expire_date)
    image=models.TextField(default="https://jlp108-my-ride.s3.amazonaws.com/media/myride/8900044488/png-clipart-city-car-sports-car-computer-icons-vehicle-city-silhouette_BFKXiKM.png")
    class Meta:
        db_table = 'cab_booking_coupon_code_setting'
    objects=models.Manager()
    def __str__(self):
        return self.coupon_code
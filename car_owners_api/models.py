from django.db import models
from accounts.models import User,  CarOwner, Customer
from cabs.models import *
# Create your models here.



class Car_Owner_Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    vehicle_type=models.ForeignKey(CabType, on_delete=models.CASCADE, blank=True, null=True)
    vehicle_maker=models.ForeignKey(VehicleMaker, on_delete=models.CASCADE, blank=True, null=True)
    vehicle_model=models.ForeignKey(VehicleModel, on_delete=models.CASCADE, blank=True, null=True)
    vehicle_class = models.ForeignKey(CabClass, on_delete=models.CASCADE, blank=True, null=True)
    vehicle_plate_no=models.CharField(max_length=100,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    class Meta:
        db_table = 'car_owner_vehicle'
    objects=models.Manager()

class Car_Owner_Vehicle_Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  blank=True, null=True)
    # vehicle_id=models.CharField(max_length=500, null=True, blank=True)
    vehicle=models.ForeignKey(Car_Owner_Vehicle, on_delete=models.CASCADE, blank=True, null=True)
    vehicle_front_image=models.CharField(max_length=500, null=True, blank=True)
    vehicle_back_image=models.CharField(max_length=500, null=True, blank=True)
    vehicle_left_image=models.CharField(max_length=500, null=True, blank=True)
    vehicle_right_image=models.CharField(max_length=500, null=True, blank=True)
    driver_seat_image=models.CharField(max_length=500, null=True, blank=True)
    passager_seat_image=models.CharField(max_length=500, null=True, blank=True)
    front_head_light_image=models.CharField(max_length=500, null=True, blank=True)
    back_head_light_image=models.CharField(max_length=500, null=True, blank=True)
    class Meta:
        db_table = 'car_owner_vehicle_image'
    objects=models.Manager()

class Car_Owner_Vehicle_Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    # vehicle_id=models.CharField(max_length=500, null=True, blank=True)
    vehicle=models.ForeignKey(Car_Owner_Vehicle, on_delete=models.CASCADE, blank=True, null=True)
    insurance=models.CharField(max_length=500,null=True, blank=True)
    RC_book=models.CharField(max_length=500,null=True, blank=True)
    C_book=models.CharField(max_length=500,null=True, blank=True)
    class Meta:
        db_table = 'car_owner_vehicle_certificate'
    objects=models.Manager()

class Car_Booking(models.Model):
    car_owner=models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name='bookings_as_car_owner')
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings_as_customer')
    vehicle=models.ForeignKey(Car_Owner_Vehicle, on_delete=models.CASCADE)
    pick_up_locations=models.CharField(max_length=100, null=True, blank=True)
    drop_off_locations=models.CharField(max_length=100, null=True, blank=True)
    pick_up_data_time=models.DateTimeField()
    drop_up_date_time=models.DateTimeField()
    duration=models.CharField(max_length=100, null=True, blank=True)
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    CANCELED = 'Canceled'
    COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELED, 'Canceled'),
        (COMPLETED,'Completed')
    ]
    booking_status=models.CharField(max_length=100, choices=STATUS_CHOICES, default=PENDING)
    status_choices = (
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    )
    payment_status=models.CharField(max_length=10, choices=status_choices)
    applied_coupon=models.CharField(max_length=20,blank=True, null=True)
    coupon_discount_amount=models.FloatField(default=0.0)
    basic_price=models.FloatField(default=0.0)
    tax_amount=models.FloatField(default=0.0)
    payment_price=models.FloatField()
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    before_front = models.TextField(null=True, blank=True)
    before_back = models.TextField(null=True, blank=True)
    before_right = models.TextField(null=True, blank=True)
    before_left = models.TextField(null=True, blank=True)
    before_speedo_meter = models.TextField(null=True, blank=True)
    before_inside_car = models.TextField(null=True, blank=True)

    after_front = models.TextField(null=True, blank=True)
    after_back = models.TextField(null=True, blank=True)
    after_right = models.TextField(null=True, blank=True)
    after_left = models.TextField(null=True, blank=True)
    after_speedo_meter = models.TextField(null=True, blank=True)
    after_inside_car = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'car_booking'
    objects=models.Manager()


class Accident_Support(models.Model):
    vehicle=models.ForeignKey(Car_Owner_Vehicle, on_delete=models.CASCADE)
    vehicle_image=models.TextField(null=True, blank=True)
    vehicle_video=models.TextField(null=True, blank=True)
    description=models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'accident_support'
    objects=models.Manager()
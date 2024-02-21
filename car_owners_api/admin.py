from django.contrib import admin
from car_owners_api.models import Car_Owner_Vehicle,Car_Owner_Vehicle_Image,Car_Owner_Vehicle_Certificate,Car_Booking
# Register your models here.
admin.site.register(Car_Owner_Vehicle)
admin.site.register(Car_Owner_Vehicle_Image)
admin.site.register(Car_Owner_Vehicle_Certificate)
admin.site.register(Car_Booking)

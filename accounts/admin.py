from django.contrib import admin

# Register your models here.
from accounts.models import User, Driver, Customer, DriverPhoneVerify, CustomerPhoneVerify,CarOwnerPhoneVerify

admin.site.register(User)
admin.site.register(Driver)
admin.site.register(Customer)
admin.site.register(DriverPhoneVerify)
admin.site.register(CustomerPhoneVerify)
admin.site.register(CarOwnerPhoneVerify)

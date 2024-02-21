from rest_framework import serializers
from django.db.models import Q
from datetime import datetime
from accounts.models import User
from trips.models import Trip
from accounts.models import User, Driver

from cab_booking_api.models import *

class MessageSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message_Support
        fields = ['id', 'user', 'subject', 'message', 'created_at']


class CustomerSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = "Customer_Support"
        fields = ['id', 'cutomer', 'name','email', 'phone', 'message', 'created_at']
    
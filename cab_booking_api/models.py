from django.db import models

from utility.model import BaseModel
from django.utils import timezone
from accounts.models import User, Customer

# Create your models here.
class Message_Support(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject=models.CharField(max_length=1000)
    message=models.TextField()
    class Meta:
        db_table = 'message_support'
    objects=models.Manager()
    def __str__(self):
        return self.subject


class Customer_Suppport(BaseModel):
    cutomer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=16)
    email=models.EmailField()
    message=models.TextField()
    class Meta:
        db_table = 'cutomer_support'
    objects=models.Manager()
    def __str__(self):
        return self.name
from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone_number=  models.CharField(max_length=10,null=False,unique=True)
    def __str__(self):
        return "{} {}".format(self.user,self.phone_number)

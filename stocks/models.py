from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stock(models.Model):
    stockCode = models.CharField(max_length=20)
    companyName = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.companyName} ({self.stockCode})"

class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    startingFinance = models.IntegerField()

    

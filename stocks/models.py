from django.db import models

# Create your models here.
class Stock(models.Model):
    stockCode = models.CharField(max_length=20)
    companyName = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.companyName} ({self.stockCode})"
    

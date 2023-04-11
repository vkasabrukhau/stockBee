from django.contrib import admin
from .models import Stock, ExtendedUser

admin.site.register(Stock)
admin.site.register(ExtendedUser)
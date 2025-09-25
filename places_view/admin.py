from django.contrib import admin

# Register your models here.
from .models import User, Places, Location
admin.site.register(User)
admin.site.register(Places)
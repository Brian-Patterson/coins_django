from django.contrib import admin
from .models import Coins, Owner, Category
# Register your models here.

admin.site.register(Coins)
admin.site.register(Owner)
admin.site.register(Category)

from django.contrib import admin
from vending.models import VendingMachine, CoffeeOrder, CoffeeType

# Register your models here.
admin.site.register(VendingMachine)
admin.site.register(CoffeeOrder)
admin.site.register(CoffeeType)

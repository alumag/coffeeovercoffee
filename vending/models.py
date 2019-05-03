from django.db import models

# Create your models here.
class VendingMachine(models.Model):
    orders_counter = models.IntegerField(default=0, help_text="Orders counter")
    availability = models.BooleanField(default=True, help_text="Is the machine available?")


class CoffeeOrder(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.TextField(default="", max_length=30, blank=True, help_text="Customer name")

    def get_coffee_stream(self):
        pass

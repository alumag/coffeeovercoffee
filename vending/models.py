from django.db import models

# Create your models here.
class VendingMachine(models.Model):
    orders_counter = models.IntegerField(default=0, help_text="Orders counter")
    availability = models.BooleanField(default=True, help_text="Is the machine available?")


class CoffeeType(models.Model):
    name = models.TextField(primary_key=True, max_length=30, help_text="Coffee type name")
    available = models.BooleanField(default=True)
    code = models.TextField(default="", max_length=30, help_text="Coffee binary code")

    def repr(self):
        return self.name


class CoffeeOrder(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.TextField(default="", max_length=30, blank=True, help_text="Customer name")
    coffee = models.ForeignKey("CoffeeType", default=None, on_delete=models.PROTECT)

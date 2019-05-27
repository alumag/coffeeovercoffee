from django.shortcuts import render

from vending.models import VendingMachine, CoffeeOrder, CoffeeType
from vending.forms import OrderCoffeeForm

import serial

def encrypt(blob):
    hex_blob = int(blob, 16)
    lst = list()

    for _ in range(8):
        b = hex_blob & 0xff
        b = b ^ 0xca
        b = b ^ 0xfe
        lst.append(b)
        hex_blob = hex_blob >> 8

    return int("".join([hex(value)[2:] for value in arr[::-1]]), 16)


def write_packet(encrypted_hex):
    s = serial.Serial("/dev/ttyUSB0", 115200)
    s.write(encrypted_hex)
    s.close()


def create_order(form):
    data = form.cleaned_data
    order = CoffeeOrder(
        customer=data['customer_name'],
        coffee=data['coffee_type']
    )
    order.save()

    machine = VendingMachine.objects.all()[0]
    machine.orders_counter += 1
    machine.save()

    encrypted_coffee = encrypt(order.coffee.code)
    write_packet(encrypted_coffee)


def index(request):
    """View function for home page of site."""
    machine = VendingMachine.objects.all()[0]

    if request.method == 'POST':
        form = OrderCoffeeForm(request.POST)
        if form.is_valid():
            create_order(form)
    elif machine.availability:
        form = OrderCoffeeForm()
    else:
        form = None
    
    context = {
        "orders_count": machine.orders_counter,
        "form": form
    }
    
    return render(request, 'index.html', context=context)

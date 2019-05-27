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

    return int("".join([hex(value)[2:] for value in lst[::-1]]), 16)


def write_packet(encrypted_hex):
    # Send the data to the arduino
    s = serial.Serial("/dev/ttyUSB0", 115200)
    s.write(encrypted_hex)
    s.close()


def create_order(form):
    # Make order object
    data = form.cleaned_data
    order = CoffeeOrder(
        customer=data['customer_name'],
        coffee=data['coffee_type']
    )
    order.save()

    # Update the machine state
    machine = VendingMachine.objects.all()[0]
    machine.orders_counter += 1
    machine.availability = False
    machine.save()

    # Send the coffee request
    encrypted_coffee = encrypt(order.coffee.code)
    write_packet(encrypted_coffee)


def index(request):
    """View function for home page of site."""
    machine = VendingMachine.objects.all()[0]
    availability = machine.availability

    error = False

    if request.method == 'POST':
        form = OrderCoffeeForm(request.POST)
        if form.is_valid() and availability:
            create_order(form)
        else:
            error = True

    elif availability:
        # GET: make new order
        form = OrderCoffeeForm()

    else:
        # The machine is not ready
        form = None
        error = True
    
    context = {
        "orders_count": machine.orders_counter,
        "form": form,
        "machine_errors": error
    }
    
    return render(request, 'index.html', context=context)

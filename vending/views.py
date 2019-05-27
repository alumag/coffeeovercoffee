from django.shortcuts import render
from background_task import background

from vending.models import VendingMachine, CoffeeOrder, CoffeeType
from vending.forms import OrderCoffeeForm
from vending.utils import encrypt, write_packet

import logging
logger = logging.getLogger(__name__)


class MachineUnavailableError(Exception):
    pass


@background(schedule=60*3)
def unlock_machine():
    machine = VendingMachine.objects.all()[0]
    machine.availability = True
    machine.save()
    logger.info("Machine Unlocked")


def lock_machine():
    machine = VendingMachine.objects.all()[0]
    if not machine.availability:
        raise MachineUnavailableError()
    machine.availability = False
    machine.save()
    logger.info("Machine locked")


def _create_order_obj(data):
    order = CoffeeOrder(
        customer=data['customer_name'],
        coffee=data['coffee_type']
    )
    order.save()
    logger.info("Order created: {} by {}".format(order.coffee.code, order.customer))


def create_order(form):
    ## -- Critical section ##
    # FIRST: Turn machine unavailable
    lock_machine()
    ## -- Critical section end ##

    # Make order object
    _create_order_obj(form.cleaned_data)
    machine.orders_counter += 1
    machine.save()

    # Send the coffee request
    encrypted_coffee = encrypt(order.coffee.code)
    write_packet(encrypted_coffee)

    unlock_machine()


def index(request):
    """View function for home page of site."""
    machine = VendingMachine.objects.all()[0]
    availability = machine.availability
    counter = machine.orders_counter

    avl_error = False
    validation_error = False
    succeed = False

    # Form sent, machine is available
    if request.method == 'POST' and availability:
        form = OrderCoffeeForm(request.POST)
        if form.is_valid():
            try:
                create_order(form)
                succeed = True
            except MachineUnavailableError:
                avl_error = True
        else:
            validation_error = True
    # Form sent, machine not available
    elif request.method == 'POST' and not availability:
        form = OrderCoffeeForm(request.POST)
        avl_error = True
    # GET requests
    # Machine available
    elif availability:
        form = OrderCoffeeForm()
    # Machine is not available
    else:
        form = None
        avl_error = True
    
    context = dict(
        orders_count=counter, form=form, machine_error=avl_error,
        validation_error=validation_error, request_succeed=succeed
    )
    
    return render(request, 'index.html', context=context)

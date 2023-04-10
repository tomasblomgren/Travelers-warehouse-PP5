from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents

import stripe


def view_bag(request):
    """ A view to render the bag contents """
    return render(request, 'checkout/templates/checkout.html')


def favourites(request):
    """ A view to render the bag contents """

    favourites = Product.objects.all()
    return render(request, 'checkout/favourites.html')


def view_favourites(request):
    """ A view to render favourites """
    selected_items = request.POST.getlist('selected_items')
    context = {
        'checkout': checkout,
        'favourites': favourites,
        'selected_items': selected_items,
    }

    return render(request, 'checkout/favourites.html', context)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, 'Your bag is empty')
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    print(intent)

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51MUSoCEjEMHluTxVKcQRL8hlSlzdoqDZr3eLTj8txmslvIsiUlh5GI8ZuuAXlc24iI1FAPkr21i9RwjLxu6yFgz300C0BnMtqe',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)

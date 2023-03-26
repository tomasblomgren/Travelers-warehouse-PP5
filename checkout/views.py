from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


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
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, 'Your bag is empty')
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
    }

    return render(request, template, context)
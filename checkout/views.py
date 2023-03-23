from django.shortcuts import render


def view_bag(request):
    """ A view to render the bag contents """
    return render(request, 'checkout/templates/checkout.html')


def favourites(request):
    """ A view to render the bag contents """

    favourites = Product.objects.all()
    return render(request, 'checkout/favourites.html')


def view_favourites(request):
    """ A view to render favourites """
    context = {
        'checkout': checkout,
        'favourites': favourites,
    }

    return render(request, 'favourites.html', context)


def view_template_favourites(request):
    """ a view to get the checked favourite product to the favourites """
    selected_items = request.POST.getlist('selected_items')
    context = {'selected_items': selected_items}
    return render(request, 'view_template_favourites', context)


def checkout(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        city = request.POST['city']
        country = request.POST['country']
        zip_code = request.POST['zip']
        cardnumber = request.POST['cardnumber']
        expiry = request.POST['expiry']
        cvv = request.POST['cvv']

        if not name or not email or not address or not city or not country or not zip_code or not cardnumber or not expiry or not cvv:
            checkout_error = "Please fill out all fields."
        elif not validate_email(email):
            checkout_error = "Please enter a valid email address."
        elif not validate_cardnumber(cardnumber):
            checkout_error = "Please enter a valid card number."
        elif not validate_expiry(expiry):
            checkout_error = "Please enter a valid expiry date in the format MM/YY."
        elif not validate_cvv(cvv):
            checkout_error = "Please enter a valid CVV code."
        else:
            # Process payment and complete order
            return render(request, 'checkout_success.html')

        return render(request, 'checkout.html', {'checkout_error'})

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Favourite, Order

# Create your views here.


def all_products(request):
    """ A view to show all products including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:

            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show all products including sorting and search queries """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_to_favourites(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    favourite, created = Favourite.objects.get_or_create(user=request.user, product=product)
    if created:
        message = "Added to favourites"
    else:
        message = "Already in favourites"
    return redirect('product_detail', pk=product.pk, message=message)


@login_required
def remove_from_favourites(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    favourite = get_object_or_404(Favourite, user=request.user, product=product)
    favourite.delete()
    message = "Removed from favourites"
    return redirect('product_detail', pk=product.pk, message=message)


@login_required
def favourites_list(request):
    favourites = Favourite.objects.filter(user=request.user)
    return render(request, 'favourites.html', {'favourites': favourites})


def extra_sales(request):
    top_products = Product.objects.annotate(total_sales=Sum('order__quantity')).order_by('-total_sales')[:10]
    total_sales = Order.objects.filter(status__in=['C', 'S', 'D']).aggregate(total_sales=Sum('quantity'))['total_sales'] or 0
    return render(request, 'extra_sales.html', {'top_products': top_products, 'total_sales': total_sales})

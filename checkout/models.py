import uuid

from django.db import models
from django.core.validators import EmailValidator, RegexValidator, MinLengthValidator, MaxLengthValidator
from django.db.models import Sum
from django.conf import settings

from products.models import Product


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, validators=[EmailValidator()])
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10, validators=[RegexValidator('^[0-9]{5}(?:-[0-9]{4})?$')])


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20, validators=[RegexValidator('^[0-9]{13,19}$')])
    expiry = models.CharField(max_length=5, validators=[RegexValidator('^(0[1-9]|1[0-2])\/([0-9]{2})$')])
    cvv = models.CharField(max_length=4, validators=[RegexValidator('^[0-9]{3,4}$')])


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=50, null=False, blank=False)
    country = models.CharField(max_length=50, null=False, blank=False)
    postcode = models.CharField(max_length=50, null=True, blank=True)
    town_or_city = models.CharField(max_length=50, null=False, blank=False)
    street_adress1 = models.CharField(max_length=50, null=False, blank=False)
    street_adress2 = models.CharField(max_length=50, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def _generate_order_number(self):
        """ 
        generates random order number from uuid
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum']
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()


class OrderLineItem(models.Model):
    Order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, editable=False)


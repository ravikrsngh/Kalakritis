from django.db import models
from products.models import *
from user.models import *
from django.utils.html import mark_safe


class Wishlist(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name = "wishlist_products")
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Cart(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    size = models.CharField(max_length=5)
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.user.email


class CouponCodes(models.Model):
    name = models.CharField(max_length=8)
    discount_perecent = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    orderID = models.CharField(max_length=10)
    paymentID = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    country = models.CharField(max_length=30, default="India")
    state = models.CharField(max_length=30)
    address_line1 = models.CharField(max_length=120)
    city = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    subtotal = models.IntegerField(default=0)
    coupon_name = models.CharField(max_length=8, default="XXXX")
    coupon_discount = models.IntegerField(default=0)
    delivery_charges = models.IntegerField(default=0)
    tax = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name = "Date")
    no_of_items = models.IntegerField(default=0)
    payment_type_details = models.TextField(null=True)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return self.orderID


class OrderProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE, related_name="ordered_products")
    qty = models.IntegerField(default=0, verbose_name="Quantity")
    size = models.CharField(max_length=5, default='')
    color = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.order.orderID

    @property
    def image(self):
        product_image = ProductImages.objects.filter(product=self.product).first()
        if product_image.img:
            return mark_safe('<img src="{}" width="100" />'.format(product_image.img.url))
        return ""

    @property
    def title(self):
        return self.product.title

    @property
    def sku(self):
        return self.product.sku

    @property
    def color_bg(self):
        return mark_safe(f"<span style=\"background:#{self.color};color:white;padding:5px 30px;margin:5px 0px;border-radius:5px;\"></span>")

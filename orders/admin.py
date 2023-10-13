from django.contrib import admin
from .models import *
from django.urls import path,include
from django.db.models.functions import Cast
from django.http import HttpResponse
import decimal, csv


class OrderedProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    verbose_name = "Ordered Product"
    verbose_name_plural = "Ordered Products"
    fields = ('sku','image','title','quantity','size','color_bg')
    readonly_fields = ('sku','image','title','quantity','size','color_bg')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False



class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderedProductInline]
    readonly_fields = ('orderID','paymentID','subtotal','coupon_applied','coupon_discount','delivery_charges','tax','total')
    search_fields = ['orderID','paymentID','coupon_applied','ship_to_name','ship_to_email']
    list_display = ['orderID','paymentID','ship_to_name','total']
    list_filter = ('created_date',)
    fieldsets = (
        ('Order Details', {
            'fields': ('orderID','paymentID','subtotal','coupon_applied','coupon_discount','delivery_charges','tax','total')
        }),
        ('Shipping Details', {
            'fields': ('ship_to_name','ship_to_email' ,'ship_to_phonenumber', 'ship_to_address1','ship_to_country','ship_to_state','ship_to_city','ship_to_zip')
        })
    )


admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(CouponCodes)

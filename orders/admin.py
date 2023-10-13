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
    fields = ('sku','image','title','qty','size','color_bg')
    readonly_fields = ('sku','image','title','qty','size','color_bg')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False



class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderedProductInline]
    readonly_fields = ('orderID','paymentID','subtotal','coupon_name','coupon_discount','delivery_charges','tax','total')
    search_fields = ['orderID','paymentID','coupon_name','name','email']
    list_display = ['orderID','paymentID','name','total']
    list_filter = ('created_date',)
    fieldsets = (
        ('Order Details', {
            'fields': ('orderID','paymentID','subtotal','coupon_name','coupon_discount','delivery_charges','tax','total')
        }),
        ('Shipping Details', {
            'fields': ('name','email' ,'phone_number', 'address_line1','country','state','city','zipcode')
        })
    )


admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(CouponCodes)

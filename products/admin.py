from django.contrib import admin
from .models import *
from django.utils.html import mark_safe
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.urls import path,include
from django.db.models import F,OuterRef, Subquery, IntegerField, Sum,FloatField,ExpressionWrapper,Q,Case,When
from django.db.models.functions import Cast
from django.http import HttpResponse
import decimal, csv
from django_summernote.admin import SummernoteModelAdmin
import os
import zipfile
import tempfile
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


class ProductImageInline(admin.TabularInline):
    model = ProductImages
    extra = 0
    readonly_fields = ('img_preview',)


class ProductAdmin(SummernoteModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('sku','title', 'cost_price', 'selling_price', 'product_type')
    search_fields = ['sku','title', 'product_type__name','tags__name']
    summernote_fields = ('description','shipping_details','return_details','product_care')
    filter_horizontal = ('tags','colors','sizes')
    list_filter = ('product_type','tags','colors','sizes')


    fieldsets = (
        ('Product Info', {
            'fields': ('sku','title','product_type','colors','sizes','cost_price','selling_price','description','shipping_details','return_details','product_care','avg_rating', 'total_reviews','tags')
        }),
    )

    # def tag(self,instance):
    #     str = """"""
    #     for i in instance.tags.all():
    #         str += "<span style=\"background:#6c757d;color:white;padding:5px 10px;margin:5px 0px;border-radius:5px;\">"+i.name+"</span>"
    #     return mark_safe("<div style=\"display:flex;gap:5px;flex-wrap:wrap;\">"+str+"</div>")
    #
    # def tag(self,instance):
    #     str = """"""
    #     for i in instance.tags.all():
    #         str += "<span style=\"background:#6c757d;color:white;padding:5px 10px;margin:5px 0px;border-radius:5px;\">"+i.name+"</span>"
    #     return mark_safe("<div style=\"display:flex;gap:5px;flex-wrap:wrap;\">"+str+"</div>")
    #
    # def tag(self,instance):
    #     str = """"""
    #     for i in instance.tags.all():
    #         str += "<span style=\"background:#6c757d;color:white;padding:5px 10px;margin:5px 0px;border-radius:5px;\">"+i.name+"</span>"
    #     return mark_safe("<div style=\"display:flex;gap:5px;flex-wrap:wrap;\">"+str+"</div>")

    # def get_urls(self):
    #     urls = super().g et_urls()
    #     my_urls = [
    #         path('upload_product_sheet/', self.upload_product_sheet),
    #         path('upload_product_images/', self.upload_product_images),
    #     ]
    #     return my_urls + urls
    #
    # def upload_product_sheet(self,request):
    #     import random
    #     if request.method == "POST":
    #         print("POST Method Called")
    #         file = request.FILES['product_excel']
    #         df = pd.read_excel(file,sheet_name = 0)
    #         shop_for = FilterOptions.objects.get(id=1)
    #         materials= FilterOptions.objects.get(id=2)
    #         weight_ranges = FilterOptions.objects.get(id=3)
    #         metal = FilterOptions.objects.get(id=4)
    #         non_display = FilterOptions.objects.get(id=5)
    #         all_cols = list(df.columns)
    #         tag_start = all_cols.index('Short Description') + 1
    #         print(tag_start)
    #         for index, row in df.iterrows():
    #             category = Category.objects.get_or_create(name=row[2])[0]
    #             print("---------")
    #             print(row[5])
    #             all_tags = [
    #                 FilterOptionItems.objects.get_or_create(filter=shop_for,name=row[3])[0],
    #                 FilterOptionItems.objects.get_or_create(filter=weight_ranges, name=row[5])[0],
    #                 FilterOptionItems.objects.get_or_create(filter=metal,name=str(row[6] + " Gold"))[0],
    #                 FilterOptionItems.objects.get_or_create(filter=metal,name=str(row[7] + " Diamond"))[0],
    #             ]
    #
    #             if "Gold" in row[4] and "Diamond" in row[4]:
    #                 all_tags.append(FilterOptionItems.objects.get_or_create(filter=materials,name="Gold")[0])
    #                 all_tags.append(FilterOptionItems.objects.get_or_create(filter=materials,name="Diamond")[0])
    #             elif "Gold" in row[4]:
    #                 all_tags.append(FilterOptionItems.objects.get_or_create(filter=materials,name="Gold")[0])
    #             elif "Diamond" in row[4]:
    #                 all_tags.append(FilterOptionItems.objects.get_or_create(filter=materials,name="Diamond")[0])
    #
    #             choice_list = ["Yes","No"]
    #             for i in range(tag_start,len(all_cols)):
    #                 if random.choice(choice_list) == "Yes":
    #                     all_tags.append(FilterOptionItems.objects.get_or_create(filter=non_display,name=all_cols[i])[0])
    #             print(row[12])
    #             print(row[13])
    #             if Product.objects.filter(stock_number=row[0].strip()).exists():
    #                 print("Updating " + row[0])
    #                 Product.objects.filter(stock_number=row[0].strip()).update(
    #                     stock_number = row[0].strip(),
    #                     title = row[1],
    #                     category = category,
    #                     gold_purity = GoldPurity.objects.get_or_create(name=row[6])[0],
    #                     diamond_purity = DiamondPurity.objects.get_or_create(name=row[7])[0],
    #                     gross_weight = row[8],
    #                     net_weight = row[9],
    #                     gold_weight = row[10],
    #                     diamond_weight = row[11],
    #                     stone_weight=row[12],
    #                     stone_price = int(row[13]),
    #                     short_description = row[18],
    #                     long_description = "-",
    #                     return_details = "-",
    #                     shipping_details="-",
    #                     height="-",
    #                     width="-",
    #                 )
    #                 obj = Product.objects.filter(stock_number=row[0]).first()
    #                 for i in all_tags:
    #                     obj.tags.add(i)
    #                     obj.save()
    #             else:
    #                 print("Creating " + row[0])
    #                 obj = Product.objects.create(
    #                     stock_number = row[0].strip(),
    #                     title = row[1],
    #                     category = category,
    #                     gold_purity = GoldPurity.objects.get_or_create(name=row[6])[0],
    #                     diamond_purity = DiamondPurity.objects.get_or_create(name=row[7])[0],
    #                     gross_weight = row[8],
    #                     net_weight = row[9],
    #                     gold_weight = row[10],
    #                     diamond_weight = row[11],
    #                     stone_weight=row[12],
    #                     stone_price = int(row[13]),
    #                     short_description = row[18],
    #                     long_description = "-",
    #                     return_details = "-",
    #                     shipping_details="-",
    #                     height="-",
    #                     width="-",
    #                 )
    #                 for i in all_tags:
    #                     obj.tags.add(i)
    #                     obj.save()
    #
    #     return redirect('/admin/products/product/')
    #
    # def upload_product_images(self,request):
    #     # if request.method == 'POST' and request.FILES:
    #     #     # Get the uploaded zip file
    #     #     zip_file = request.FILES['product_images']
    #     #     with zipfile.ZipFile(zip_file) as zf:
    #     #         # Iterate over all the folders in the zip file
    #     #
    #     #         print(zf.namelist())
    #     #         for filename in zf.namelist():
    #     #             filename_parts = filename.split("/")
    #     #             print(filename_parts)
    #     #             if filename_parts[2].lower().endswith('.jpg') or filename_parts[2].lower().endswith('.png'):
    #     #                 with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
    #     #                     tmp_file.write(zf.read(filename))
    #     #                     tmp_file.flush()
    #     #                     # Create a new product object with the image file
    #     #                     try:
    #     #                         product = Product.objects.filter(stock_number__icontains=filename_parts[1]).first()
    #     #                         obj = ProductImages()
    #     #                         obj.product = product
    #     #                         obj.img.save('-'.join([filename_parts[1],filename_parts[2]]),File(tmp_file))
    #     #                         obj.save()
    #     #                         print(obj)
    #     #                     except Exception as e:
    #     #                         print(e)
    #     #                     tmp_file.close()
    #
    #     return redirect('/admin/products/product/')
    #
    # def export(self, request, queryset):
    #     response = HttpResponse(content_type='text/csv')
    #     response['Content-Disposition'] = 'attachment; filename="products.csv"'
    #     writer = csv.writer(response)
    #     writer.writerow(["SKU","Title","MRP","Selling Price","Short Description","Average Rating","Total Reviews","Category","Gold Purity","Current Gold Price","Diamond Purity","Current Diamond Price","Gross Weight","Net Weight","Gold Weight","Diamond Weight","Height","Width"])
    #     print(len(queryset))
    #     product_list = queryset.values_list("stock_number","title","mrp","selling_price","short_description","avg_rating","total_reviews","category__name","gold_purity__name","gold_purity__price","diamond_purity__name","diamond_purity__price","gross_weight","net_weight","gold_weight","diamond_weight","height","width")
    #     for i in product_list:
    #         writer.writerow(i)
    #     return response
    #
    # def set_prices(self, request, queryset):
    #     Product.objects.update(
    #
    #         making_charges_gold = Subquery(
    #         Product.objects.filter(id=OuterRef('id')).annotate(
    #         gp=ExpressionWrapper(
    #             Cast(Case(
    #                 When(
    #                     gold_purity__isnull = True,
    #                     then=0
    #                 ),
    #                 default=Sum(F('gold_purity__making_charges')*Cast(F('net_weight'), output_field=FloatField()), output_field=IntegerField()),
    #             ),
    #             output_field=IntegerField()
    #             ),
    #             output_field=IntegerField()
    #         )).values('gp')[:1]),
    #
    #         making_charges_diamond = Subquery(
    #         Product.objects.filter(id=OuterRef('id')).annotate(
    #         gp=ExpressionWrapper(
    #             Cast(Case(
    #                 When(
    #                     gold_purity__isnull = False,
    #                     then=0
    #                 ),
    #                 default=Sum(F('diamond_purity__making_charges')*Cast(F('net_weight'), output_field=FloatField()), output_field=IntegerField()),
    #             ),
    #             output_field=IntegerField()
    #             ),
    #             output_field=IntegerField()
    #         )).values('gp')[:1]),
    #
    #         gold_price = Subquery(
    #         Product.objects.filter(id=OuterRef('id')).annotate(
    #         gp=ExpressionWrapper(
    #             Cast(Case(
    #                 When(
    #                     gold_purity__isnull = True,
    #                     then=0
    #                 ),
    #                 default=Sum(F('gold_purity__price')*Cast(F('net_weight'), output_field=FloatField()),output_field=IntegerField()),
    #             ),
    #             output_field=IntegerField()
    #             ),
    #             output_field=IntegerField()
    #         )).values('gp')[:1]),
    #
    #         diamond_price = Subquery(
    #         Product.objects.filter(id=OuterRef('id')).annotate(
    #         gp=ExpressionWrapper(
    #             Cast(Case(
    #                 When(
    #                     diamond_purity__isnull = True,
    #                     then=0
    #                 ),
    #                 default=Sum(F('diamond_purity__price')*Cast(F('diamond_weight'), output_field=FloatField()),output_field=IntegerField()),
    #             ),
    #             output_field=IntegerField()
    #             ),
    #             output_field=IntegerField()
    #         )).values('gp')[:1])
    #
    #     )
    #
    #     Product.objects.update(
    #         making_charges = (F('making_charges_gold') + F('making_charges_diamond')),
    #         subtotal = (F('gold_price') + F('diamond_price')+F('making_charges_gold') + F('making_charges_diamond') + F('stone_price')),
    #         tax = Cast((F('gold_price') + F('diamond_price') + F('making_charges_gold') + F('making_charges_diamond') + F('stone_price'))*3/100,output_field=IntegerField()),
    #     )
    #     Product.objects.update(
    #         mrp = F('subtotal') + F('tax')
    #     )
    #     Product.objects.update(
    #         selling_price = F('mrp')
    #     )
    #     pass
    #
    # actions = [export, set_prices ]
    #
    # class Media:
    #     css = {
    #         "all": ("products/products_changelist.css",)
    #     }
    #     js = ("products/products_changelist.js",)


admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImages)
admin.site.register(ProductTypes)
admin.site.register(Colors)
admin.site.register(Tags)
admin.site.register(Sizes)

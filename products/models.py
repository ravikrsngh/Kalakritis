from django.db import models
from django.utils.html import mark_safe
from django.db.models.signals import pre_delete, post_delete, post_save, pre_save
from user.models import CustomUser

class Sizes(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"


class Colors(models.Model):
    name = models.CharField(max_length=20)
    hash_value = models.CharField(max_length=7)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"


class Tags(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class ProductTypes(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Type"
        verbose_name_plural = "Product Types"


class Product(models.Model):
    sku = models.CharField(max_length=10, unique=True, null=True)
    title = models.CharField(max_length=50)
    cost_price = models.IntegerField(default=0)
    selling_price = models.IntegerField(default=0)
    product_type = models.ForeignKey(ProductTypes,on_delete=models.CASCADE)
    colors = models.ManyToManyField(Colors)
    sizes = models.ManyToManyField(Sizes)
    description = models.TextField()
    features = models.TextField()
    shipping_details = models.TextField()
    return_details = models.TextField()
    product_care = models.TextField()
    avg_rating = models.IntegerField(default=0)
    total_reviews = models.IntegerField(default=0)
    on_discount = models.BooleanField(default=False)
    discount_value = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tags)


    def __str__(self):
        return self.title

    @staticmethod
    def autocomplete_search_fields():
        return 'title',

    @property
    def tags_list_str(self):
        tags_list = [i.name for i in self.tags.all()]
        return ",".join(tags_list)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"





def productimage_directory_path(instance,filename):
    return 'media/ProductImages/{0}/{1}'.format(instance.product.sku, filename)

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_images')
    img = models.ImageField(upload_to = productimage_directory_path,null=True,blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.product.title

    @property
    def img_preview(self):
        if self.img:
            return mark_safe('<img src="{}" width="100" />'.format(self.img.url))
        return ""

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"


class Review(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name="product_reviews")
    review = models.CharField(max_length=150)
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.product.sku

    class Meta:
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"


def reviewimage_directory_path(instance,filename):
    return 'media/ReviewImages/{0}/{1}'.format(instance.review.product.sku, filename)


class ReviewImages(models.Model):
    review = models.ForeignKey(Review,on_delete=models.CASCADE)
    img = models.ImageField(upload_to = reviewimage_directory_path)

    def __str__(self):
        return self.review.product.sku

    class Meta:
        verbose_name = "Product Review Images"
        verbose_name_plural = "Product Review Images"

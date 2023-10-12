from rest_framework import routers
from django.urls import path,include
from .apis import *


router = routers.SimpleRouter()
router.register(r'cart', CartAPI)
router.register(r'wishlist', WishlistAPI)
router.register(r'payment', PhonePeAPI, basename='payment')
urlpatterns = router.urls

from rest_framework import routers
from django.urls import path,include
from .apis import *


router = routers.SimpleRouter()
router.register(r'products', ProductAPI)
urlpatterns = router.urls

from rest_framework import routers
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .apis import *


router = routers.SimpleRouter()
router.register(r'users', UserAPI)
router.register(r'usersaddress', UserAddressAPI)
urlpatterns = [
    path('users/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns += router.urls

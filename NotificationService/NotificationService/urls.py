from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from mailingsapp.tasks import *
from mailingsapp.views import *

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'mailings', MailingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

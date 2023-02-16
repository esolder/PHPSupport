"""phpsupport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from controller import views
from django.views.generic import RedirectView

router = routers.DefaultRouter()
router.register(r'orders', views.OrderViewSet)
router.register(r'clients', views.OrderViewSet)
router.register(r'executors', views.OrderViewSet)
router.register(r'rates', views.OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('client/', include('client_bot.urls'), name='client'),
    path('executor/', include('executor_bot.urls'), name='executor'),

    path('', include(router.urls)),
    # TODO: removed after tests
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('', RedirectView.as_view(url='/admin/', permanent=True)),
]


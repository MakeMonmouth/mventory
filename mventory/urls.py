"""mventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from inventory import views

router = routers.DefaultRouter()
router.register(r'buildings', views.BuildingViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'storage_units', views.StorageUnitViewSet)
router.register(r'storage_bins', views.StorageBinViewSet)
router.register(r'components', views.ComponentViewSet)
router.register(r'component_measurements', views.ComponentMeasurementUnitViewSet)

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('rest/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('django_prometheus.urls'))

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

from django.shortcuts import render

# Create your views here.
from .models import Building, Room, StorageUnit, StorageBin, Component, ComponentMeasurementUnit, Supplier
from rest_framework import viewsets, permissions, filters
from inventory.serializers import (
        BuildingSerializer,
        RoomSerializer,
        StorageUnitSerializer,
        StorageBinSerializer,
        ComponentSerializer,
        ComponentMeasurementUnitSerializer,
        SupplierSerializer
        )


def index(request):
    return render(request, 'index.html')

class BuildingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Building.objects.all().order_by('name')
    search_fields = ['name', 'address', 'postcode']
    filter_backends = (filters.SearchFilter,)
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Room.objects.all()
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class StorageUnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = StorageUnit.objects.all()
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    serializer_class = StorageUnitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class StorageBinViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = StorageBin.objects.all()
    search_fields = ['name', 'short_code']
    filter_backends = (filters.SearchFilter,)
    serializer_class = StorageBinSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ComponentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Component.objects.all()
    search_fields = ["name", "sku", "upc"]
    serializer_class = ComponentSerializer


class ComponentMeasurementUnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ComponentMeasurementUnit.objects.all()
    serializer_class = ComponentMeasurementUnitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SupplierViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows suppliers to be viewed or edited.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

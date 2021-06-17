from django.shortcuts import render

# Create your views here.
from .models import Building, Room, StorageUnit, StorageBin, Component, ComponentMeasurementUnit
from rest_framework import viewsets, permissions, filters
from inventory.serializers import (
        BuildingSerializer,
        RoomSerializer,
        StorageUnitSerializer,
        StorageBinSerializer,
        ComponentSerializer,
        ComponentMeasurementUnitSerializer
        )


def index(request):
    return render(request, 'index.html')

class BuildingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Building.objects.all().order_by('name')
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]


class StorageUnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = StorageUnit.objects.all()
    serializer_class = StorageUnitSerializer
    permission_classes = [permissions.IsAuthenticated]


class StorageBinViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = StorageBin.objects.all()
    serializer_class = StorageBinSerializer
    permission_classes = [permissions.IsAuthenticated]


class ComponentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    filter_backends = (filters.SearchFilter,)
    permission_classes = [permissions.IsAuthenticated]
    queryset = Component.objects.all()
    search_fields = ["name", "product_code"]
    serializer_class = ComponentSerializer


class ComponentMeasurementUnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ComponentMeasurementUnit.objects.all()
    serializer_class = ComponentMeasurementUnitSerializer
    permission_classes = [permissions.IsAuthenticated]

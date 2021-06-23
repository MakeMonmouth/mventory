from .models import Building, Room, StorageUnit, StorageBin, Component, ComponentMeasurementUnit
from rest_framework import serializers


class BuildingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Building
        fields = ['url', 'name', 'address', 'postcode']


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ['url', 'name', 'building']

class StorageUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StorageUnit
        fields = ['url', 'name', 'room']

class StorageBinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StorageBin
        fields = ['url', 'name', 'short_code', 'unit_row','unit_column', 'storage_unit']

class ComponentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Component
        fields = ['url', 'name', 'sku', 'mpn', 'upc', 'storage_bin','measurement_unit', 'qty']

class ComponentMeasurementUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComponentMeasurementUnit
        fields = ['url', 'name', 'description']

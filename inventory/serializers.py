from .utils import OctopartClient
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
    octopart_data = serializers.SerializerMethodField()

    def get_octopart_data(self, obj):
        op_data = {}
        if obj.mpn is not None:
            oc = OctopartClient()
            parts_res = oc.match_mpns([obj.mpn])
            op_data["hits"] = parts_res[0]["hits"]
            for doc in parts_res[0]["parts"][0]["document_collections"][0]["documents"]:
                if doc["name"] == "Datasheet":
                    op_data["datasheet_url"] = doc["url"]
                else:
                    op_data["datasheet_url"] = None
        return op_data

    class Meta:
        model = Component
        fields = ['url', 'name', 'sku', 'mpn', 'upc', 'octopart_data', 'storage_bin','measurement_unit', 'qty']
        depth = 4

class ComponentMeasurementUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComponentMeasurementUnit
        fields = ['url', 'unit_name', 'unit_description']

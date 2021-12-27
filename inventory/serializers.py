import os
import logging
from .utils import OctopartClient
from .models import Building, Room, StorageUnit, StorageBin, Component, ComponentMeasurementUnit
from rest_framework import serializers

# Get an instance of a logger
logger = logging.getLogger(__name__)

class BuildingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Building
        fields = ['url', 'name', 'address', 'postcode']
        logger.info("Serialising Buildings")


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ['url', 'name', 'building']
        logger.info("Serialising Rooms")

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
        if os.getenv("MVENTORY_OCTOPART_API_KEY"):
            if obj.mpn is not None:
                logger.debug(f"Found Octopart API Key and MPN, retrieving data for {obj.name}")
                oc = OctopartClient()
                parts_res = oc.match_mpns([obj.mpn])
                if parts_res != {}:
                    op_data["hits"] = parts_res[0]["hits"]
                    if op_data["hits"] > 0:
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

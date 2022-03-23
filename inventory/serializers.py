import os
from .utils import OctopartClient
from .models import Building, Room, StorageUnit, StorageBin, Component, ComponentMeasurementUnit, ComponentSupplier, Supplier
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

class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = ['url', 'name', 'description']

class ComponentSerializer(serializers.HyperlinkedModelSerializer):
    octopart_data = serializers.SerializerMethodField()
    component_prices = serializers.SerializerMethodField()

    def get_octopart_data(self, obj):
        op_data = {}
        if os.getenv("MVENTORY_OCTOPART_API_KEY"):
            if obj.mpn is not None:
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

    def get_component_prices(self, obj):
        prices = []

        for supplier in obj.supplier_options.all():
            suppliers = serializers.HyperlinkedRelatedField(
                view_name='suppliers',
                lookup_field='supplier',
                read_only=True
            )
            details = {}
            details['supplier'] = supplier.name
            cs_details = ComponentSupplier.objects.get(supplier=supplier, component=obj)
            details['price'] = cs_details.members_price
            details['currency'] = cs_details.currency
            details['included_donation_amount'] = cs_details.members_price - cs_details.bought_at
            prices.append(details)

        return prices

    class Meta:
        model = Component
        fields = ['url', 'name', 'sku', 'mpn', 'upc', 'octopart_data', 'storage_bin','measurement_unit', 'qty', 'component_prices']
        depth = 4

class ComponentMeasurementUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComponentMeasurementUnit
        fields = ['url', 'unit_name', 'unit_description']

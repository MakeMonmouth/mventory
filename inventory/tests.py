from django.test import TestCase
from django.test import Client
from rest_framework.test import APIClient
from inventory import models

class RestComponentTest(TestCase):
    def setUp(self):
        test_building = models.Building.objects.create(
                name="My Building",
                address="My Street",
                postcode="MY01 1BD"
                )
        test_room = models.Room.objects.create(
                name="My Room",
                building=test_building
                )
        test_su = models.StorageUnit.objects.create(
                name="My Storage Unit",
                room = test_room
                )
        test_sb = models.StorageBin.objects.create(
                name="My Storage Bin",
                storage_unit = test_su
                )
        test_mu = models.ComponentMeasurementUnit.objects.create(
                unit_name="cm",
                unit_description="Centimetres"
                )
        test_com = models.Component.objects.create(
                name="My First Component",
                measurement_unit = test_mu,
                sku = "mfc-000001",
                upc = "123456789101",
                mpn = "NHD-C128128BZ-FSW-GBW",
                qty = 12
                )
        test_com.storage_bin.add(test_sb)

        # Every test needs a client.
        self.apiclient = APIClient()
        self.client = Client()

    def test_rest_root(self):
        # Issue a GET request.
        response = self.client.get('/rest/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_rest_component(self):
        apiresponse = self.apiclient.get('/rest/components/1/')
        component = apiresponse.data

        # Check that the component is returned correctly
        self.assertEqual(component['name'], "My First Component")

#    def test_octopart_api(self):
#        apiresponse = self.apiclient.get('/rest/components/1/')
#        component = apiresponse.data
#
#        # Check that we have a hit on the octopart API
#        self.assertEqual(component["octopart_data"]["hits"], 1)
#        # Check that we have a datasheet url
#        self.assertEqual(component["octopart_data"]["datasheet_url"], "https://datasheet.octopart.com/NHD-C128128BZ-FSW-GBW-Newhaven-Display-datasheet-13083747.pdf")

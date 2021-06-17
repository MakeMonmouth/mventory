from django.test import TestCase
from django.test import Client
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

        # Every test needs a client.
        self.client = Client()

    def test_rest_root(self):
        # Issue a GET request.
        response = self.client.get('/rest/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

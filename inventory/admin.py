from django.contrib import admin

# Register your models here.
from .models import (ComponentMeasurementUnit,
                    Building,
                    Room,
                    StorageUnit,
                    StorageBin,
                    Component)

admin.site.register(ComponentMeasurementUnit)
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(StorageUnit)
admin.site.register(StorageBin)
admin.site.register(Component)

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from apps.comercial import models


class TruckBrandAdmin(ImportExportModelAdmin):
    list_display = ('name',)


admin.site.register(models.TruckBrand, TruckBrandAdmin)


class TruckModelAdmin(ImportExportModelAdmin):
    list_display = ('name', 'truck_brand')


admin.site.register(models.TruckModel, TruckModelAdmin)


class OwnerAdmin(ImportExportModelAdmin):
    list_display = ('name',)


admin.site.register(models.Owner, OwnerAdmin)


class TruckAdmin(ImportExportModelAdmin):
    list_display = ('license_plate', 'truck_model', 'drive_type', 'owner', 'is_active')
    list_filter = ('drive_type', 'is_active', 'fuel_type')
    search_fields = ('license_plate',)


admin.site.register(models.Truck, TruckAdmin)


class ProgrammingAdmin(ImportExportModelAdmin):
    list_display = ('id', 'departure_date', 'service_type', 'status', 'truck', 'subsidiary')
    list_filter = ('service_type', 'status', 'departure_date')
    search_fields = ('truck__license_plate', 'correlative', 'serial')


admin.site.register(models.Programming, ProgrammingAdmin)

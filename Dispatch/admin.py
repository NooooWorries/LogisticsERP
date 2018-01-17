from django.contrib import admin
from Dispatch.models import DispatchRecord, Driver


class TagInline(admin.TabularInline):
    model = DispatchRecord, Driver


class DriverAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "identity_number", "birthday", "license")
    search_fields = ("name", "identity_number", "license", "comments")


class DispatchRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "get_driver_name", "vehicle_number", "dispatch_date", "origin", "destination", "status")
    search_fields = ("driver__name", "vehicle_number", "origin", "destination", "comments")
    list_filter = ("dispatch_date", "driver__name")

    def get_driver_name(self, obj):
        return obj.driver.name


admin.site.register(Driver, DriverAdmin)
admin.site.register(DispatchRecord, DispatchRecordAdmin)

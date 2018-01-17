from django.contrib import admin
from ShipmentOrder.models import ShipmentOrder, Goods


class TagInline(admin.TabularInline):
    model = ShipmentOrder, Goods


class ShipmentOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "from_address", "receiver",
                    "to_address", "market", "status", "mode",
                    "create_date", "totalPrice", "payable", "get_handle_name")
    search_fields = ("sender", "from_address", "sender_contact", "receiver",
                    "to_address", "receiver_contact", "market", "mode", "comments", "handle__username")
    list_filter = ("create_date", "sender", "receiver", "market", "mode")

    def get_handle_name(self, obj):
        return obj.handle.username


class GoodAdmin(admin.ModelAdmin):
    list_display = ("id", "goods_name", "get_sender", "get_from_address", "get_receiver",
                    "get_to_address", "amount", "weight", "volume", "density",
                    "store_date", "send_date", "receive_date")
    search_fields = ("goods_name", "shipment_order_id__sender", "shipment_order_id__from_address",
                     "shipment_order_id__receiver", "shipment_order__to_address", "comments")
    list_filter = ("store_date", "send_date", "receive_date")

    def get_sender(self, obj):
        return obj.shipment_order_id.sender

    def get_from_address(self, obj):
        return obj.shipment_order_id.from_address

    def get_receiver(self, obj):
        return obj.shipment_order_id.receiver

    def get_to_address(self, obj):
        return obj.shipment_order_id.to_address


admin.site.register(ShipmentOrder, ShipmentOrderAdmin)
admin.site.register(Goods, GoodAdmin)
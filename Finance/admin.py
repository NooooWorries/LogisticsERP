from django.contrib import admin
from Finance.models import PaymentOrder


class TagInline(admin.TabularInline):
    model = PaymentOrder


class PaymentOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_shipment_id','get_receiver', 'payment_date', 'amount', 'handle')
    search_fields = ('comments', 'shipment_order__receiver',
                     'shipment_order__sender', 'shipment_order__to_address',
                     'shipment_order__from_address', 'shipment_order__comments')
    list_filter = ('payment_date',)


    def get_shipment_id(self, obj):
        return obj.shipment_order.id
    get_shipment_id.short_description = '订单ID'

    def get_receiver(self, obj):
        return obj.shipment_order.receiver
    get_receiver.short_description = '收货人'


admin.site.register(PaymentOrder, PaymentOrderAdmin)

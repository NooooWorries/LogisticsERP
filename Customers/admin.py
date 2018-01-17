from django.contrib import admin
from Customers.models import CustomerClass, Customer


class TagInline(admin.TabularInline):
    model = CustomerClass, Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "get_class_name", "customer_name", "contact_person", "contact_number")
    search_fields = ("customer_class__class_name", "contact_person",
                     "contact_number", "identity_number", "address", "comments")
    list_filter = ("customer_class__class_name", )

    def get_class_name(self, obj):
        return obj.customer_class.class_name


class CustomerClassAdmin(admin.ModelAdmin):
    list_display = ("id", "class_name", "comments")
    search_fields = ("class_name", "comments")


admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerClass, CustomerClassAdmin)

from django.contrib import admin
from .models import AutoModel, Auto, Service, OrderData, OrderLine
# Register your models here.

class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0
    fields = ['service', 'qty']

class OrderDataAdmin(admin.ModelAdmin):
    list_display = ['order_date', 'auto', 'suma']
    inlines = [OrderLineInLine]

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['service', 'qty', 'kaina']

class AutoAdmin(admin.ModelAdmin):
    list_display = ['client', 'automodel', 'l_plate', 'vin_code']
    list_filter = ['client', 'automodel']
    search_fields = ['l_plate', 'vin_code']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'price']

admin.site.register(AutoModel)
admin.site.register(Auto, AutoAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(OrderData, OrderDataAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
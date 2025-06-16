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


admin.site.register(AutoModel)
admin.site.register(Auto)
admin.site.register(Service)
admin.site.register(OrderData, OrderDataAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
from django.contrib import admin
from .models import AutoModel, Auto, Service, OrderData, OrderLine
# Register your models here.

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order_date', 'auto', 'suma']



admin.site.register(AutoModel)
admin.site.register(Auto)
admin.site.register(Service)
admin.site.register(OrderData, OrderLineAdmin)
admin.site.register(OrderLine)
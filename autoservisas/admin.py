from django.contrib import admin
from .models import AutoModel, Auto, Service, OrderData, OrderLine, Comment, Profile
from .forms import AutoModelForm


# Register your models here.
class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0
    fields = ['service', 'qty']

class OrderDataAdmin(admin.ModelAdmin):
    list_display = ['auto', 'suma', 'status', 'deadline_date', 'deadline_time', 'is_overdue']
    list_editable = ['deadline_date', 'deadline_time', 'status']
    readonly_fields = ['order_date', 'suma']
    inlines = [OrderLineInLine]

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['service', 'service__price', 'qty', 'kaina']

class AutoAdmin(admin.ModelAdmin):
    list_display = ['automodel', 'owner', 'l_plate', 'vin_code', 'cover']
    list_filter = ['automodel']
    search_fields = ['l_plate', 'vin_code', 'automodel__make', 'automodel__model']
    list_editable = ['owner']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'price']

class AutoModelAdmin(admin.ModelAdmin):
    form = AutoModelForm
    list_display = ['make', 'model', 'year']

class CommentAdmin(admin.ModelAdmin):

    list_display = ['order', 'author', 'date']

admin.site.register(AutoModel, AutoModelAdmin)
admin.site.register(Auto, AutoAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(OrderData, OrderDataAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile)
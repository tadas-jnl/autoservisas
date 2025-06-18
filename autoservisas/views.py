from django.shortcuts import render
from .models import Auto, OrderData, Service
# Create your views here.
def index(request):
    context = {
        "cars_count": Auto.objects.all().count(),
        "paid_orders": OrderData.objects.filter(status__exact='a').count(),
        "services_count": Service.objects.count(),

    }
    return render(template_name="index.html", request=request, context=context)

def automobiliai(request):
    context = {
        "automobiliai": Auto.objects.all(),
    }
    return render(request, template_name='cars.html', context=context)

def automobilis(request, car_id):
    car = Auto.objects.get(pk=car_id)
    return render(request, template_name='car.html', context={'car': car})
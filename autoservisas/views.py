from django.contrib.admin.templatetags.admin_list import pagination
from django.shortcuts import render
from django.views import generic
from .models import Auto, OrderData, Service, AutoModel
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def index(request):
    context = {
        "cars_count": Auto.objects.all().count(),
        "paid_orders": OrderData.objects.filter(status__exact='a').count(),
        "services_count": Service.objects.count(),

    }
    return render(template_name="index.html", request=request, context=context)

def automobiliai(request):
    cars = Auto.objects.all()
    paginator = Paginator(cars, per_page=3)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    context = {
        "automobiliai": paged_cars,
    }
    return render(request, template_name='cars.html', context=context)

def automobilis(request, car_id):
    car = Auto.objects.get(pk=car_id)
    return render(request, template_name='car.html', context={'car': car})

class OrderListView(generic.ListView):
    model = OrderData
    template_name = 'orders.html'
    context_object_name = 'orders'
    paginate_by = 3

class OrderDetailView(generic.DetailView):
    model = OrderData
    template_name = 'order.html'
    context_object_name = 'order'

def search(request):
    query = request.GET.get('query')
    car_search_results = Auto.objects.filter(
        Q(l_plate__icontains=query) | Q(client__icontains=query) | Q(automodel__make__icontains=query) | Q(automodel__model__icontains=query) | Q(vin_code__icontains=query)
    )
    context = {
        'query': query,
        'cars': car_search_results,
    }
    return render(request, template_name="search.html", context=context)
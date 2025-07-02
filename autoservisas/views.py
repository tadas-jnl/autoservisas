from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import password_validation
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.views.generic.edit import FormMixin
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Auto, OrderData, Service, OrderLine
from .forms import OrderCommentForm, UserUpdateForm, ProfileUpdateForm, CreateOrderForm, ManageOrderForm, CreateOrderLineForm

# Create your views here.
def index(request):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        "cars_count": Auto.objects.all().count(),
        "paid_orders": OrderData.objects.filter(status__exact='a').count(),
        "services_count": Service.objects.count(),
        'MEDIA_URL': settings.MEDIA_URL,
        'num_visits': num_visits,
    }
    return render(template_name="index.html", request=request, context=context)

def automobiliai(request):
    cars = Auto.objects.all()
    paginator = Paginator(cars, per_page=4)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    context = {
        "automobiliai": paged_cars,
    }
    return render(request, template_name='cars.html', context=context)

def automobilis(request, car_id):
    car = Auto.objects.get(pk=car_id)

    return render(request, template_name='car.html', context={'car': car})

def search(request):
    query = request.GET.get('query')
    car_search_results = Auto.objects.filter(
        Q(l_plate__icontains=query) | Q(automodel__make__icontains=query) | Q(automodel__model__icontains=query) | Q(vin_code__icontains=query)
    )
    context = {
        'query': query,
        'cars': car_search_results,
    }
    return render(request, template_name="search.html", context=context)

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'{email} jau užregistruotas!')
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as e:
                        for error in e:
                            messages.error(request, error)
                        return redirect('register')

                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} sėkmingai užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')

class OrderListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = OrderData
    template_name = 'orders.html'
    context_object_name = 'orders'
    paginate_by = 5

    def test_func(self):
        return self.request.user.profile.is_employee

class OrderDetailView(LoginRequiredMixin, FormMixin, UserPassesTestMixin, generic.DetailView):
    model = OrderData
    template_name = 'order.html'
    context_object_name = 'order'
    form_class = OrderCommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['orderline_form'] = CreateOrderLineForm(initial={
            'order_data': self.object
        })
        return context

    def test_func(self):
        user = self.request.user
        order = self.get_object()
        return order.auto.owner == user or user.profile.is_employee

    def get_success_url(self):
        return reverse("order", kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        submit_type = request.POST.get("submit_type")

        if submit_type == 'comment':
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        elif submit_type == "orderline":
            orderline_form = CreateOrderLineForm(request.POST)
            if orderline_form.is_valid():
                line = orderline_form.save(commit=False)
                line.order_data = self.object
                line.save()
        return redirect(self.get_success_url())

    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

class MyOrdersList(LoginRequiredMixin, generic.ListView):
    model = OrderData
    template_name = 'my_orders.html'
    context_object_name = 'my_orders'
    paginate_by = 5

    def get_queryset(self):
        return OrderData.objects.filter(auto__owner=self.request.user)

class AddOrder(LoginRequiredMixin, generic.CreateView):
    model = OrderData
    form_class = CreateOrderForm
    template_name = "add_order.html"

    def get_success_url(self):
        return reverse("order", kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Inject user into form
        return kwargs

    def form_valid(self, form):
        form.instance.auto.owner = self.request.user
        messages.success(self.request, "Užsakymas sukurtas")
        return super().form_valid(form)


class ManageOrder(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = OrderData
    form_class = ManageOrderForm
    template_name = "manage_order.html"

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.request.user.profile.is_employee

    def form_valid(self, form):
        messages.success(self.request, "Užsakymas atnaujintas")
        return super().form_valid(form)
    
    def get_form_kwargs(self):  
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class DeleteOrder(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = OrderData
    context_object_name = "order"
    template_name = "delete_order.html"
    success_url = "/autoservisas/orders"

    def test_func(self):
        return self.request.user.profile.is_employee
    

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, "Duomenys atnaujinti!")
            return redirect('profile')
        else: 
            print("u_form errors:", u_form.errors)
            print("p_form errors:", p_form.errors)
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context=context)


# class AddOrder(LoginRequiredMixin, generic.View):
#     def get(self, request):
#         form = CreateOrderForm(user=request.user)
#         formset = OrderLineFormSet()
#         return render(request, 'add_order.html', {'form': form, 'formset': formset})
#
#     def post(self, request):
#         form = CreateOrderForm(request.POST, user=request.user)
#         formset = OrderLineFormSet(request.POST)
#
#         if form.is_valid() and formset.is_valid():
#             order = form.save(commit=False)
#             order.customer = request.user
#             order.save()
#
#             formset.instance = order
#             formset.save()
#
#             messages.success(request, "Užsakymas sukurtas su paslaugomis")
#             return redirect('my_orders')
#
#         return render(request, 'add_order.html', {'form': form, 'formset': formset})
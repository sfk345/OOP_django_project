from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DeleteView

from design.forms import RegisterUserForm, CreateOrder
from design.models import *


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')


def create_order(request):
    if request.method == 'POST':
        form = CreateOrder(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return render(request, 'general/orders.html', {'form': form})
    else:
        form = CreateOrder()
    return render(request, 'registration/create_order.html', {'form': form})


class Home(generic.ListView):
    model = Order
    template_name = 'general/home.html'
    paginate_by = 4


class DeleteOrder(DeleteView):
    template_name = 'general/order_delete.html'
    model = Order
    success_url = reverse_lazy('orders')


class OrdersByUser(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'general/orders.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-time_create')

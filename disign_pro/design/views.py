from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView

from design.forms import RegisterUserForm
from design.models import *


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')


def home(request):
    return render(request, 'general/home.html')


@login_required()
def application(request):
    return render(request, 'general/application.html')


class OrdersByUser(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'general/orders.html'
    paginate_by = 5

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('time_create')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs, )
    #     context['filter'] = OrderFilter(self.request.GET, queryset=self.get_queryset())
    #     return context

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from design.filters import OrderFilter, AdminOrderFilter
from design.forms import RegisterUserForm, CreateOrder, DeleteCategory, StatusUpdate
from design.models import *


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')


class OrdersAdmin(PermissionRequiredMixin, generic.ListView):
    """
    Все заявки (для администратора)
    """
    permission_required = 'app.can_change_status'
    model = Order
    template_name = 'general/admin_orders.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.order_by('-time_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs, )
        context['filter'] = AdminOrderFilter(self.request.GET, queryset=self.get_queryset())
        return context


def create_order(request):
    if request.method == 'POST':
        form = CreateOrder(request.POST, request.FILES)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.name = request.user
            stock.save()
            form.save_m2m()
            return redirect('myorders')
    else:
        form = CreateOrder()
    return render(request, 'registration/create_order.html', {'form': form})


class DetailOrder(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'general/detail_orders.html'


class Home(generic.ListView):
    model = Order
    template_name = 'general/home.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = {
            'num_accepted': Order.objects.filter(status='accepted').count(),
            'order_list': Order.objects.filter(status='done').order_by('time_create')[:3]
        }
        return context


class DeleteOrder(DeleteView):
    template_name = 'general/order_delete.html'
    model = Order
    success_url = reverse_lazy('myorders')

    def get_object(self, queryset=None):
        obj = super(DeleteOrder, self).get_object(queryset)
        if obj.name != self.request.user:
            raise Http404(
                "Заявка может быть удалена только автором!"
            )
        if obj.status != 'new':
            raise Http404(
                "Заявка может быть удалена только если она находится в статусе 'Новая'"
            )
        return obj


class OrdersByUser(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'general/orders.html'
    paginate_by = 5

    def get_queryset(self):
        return Order.objects.filter(name=self.request.user).order_by('-time_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = OrderFilter(self.request.GET, queryset=self.get_queryset())
        return context


@login_required
@permission_required('app.can_change_status')
def deletecategory(request):
    if request.method == 'POST':
        form = DeleteCategory(request.POST)
        if form.is_valid():
            category = Category.objects.get(name=form.cleaned_data['name'])
            category.delete()
            return HttpResponseRedirect(reverse('adm_orders'))
    else:
        form = DeleteCategory()
    return render(request, 'general/del_category.html', {'form': form})


class AddCategory(PermissionRequiredMixin, CreateView):
    permission_required = 'app.can_change_status'
    model = Category
    fields = ['name']
    template_name = 'general/add_category.html'
    success_url = '/'


@login_required
@permission_required('app.can_change_status')
def changeofstatus(request, pk):
    model = Order
    order = get_object_or_404(Order, pk=pk)
    previous_status = order.status
    if request.method == 'POST':
        form = StatusUpdate(request.POST)
        if form.is_valid():
            order.status = form.cleaned_data['status']
            if order.status == 'done':
                return redirect('full_status_change', pk)
            elif previous_status == 'done' or previous_status == 'accepted':
                return HttpResponse('<h1>Смена статуса с «Принято в работу» или «Выполнено» невозможна</h1>')
            elif order.status == 'accepted':
                return redirect('accepted_status_change', pk)
            else:
                order.save()
            return HttpResponseRedirect(reverse('adm_orders'))
    else:
        form = StatusUpdate()
    return render(request, 'general/status_update.html', {'form': form, 'order': order})


class FullStatusChange(PermissionRequiredMixin, UpdateView):
    permission_required = 'app.can_change_status'
    model = Order
    fields = ['status', 'photo_design']
    initial = {'status': 'done'}
    success_url = '/'
    template_name = 'general/status_update.html'

    def get_form(self, form_class=None):
        form = super(FullStatusChange, self).get_form(form_class)
        form.fields['photo_design'].required = True
        form.fields['status'].disabled = True
        return form


class AcceptedStatusChange(PermissionRequiredMixin, UpdateView):
    permission_required = 'app.can_change_status'
    model = Order
    fields = ['status', 'comment']
    initial = {'status': 'accepted'}
    success_url = '/'
    template_name = 'general/status_update.html'

    def get_form(self, form_class=None):
        form = super(AcceptedStatusChange, self).get_form(form_class)
        form.fields['comment'].required = True
        form.fields['status'].disabled = True
        return form

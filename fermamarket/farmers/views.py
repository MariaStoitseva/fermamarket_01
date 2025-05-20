from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import FarmerProfileForm, ProductForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import FarmerProfile, Product
from ..customusers.decorators import group_required
from ..orders.models import OrderItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import FarmerProfile


@login_required
def view_farmer_profile(request):
    farmer = get_object_or_404(FarmerProfile, user=request.user)
    return render(request, 'farmers/view_farmer_profile.html', {'farmer': farmer})


@group_required('Farmers')
def edit_farmer_profile(request):
    profile = getattr(request.user, 'farmerprofile', None)
    if not profile:
        return HttpResponseForbidden("Нямате фермерски профил.")

    if request.method == 'POST':
        form = FarmerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('farmer_profile')
    else:
        form = FarmerProfileForm(instance=profile)
    return render(request, 'farmers/profile_edit.html', {'form': form})


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'farmers/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        farmer = FarmerProfile.objects.get(user=self.request.user)
        return Product.objects.filter(farmer=farmer)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'farmers/product_create.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        farmer = FarmerProfile.objects.get(user=self.request.user)
        form.instance.farmer = farmer
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'farmers/product_edit.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        farmer = FarmerProfile.objects.get(user=self.request.user)
        return Product.objects.filter(farmer=farmer)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'farmers/product_delete.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        farmer = FarmerProfile.objects.get(user=self.request.user)
        return Product.objects.filter(farmer=farmer)


@login_required
@group_required('Farmers')
def farmer_orders(request):
    farmer = FarmerProfile.objects.get(user=request.user)
    order_items = OrderItem.objects.filter(farmer=farmer).select_related('order', 'product').order_by('-order__created_at')

    return render(request, 'farmers/farmer_orders.html', {
        'order_items': order_items,
    })


@require_POST
@group_required('Farmers')
def mark_as_sent(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, farmer__user=request.user)
    item.status = 'Sent'
    item.save()

    order = item.order

    # Проверка: Има ли останали item-и със статус различен от 'Sent'?
    if not order.items.filter(~Q(status='Sent')).exists():
        order.status = 'sent'
        order.save()

    return redirect('farmer_orders')
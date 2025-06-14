from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from .forms import FarmerProfileForm, ProductForm
from .models import FarmerProfile, Product
from ..orders.models import OrderItem


@login_required
@permission_required('farmers.view_farmerprofile', raise_exception=True)
def view_farmer_profile(request):
    farmer = get_object_or_404(FarmerProfile, user=request.user)
    return render(request, 'farmers/view_farmer_profile.html', {'farmer': farmer})


@login_required
@permission_required('farmers.change_farmerprofile', raise_exception=True)
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


@login_required
@permission_required('orders.view_orderitem', raise_exception=True)
def farmer_orders(request):
    farmer = FarmerProfile.objects.get(user=request.user)
    order_items = OrderItem.objects.filter(farmer=farmer).select_related('order', 'product').order_by('-order__created_at')
    return render(request, 'farmers/farmer_orders.html', {'order_items': order_items})


@require_POST
@login_required
@permission_required('orders.change_orderitem', raise_exception=True)
def mark_as_sent(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, farmer__user=request.user)
    item.status = 'Sent'
    item.save()

    order = item.order
    if not order.items.filter(~Q(status='Sent')).exists():
        order.status = 'sent'
        order.save()

    return redirect('farmer_orders')


@method_decorator(permission_required('farmers.view_product', raise_exception=True), name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'farmers/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        farmer = FarmerProfile.objects.get(user=self.request.user)
        return Product.objects.filter(farmer=farmer)


@method_decorator(permission_required('farmers.add_product', raise_exception=True), name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'farmers/product_create.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        farmer = FarmerProfile.objects.get(user=self.request.user)
        form.instance.farmer = farmer
        return super().form_valid(form)


@method_decorator(permission_required('farmers.change_product', raise_exception=True), name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'farmers/product_edit.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        farmer = FarmerProfile.objects.get(user=self.request.user)
        return Product.objects.filter(farmer=farmer)


@method_decorator(permission_required('farmers.delete_product', raise_exception=True), name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'farmers/product_delete.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        farmer = FarmerProfile.objects.get(user=self.request.user)
        return Product.objects.filter(farmer=farmer)

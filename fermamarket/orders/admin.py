from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'created_at', 'status', 'total_price')
    list_filter = ('status', 'created_at')
    search_fields = ('client__user__username',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'total_price')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'farmer')
    search_fields = ('product__title', 'farmer__farm_name')


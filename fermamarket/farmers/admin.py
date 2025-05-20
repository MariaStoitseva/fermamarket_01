from django.contrib import admin
from .models import Product, FarmerProfile, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'farmer', 'price', 'quantity', 'created_at')
    search_fields = ('title', 'farmer__farm_name')
    list_filter = ('created_at', 'price')
    ordering = ('-created_at',)


@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('farm_name', 'user', 'location', 'phone')
    search_fields = ('farm_name', 'user__username')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

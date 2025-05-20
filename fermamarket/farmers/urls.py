from django.urls import path
from .views import edit_farmer_profile, farmer_orders, \
    mark_as_sent, ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, view_farmer_profile

urlpatterns = [
    path('profile/', view_farmer_profile, name='farmer_profile'),
    path('profile/edit/', edit_farmer_profile, name='farmer_profile_edit'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='create_product'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='edit_product'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),
    path('orders/', farmer_orders, name='farmer_orders'),
    path('orders/mark-sent/<int:item_id>/', mark_as_sent, name='mark_as_sent'),


]

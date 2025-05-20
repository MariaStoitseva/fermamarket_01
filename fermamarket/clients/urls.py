from django.urls import path
from .views import edit_client_profile, product_catalog, add_to_cart, view_cart, checkout, order_success, order_history, \
    view_client_profile, product_detail

urlpatterns = [
    path('profile/', view_client_profile, name='client_profile'),
    path('profile/edit/', edit_client_profile, name='edit_client_profile'),
    path('catalog/', product_catalog, name='product_catalog'),
    path('product/<int:pk>/', product_detail, name='product_detail'),

    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-success/', order_success, name='order_success'),
    path('order-history/', order_history, name='order_history'),

]

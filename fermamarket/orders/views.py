from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from fermamarket.orders.models import Order, OrderItem
from decimal import Decimal


@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, client=request.user.clientprofile)
    items = order.items.select_related('product', 'farmer')

    # Изчисляване на междинна стойност за всеки елемент
    for item in items:
        item.subtotal = item.price * item.quantity

    return render(request, 'clients/order_details.html', {
        'order': order,
        'items': items,
    })

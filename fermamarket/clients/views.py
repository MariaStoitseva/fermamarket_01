from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import ClientProfileForm, CheckoutForm
from .models import ClientProfile
from django.contrib.auth.decorators import login_required, permission_required
from ..farmers.models import Product, Category
from ..orders.models import Order, OrderItem


@login_required
@permission_required('clients.view_clientprofile', raise_exception=True)
def view_client_profile(request):
    profile = getattr(request.user, 'clientprofile', None)
    return render(request, 'clients/profile_view.html', {'profile': profile})


@permission_required('clients.view_clientprofile', raise_exception=True)
def edit_client_profile(request):
    profile = getattr(request.user, 'clientprofile', None)
    if not profile:
        return HttpResponseForbidden("Нямате клиентски профил.")

    if request.method == 'POST':
        form = ClientProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('client_profile')
    else:
        form = ClientProfileForm(instance=profile)
    return render(request, 'clients/profile_edit.html', {'form': form})


def product_catalog(request):
    category_name = request.GET.get('category')
    search_query = request.GET.get('search', '')

    categories = Category.objects.all()
    products = Product.objects.all()

    if category_name:
        products = products.filter(category__name=category_name)

    search_query = request.GET.get('search', '').strip().lower()

    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    sort = request.GET.get('sort')

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    return render(request, 'product_catalog.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_name,
        'search_query': search_query,
        'sort': sort,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


@require_POST
def add_to_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity

    request.session['cart'] = cart
    return redirect('product_catalog')


from django.views.decorators.http import require_http_methods


@login_required
@permission_required('clients.view_clientprofile', raise_exception=True)
@require_http_methods(["GET", "POST"])
def view_cart(request):
    cart = request.session.get('cart', {})

    if request.method == 'POST':
        action = request.POST.get('action')
        product_id = str(request.POST.get('product_id'))

        if action == 'remove':
            cart.pop(product_id, None)
        elif action == 'update':
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                cart[product_id] = quantity
            else:
                cart.pop(product_id, None)

        request.session['cart'] = cart
        return redirect('view_cart')

    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total_price = 0

    for product in products:
        quantity = cart[str(product.id)]
        total = product.price * quantity
        total_price += total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': total,
        })

    return render(request, 'clients/shop-cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


# def view_cart(request):
#     cart = request.session.get('cart', {})
#     products = Product.objects.filter(id__in=cart.keys())
#     cart_items = []
#
#     total_price = 0
#     for product in products:
#         quantity = cart[str(product.id)]
#         total = product.price * quantity
#         total_price += total
#         cart_items.append({
#             'product': product,
#             'quantity': quantity,
#             'total': total,
#         })
#
#     return render(request, 'clients/shop-cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
@permission_required('clients.view_clientprofile', raise_exception=True)
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_catalog')

    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total_price = 0
    for product in products:
        quantity = cart.get(str(product.id), 0)
        total = product.price * quantity
        total_price += total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': total,
        })

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            client_profile = ClientProfile.objects.get(user=request.user)

            # Проверка за наличност
            for item in cart_items:
                product = item['product']
                quantity = item['quantity']

                if product.quantity < quantity:
                    form.add_error(None, f"Продуктът '{product.title}' има само {product.quantity} налични.")

            # Ако има грешки – прекрати
            if form.errors:
                return render(request, 'clients/shop-checkout.html', {
                    'form': form,
                    'cart_items': cart_items,
                    'total_price': total_price,
                })

            # Създаване на поръчка
            order = Order.objects.create(client=client_profile, total_price=0)
            total = 0

            for item in cart_items:
                product = item['product']
                quantity = item['quantity']
                subtotal = item['total']

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price,
                    farmer=product.farmer,
                )

                product.quantity -= quantity
                product.save()
                total += subtotal

            order.total_price = total
            order.save()

            # Изчистване на количката
            request.session['cart'] = {}

            # Изпращане на имейли (по желание):
            # subject_client = f'Вашата поръчка #{order.id} е получена'
            # message_client = render_to_string('emails/order_confirmation_client.html', {
            #     'order': order,
            #     'cart_items': cart_items,
            #     'total_price': total,
            #     'client': client_profile,
            # })
            # send_mail(
            #     subject_client,
            #     message_client,
            #     settings.DEFAULT_FROM_EMAIL,
            #     [client_profile.user.email],
            #     fail_silently=False,
            #     html_message=message_client,
            # )

            # farmers_notified = set()
            # for item in cart_items:
            #     farmer = item['product'].farmer
            #     if farmer.user.email not in farmers_notified:
            #         farmers_notified.add(farmer.user.email)
            #         subject_farmer = 'Нова поръчка във вашия фермерски магазин'
            #         message_farmer = render_to_string('emails/order_notification_farmer.html', {
            #             'farmer': farmer,
            #             'order': order,
            #         })
            #         send_mail(
            #             subject_farmer,
            #             message_farmer,
            #             settings.DEFAULT_FROM_EMAIL,
            #             [farmer.user.email],
            #             fail_silently=True,
            #             html_message=message_farmer,
            #         )

            return redirect('order_success')
    else:
        form = CheckoutForm()

    return render(request, 'clients/shop-checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
@permission_required('clients.view_clientprofile', raise_exception=True)
def order_success(request):
    return render(request, 'clients/order_success.html')


@login_required
@permission_required('orders.view_order', raise_exception=True)
def order_history(request):
    client_profile = request.user.clientprofile
    orders = Order.objects.filter(client=client_profile).order_by('-created_at')
    return render(request, 'clients/order_history.html', {'orders': orders})

from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from fermamarket.clients.models import ClientProfile
from fermamarket.customusers.forms import RegistrationForm
from fermamarket.farmers.models import FarmerProfile


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            role = form.cleaned_data['role']
            if role == 'farmer':
                group = Group.objects.get(name='Farmers')
                user.groups.add(group)
                FarmerProfile.objects.create(user=user, farm_name='', location='', phone='')
            else:
                group = Group.objects.get(name='Clients')
                user.groups.add(group)
                ClientProfile.objects.create(user=user, full_name='', address='', phone='')

            login(request, user)

            # send_mail(
            #     subject='Добре дошли във FermaMarket!',
            #     message=f'Здравей, {user.username}!\n\nБлагодарим, че се регистрирахте във FermaMarket.',
            #     from_email=None,  # взема DEFAULT_FROM_EMAIL
            #     recipient_list=[user.email],
            # )

            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def custom_logout_view(request):
    logout(request)
    return redirect('home')

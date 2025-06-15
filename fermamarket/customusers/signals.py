from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.conf import settings


@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    farmers_group, created = Group.objects.get_or_create(name='Farmers')
    clients_group, created = Group.objects.get_or_create(name='Clients')

    # Права за фермери
    farmers_perms = {
        'farmers': [
            'add_category', 'change_category', 'delete_category', 'view_category',
            'add_farmerprofile', 'change_farmerprofile', 'delete_farmerprofile', 'view_farmerprofile',
            'add_product', 'change_product', 'delete_product', 'view_product',
        ],
        'orders': [
            'change_order', 'view_order',
            'change_orderitem', 'view_orderitem',
        ],
    }

    # Права за клиенти
    clients_perms = {
        'clients': [
            'add_clientprofile', 'change_clientprofile', 'delete_clientprofile', 'view_clientprofile',
        ],
        'orders': [
            'add_order', 'view_order',
            'view_orderitem',
        ],
    }

    def add_permissions(group, perms_dict):
        for app_label, codenames in perms_dict.items():
            for codename in codenames:
                perm = Permission.objects.filter(
                    codename=codename,
                    content_type__app_label=app_label
                ).first()

                if perm:
                    group.permissions.add(perm)
                elif settings.DEBUG:
                    print(f"[Warning] Permission {codename} в {app_label} не е намерено.")

    add_permissions(farmers_group, farmers_perms)
    add_permissions(clients_group, clients_perms)

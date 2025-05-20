from django.contrib import admin
from .models import ClientProfile


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'phone')
    search_fields = ('full_name', 'user__username')

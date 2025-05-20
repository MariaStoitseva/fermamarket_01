from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from fermamarket import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('terms/', TemplateView.as_view(template_name='info/terms.html'), name='terms'),
    path('privacy/', TemplateView.as_view(template_name='info/privacy.html'), name='privacy'),
    path('shipping/', TemplateView.as_view(template_name='info/shipping.html'), name='shipping'),
    path('farmer-requirements/', TemplateView.as_view(template_name='info/farmer_requirements.html'), name='farmer_requirements'),
    path('accounts/', include('fermamarket.customusers.urls')),
    path('farmer/', include('fermamarket.farmers.urls')),
    path('client/', include('fermamarket.clients.urls')),
    path('orders/', include('fermamarket.orders.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

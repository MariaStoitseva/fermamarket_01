from django.db import models
from fermamarket.clients.models import ClientProfile
from fermamarket.farmers.models import FarmerProfile
from fermamarket.farmers.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Изчаква се'),
        ('sent', 'Изпратена'),
        ('completed', 'Завършена'),
    ]

    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Поръчка #{self.id} от {self.client.user.username}"


class OrderItem(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Очаква се'),
        ('Sent', 'Изпратено'),
    ]

    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('farmers.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    farmer = models.ForeignKey('farmers.FarmerProfile', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')


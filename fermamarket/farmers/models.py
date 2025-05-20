from django.db import models
from django.utils import timezone
from fermamarket.customusers.models import CustomUser


class FarmerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    farm_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='farms/', blank=True, null=True)

    def __str__(self):
        return self.farm_name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True, blank=True,
        help_text="Тегло или количество (напр. в кг)"
    )
    weight_unit = models.CharField(
        max_length=10,
        choices=[('kg', 'кг'), ('g', 'гр'), ('l', 'литра'), ('pcs', 'брой')],
        default='kg',
        help_text="Мярка за тегло/обем"
    )

    def __str__(self):
        return self.title


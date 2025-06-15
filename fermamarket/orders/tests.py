from django.test import TestCase
from django.contrib.auth import get_user_model

from fermamarket.clients.models import ClientProfile
from fermamarket.farmers.models import FarmerProfile, Product
from fermamarket.orders.models import Order, OrderItem

User = get_user_model()


class OrderTests(TestCase):

    def setUp(self):
        self.client_user = User.objects.create_user(
            username='client',
            email='client@test.com',
            password='pass'
        )
        self.client_profile = ClientProfile.objects.create(
            user=self.client_user,
            full_name='Test Client',
            address='ул. Примерна 1',
            phone='0888123456'
        )

        self.farmer_user = User.objects.create_user(
            username='farmer',
            email='farmer@test.com',
            password='pass'
        )
        self.farmer_profile = FarmerProfile.objects.create(
            user=self.farmer_user,
            farm_name='Ферма Здраве',
            description='Екологична ферма',
            location='Село Примерно',
            phone='0888999555'
        )

        self.product = Product.objects.create(
            farmer=self.farmer_profile,
            title='Cucumber',
            description='Fresh cucumbers',
            price=2.0,
            quantity=10,
            weight=1.0,
            weight_unit='kg'
        )

        self.order = Order.objects.create(
            client=self.client_profile,
            status='pending',
            total_price=0.00
        )

    def test_create_order_item(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
            price=self.product.price,
            farmer=self.farmer_profile
        )
        self.assertEqual(item.quantity, 3)
        self.assertEqual(item.product.title, 'Cucumber')
        self.assertEqual(item.farmer, self.farmer_profile)

    def test_order_item_links_to_product(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=self.product.price,
            farmer=self.farmer_profile
        )
        self.assertEqual(item.product, self.product)

    def test_order_status_change(self):
        self.order.status = 'sent'
        self.order.save()
        self.assertEqual(self.order.status, 'sent')

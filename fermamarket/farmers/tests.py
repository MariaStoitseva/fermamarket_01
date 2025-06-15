from django.test import TestCase
from django.contrib.auth import get_user_model
from fermamarket.farmers.models import FarmerProfile, Product

User = get_user_model()


class FarmerTests(TestCase):

    def setUp(self):
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

    def test_farmer_profile_created(self):
        self.assertEqual(self.farmer_profile.farm_name, 'Ферма Здраве')

    def test_create_product(self):
        product = Product.objects.create(
            farmer=self.farmer_profile,
            title='Carrot',
            description='Fresh carrots',
            price=1.25,
            quantity=50,
            weight=1.0,
            weight_unit='kg'
        )
        self.assertEqual(product.title, 'Carrot')
        self.assertEqual(product.farmer, self.farmer_profile)

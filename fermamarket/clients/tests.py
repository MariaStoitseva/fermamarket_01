from django.test import TestCase
from django.contrib.auth import get_user_model
from fermamarket.clients.models import ClientProfile

User = get_user_model()

class ClientTests(TestCase):

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

    def test_client_profile_created(self):
        self.assertEqual(self.client_profile.full_name, 'Test Client')
        self.assertEqual(self.client_profile.user.username, 'client')

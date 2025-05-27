from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from api.models import ApiUser, Warehouse, Product, Request

class ViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = ApiUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_supplier=False
        )
        self.supplier = ApiUser.objects.create_user(
            username='supplier',
            email='supplier@example.com',
            password='testpass123',
            is_supplier=True
        )
        self.admin = ApiUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.warehouse = Warehouse.objects.create(name='Main Warehouse')
        self.product = Product.objects.create(
            name='Test Product',
            producer=self.supplier
        )
        self.request = Request.objects.create(
            product=self.product,
            amount=10,
            warehouse=self.warehouse,
            customer=self.user
        )

    def test_user_registration(self):
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'is_supplier': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(ApiUser.objects.filter(username='newuser').exists())

    def test_product_creation_by_supplier(self):
        self.client.force_authenticate(user=self.supplier)
        url = reverse('product-list')
        data = {
            'name': 'New Product'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)

    def test_request_creation_by_requester(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('request-list')
        data = {
            'product': self.product.id,
            'amount': 5,
            'warehouse': self.warehouse.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Request.objects.count(), 2)
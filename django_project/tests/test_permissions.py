from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from api.models import ApiUser, Product

class PermissionTests(APITestCase):
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
        self.product = Product.objects.create(
            name='Test Product',
            producer=self.supplier
        )

    def test_product_creation_by_non_supplier(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product-list')
        data = {
            'name': 'New Product'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_product_update_by_non_owner(self):
        other_supplier = ApiUser.objects.create_user(
            username='other',
            email='other@example.com',
            password='testpass123',
            is_supplier=True
        )
        self.client.force_authenticate(user=other_supplier)
        url = reverse('product-detail', args=[self.product.id])
        data = {
            'name': 'Updated Product'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 403)
from django.test import TestCase
from api.models import ApiUser, Warehouse, Product, Request

class ModelTests(TestCase):
    def setUp(self):
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
        self.warehouse = Warehouse.objects.create(name='Main Warehouse')
        self.product = Product.objects.create(
            name='Test Product',
            producer=self.supplier
        )

    def test_warehouse_creation(self):
        self.assertEqual(self.warehouse.name, 'Main Warehouse')
        self.assertEqual(str(self.warehouse), 'Main Warehouse')

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.producer, self.supplier)
        self.assertEqual(str(self.product), 'Test Product')

    def test_request_creation(self):
        request = Request.objects.create(
            product=self.product,
            amount=10,
            warehouse=self.warehouse,
            customer=self.user
        )
        self.assertEqual(request.amount, 10)
        self.assertFalse(request.request_supplied)
        self.assertFalse(request.request_retrieved)
# pylint: disable=missing-function-docstring
"""
Файл для тестов
"""
# from django.test import TestCase

# Create your tests here.
from django.test import TestCase


class HomepageTests(TestCase):
    """
    Тест проверки доступности главной страницы
    """
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

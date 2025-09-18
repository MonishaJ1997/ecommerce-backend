from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Product, Category

class ShopAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="pass")
        c = Category.objects.create(name="C")
        Product.objects.create(name="P1", description="d", price=10, category=c)
        self.client = APIClient()

    def test_products(self):
        res = self.client.get("/api/v1/products/")
        self.assertEqual(res.status_code, 200)
        self.assertTrue("results" in res.data)

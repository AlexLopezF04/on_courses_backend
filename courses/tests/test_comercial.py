from django.test import TestCase
from rest_framework import status

from helpers import create_user, create_admin, auth_client, unauth_client
from courses.tests.helpers import create_category, create_course
from courses.models import Cart, CartItem


class CartTests(TestCase):
    """Pruebas del carrito de compras."""

    def setUp(self):
        self.student = create_user("juan")
        self.client = auth_client(self.student)
        cat = create_category()
        self.course = create_course(cat, create_user("prof3", role="professor"))

    def test_get_my_cart(self):
        resp = self.client.get("/api/carts/mine/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("items", resp.data)

    def test_add_item_to_cart(self):
        resp = self.client.post("/api/cart-items/", {"course": self.course.id})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)


class OrderTests(TestCase):
    """Pruebas de órdenes de compra."""

    def setUp(self):
        self.student = create_user("kevin")
        self.client = auth_client(self.student)
        cat = create_category()
        prof = create_user("prof4", role="professor")
        self.course = create_course(cat, prof, price=50)

    def test_create_order_from_cart(self):
        # Primero agrega al carrito
        cart, _ = Cart.objects.get_or_create(user=self.student)
        CartItem.objects.create(cart=cart, course=self.course)
        # Crea la orden
        resp = self.client.post("/api/orders/", {})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(resp.data["total"]), 50.0)

    def test_empty_cart_returns_400(self):
        resp = self.client.post("/api/orders/", {})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

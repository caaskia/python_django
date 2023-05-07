from string import ascii_letters
from random import choices

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Product, Order
from shopapp.utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "A good table",
                "discount": "10",
            }
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )


class ProductDetailsViewTestCaseA(TestCase):
    def setUp(self) -> None:
        self.product = Product.objects.create(name="Best Product")

    def tearDown(self) -> None:
        self.product.delete()

    def test_get_product(self):
        self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )


class ProductDetailsViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Best Product")

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_links(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductListViewTestCaseA(TestCase):
    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"))
        for product in Product.objects.filter(archived=False).all():
            self.assertContains(response, product.name)


class ProductListViewTestCase(TestCase):
    fixtures = [
        'products-fixtures.json',
    ]

    def test_products_01(self):
        response = self.client.get(reverse("shopapp:products_list"))
        products = Product.objects.filter(archived=False).all()
        products_ = response.context['products']
        for p, p_ in zip(products, products_):
            self.assertEqual(p.pk, p_.pk)

    def test_products_02(self):
        response = self.client.get(reverse("shopapp:products_list"))
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context['products']),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, "shopapp/products-list.html")


class OrderListViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        # cls.credentials = dict(username='bob_test', password='qwerty')
        # cls.user = User.objects.create_user(**cls.credentials)

        cls.user = User.objects.create_user(username='bob_test', password='qwerty')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        # self.client.login(**self.credentials)
        self.client.force_login(self.user)

    def test_order_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_order_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        # self.assertRedirects(response, str(settings.LOGIN_URL))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductExportViewTestCase(TestCase):
    fixtures = [
        'products-fixtures.json',
    ]

    def test_get_product_view(self):
        response = self.client.get(
            reverse("shopapp:products-export"),
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]

        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data
        )


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username='bob_test', password='qwerty')
        cls.user = User.objects.create_user(**cls.credentials)
        permission_order = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission_order)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        # self.client.force_login(self.user)
        self.client.login(**self.credentials)
        self.order = Order.objects.create(
            delivery_address='ul.Mauri, d.3',
            promocode='Spring-2023',
            user=self.user)

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(reverse(
            'shopapp:order_details',
            kwargs={'pk': self.order.pk})
        )
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)

        order_data = response.context_data['order']
        self.assertEqual(
            order_data.pk,
            self.order.pk
        )

class OrdersExportTestCase(TestCase):

    # fixtures = [
    #     'products-fixtures.json',
    #     'orders-fixtures.json',
    #     'auth-fixtures.json',
    # ]
    @classmethod
    def setUpClass(cls):
        # cls.credentials = dict(username='staff_test', password='qwerty', is_staff = True)
        cls.credentials = dict(username='staff_test', password='qwerty')

        cls.user = User.objects.create_user(**cls.credentials)
        cls.user.is_staff = True
        cls.user.save()

        permission_order = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission_order)


    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.login(**self.credentials)


    def test_get_product_view(self):
        response = self.client.get(
            reverse("shopapp:orders-export"),
        )
        self.assertEqual(response.status_code, 200)

        orders = Order.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": order.pk,
                "address": order.delivery_address,
                "promocode": order.promocode,
                "user": order.user.username,
                "products": [product.pk for product in order.products.all()],
            }
            for order in orders
        ]

        orders_data = response.json()
        self.assertEqual(
            orders_data["orders"],
            expected_data
        )



import logging
from timeit import default_timer

from csv import DictWriter

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.core.cache import cache

from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .forms import ProductForm
from .models import Product, Order, ProductImage, User

from .serializers import ProductSerializer, OrderSerializer
from .common import save_csv_products

log = logging.getLogger(__name__)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @method_decorator(cache_page(60))
    def list(self, *args, **kwargs):
        # print('Hello from product list view')
        return super().list(*args, **kwargs)

    @action(detail=False, methods=["get"])
    def download_csv(self, request: HttpRequest) -> HttpResponse:
        response = HttpResponse(content_type="text/csv")
        filename = "products-export.csv"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "description",
            "price",
            "discount",
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        # for product in queryset:
        #     writer.writerow({
        #         "name": product.name,
        #         "description": product.description,
        #         "price": product.price,
        #         "discount": product.discount,
        #     })

        for product in queryset:
            writer.writerow({
                field: getattr(product, field) for field in fields
            })

        return response

    @action(detail=False, methods=["post"], parser_classes=[MultiPartParser])
    def upload_csv(self, request: Request) -> Response:
        products = save_csv_products(
            request.FILES["file"].file,
            encoding=request.encoding,)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class ShopIndexView(View):

    # @method_decorator(cache_page(60))
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
        }
        print("Product for shop index view: ", products)
        log.debug("Product for shop index view: %s", products)
        log.info("Rendering shop index view")
        return render(request, 'shopapp/shop-index.html', context=context)


class ProductDetailsView(DetailView):
    template_name = "shopapp/products-details.html"
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    # model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(CreateView):
    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products_list")


class ProductUpdateView(UpdateView):
    model = Product
    # fields = "name", "price", "description", "discount", "preview"
    template_name_suffix = "_update_form"
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )

        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by('pk').all()
            products_data = [
                {
                    "pk": product.pk,
                    "name": product.name,
                    "price": product.price,
                    "archived": product.archived,
                }
                for product in products
            ]
            elem = products_data[0]
            name = elem["name"]
            print("name: ", name)

            cache.set(cache_key, products_data, timeout=120)

        return JsonResponse({"products": products_data})

class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/user_order_list.html'
    context_object_name = 'orders'
    queryset = Order.objects.select_related('user')

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        self.user = user
        return super().get_queryset().filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        return context


class UserOrdersExportView(View):
    def get(self, request, user_id):
        user = User.objects.filter(pk=user_id).first()
        if not user:
            return HttpResponseNotFound("User not found")

        cache_key = f"user_orders_export_{user_id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return JsonResponse(cached_data)

        orders = Order.objects.filter(user=user_id).order_by('pk')
        serializer = OrderSerializer(orders, many=True)
        serialized_data = serializer.data

        cache.set(cache_key, serialized_data, timeout=180)

        return JsonResponse(serialized_data, safe=False)


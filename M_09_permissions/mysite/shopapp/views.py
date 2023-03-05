from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from .models import Product, Order


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
        }
        return render(request, 'shopapp/shop-index.html', context=context)

class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ["shopapp.add_product", ]
    model = Product
    fields = "name", "price", "description", "discount"  #, "created_by"
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        super().form_valid(form)
        return HttpResponseRedirect(self.success_url)

class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)

class ProductDetailsView(DetailView):
    template_name = "shopapp/products-details.html"
    model = Product
    context_object_name = "product"

class ProductUpdateView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = ["shopapp.change_product", ]
    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def test_func(self):

        if self.request.user.is_superuser:
            return True
        else:
            queryset = self.get_queryset()
            item = super().get_object(queryset)
            result = True if self.request.user.id == item.created_by_id else False
            return result

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

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
    # permission_required = ["view_order",]
    permission_required = ["shopapp.view_order",]
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )

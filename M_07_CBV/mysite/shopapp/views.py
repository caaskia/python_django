from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy

from .models import Product, Order

from django.contrib.auth.models import Group
from .forms import GroupForm

class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'shopapp/index.html')


class ProductListView(ListView):
    # model = Product
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'products'
    template_name = 'shopapp/products-list.html'

class ProductDetailsView(DetailView):
    template_name = 'shopapp/products-details.html'
    model = Product
    context_object_name = 'product'

class ProductCreateView(CreateView):
    model = Product
    fields =  'name', 'price', 'description', 'discount'
    success_url = reverse_lazy("shopapp:products_list")

class ProductUpdateView(UpdateView):
    model = Product
    fields =  'name', 'price', 'description', 'discount'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
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



class OrdersListView(ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )
    # template_name = 'shopapp/products-list.html'
    context_object_name = 'orders'

class OrdersDetailView(DetailView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )

class OrdersCreateView(CreateView):
    model = Order
    fields =  'delivery_address', 'user', 'products', 'promocode'
    template_name_suffix = '_create_form'
    success_url = reverse_lazy("shopapp:orders_list")

class OrdersUpdateView(UpdateView):
    model = Order
    fields =  'delivery_address', 'user', 'products', 'promocode'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:order_details',
            kwargs={"pk": self.object.pk},
        )

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")

    # def form_valid(self, form):
    #     success_url = self.get_success_url()
    #     self.object.archived = True
    #     self.object.save()
    #     return HttpResponseRedirect(success_url)



# Simple View
class ProductListView_TemplateView(TemplateView):
    template_name = 'shopapp/products-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        context["products"] = products
        return context

class ProductDetailsView_View(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        # product = Product.objects.get(pk=pk)
        product = get_object_or_404(Product, pk=pk)
        context = {
            "product": product,
        }
        return render(request, 'shopapp/products-details.html', context=context)




class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        groups_permission = Group.objects.prefetch_related('permissions').all()
        context = {
            "form": GroupForm(),
            "groups": groups_permission,
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)



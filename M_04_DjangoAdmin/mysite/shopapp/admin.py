from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Product, Order

from .admin_mixins import ExportAsCSVMixin

# class OrderInLine(admin.TabularInline):
class OrderInLine(admin.StackedInline):
    model = Product.orders.through

@admin.action(description='Archive products')
def mark_archivied(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archivied=True)

@admin.action(description='Unarchive products')
def mark_unarchivied(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archivied=False)

@ admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archivied,
        mark_unarchivied,
        'export_csv',
    ]
    inlines = [
        OrderInLine,
    ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archivied'
    list_display_links = 'pk', 'name'
    list_filter = 'name', 'archivied'
    ordering = 'name', 'pk'
    search_fields = 'name', 'description', 'price'

    fieldsets = [
        (None,{
            "fields": ('name', 'description'),
        }),
        ('Price options', {
            "fields": ('price', 'discount'),
            "classes": ('collapse','wide')
        }),
        ('Extra options', {
            "fields": ('archivied',),
            "classes": ('collapse', ),
            "description": "Field 'archivied' is soft delete"
        }),
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return str(obj.description)
        return obj.description[:48] + '...'

# admin.site.register(Product, ProductAdmin)

# class ProductInLine(admin.TabularInline):
class ProductInLine(admin.StackedInline):
    model = Order.products.through

@ admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInLine,
    ]
    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    def get_queryset(self, request):
        # return Order.objects.select_related('user')
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

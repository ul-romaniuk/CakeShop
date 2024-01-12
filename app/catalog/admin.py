from django.contrib import admin

from catalog.models import Category, Order, Product, OrderItem


class ProductCategoryInline(admin.StackedInline):
    model = Product.category.through
    extra = 1


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [ProductCategoryInline]


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'min_order', 'unit', 'is_active', 'image']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['phone', 'status']
    inlines = [OrderItemInline]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'order']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

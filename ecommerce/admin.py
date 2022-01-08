from django.contrib import admin

from .models import *


# Register your models here.

@admin.register(Setting)
class AdminSetting(admin.ModelAdmin):
    list_filter = ['c_name']
    list_display = ['c_name', 'c_email', 'c_phone', 'c_address']
    search_fields = ['c_name']


@admin.register(Attribute)
class AdminAttribute(admin.ModelAdmin):
    pass


@admin.register(AttributeValue)
class AdminAttributeValue(admin.ModelAdmin):
    pass


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    pass


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    prepopulated_fields = {'product_slug': ('product_name',)}


@admin.register(ProductImage)
class AdminProductImage(admin.ModelAdmin):
    pass


@admin.register(ProductAttribute)
class AdminProductAttribute(admin.ModelAdmin):
    pass


@admin.register(UniqueCart)
class AdminCart(admin.ModelAdmin):
    pass


@admin.register(CartProduct)
class AdminCartProduct(admin.ModelAdmin):
    pass


@admin.register(Order)
class AdminProductOrder(admin.ModelAdmin):
    pass

from django.contrib import admin

from .models import User, Item, Order, Discount, Tax


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active')
    list_filter = ('id', 'is_active')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price')
    list_filter = ('id', 'name', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ('items',)
    list_display = ('id', 'user', 'paid', 'total_price', 'tax', 'discount', 'created_at')
    list_filter = ('id', 'user', 'paid', 'total_price', 'created_at', 'tax', 'discount',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'percent')
    list_filter = ('id', 'percent')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'tax_rate')
    list_filter = ('id', 'tax_rate')

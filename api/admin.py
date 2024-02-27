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
    list_display = ('id', 'user', 'items', 'payment_id', 'paid', 'total_price', 'created_at')
    list_filter = ('id', 'user', 'paid', 'total_price', 'created_at')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'name', 'percent')
    list_filter = ('id', 'name', 'percent')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'tax_rate', 'tax_amount')
    list_filter = ('id', 'tax_rate', 'tax_amount')

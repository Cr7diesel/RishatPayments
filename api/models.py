from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    pass


class Item(models.Model):

    name = models.CharField(max_length=255, verbose_name="Название товара")
    price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Стоимость товара"
    )
    description = models.TextField(verbose_name="Описание товара")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Список товаров"


class Order(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_orders"
    )
    items = models.ManyToManyField(
        Item, related_name="order_items", verbose_name="Список товаров"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания заказа"
    )
    paid = models.BooleanField(default=False, verbose_name="Статус заказа")
    total_price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Стоимость товаров"
    )
    tax = models.ForeignKey(
        to="Tax",
        on_delete=models.CASCADE,
        related_name="order_tax",
        verbose_name="Налог",
    )
    discount = models.ForeignKey(
        to="Discount",
        on_delete=models.CASCADE,
        related_name="order_discount",
        verbose_name="Скидка",
    )

    def __str__(self):
        return self.total_price

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Список заказов"
        ordering = ("-created_at",)


class Discount(models.Model):

    percent = models.PositiveIntegerField(default=0, verbose_name="Процент скидки")

    def __str__(self):
        return self.percent

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"


class Tax(models.Model):

    tax_rate = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name="Налоговая ставка в процентах"
    )

    def __str__(self):
        return self.tax_rate

    class Meta:
        verbose_name = "Налоговая ставка"
        verbose_name_plural = "Налоговые ставки"

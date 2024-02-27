from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    pass


class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(Item)
    payment_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.created_at

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Список заказов'
        ordering = ('-created_at',)


class Discount(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='discounts')
    name = models.CharField(max_length=255)
    percent = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Tax(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='taxes')
    tax_rate = models.DecimalField(max_digits=3, decimal_places=1)
    tax_amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.tax_rate

    class Meta:
        verbose_name = 'Налоговая ставка'
        verbose_name_plural = 'Налоговые ставки'

from .utils import get_distance, fetch_coordinates

from functools import reduce
from django.db import models
from django.db.models import Sum, F, DecimalField
from django.core.validators import MinValueValidator, MaxValueValidator

from phonenumber_field.modelfields import PhoneNumberField

STATUS_CHOICES = (
    ('UNPROCESSED', 'Не обработан'),
    ('IN PROCESS', 'Собирается'),
    ('IN DELIVERY', 'Доставляется'),
    ('DONE', 'Выполнен'),
)

PAYMENT_CHOICES = (
    ('CASH', 'Наличка'),
    ('ONLINE', 'Онлайн'),
    ('CARD', 'Картой'),
)


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
                .filter(availability=True)
                .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def get_order_cost(self):
        return self.annotate(order_cost=Sum('items__price'))

    def get_order_restaurants(self):
        restaurant_menu_product = RestaurantMenuItem.objects.select_related('product', 'restaurant')
        for order in self:
            restaurants_products = []
            for order_product in order.items.all():
                restaurants_products.append([restaurant_item.restaurant for restaurant_item in restaurant_menu_product
                                             if order_product.product_id == restaurant_item.product.id])
            available_restaurants = reduce(set.intersection, map(set, restaurants_products))
            for restaurant in available_restaurants:
                restaurant.distance = get_distance(fetch_coordinates(order.address), fetch_coordinates(restaurant.address))
            order.available_restaurant = available_restaurants
        return self


class Order(models.Model):
    firstname = models.CharField(
        'Имя заказчика',
        max_length=20
    )
    lastname = models.CharField(
        'Фамилия заказчика',
        max_length=20
    )
    phonenumber = PhoneNumberField()
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    objects = OrderQuerySet.as_manager()
    status = models.CharField(
        'Статус заказа',
        max_length=20,
        choices=STATUS_CHOICES,
        default='UNPROCESSED',
        db_index=True
    )
    comment = models.TextField(
        'Комментарий к заказу',
        blank=True
    )
    payment = models.CharField(
        'Способ оплаты',
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='NOT STATED',
        db_index=True
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        verbose_name='заказ',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name='items',
        verbose_name='товар',
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(
        'количество',
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    price = models.DecimalField(
        'цена позиции',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"{self.order.id} {self.order.phonenumber}"

    class Meta:
        verbose_name = 'позиции заказа'
        verbose_name_plural = 'позиции заказа'

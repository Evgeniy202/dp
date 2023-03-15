from email.mime import image
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Найменування категорії')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Найменування')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Зображення')
    description = models.TextField(verbose_name='Опис', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Ціна')
    features = models.ManyToManyField("specs.ProductFeatures", blank=True, related_name='features_for_product')
    active = models.BooleanField(verbose_name="Товар в наявності", default=True)
    img1 = models.ImageField(verbose_name="Додаткове зображення (не обов'язково)", null=True, blank=True)
    img2 = models.ImageField(verbose_name="Додаткове зображення (не обов'язково)", null=True, blank=True)
    img3 = models.ImageField(verbose_name="Додаткове зображення (не обов'язково)", null=True, blank=True)
    img4 = models.ImageField(verbose_name="Додаткове зображення (не обов'язково)", null=True, blank=True)
    img5 = models.ImageField(verbose_name="Додаткове зображення (не обов'язково)", null=True, blank=True)
    img6 = models.ImageField(verbose_name="Додаткове зображення (не обов'язково)", null=True, blank=True)
    img7 = models.ImageField(verbose_name="Додаткове зображення (не обов'язково)", null=True, blank=True)
    img8 = models.ImageField(verbose_name="Додаткове зображення (не обов'язково)", null=True, blank=True)
    mainView = models.BooleanField(verbose_name="Показувати на головній", default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_features(self):
        return {f.feature.feature_name: ' '.join([f.value, f.feature.unit or ""]) for f in self.features.all()}


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупець', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Кошик', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Загальна ціна')

    def __str__(self):
        return "Товар: {} (для кошика)".format(self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', null=True, verbose_name='Власник', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Загальна ціна')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Покупець', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Замовлення покупця', related_name='related_order')

    def __str__(self):
        return "Покупець: {} {}".format(self.user.first_name, self.user.last_name)


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELED = 'canceled'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Нове замовлення'),
        (STATUS_IN_PROGRESS, 'Замовлення в оброці'),
        (STATUS_READY, 'Замовлення готове'),
        (STATUS_COMPLETED, 'Замовленння виконане'),
        (STATUS_CANCELED, 'Замовлення скасовано')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовивіз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупець', related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name="Ім'я")
    last_name = models.CharField(max_length=255, verbose_name='Прізвище')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Кошик', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адреса', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус замовлення',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип замовлення',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментар щодо замовлення', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата створення замовлення')

    # order_date = models.DateField(verbose_name='Дата отримання замовлення', default=timezone.now)

    def __str__(self):
        return str(self.id)


class Banner(models.Model):
    title = models.CharField(max_length=255, verbose_name="Назва банера")
    slug = models.SlugField(unique=True)
    link = models.CharField(max_length=255, verbose_name="Посилання (Не обов'язково)", null=True, blank=True)
    image = models.ImageField(verbose_name="Зображення")
    first = models.BooleanField(verbose_name='Перший в слайдері', default=False)
    active = models.BooleanField(verbose_name='Активність', default=False)

    def __str__(self):
        return self.title


class ChangePassword(models.Model):
    login = models.CharField(max_length=255, verbose_name="Ваш логін")
    email = models.EmailField(verbose_name="Ваша електронна пошта")
    newPassword = models.CharField(max_length=255, verbose_name="Новий пароль")
    ready = models.BooleanField(default=False, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата')

    def __str__(self):
        return str(self.id)


class CommentModel(models.Model):
    product = models.CharField(max_length=255, verbose_name="Товар")
    name = models.CharField(max_length=255, verbose_name="Ваше ім'я")
    generalDescription = models.CharField(max_length=255, verbose_name="Коротка оцінка товару")
    comment = models.TextField(verbose_name="Коментар", null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата створення замовлення')

    def __str__(self):
        return str(self.id)


class Support(models.Model):

    STATUS_NEW = 'new'
    STATUS_PROSSES = 'prosses'
    STATUS_CLOSED = 'closed'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Нове'),
        (STATUS_PROSSES, 'В процеці'),
        (STATUS_CLOSED, 'Закрито')
    )


    name = models.CharField(max_length=255, verbose_name='Як до вас звертатись')
    contact = models.CharField(max_length=255, verbose_name="Електронна поошта або номер телефону для зв'язку")
    description = models.TextField(verbose_name='Задайте питання або опишіть проблему')
    status = models.CharField(
        max_length=100,
        verbose_name='Статус',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата створення замовлення')

    def __str__(self):
        return str(self.id)
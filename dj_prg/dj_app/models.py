from django.db import models
from django.contrib.auth.models import AbstractUser  # Импортируем встроенную модель "Пользователи"
from django.core.validators import RegexValidator  # Для сохранения номера телефона
# from phonenumber_field.modelfields import PhoneNumberField  # Для номера телефона с префиксом

# Commands for migrations:
# python manage.py makemigrations
# python manage.py migrate


# Модель User (для создания страницы с профилем)
class User(AbstractUser):
    image = models.ImageField(upload_to='user_img', null=True, blank=True, verbose_name="Добавить изображение")


# Модель Компания (главная таблица)
class Company(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название компании")
    objects = models.Model

    # При просмотре всей модели из админки (поле которое будет отображаться в таблице)
    def __str__(self):
        return self.name

    # НАСТРОЙКИ перевода модели и сортировки объектов на главной таблице
    class Meta:
        verbose_name = "Компанию"  # Название модели в ед.числе
        verbose_name_plural = "Компании"  # Название модели в мнж.числе
        ordering = ["name"]  # Сортировка по полю (если с "-" то в обратном порядке)


# Модель Страна (Country)
class Country(models.Model):
    name = models.CharField(max_length=20, verbose_name="Страна")
    objects = models.Model

    # При просмотре всей модели из админки (поле которое будет отображаться в таблице)
    def __str__(self):
        return self.name

    # НАСТРОЙКИ перевода модели и сортировки объектов на главной таблице
    class Meta:
        verbose_name = "Страна"  # Название модели в ед.числе
        verbose_name_plural = "Страны"  # Название модели в мнж.числе
        ordering = ["name"]  # Сортировка по полю (если с "-" то в обратном порядке)


# Модель Сторона (Side)
class Side(models.Model):
    side = models.CharField(max_length=20, help_text="Введите сторону", verbose_name="Сторона")
    objects = models.Model

    # При просмотре всей модели из админки (поле которое будет отображаться в таблице)
    def __str__(self):
        return self.side

    # НАСТРОЙКИ перевода модели и сортировки объектов на главной таблице
    class Meta:
        verbose_name = "Сторона"  # Название модели в ед.числе
        verbose_name_plural = "Стороны"  # Название модели в мнж.числе
        ordering = ["side"]  # Сортировка по полю (если с "-" то в обратном порядке)


# Модель Группа (GroupProduct)
class GroupProduct(models.Model):
    view = models.CharField(max_length=20, unique=True, help_text="Введите вид товара", verbose_name="Вид товара")
    slug = models.SlugField(max_length=200, blank=True)
    objects = models.Model

    # При просмотре всей модели из админки (поле которое будет отображаться в таблице)
    def __str__(self):
        return self.view

    # НАСТРОЙКИ перевода модели и сортировки объектов на главной таблице
    class Meta:
        verbose_name = "Категория товара"  # Название модели в ед.числе
        verbose_name_plural = "Категории товаров"  # Название модели в мнж.числе
        ordering = ["view"]  # Сортировка по полю (если с "-" то в обратном порядке)


# Модель Продукт (второстепенная таблица)
class Product(models.Model):
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, help_text="Выберите компанию", verbose_name="Компания")  # Связывающее поле
    slug = models.SlugField(max_length=200, db_index=True, blank=True, verbose_name="url")
    title = models.CharField(max_length=200, help_text="Введите название товара", verbose_name="Название товара")
    summary = models.TextField(max_length=1000, help_text="Введите описание товара", verbose_name="Описание товара")
    product_code = models.IntegerField(null=True, help_text="Введите код товара", verbose_name="Код товара")
    manufacturer = models.ForeignKey(Country, null=True, on_delete=models.CASCADE, max_length=20, help_text="Введите страну производителя", verbose_name="Страна производителя")
    price = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="Введите цену товара", verbose_name="Цена товара")
    quantity = models.PositiveIntegerField(default=0, help_text="Введите количество товара", verbose_name="Количество товара")
    view = models.ForeignKey(GroupProduct, related_name='products', null=True, on_delete=models.CASCADE, help_text="Выберите вид (категорию) товара", verbose_name="Вид (категория) товара")
    side = models.ForeignKey(Side, null=True, on_delete=models.CASCADE, help_text="Выберите сторону", verbose_name="Сторона")
    image = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True, verbose_name="Добавить изображение")
    available = models.BooleanField(default=True)
    objects = models.Model

    # При просмотре всей модели из админки (поле которое будет отображаться в таблице)
    def __str__(self):
        return self.title

    # [ВНУТРЕННИЙ МЕТОД] Возвращающий ссылку на товар
    def get_absolute_url(self):
        return f'/product/{self.pk}'

    # НАСТРОЙКИ перевода модели и сортировки объектов на главной таблице
    class Meta:
        verbose_name = "Продукт"  # Название модели в ед.числе
        verbose_name_plural = "Продукты"  # Название модели в мнж.числе
        ordering = ["title"]  # Сортировка по полю (если с "-" то в обратном порядке)
        index_together = (('id', 'slug'),)


# Модель Статьи
class Articles(models.Model):
    title = models.CharField(max_length=30, verbose_name="Заголовок статьи")
    anons = models.CharField(max_length=250, verbose_name="Анонс статьи")
    summary = models.TextField(max_length=1000, verbose_name="Описание товара")
    date = models.DateField(blank=True, null=True, verbose_name="Дата публикации")
    image = models.ImageField(upload_to='articles/%Y/%m/%d', null=True, blank=True, verbose_name="Добавить изображение")
    objects = models.Model

    # При просмотре всей модели из админки (поле которое будет отображаться в таблице)
    def __str__(self):
        return self.title

    # [ВНУТРЕННИЙ МЕТОД] Возвращающий ссылку на статью
    def get_absolute_url(self):
        return f'/article/{self.pk}'
        # return "/article/{}".format(self.pk)  # то же самое
        # !!! На будущее лучше называть модели в ед. числе, чтобы не было потом путаницы !!!

    # НАСТРОЙКИ перевода модели и сортировки объектов на главной таблице
    class Meta:
        verbose_name = "Статью"  # Название модели в ед.числе
        verbose_name_plural = "Статьи"  # Название модели в мнж.числе
        ordering = ["-date"]  # Сортировка по полю (если с "-" то в обратном порядке)


# Модель Обратная связь
class Feedback(models.Model):
    name = models.CharField(null=True, max_length=10, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=False)
    # phone = PhoneNumberField()  # для способа с префиксом (нужна доработка)
    message = models.TextField(max_length=200, verbose_name="Текст сообщения")
    objects = models.Model

    # При просмотре всей модели из админки (поле которое будет отображаться в таблице)
    def __str__(self):
        return self.name

    # НАСТРОЙКИ перевода модели и сортировки объектов на главной таблице
    class Meta:
        verbose_name = "Обращение"  # Название модели в ед.числе
        verbose_name_plural = "Обращения"  # Название модели в мнж.числе
        ordering = ["-email"]  # Сортировка по полю (если с "-" то в обратном порядке)

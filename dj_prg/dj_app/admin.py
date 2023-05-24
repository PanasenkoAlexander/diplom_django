from django.contrib import admin
from .models import *

# # Аналогичный (упрощенный) способ:
# admin.site.register(User)
# admin.site.register(Company)
# admin.site.register(Country)
# admin.site.register(Side)
# admin.site.register(GroupProduct)
# admin.site.register(Product)
# admin.site.register(Articles)
# admin.site.register(Feedback)


# Регистрация и настройка модели User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username"]


# Регистрация и настройка модели Company
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # Пагинация в админке (При отображении модели)
    list_per_page = 3
    # Отображение поискового поля
    search_fields = ['__str__']


# Регистрация и настройка модели Country
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    # Отображение поискового поля
    search_fields = ['name']


# Регистрация и настройка модели Side
@admin.register(Side)
class SideAdmin(admin.ModelAdmin):
    # Порядок вывода СТОЛБИКОВ (При отображении модели)
    list_display = ["side"]


# Регистрация и настройка модели GroupProduct
@admin.register(GroupProduct)
class GroupProductAdmin(admin.ModelAdmin):
    # Порядок вывода СТОЛБИКОВ (При отображении модели)
    list_display = ['view']
    # prepopulated_fields = {'slug': ('view',)}


# Регистрация и настройка модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Порядок вывода СТОЛБИКОВ (При отображении модели)
    list_display = ['title', 'company', 'view', 'side', 'price', 'product_code']
    # # Возможность корректировки СТОЛБИКОВ (первый столбик убираем, поскольку он должен быть кликабелен)
    list_editable = ['price']
    # Пагинация в админке (При отображении модели)
    list_per_page = 3
    # Отображение поискового поля
    search_fields = ['title', 'price']
    # Добавление ФИЛЬТРА (По перечисленным полям)
    list_filter = ['title', 'company', 'view', 'price']
    # Порядок вывода ПОЛЕЙ (При заполнении модели)
    fieldsets = (("Основное", {"fields": ('title', 'company', 'price', 'view', 'side')}),
                 ("Дополнительное", {"fields": ("manufacturer", "summary", "product_code", "quantity", "image")}))
    # prepopulated_fields = {'slug': ('title',)}


# Регистрация и настройка модели Articles
@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    pass


# Регистрация и настройка модели Feedback
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    # Порядок вывода СТОЛБИКОВ (При отображении модели)
    list_display = ["name", 'email', 'phoneNumber']
    # Отображение поискового поля
    search_fields = ['name', 'phoneNumber']
    # Добавление ФИЛЬТРА (По перечисленным полям)
    list_filter = ['name', 'phoneNumber']

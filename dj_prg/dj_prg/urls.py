from django.contrib import admin
from django.urls import path, include
from dj_app import views
from django.conf.urls.static import static  # Для обработки картинок
from django.conf import settings  # Для обработки картинок

admin.site.site_header = "Django админка"
admin.site.index_title = "Моя админ-панель"

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name="index"),  # Маршрут: Главная
    path('about', views.about, name="about"),  # Маршрут: О нас
    path('contacts', views.contacts, name="contacts"),  # Маршрут: Контакты
    path('rating', views.rating, name="rating"),  # Маршрут: Рейтинг
    path('agreement', views.agreement, name="agreement"),  # Маршрут: Пользовательские условия

    path('profile', views.profile, name="profile"),  # Маршрут: Профиль
    path('accounts/login/', views.LoginUser.as_view(), name="login"),  # Маршрут для входа/выхода (Переназначение)
    path('accounts/', include("django.contrib.auth.urls")),  # Маршрут для работы с аккаунтами
    path('registration', views.registration, name="registration"),  # Маршрут: Регистрация

    path('articles', views.ArticlesListView.as_view(), name="articles"),  # Маршрут: Все Статьи
    path('article/<int:pk>', views.ArticlesDetailView.as_view(), name="article"),  # Маршрут: Конкретная статья
    # path('add_articles', views.add_articles, name="add_articles"),  # Маршрут: Добавления статьи (самописный)
    path('article/create', views.ArticlesCreate.as_view(), name='add_articles'),  # Маршрут: Добавление статьи
    path('article/<int:pk>/update', views.ArticlesUpdateView.as_view(), name="article_update"),  # Маршрут: Обновление статьи
    path('article/<int:pk>/delete', views.ArticlesDeleteView.as_view(), name="article_delete"),  # Маршрут: Удаление статьи

    path('products', views.ProductListView.as_view(), name="products"),  # Маршрут: Все товары
    path('product/<int:pk>', views.ProductDetailView.as_view(), name="product"),  # Маршрут: Конкретный товар
]

# Для обработки картинок - Настройка на уровне разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

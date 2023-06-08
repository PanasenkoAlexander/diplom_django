from django.test import TestCase

# - использование include в url
# - использование include в html - {% include 'test.html' %} - заимствование одного html в другом
# - отслеживание страницы по name в url через href="{% url 'index' %}"
# - использование названий страниц с помощью шаблонизатора {{ title }} - выведет название страницы во вкладке
# - использование сортировки в функции - Articles.objects.order_by("title")
# - {# для комментариев в шаблонизаторе #}
# - {% filter lower/upper %} - для нижнего/верхнего регистра букв
# - object_list - универсальная переменная для списка объектов при использовании внутреннего метода
# - reverse (для функций), reverse_lazy (для классов)

# Настройка PostgreSQL
# CREATE DATABASE website_db;
# CREATE ROLE store_username with password ‘324665’;
# ALTER ROLE "store_username" WITH LOGIN;
# GRANT ALL PRIVILEGES ON DATABASE "website_db" to store_username;
# ALTER USER store_username CREATEDB;
# \list – просмотр всех баз данных
# \connect website_db – подключение БД
# \dt – проверка на наличие таблиц в БД



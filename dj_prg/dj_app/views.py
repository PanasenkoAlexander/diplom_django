from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from .models import *
from rating_far import RatingFar  # использование парсинга
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView  # Для авто чтения модели
from django.contrib.auth.views import LoginView  # Для входа/выхода
from django.db.utils import IntegrityError  # Импорт ошибки при регистрации
from django.core.mail import EmailMultiAlternatives  # Импорт для боевой отправки по почте
from django.template.loader import render_to_string  # Импорт для боевой отправки по почте
from django.urls import reverse, reverse_lazy  # Для правильного перехода после отправки формы


# Метод Главной страницы сайта
def index(request):
    return render(request, "index.html")


# Метод Входа(Авторизации)/Выхода
class LoginUser(LoginView):
    form_class = Login
    template_name = "registration/login.html"


# Метод Формы регистрации
def registration(request):
    if request.method == "GET":
        form = Registration()  # Создать форму
        context = {"form": form}  # Генерация context
        # Показываем шаблон
        return render(request, "registration/registration.html", context=context)
    if request.method == "POST":
        # Получаем данные из формы
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        # Записываем данные в БД (нового пользователя)
        try:
            User.objects.create_user(username, email, password).save()
            context = {"username": username}  # Генерация context
            # Показываем шаблон
            return render(request, "registration/registration.html", context=context)
        # В случае если логин нового пользователя уже есть в БД
        except IntegrityError:
            context = {"error": username}  # Генерация context
            # Показываем шаблон
            return render(request, "registration/registration.html", context=context)


# Метод страницы Профиль
def profile(request):
    if request.method == 'POST':
        form = UserProfile(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            print("Успешно")
            return HttpResponseRedirect(reverse('profile'))
        else:
            print(form.errors)
    else:
        form = UserProfile(instance=request.user)
    context = {"form": form}
    return render(request, "registration/profile.html", context=context)


# Метод страницы О нас
def about(request):
    year = 2015
    workers = 50
    companies = "BOSCH, TYC, DEPO, HELLA, VALEO"
    context = {"year": year, "workers": workers, "companies": companies}
    return render(request, "about.html", context=context)


# Метод страницы Контакты + Обратная связь
def contacts(request):
    if request.method == "GET":
        form = FeedbackForm()  # Создание формы
        context = {"form": form}  # Генерация context
        return render(request, "contacts.html", context=context)  # Показываем шаблон
    if request.method == "POST":
        # Получаем данные из формы
        name = request.POST.get("name")
        email = request.POST.get("email")
        phoneNumber = request.POST.get("phoneNumber")
        message = request.POST.get("message")
        try:
            if not name == "" and not email == "" and not phoneNumber == "" and not message == "":
                kwargs = {"name": name, "email": email, "phoneNumber": phoneNumber, "message": message}  # Передаваемые аргументы
                DataBase.write(model=Feedback, **kwargs)  # Запись в БД
            # return redirect("contacts")  # альтернативный вариант без уведомления пользователя
            DataBase.read(model=Feedback)  # Читаю таблицу
            context = {"name": name}  # Генерация context
            return render(request, "contacts.html", context=context)  # Показываем шаблон
        except IntegrityError:
            context = {"error": name}  # Генерация context
            return render(request, "contacts.html", context=context)


# Метод страницы Рейтинг
def rating(request):
    obj_rating = RatingFar
    table_rating = obj_rating.get_rows()  # исходные данные рейтинга
    data = [[row[i] for row in table_rating]
            for i in range(len(table_rating[0]))]  # преобразование данных из table_rating в новые списки
    context = {"table_rating": data}  # , "my_loop": [0] (для второго способа)
    return render(request, "rating.html", context=context)


# Метод страницы Соглашение
def agreement(request):
    return render(request, "agreement.html")


# Метод добавления статей (самописный запасной вместо CreateView)
# def add_articles(request):
#     if request.method == "GET":
#         form = ArticlesForm()  # Создание формы
#         data = DataBase.read(model=Articles)  # Читаю таблицу
#         context = {"data": data, "form": form}  # Генерация context
#         return render(request, "add_articles.html", context=context)  # Показываем шаблон
#     if request.method == "POST":
#         # Получаем данные из формы
#         title = request.POST.get("title")
#         anons = request.POST.get("anons")
#         summary = request.POST.get("summary")
#         date = request.POST.get("date")
#         image = request.POST.get('image')
#         if not title == "" and not anons == "" and not summary == "" and not date == "" and not image == "":
#         # Передаваемые аргументы
#             kwargs = {"title": title, "anons": anons, "summary": summary, "date": date, "image": image}
#             DataBase.write(model=Articles, **kwargs)  # Запись в БД
#         return redirect("articles")


# Список всех статей (Автоматически генерируется при помощи ListView)
# Шаблон: "templates/dj_app/articles_list.html"
# Переменная (шаблона/ключ): "articles_list", такое название используется по умолчанию
class ArticlesListView(ListView):
    model = Articles  # Модель читаемая для шаблона
    paginate_by = 3  # Сколько объектов будет передано в шаблон


# Конкретная статья (Автоматически генерируется при помощи DetailView)
# Шаблон: "templates/dj_app/articles_detail.html"
# Переменная (шаблона/ключ): "article"
class ArticlesDetailView(DetailView):
    model = Articles


# Метод добавления статей (Автоматически генерируется при помощи CreateView)
# Шаблон: "templates/dj_app/articles_form.html"
class ArticlesCreate(CreateView):
    model = Articles
    form_class = ArticlesForm
    # fields = "__all__"  # все поля по умолчанию
    success_url = reverse_lazy("articles")  # Адрес перенаправления на список всех книг (после успешной отправки формы)


# Метод обновления статьи (Автоматически генерируется при помощи UpdateView)
# Шаблон: "templates/dj_app/articles_form.html"
class ArticlesUpdateView(UpdateView):
    model = Articles
    form_class = ArticlesForm
    # template_name = "dj_app/articles_form.html"  # задаётся если вдруг нужен другой шаблон
    # fields = ["title", "anons", "summary", "date", "image"]  # для стандартного отображения полей либо = "__all__"


# Метод удаления статьи (Автоматически генерируется при помощи DeleteView)
# Шаблон: "templates/dj_app/articles_confirm_delete.html"
class ArticlesDeleteView(DeleteView):
    model = Articles
    success_url = '/articles'


# Список всех статей (Автоматически генерируется при помощи ListView)
# Шаблон: "templates/dj_app/product_list.html"
# Переменная (шаблона/ключ): "product_list", такое название присваивается по умолчанию
class ProductListView(ListView):
    model = Product  # Модель читаемая для шаблона
    paginate_by = 6  # Сколько объектов будет передано в шаблон


# Конкретная статья (Автоматически генерируется при помощи DetailView)
# Шаблон: "templates/dj_app/product_detail.html"
# Переменная (шаблона/ключ): "product"
class ProductDetailView(DetailView):
    model = Product


# Класс содержащий ВНУТРЕННЮЮ работу с БД
class DataBase:

    @staticmethod
    # Чтение из таблицы "model" полей которые передаем {} через "kwargs"
    def read(model, mode="all", **kwargs):
        # .count() - метод возвращающий количество
        if mode == "all":  # Получить данные для [всех объектов]
            result = model.objects.all()
            return list(result.values())
        if mode == "filter":  # Получить данные [все которые = фильтр]
            result = model.objects.filter(**kwargs)
            return list(result.values())
        if mode == "exclude":  # Получить данные [все которые = не фильтр]
            result = model.objects.exclude(**kwargs)
            return list(result.values())
        if mode == "get":  # Получить данные для [одного объекта]
            result = model.objects.get(**kwargs)  # id/pk одно и тоже
            print(result, type(result))
            return [result]

    @staticmethod
    # Запись в таблицу "model" полей которые передаем {} через "kwargs"
    def write(model, **kwargs):
        model(**kwargs).save()  # или Person.objects.create(**kwargs)

    @staticmethod
    # Обновление объекта с "elm_id" в таблице "model", а именно перезапись полей на те, которые в {} через "kwargs"
    def update(model, elm_id, **kwargs):
        model.objects.filter(id=elm_id).update(**kwargs)

    @staticmethod
    # Удаление из таблицы "model" записи, удовлетворяющей фильтру переданному в {} через "kwargs"
    def delete(model, **kwargs):
        model.objects.filter(**kwargs).delete()

    # @staticmethod
    # # Создание нового пользователя "login" "password" "email"
    # def create_user(login, password, email):
    #     # DataBase.create_user("moderator2", "12345", "david@ewfi.com")
    #     try:
    #         User.objects.create_user(login, email, password).save()
    #     except IntegrityError:
    #         pass

    @staticmethod
    # Преобразование queryset в list в зависимости от режима "mode"
    def queryset_to_list(qs, mode=""):
        if mode == "elements":  # Финальный список из (элементов)
            result = []
            for elm in qs:
                result.append(elm)
            return result
        if mode == "name":  # Финальный список из (названий)
            result = []
            for elm in qs:
                result.append(elm.name)
            return result

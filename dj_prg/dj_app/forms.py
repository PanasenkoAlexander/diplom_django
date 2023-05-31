from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from .models import *
# from phonenumber_field.formfields import PhoneNumberField  # для иного способа поля с телефоном
# from phonenumber_field.widgets import PhoneNumberPrefixWidget  # для иного способа поля с телефоном с префиксом


# Переназначение формы Входа (на основе наследования)
class Login(AuthenticationForm):
    username = forms.CharField(label="Логин", max_length=10, widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'id': "floatingInput", "placeholder": "Username"}))
    password = forms.CharField(label="Пароль", widget=forms.widgets.PasswordInput(attrs={'class': 'form-control', 'id': "floatingInput", "placeholder": "Password"}))


# Создание формы Регистрации
class Registration(forms.Form):
    username = forms.CharField(label="Username", required=False, max_length=10, widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'id': 'floatingInput', 'placeholder': 'Username'}))
    password = forms.CharField(label="Password", required=True, widget=forms.widgets.PasswordInput(attrs={'type': 'password', 'class': 'form-control', 'id': 'floatingPassword', 'placeholder': 'Password'}))
    email = forms.EmailField(label="Email", required=True, widget=forms.widgets.EmailInput(attrs={'type': 'email', 'class': 'form-control', 'id': 'floatingInput', 'placeholder': 'name@example.com'}))


# Переназначение профиля пользователя (на основе наследования)
class UserProfile(UserChangeForm):
    image = forms.ImageField(label="Изображение", widget=forms.FileInput(attrs={'type': 'file', 'class': 'form-control'}), required=False)
    username = forms.CharField(label="Никнейм", max_length=10, widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'id': "floatingInput", "placeholder": "Username", 'readonly': True}))
    email = forms.EmailField(label="Email", widget=forms.widgets.EmailInput(
        attrs={'type': 'email', 'class': 'form-control', 'id': 'floatingInput', 'placeholder': 'login@example.com', 'readonly': True}))

    class Meta:
        model = User
        # fields = "__all__"  # вот где была загвоздка
        fields = ('image', 'username', 'email')


# Создание формы Добавление статьи
class ArticlesForm(forms.ModelForm):
    title = forms.CharField(label="Название", max_length=100, widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'id': 'floatingInput', 'placeholder': 'Название'}))
    anons = forms.CharField(label="Анонс", required=False, max_length=250, widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'id': 'floatingInput', 'placeholder': 'Анонс'}))
    summary = forms.CharField(label="Статья", widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'floatingInput', 'placeholder': 'Текст статьи'}))
    date = forms.DateField(label="Дата публикации", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Дата публикации'}))
    image = forms.ImageField(label="Изображение", widget=forms.FileInput(attrs={'type': 'file', 'class': 'form-control'}), required=False)

    class Meta:
        model = Articles
        fields = '__all__'


# Создание формы Обратной связи
class FeedbackForm(forms.Form):
    name = forms.CharField(label="Имя", required=True, max_length=10, widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'id': 'floatingInput', 'placeholder': 'Имя'}))
    email = forms.EmailField(label="Email", required=True, widget=forms.widgets.EmailInput(attrs={'type': 'email', 'class': 'form-control', 'id': 'floatingInput', 'placeholder': 'email'}))
    phoneNumber = forms.RegexField(regex=r'^\+?1?\d{8,15}$', label="Телефон", required=False, widget=forms.widgets.NumberInput(attrs={'type': 'phone', 'class': 'form-control', 'id': 'floatingInput', 'placeholder': 'Номер телефона в формате +375__ ___ __ __'}))
    message = forms.CharField(label="Краткое сообщение (до 200 символов)", required=False, max_length=200, widget=forms.widgets.Textarea(attrs={'class': 'form-control', 'id': 'floatingInput', 'placeholder': 'Краткое сообщение'}))

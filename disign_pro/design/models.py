from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.crypto import get_random_string


def get_name_file(instance, filename):
    return '/'.join([get_random_string(length=5) + '_' + filename])


class User(AbstractUser):
    name = models.CharField(max_length=254, verbose_name='ФИО', blank=False)
    login = models.CharField(max_length=254, verbose_name='Логин', blank=False, unique=True)
    email = models.EmailField(max_length=254, verbose_name='E-mail', blank=False, unique=True)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)
    role = models.CharField(max_length=254, verbose_name='Роль пользователя', blank=False,
                            choices=(('admin', 'Администратор'), ('user', 'Пользователь')), default='user')
    approval = models.BooleanField(verbose_name='Согласие на обработку персональных данных', default=True)

    username = None

    USERNAME_FIELD = 'login'

    def __str__(self):
        return str(self.name) + "/" + str(self.login)


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('accepted', 'Принято'),
        ('done', 'Выполнено')
    ]
    title = models.CharField(max_length=254, verbose_name='Заявка', blank=False)
    description = models.CharField(max_length=500, verbose_name='Описание', blank=False)
    photo = models.ImageField(max_length=254, upload_to=get_name_file, verbose_name="Фото", blank=False,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp'])])
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE, blank=False)
    status = models.CharField(max_length=254, verbose_name='Статус', choices=STATUS_CHOICES,
                              default='new', blank=False)


class Category(models.Model):
    name = models.CharField(max_length=254, verbose_name='Категория', blank=False)

    def __str__(self):
        return self.name

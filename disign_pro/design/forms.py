from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from design.models import User, Order


class RegisterUserForm(forms.ModelForm):
    name = forms.CharField(label='ФИО',
                           validators=[RegexValidator('^[а-яА-Я- ]+$',
                                                      message='Разрешены только кириллические символы, дефис и '
                                                              'пробелы')],
                           error_messages={
                               'required': 'Поле обязательно для заполнения', }
                           )
    login = forms.CharField(label='Логин',
                            validators=[RegexValidator('^[a-zA-Z-]+$',
                                                       message='Разрешены только латинские символы и дефис')],
                            error_messages={
                                'required': 'Поле обязательно для заполнения',
                                'unique': 'Такой логин уже существует'
                            })
    email = forms.EmailField(label='E-mail',
                             error_messages={
                                 'invalid': 'Неверный синтаксис электронной почты',
                                 'unique': 'Такая почта уже существует'
                             })
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput,
                               error_messages={
                                   'required': 'Поле обязательно для заполнения'
                               })
    password2 = forms.CharField(label='Повтор пароля',
                                widget=forms.PasswordInput,
                                error_messages={
                                    'required': 'Поле обязательно для заполнения'
                                })
    approval = forms.BooleanField(initial=True,
                                  label='Согласие на обработку персональных данных',
                                  error_messages={
                                      'required': 'Поле обязательно для заполнения'
                                  })

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise ValidationError({
                'password2': ValidationError('Пароли не совпадают')
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('name', 'login', 'email', 'password', 'password2', 'approval')


class CreateOrder(forms.ModelForm):
    title = forms.CharField(label='Заказ', validators=[RegexValidator('^[а-яА-Я- ]+$',
                                                                      message='Разрешены только кириллические '
                                                                              'символы, дефис и '
                                                                              'пробелы')],
                            error_messages={
                                'required': 'Поле обязательно для заполнения', }
                            )
    description = forms.CharField(label='Заказ', widget=forms.Textarea, error_messages={
        'required': 'Поле обязательно для заполнения'})
    category = forms.ChoiceField(label='Категория')
    photo = forms.ImageField(label='Фото', widget=forms.ClearableFileInput, error_messages={'required': 'Поле '
                                                                                                        'обязательно '
                                                                                                        'для '
                                                                                                        'заполнения'})

    class Meta:
        model = Order
        fields = ('title', 'description', 'category', 'photo')

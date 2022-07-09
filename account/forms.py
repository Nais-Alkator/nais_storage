from django import forms
from django.contrib.auth.models import User
from .models import Profile
from phonenumber_field.formfields import PhoneNumberField

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput)
    first_name = forms.CharField(label='Имя', widget=forms.TextInput)
    patronymic = forms.CharField(label='Отчество', widget=forms.TextInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget(years=range(1900, 2010)))
    contact_phone = PhoneNumberField(label='Контактный телефон')
    passport = forms.CharField(label="Серия и номер паспорта", widget=forms.TextInput)
    address = forms.CharField(label="Адрес", widget=forms.TextInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("last_name", 'first_name', 'patronymic', 'date_of_birth',
                  'contact_phone', 'passport', 'address')
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)
    last_name = models.CharField(verbose_name="фамилия", max_length=50, db_index=True)
    first_name = models.CharField(verbose_name="имя", max_length=50, db_index=True)
    patronymic = models.CharField(verbose_name="отчество", db_index=True, max_length=50)
    email = models.EmailField(verbose_name="email", max_length=100, db_index=True, blank=True)
    contact_phone = PhoneNumberField(verbose_name="контактный телефон", db_index=True)
    date_of_birth = models.DateField(verbose_name="дата рождения", db_index=True)
    passport = models.CharField(verbose_name="серия и номер паспорта", max_length=20)
    address = models.CharField(verbose_name="адрес", db_index=True, max_length=150)
    qr_code = models.ImageField(verbose_name="qr-код", upload_to="user_qr_codes/", null=True, blank=True)

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

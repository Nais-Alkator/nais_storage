from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from account.models import Profile
from django.core.validators import MinValueValidator


class Storage(models.Model):
    name = models.CharField(verbose_name="название", max_length=30)
    address = models.CharField(verbose_name="адрес", max_length=100)
    contact_phone = PhoneNumberField(verbose_name="контактный телефон")
    longitude = models.DecimalField(verbose_name="долгота", max_digits=11, decimal_places=8, null=True, blank=True)
    latitude = models.DecimalField(verbose_name="широта", max_digits=10, decimal_places=8, null=True, blank=True)

    class Meta:
        verbose_name = "склад"
        verbose_name_plural = "склады"

    def __str__(self):
        return self.name


class Box(models.Model):
    name = models.CharField(verbose_name="название", max_length=20)
    size = models.IntegerField(verbose_name="размер в м.кв.")
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = "бокс"
        verbose_name = "боксы"

    def __str__(self):
        return self.name


class Order(models.Model):
    storage = models.ForeignKey(Storage, verbose_name="склад", related_name="orders", null=True, blank=True,
                                on_delete=models.SET_NULL)
    date_from = models.DateField(verbose_name="дата хранения с")
    date_to = models.DateField(verbose_name="дата хранения по")
    client = models.ForeignKey(Profile, verbose_name="клиент", related_name="orders", null=True, blank=True,
                               on_delete=models.SET_NULL)
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2,
                                validators=[MinValueValidator(0)])


    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return f'{self.client}'


class BoxOrder(Order):
    box = models.ForeignKey(Box, verbose_name="бокс", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "боксовый заказ"
        verbose_name_plural = "боксовые заказы"

    def __str__(self):
        return f'{self.client}'




class SeasonItem(models.Model):
    CATEGORY_CHOICES = [("МГВ", "Малогабаритная вещь"), ("СГВ", "Среднегабаритная вещь"),
                      ("КГВ", "Крупногабаритная вещь"), ("ВОХ", "Вещь для особого хранения")]

    name = models.CharField(verbose_name="название", db_index=True, max_length=30)
    image = models.ImageField(verbose_name="картинка", upload_to="season_items/", max_length=30)
    category = models.CharField(verbose_name="категория", choices=CATEGORY_CHOICES, max_length=30)

    class Meta:
        verbose_name = "вещь сезонного хранения"
        verbose_name_plural = "вещи для сезонного хранения"

    def __str__(self):
        return self.name


class SeasonOrder(Order):
    item = models.ForeignKey(SeasonItem, verbose_name="сезонная вещь", related_name="orders",
                             blank=True, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(verbose_name="количество", default=1, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = "заказ сезонного хранения"
        verbose_name_plural = "заказы сезонного хранения"

    def annotate_price(self):
        if self.item.category == "МГВ" and self.quantity in range(1, 4):
            self.price = 60
        elif self.item.category == "МГВ" and self.quantity in range(4, 7):
            self.price = 70
        elif self.item.category == "МГВ" and self.quantity in range(7, 11):
            self.price = 80
        elif self.item.category == "СГВ" and self.quantity in range(1, 4):
            self.price = 60
        elif self.item.category == "СГВ" and self.quantity in range(1, 4):
            self.price = 80
        elif self.item.category == "КГВ" and self.quantity in range(1, 4):
            self.price = 100
        return self.price

    def __str__(self):
        return f'{self.client.last_name} {self.client.first_name} {self.client.patronymic}'


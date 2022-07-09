from django.test import TestCase
from account.models import Profile
from nais_storage.models import Box

box = Box.objects.first()

class TestVerboseNameMixin:
    def run_verbose_names_test(self):
        for field_name, value in self.verbose_names.items():
            with self.subTest(f'{field_name=}'):
                field = self.model._meta.get_field(field_name)
                real_verbose_name = getattr(field, "verbose_name")
                self.assertEqual(real_verbose_name, value)


class TestMaxLengthMixin:
    def run_max_length_test(self):
        for field_name, value in self.max_lengthes.items():
            with self.subTest(f'{field_name=}'):
                field = self.model._meta.get_field(field_name)
                real_verbose_name = getattr(field, "max_length")
                self.assertEqual(real_verbose_name, value)


class TestModelVerboseNameMixin:
    def run_model_verbose_name_test(self, expected_verbose_name):
        self.assertEqual(self.model._meta.verbose_name, expected_verbose_name)


class TestModelVerboseNamePluralMixin:
    def run_model_verbose_name_plural_test(self, expected_verbose_name_plural):
        self.assertEqual(self.model._meta.verbose_name_plural, expected_verbose_name_plural)

MIXINS = (
    TestVerboseNameMixin, TestMaxLengthMixin, TestModelVerboseNameMixin, TestModelVerboseNamePluralMixin
)


class BoxTests(TestCase, *MIXINS):
    @classmethod
    def setUpTestData(cls):
        cls.model = box
        cls.verbose_names = {"name": "название", "size": "размер в м.кв.", "price": "цена"}
        cls.max_lengthes = {"name": 20}

    def test_verbose_name(self):
        super().run_verbose_names_test()

    def test_max_length(self):
        super().run_max_length_test()

    def test_str_method(self):
        str_method = f"{self.model.name}"
        self.assertEqual(str(self.model), str_method)

    def test_model_verbose_name(self):
        super().run_model_verbose_name_test("боксы")

    def test_model_verbose_name_plural(self):
        super().run_model_verbose_name_plural_test("боксыs")
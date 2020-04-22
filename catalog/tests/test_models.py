from django.test import TestCase

from catalog.models import Author


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        Author.objects.create(name='Jan', surname='Kowalski')

    def test_label_name_author(self):
        author = Author.objects.get(id=1)
        label_name = author._meta.get_field('name').verbose_name
        self.assertEqual(label_name, 'name')

    def test_label_surname_author(self):
        author = Author.objects.get(id=1)
        label_surname = author._meta.get_field('surname').verbose_name
        self.assertEqual(label_surname, 'surname')

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expect_object_name = f'{author.name} {author.surname}'
        self.assertEqual(expect_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')

    def test_label_date_death_author(self):
        author = Author.objects.get(id=1)
        label_date_of_death = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(label_date_of_death, 'Date Death')

    def test_value_max_length_name(self):
        author = Author.objects.get(id=1)
        max_value = author._meta.get_field('name').max_length
        self.assertEqual(max_value, 20)

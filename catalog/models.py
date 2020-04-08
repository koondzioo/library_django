from django.db import models

from enum import Enum


# class Categories(Enum):
#     Fantasy = 'Fantasy'
#     Horror = 'Horror'
#     History = 'History'
#     Mystery = 'Mystery'
#     Poetry = 'Poetry'
from django.urls import reverse


class Category(models.Model):
    """"""
    name = models.CharField(max_length=200, help_text="Insert book category")

    def __str__(self):
        """"""
        return self.name




class Book(models.Model):
    """"""
    title = models.CharField(max_length=20, help_text='Book Title')
    category = models.ManyToManyField(Category, help_text='Book Categories', verbose_name='Category')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, help_text='Book Author')
    # copies = models.CharField(max_length=20, help_text='Book Copies')
    isbn = models.CharField(max_length=13, help_text='Book ISBN')
    description = models.TextField(max_length=1000, help_text='Book Description', verbose_name='Book Description')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class Author(models.Model):
    """Definicja klasy dziedzicząca własności po wbudowanej klasie models.Model"""
    name = models.CharField(max_length=20, help_text='Author Name')
    surname = models.CharField(max_length=20, help_text='Author Category')
    book_lists = models.ManyToManyField(Book)
    rating = models.CharField(max_length=20, help_text='Author Rating')


class Ordered_book(models.Model):
    """Definicja klasy dziedzicząca własności po wbudowanej klasie models.Model"""
    book_id = models.CharField(max_length=20, help_text='Book ID')
    user_id = models.CharField(max_length=20, help_text='User ID')
    date_of_return = models.CharField(max_length=20, help_text='Date Return')



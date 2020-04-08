from enum import Enum

from django.db import models


class Categories(Enum):
    Fantasy = 'Fantasy'
    Horror = 'Horror'
    History = 'History'
    Mystery = 'Mystery'
    Poetry = 'Poetry'


class Book(models.Model):
    """Definicja klasy dziedzicząca własności po wbudowanej klasie models.Model"""
    name = models.CharField(max_length=20, help_text='Book Name')
    category = models.CharField(choices=Categories.choices(), help_text='Book Category')
    authors = models.CharField(max_length=20, help_text='Book Authors')
    copies = models.CharField(max_length=20, help_text='Book Copies')
    rating = models.CharField(max_length=20, help_text='Book Rating')


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



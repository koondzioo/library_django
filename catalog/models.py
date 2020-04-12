import uuid
from datetime import date

from django.contrib.auth.models import User
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
    """Category Model"""
    name = models.CharField(max_length=200, help_text="Insert book category")

    def __str__(self):
        """Function to print categories"""
        return self.name


class Language(models.Model):
    """Language Model"""
    name = models.CharField(max_length=200, help_text="Insert book language")

    def __str__(self):
        """Function to print languages"""
        return self.name


class Book(models.Model):
    """Book Model"""
    title = models.CharField(max_length=20, help_text='Book Title')
    category = models.ManyToManyField(Category, help_text='Book Categories', verbose_name='Category')
    language = models.ManyToManyField(Language, help_text='Book Language', verbose_name='Language')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, help_text='Book Author')
    # copies = models.CharField(max_length=20, help_text='Book Copies')
    isbn = models.CharField(max_length=13, help_text='Book ISBN')
    description = models.TextField(max_length=1000, help_text='Book Description', verbose_name='Book Description')

    def __str__(self):
        """Function to print title"""
        return self.title

    def get_absolute_url(self):
        """Function return absolute url"""
        return reverse('book-detail', args=[str(self.id)])

    def display_category(self):
        """Function to display all categories"""
        return ', '.join(category.name for category in self.category.all())


class Author(models.Model):
    """Author Model"""
    name = models.CharField(max_length=20, help_text='Author Name')
    surname = models.CharField(max_length=20, help_text='Author Surname')
    date_of_death = models.DateField(null=True, blank=True, verbose_name='Date Death')

    def get_absolute_url(self):
        """Function return absolute url"""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """Function to print author"""
        return f'{self.name}, {self.surname}, {self.date_of_death}, {self.book_set}'


class BookOrder(models.Model):
    """BookOrder Model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, verbose_name='Book title')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, max_length=20, help_text='User')
    date_of_return = models.DateField(null=True, blank=True, verbose_name='Date Return')
    imprint = models.CharField(max_length=200)

    STATUS = (
        ('m', 'maintenance'),
        ('o', 'on loan'),
        ('a', 'available'),
        ('r', 'reserved')
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='m',
        help_text="Book Status"
    )

    class Meta:
        """Meta class ordering by date return book"""
        ordering = ['date_of_return']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """Function to display Book Order"""
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        if self.date_of_return and date.today() > self.date_of_return:
            return True
        return False

from django.contrib import admin

# Register your models here.
from catalog.models import Book, Author, Category, Language, BookOrder

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Language)
admin.site.register(BookOrder)

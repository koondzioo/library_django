
from django.contrib import admin
from .models import Author, Category, Book, BookOrder, Language

class BookInline(admin.TabularInline):
    model = Book
    extra = 0


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'date_of_death')
    fields = ['name', 'surname', 'date_of_death']
    inlines = [BookInline]


class BookOrderInLine(admin.TabularInline):
    model = BookOrder
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_category')
    inlines = [BookOrderInLine]


@admin.register(BookOrder)
class BookOrderAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'user', 'date_of_return', 'id')
    list_filter = ('status', 'date_of_return')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Available', {
            'fields': ('status', 'date_of_return', 'user')
        }),
    )



admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Language)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import generic

from catalog.models import Book, BookOrder, Author, Category


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookOrder.objects.all().count()
    num_categories = Category.objects.all().count()

    num_instances_available = BookOrder.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_categories': num_categories,
        'num_authors': num_authors
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    template_name = 'book_list.html'

    def get_queryset(self):
        """Function return last five Books"""
        return Book.objects.all()


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'author_list.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookOrder
    template_name = 'bookorder_list_borrowed_user.html'

    def get_queryset(self):
        return BookOrder.objects.filter(user=self.request.user).filter(status__exact='o').order_by('date_of_return')

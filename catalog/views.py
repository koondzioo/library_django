import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from catalog.forms import RenewalBookForm, ChangeBookOrderStatusForm
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


class AllLoanedBooksByUsersListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookOrder
    template_name = 'bookorder_list_borrowed.html'

    def get_queryset(self):
        return BookOrder.objects.all().filter(status__exact='o')


class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    template_name = 'author_create.html'
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}


class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    template_name = 'author_update.html'
    model = Author
    fields = ['name', 'surname', 'date_of_death']


class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    template_name = 'author_confirm_delete.html'
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    template_name = 'book_create.html'
    model = Book
    fields = '__all__'


class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    template_name = 'book_update.html'
    model = Book
    fields = '__all__'


class BookDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    template_name = 'book_confirm_delete.html'
    model = Book
    success_url = reverse_lazy('books')


class AllBooksEditListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    template_name = 'book_list_edit.html'


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_order = get_object_or_404(BookOrder, pk=pk)

    if request.method == 'POST':

        form = RenewalBookForm(request.POST)

        if form.is_valid():
            book_order.date_of_return = form.cleaned_data['renewal_date']
            book_order.save()

            return HttpResponseRedirect(reverse('all-borrowed-books'))


    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewalBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_order': book_order,
    }

    return render(request, 'book_renew_librarian.html', context)


class AllAuthorsEditListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    template_name = 'author_list_edit.html'


class BookOrderStatusUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    template_name = 'bookorder_form.html'
    model = BookOrder
    form_class = ChangeBookOrderStatusForm

    def get_success_url(self):
        book_pk = self.kwargs.get("book_pk")
        if book_pk:
            return reverse_lazy('book-detail', kwargs={'pk': book_pk})
        else:
            return reverse_lazy('borrowed-books-return')


class AllBooksToReturnListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookOrder
    template_name = 'bookorder_list_borrowed_return.html'

    def get_queryset(self):
        return BookOrder.objects.all().filter(status__exact='o')

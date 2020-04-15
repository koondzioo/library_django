from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('myBooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('all-borrowed-nooks/', views.AllLoanedBooksByUsersListView.as_view(), name='all-borrowed-books'),

    path('book-order/renew/<uuid:pk>', views.renew_book_librarian, name='renew-book-librarian'),
    path('book-order/return/<uuid:pk>', views.BookOrderStatusUpdate.as_view(), name='book-return'),
    path('book-order-returns/', views.AllBooksToReturnListView.as_view(), name='borrowed-books-return'),

    path('authors-edit/', views.AllAuthorsEditListView.as_view(), name='authors-edit'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('books-edit/', views.AllBooksEditListView.as_view(), name='books-edit'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]

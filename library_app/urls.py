from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Books
    path('books/', views.book_list, name='book-list'),
    path('books/add/', views.add_book, name='add-book'),
    path('books/edit/<int:pk>/', views.edit_book, name='edit-book'),
    path('books/delete/<int:pk>/', views.delete_book, name='delete-book'),

    # Borrow & Return
    path('books/borrow/<int:pk>/', views.borrow_book, name='borrow-book'),
    path('my-books/', views.my_books, name='my-books'),
    path('books/return/<int:pk>/', views.return_book, name='return-book'),
]

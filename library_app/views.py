from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import *
from .models import *

def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    else:
        form = RegisterForm()

    return render(
        request,
        'library/register.html',
        {'form': form}
    )
    
def login_view(request):

    if request.method == "POST":

        form = LoginForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect('home')

    else:
        form = LoginForm()

    return render(
        request,
        'library/login.html',
        {'form': form}
    )
    
def logout_view(request):

    logout(request)

    return redirect('login')

@login_required
def home_view(request):

    return render(
        request,
        'library/home.html'
    )
    
@login_required
def book_list(request):

    books = Book.objects.all()

    context = {
        'books': books
    }

    return render(
        request,
        'library/book_list.html',
        context
    )
    
@login_required
def add_book(request):

    if request.user.role != 'librarian':
        return redirect('book-list')

    if request.method == 'POST':

        form = BookForm(request.POST)

        if form.is_valid():

            book = form.save(commit=False)

            book.added_by = request.user

            book.save()

            return redirect('book-list')

    else:
        form = BookForm()

    return render(
        request,
        'library/add_book.html',
        {'form': form}
    )
  
@login_required
def edit_book(request, pk):

    if request.user.role != 'librarian':
        return redirect('book-list')

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':

        form = BookForm(
            request.POST,
            instance=book
        )

        if form.is_valid():
            form.save()

            return redirect('book-list')

    else:
        form = BookForm(instance=book)

    return render(
        request,
        'library/edit_book.html',
        {'form': form}
    )
    
@login_required
def delete_book(request, pk):

    if request.user.role != 'librarian':
        return redirect('book-list')

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':

        book.delete()

        return redirect('book-list')

    return render(
        request,
        'library/delete_book.html',
        {'book': book}
    )
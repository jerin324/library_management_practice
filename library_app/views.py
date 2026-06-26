from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Book, BorrowRecord, Student
from .forms import UserRegistrationForm, BookForm, StudentProfileForm

# Decorators
def librarian_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'librarian':
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied. Librarians only.")
        return redirect('dashboard')
    return wrapper

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'student':
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied. Students only.")
        return redirect('dashboard')
    return wrapper

# Auth
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'library/register.html', {'form': form})

# Dashboards
@login_required
def dashboard_view(request):
    books = Book.objects.all()
    if request.user.role == 'librarian':
        records = BorrowRecord.objects.all().order_by('-borrow_date')
        return render(request, 'library/librarian_dashboard.html', {'books': books, 'records': records})
    else:
        my_records = BorrowRecord.objects.filter(user=request.user).order_by('-borrow_date')
        return render(request, 'library/student_dashboard.html', {'books': books, 'my_records': my_records})

# Book CRUD
@login_required
@librarian_required
def add_book_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            book.save()
            messages.success(request, f"'{book.title}' added successfully!")
            return redirect('dashboard')
    else:
        form = BookForm()
    return render(request, 'library/add_book.html', {'form': form})

@login_required
@librarian_required
def edit_book_view(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "The requested book was not found.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{book.title}' updated successfully!")
            return redirect('dashboard')
    else:
        form = BookForm(instance=book)
    return render(request, 'library/edit_book.html', {'form': form, 'book': book})

@login_required
@librarian_required
def delete_book_view(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "The requested book was not found.")
        return redirect('dashboard')

    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f"'{title}' has been removed from the catalog.")
        return redirect('dashboard')
    return render(request, 'library/delete_book_confirm.html', {'book': book})

# Student Operations
@login_required
@student_required
def student_profile_view(request):
    try:
        student_profile = request.user.student_profile
    except Student.DoesNotExist:
        student_profile = Student.objects.create(user=request.user, student_id="PENDING")

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect('student_profile')
    else:
        form = StudentProfileForm(instance=student_profile)
    
    total_borrowed = BorrowRecord.objects.filter(user=request.user).count()
    currently_holding = BorrowRecord.objects.filter(user=request.user, is_returned=False).count()
    return render(request, 'library/student_profile.html', {
        'form': form, 'student': student_profile, 'total_borrowed': total_borrowed, 'currently_holding': currently_holding
    })

@login_required
@student_required
def borrow_book_view(request, book_id):
    if request.method == 'POST':
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            messages.error(request, "The selected book does not exist.")
            return redirect('dashboard')
        
        if BorrowRecord.objects.filter(user=request.user, book=book, is_returned=False).exists():
            messages.warning(request, "You currently have an unreturned copy of this book.")
            return redirect('dashboard')

        if book.total_copies > 0:
            BorrowRecord.objects.create(user=request.user, book=book)
            book.total_copies -= 1
            book.save()
            messages.success(request, f"You have successfully borrowed '{book.title}'.")
        else:
            messages.error(request, f"'{book.title}' is currently out of stock.")
    return redirect('dashboard')

@login_required
@student_required
def return_book_view(request, record_id):
    if request.method == 'POST':
        try:
            record = BorrowRecord.objects.get(id=record_id, user=request.user, is_returned=False)
        except BorrowRecord.DoesNotExist:
            messages.error(request, "Active loan history entry missing.")
            return redirect('dashboard')

        record.is_returned = True
        record.return_date = timezone.now().date()
        record.save()
        
        record.book.total_copies += 1
        record.book.save()
        messages.success(request, f"Thank you for returning '{record.book.title}'.")
    return redirect('dashboard')
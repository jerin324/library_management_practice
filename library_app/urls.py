from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='library/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # CRUD
    path('book/add/', views.add_book_view, name='add_book'),
    path('book/edit/<int:book_id>/', views.edit_book_view, name='edit_book'),
    path('book/delete/<int:book_id>/', views.delete_book_view, name='delete_book'),
    
    # Loans & Profiles
    path('book/borrow/<int:book_id>/', views.borrow_book_view, name='borrow_book'),
    path('book/return/<int:record_id>/', views.return_book_view, name='return_book'),
    path('profile/', views.student_profile_view, name='student_profile'),
]
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student, Book

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES, 
        required=True, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    student_id = forms.CharField(
        max_length=50, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter Student ID (If Student)'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        student_id = cleaned_data.get('student_id')

        if role == 'student' and not student_id:
            self.add_error('student_id', 'Student ID is required for student registration.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if user.role == 'student':
                Student.objects.create(user=user, student_id=self.cleaned_data.get('student_id'))
        return user


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id']
        widgets = {
            'student_id': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Update your Student ID'
            }),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'total_copies']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'total_copies': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
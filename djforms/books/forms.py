from django.forms import ModelForm
from .models import  Author, Book

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['user', 'name', 'title', 'birth_date']

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['user', 'name', 'author', 'due_date']
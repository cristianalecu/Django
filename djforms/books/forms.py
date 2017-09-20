from django.forms import ModelForm, Textarea, DateInput, BaseModelFormSet
from .models import  Author, Book

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'title', 'birth_date']

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'due_date']
        labels = {
            'name': 'Book title',
        }
        help_texts = {
            'name': 'Some useful help text.',
        }
        error_messages = {
            'name': {
                'max_length': "This book's title is too long.",
            },
        }
        widgets = {
            'due_date': DateInput(),
        }
        
class BaseBookFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Book.objects.filter(name__startswith='O')

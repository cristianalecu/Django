from django.shortcuts import render, get_object_or_404
from .models import Author, Book
from .forms import AuthorForm, BookForm
from django.shortcuts import redirect

from django.forms import modelformset_factory, inlineformset_factory

def books_list(request):
    objs = Book.objects.filter(user=request.user)
    return render(request, 'books/books_list.html', {'objs': objs})

def book_detail(request, pk):
    objs = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'objs': objs})

def book_new(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('book_detail', pk=obj.pk)
    else:
        form = BookForm(initial={'due_date': '2000-01-01'})
    
    form.fields['author'].queryset = Author.objects.filter(user=request.user)
    return render(request, 'books/book_edit.html', {'form': form})

def book_edit(request, pk):
    obj = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('book_detail', pk=obj.pk)
    else:
        form = BookForm(instance=obj)
        
    form.fields['author'].queryset = Author.objects.filter(user=request.user)
    return render(request, 'books/book_edit.html', {'form': form})

def book_delete(request, pk):
    obj = get_object_or_404(Book, pk=pk)
    obj.delete()
    return redirect('books_list')

def authors_list(request):
    objs = Author.objects.filter(user=request.user)
    return render(request, 'books/authors_list.html', {'objs': objs})

def author_detail(request, pk):
    obj = get_object_or_404(Author, pk=pk)
    instances = Book.objects.filter(user=obj.user, author=obj)
    return render(request, 'books/author_detail.html', {'objs': obj, 'instances': instances})

def author_new(request):
    BooksFormSet = modelformset_factory(Book, fields=('name', 'due_date'), max_num=10, extra=2)
    if request.method == "POST":
        form = AuthorForm(request.POST)
        formset = BooksFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid() :
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.author = obj
                instance.save()
            return redirect('author_detail', pk=obj.pk)
    else:
        form = AuthorForm()
        formset = BooksFormSet(queryset=Book.objects.none())
     
    return render(request, 'books/author_edit.html', {'form': form, 'formset': formset})
 
def author_edit(request, pk):
    obj = get_object_or_404(Author, pk=pk)
    BooksFormSet = modelformset_factory(Book, fields=('name', 'due_date'), max_num=10, extra=2)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=obj)
        formset = BooksFormSet(request.POST, request.FILES, queryset=Book.objects.filter(author=obj))
        if form.is_valid() and formset.is_valid() :
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.author = obj
                instance.save()
            return redirect('author_detail', pk=obj.pk)
    else:
        form = AuthorForm(instance=obj)
     
    formset = BooksFormSet(queryset=Book.objects.filter(author=obj))
    return render(request, 'books/author_edit.html', {'form': form, 'formset': formset})

def author_delete(request, pk):
    obj = get_object_or_404(Author, pk=pk)
    obj.delete()
    return redirect('authors_list')
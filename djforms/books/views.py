from django.shortcuts import render, get_object_or_404
from .models import Author, Book
from .forms import AuthorForm, BookForm
from django.shortcuts import redirect

def books_list(request):
    objs = Book.objects.all()
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
        form = BookForm()
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
    return render(request, 'books/book_edit.html', {'form': form})

def book_delete(request, pk):
    obj = get_object_or_404(Book, pk=pk)
    obj.delete()
    return redirect('books_list')

def authors_list(request):
    objs = Author.objects.all()
    return render(request, 'books/authors_list.html', {'objs': objs})

def author_detail(request, pk):
    objs = get_object_or_404(Author, pk=pk)
    return render(request, 'books/author_detail.html', {'objs': objs})

def author_new(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('author_detail', pk=obj.pk)
    else:
        form = AuthorForm()
    return render(request, 'books/author_edit.html', {'form': form})

def author_edit(request, pk):
    obj = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('author_detail', pk=obj.pk)
    else:
        form = AuthorForm(instance=obj)
    return render(request, 'books/author_edit.html', {'form': form})

def author_delete(request, pk):
    obj = get_object_or_404(Author, pk=pk)
    obj.delete()
    return redirect('authors_list')
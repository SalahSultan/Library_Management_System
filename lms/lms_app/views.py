from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Book, Category
from .forms import BookForm, CategoryForm, CustomUserCreationForm




# ---------------------- INDEX ----------------------
@login_required
def index(request):
    # Handle POST requests for adding books or categories
    if request.method == 'POST':
        add_book = BookForm(request.POST, request.FILES)
        if add_book.is_valid():
            add_book.save()
            messages.success(request, "Book added successfully.")

        add_category = CategoryForm(request.POST)
        if add_category.is_valid():
            add_category.save()
            messages.success(request, "Category added successfully.")

    # Prepare context for template
    context = {
        'category': Category.objects.all(),
        'books': Book.objects.all(),
        'form': BookForm(),
        'formcat': CategoryForm(),
        'allbooks': Book.objects.filter(active=True).count(),
        'booksold': Book.objects.filter(status='sold').count(),
        'bookrental': Book.objects.filter(status='rental').count(),
        'bookavailable': Book.objects.filter(status='available').count(),
    }
    return render(request, 'pages/index.html', context)


# ---------------------- BOOKS ----------------------
@login_required
def books(request):
    search = Book.objects.all()
    title = request.GET.get('search_name', None)
    if title:
        search = search.filter(title__icontains=title)

    context = {
        'category': Category.objects.all(),
        'books': search,
        'formcat': CategoryForm(),
    }
    return render(request, 'pages/books.html', context)


# ---------------------- UPDATE BOOK ----------------------
@login_required
def update(request, id):
    book_instance = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully.")
            return redirect('index')
    else:
        form = BookForm(instance=book_instance)

    return render(request, 'pages/update.html', {'form': form})


# ---------------------- DELETE BOOK ----------------------
@login_required
def delete(request, id):
    book_instance = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book_instance.delete()
        messages.success(request, "Book deleted successfully.")
        return redirect('index')
    return render(request, 'pages/delete.html', {'book': book_instance})


# ---------------------- SIGNUP ----------------------
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user
            messages.success(request, "Account created successfully! Please log in.")  # Store success message
            return redirect('login')  # Redirect to login page
    else:
        form = CustomUserCreationForm()

    # Render signup page with form (including errors if invalid)
    return render(request, 'pages/signup.html', {'form': form})

# ---------------------- LOGIN ----------------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})


# ---------------------- LOGOUT ----------------------
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')


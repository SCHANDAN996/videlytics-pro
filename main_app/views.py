from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages

# Home page view wahi hai
def home_view(request):
    return render(request, 'index.html')

# Naya Registration view
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('home')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            for error in form.non_field_errors():
                 messages.error(request, error)

    form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Naya Login view
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.info(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            
    form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Naya Logout view
def logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('home')



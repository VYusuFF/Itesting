from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect("dashboard")
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'Invalid username or password')
            return render(request, "auth/login.html")
        
    return render(request, "auth/login.html")



def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if len(username) == 0:
            messages.error(request, "Please correct the error in the name field.")
            return render(request, "auth/register.html")
        
        if len(email) == 0:
            messages.error(request, "Please correct the error in the email field.")
            return render(request, "auth/register.html")
        
        if len(password) == 0:
            messages.error(request, "Please correct the error in the password field.")
            return render(request, "auth/register.html")
        try:
            user = User.objects.get(username=username)
            messages.error(request, "Username already exists")
            return render(request, "auth/register.html")

        except User.DoesNotExist:
            # password = make_password(password)
            user = User.objects.create_user(first_name=name, email=email, password=password, username=username)
            return redirect('login')
    return render(request, "auth/register.html")


def reset(request):
    return render(request, 'auth/reset.html')





def main(request):
    return render(request, 'auth/main.html')

def faqs(request):
    return render(request, 'otherpages/faqs.html')

def terms(request):
    return render(request, 'otherpages/terms-policy.html')

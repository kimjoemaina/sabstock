from django.shortcuts import render, redirect
from application.forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings

def login_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    form = LoginForm()

    context = {}
    context["form"] = form

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
             messages.error(request, 'Invalid email or password.')
             return redirect('login')



    return render(request, "application/pages/login.html", context=context)



def logout_view(request):
    logout(request)
    return redirect("/")
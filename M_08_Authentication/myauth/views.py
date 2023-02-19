from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from .forms import AuthForm


class MyLoginView(LoginView):
    template_name = 'myauth/login.html'


class MyLogoutView(LogoutView):
    # template_name = 'users/logout.html'
    # next_page = '/'
    next_page = reverse_lazy("myauth:login")


def logout_view0(request):
    logout(request)
    return HttpResponse('Вы вышли из-под своей учетной записи')


def logout_view(request):
    logout(request)
    return redirect("myauth:login")

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/admin/')

        return render(request, 'myauth/login.html')

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/admin/')
        return render(request, 'myauth/login.html', {"error": "Invalid login credentials"})


def login_view_dbl(request):
    if request.method == 'POST':
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid:
            cleaned_data = auth_form.cleaned_data
            username = cleaned_data['username']
            password = cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Вы успешно вошли в систему')
                else:
                    auth_form.add_error('__all__', 'Ошибка. Учетная запись пользователя не активна')
            else:
                auth_form.add_error('__all__', 'Ошибка. Проверте правильность логина и пароля')
    else:
        auth_form = AuthForm()
    context = {
        'form': auth_form
    }
    return render(request, 'users/login.html', context = context)

def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f" Cookie value: {value!r}")

def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set")

def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f" Session value: {value!r}")
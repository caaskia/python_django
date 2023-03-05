from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from .models import Profile
from .forms import AuthForm

class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(self.request, user=user)
        return response


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

# @user_passes_test(lambda u:u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f" Cookie value: {value!r}")

@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set")

@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f" Session value: {value!r}")
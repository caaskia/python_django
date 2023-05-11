from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # , PermissionRequiredMixin


from .models import Profile

# class AboutMeView(TemplateView):
class AboutMeView(UpdateView):
    template_name = "myauth/about-me.html"

    model = Profile
    fields = "bio", "agreement_accepted", "avatar"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.profile.pk)

    def get_success_url(self):
        return reverse(
            "myauth:about-me",
        )

class UsersListView(ListView):
    template_name = "myauth/users-list.html"
    User = get_user_model()
    queryset = User.objects.all()
    context_object_name = "user_list"


class ProfileDetailsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    # template_name_suffix = "_update_form"
    template_name = "myauth/profile.html"

    model = Profile
    fields = "bio", "agreement_accepted", "avatar"
    context_object_name = "profile"

    def test_func(self):
        # if self.request.user.is_superuser:
        if self.request.user.is_staff:
            self.permit = True
        else:
            queryset = self.get_queryset()
            item = super().get_object(queryset)
            self.permit = True if self.request.user.id == item.user_id else False
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        profile = context.get("profile")
        context['usr'] = get_object_or_404(User, pk=profile.user_id)
        context['permit'] = self.permit
        return context

    def get_success_url(self):
        return reverse(
            "myauth:users-list",
        )


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # template_name_suffix = "_update_form"
    template_name = "myauth/profile_update_form.html"

    model = Profile
    fields = "bio", "agreement_accepted", "avatar"
    context_object_name = "profile"

    def test_func(self):
        # if self.request.user.is_superuser:
        if self.request.user.is_staff:
            permit = True
        else:
            queryset = self.get_queryset()
            item = super().get_object(queryset)
            permit = True if self.request.user.id == item.user_id else False
        return permit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        profile = context.get("profile")
        context['usr'] = get_object_or_404(User, pk=profile.user_id)
        return context

    def get_success_url(self):
        return reverse(
            "myauth:users-list",
        )


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
            password=password,
        )
        login(request=self.request, user=user)
        return response


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})

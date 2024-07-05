import secrets

# from django.contrib.auth import get_user_model
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserLoginForm, UserProfileForm, UserRecoveryForm
from users.models import User
from users.services import make_random_password


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет! Перейди по ссылке для подтверждения почты - {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


class UserLoginView(LoginView):
    model = User
    form_class = UserLoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('mailing:home')


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordResetView(PasswordResetView):
    form_class = UserRecoveryForm
    template_name = 'users/recovery_form.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if self.request.method == 'POST':
            user_email = self.request.POST.get('email')
            user = User.objects.filter(email=user_email).first()
            if user:
                new_password = make_random_password()
                user.set_password(new_password)
                user.save()
                try:
                    send_mail(
                        subject="Восстановление пароля",
                        message=f"Здравствуйте! Ваш пароль для доступа на наш сайт изменен:\n"
                                f"Данные для входа:\n"
                                f"Email: {user_email}\n"
                                f"Пароль: {new_password}",
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[user.email]
                    )
                except Exception:
                    print(f'Ошибка пр отправке письма, {user.email}')
                return HttpResponseRedirect(reverse('users:login'))


# class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
#     model = User
#     template_name = 'users/user_list.html'
#
#     def test_func(self):
#         return self.request.user.is_staff
#
#     def get_queryset(self):
#         queryset = User.objects.filter(is_staff=False)
#         return queryset


# class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     model = get_user_model()
#     # template_name = 'users/user_form.html'
#     # success_url = reverse_lazy('users:user_list')
#     permission_required = 'users.set_active'
#     fields = ['is_active', ]

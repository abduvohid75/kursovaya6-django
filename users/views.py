from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from users.models import User
from users.forms import UserRegisterForm, UserProfileForm


@login_required(login_url='users:login')
def send_verification_email(request):
    current_site = get_current_site(request)
    mail_subject = "Подтвердите свою почту"
    message = render_to_string('users/verification_email.html', {
        'user': request.user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
        'token': default_token_generator.make_token(request.user)
    })
    send_mail(mail_subject, message, 'sendinfoforauth@gmail.com', [request.user.email])

    return render(request, 'users/verification_sent.html')

@login_required(login_url='users:login')
def verify_email(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = get_user_model().objects.get(pk=uid)
    except:
        user = None

    else:
        if user is not None and default_token_generator.check_token(user, token):
            user.is_email_verified = True
            user.save()
            return render(request, 'users/success_verification.html')
        else:
            return render(request, 'users/error_verification.html')

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Зарегистрируйтесь для использования сервиса'

        return context_data

class ProfileView(LoginRequiredMixin,UpdateView):
    login_url = 'users:login'
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        email = self.request.user.email

        context_data['title'] = 'Здесь вы можете изменить свои данные'
        context_data['page_info'] = email

        return context_data

class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'users:login'
    model = User
    template_name = 'users/view_users.html'
    permission_required = 'user.view_user'

class UsersDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    login_url = 'users:login'
    model = User
    template_name = 'users/detail_user.html'
    permission_required = 'user.view_user'

@permission_required('user.change_user')
def block_user(request, pk):
    user = get_object_or_404(User, id=pk)
    user.is_blocked = True
    user.save()

    return render(request, 'users/user_blocked.html', context={'text': f'Пользователь {user.email} был успешно заблокирован'})

@permission_required('user.change_user')
def unblock_user(request, pk):
    user = get_object_or_404(User, id=pk)
    user.is_blocked = False
    user.save()

    return render(request, 'users/user_blocked.html', context={'text': f'Пользователь {user.email} был успешно разблокирован'})

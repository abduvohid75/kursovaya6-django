from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.db.models import Count
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from django.utils import timezone


from main.models import Client, Mails
from main.forms import UserForm, MailForm, MailUpdateForm

from blogs.models import Blog

class Blogs:
    pass


@cache_page(15)
def home(request):
    count = Mails.objects.count()
    count_active = Mails.objects.filter(status=False).count()
    
    blogs = Blog.objects.order_by('?')[:3]

    clients = []

    all_emails = Mails.objects.all()

    for email in all_emails:
        for client in email.users.all():
            if client.email not in clients:
                clients.append(client.email)
    if request.user.is_authenticated:
        page_info = f'Вы авторизованы как {request.user.email}'
    else:
        page_info = f'Вы еще не авторизованы'

    context = {
        'title': 'Главная',
        'page_info': f'Это сервис по управлению рассылками. {page_info}',
        'count' : count,
        'count_active' : count_active,
        'count_clients': len(clients),
        'object_list': blogs,
    }
    return render(request, 'main/index.html', context)


class UserCreateView(LoginRequiredMixin, CreateView):
    login_url = 'users:login'
    model = Client
    form_class = UserForm
    success_url = reverse_lazy('main:home')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Создать пользователя'
        context_data['page_info'] = ''
        return context_data

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        self.object = form.save()
        self.object.author = self.request.user
        user = form.save(commit=False)
        user.save()
        return super().form_valid(form)

class UserListView(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    model = Client
    template_name = 'main/users_view.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Список всех клиентов, зарегистрированных в системе'

        return context_data

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not Group.objects.get(name='Менеджеры') in self.request.user.groups.all():
            queryset = queryset.filter(author=self.request.user)
        queryset = queryset.annotate(mails_count=Count('mails'))

        return queryset

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = 'users:login'
    model = Client
    success_url = reverse_lazy('main:home')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Подтвердите удаление клиента'
        context_data['page_info'] = 'После удаления клиента все рассылки, которые ссылаются на email клиента будут отменены'

        return context_data
    def test_func(self):
        mail = self.get_object()

        return mail.author == self.request.user or Group.objects.get(name='Менеджеры') in self.request.user.groups.all()

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = 'users:login'
    model = Client
    form_class = UserForm
    success_url = reverse_lazy('main:users')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Внесите желаемые изменения'
        context_data['page_info'] = ''

        return context_data
    def test_func(self):
        client = self.get_object()

        return client.author == self.request.user or Group.objects.get(name='Менеджеры') in self.request.user.groups.all()

class MailCreateView(LoginRequiredMixin, CreateView):
    login_url = 'users:login'
    model = Mails
    form_class = MailForm
    success_url = reverse_lazy('main:home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Создать рассылку'
        context_data['page_info'] = 'Время необходимо вводить в формате GMT+0'
        context_data['info'] = 'При неуказывании запланированной даты, рассылка начнется мгновенно'
        return context_data

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        self.object = form.save()
        self.object.author = self.request.user
        users = form.cleaned_data["users"]
        self.object.users.set(users)

        return super().form_valid(form)

class MailListView(ListView):
    model = Mails
    template_name = 'main/mails_view.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Все рассылки, включая созданные'
        context_data['is_success'] = False

        return context_data or Group.objects.get(name='Менеджеры') in self.request.user.groups.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if not Group.objects.get(name='Менеджеры') in self.request.user.groups.all():
            queryset = queryset.filter(author=self.request.user)

        return queryset


class SuccessMailListView(ListView):
    model = Mails
    template_name = 'main/mails_view.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not Group.objects.get(name='Менеджеры') in self.request.user.groups.all():
            queryset = queryset.filter(author=self.request.user, status=True)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Список всех проведенных рассылок'
        context_data['is_success'] = True

        return context_data


class MailDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = 'users:login'
    model = Mails
    success_url = reverse_lazy('main:mails')

    def test_func(self):
        mail = self.get_object()

        return mail.author == self.request.user or Group.objects.get(name='Менеджеры') in self.request.user.groups.all()
    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Подтвердите отмену рассылки'
        context_data['page_info'] = 'После подтверждения все запланированные рассылки будут отменены'

        return context_data

class MailDetailView(LoginRequiredMixin, DetailView):
    login_url = 'users:login'
    model = Mails

    def test_func(self):
        mail = self.get_object()

        return mail.author == self.request.user or Group.objects.get(name='Менеджеры') in self.request.user.groups.all()
    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = f'Информация о рассылке'

        if self.object.scheduled and self.object.scheduled <= timezone.now():
            context_data['zapusheno'] = 'Запущена'
        else:
            context_data['zapusheno'] = ''

        return context_data

class MailUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'users:login'
    model = Mails
    form_class = MailUpdateForm
    success_url = reverse_lazy('main:mails')

    def test_func(self):
        mail = self.get_object()

        return mail.author == self.request.user

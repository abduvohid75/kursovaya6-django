
from django.db.models import Count
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from django.utils import timezone


from main.models import User, Mails
from main.forms import UserForm, MailForm
# Create your views here.
def home(request):
    context = {
        'title': 'Главная',
        'page_info': 'Это сервис по управлению рассылками. Вы авторизованы как username',
    }
    return render(request, 'main/index.html', context)


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('main:home')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Создать пользователя'
        context_data['page_info'] = ''
        return context_data

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        return super().form_valid(form)

class UserListView(ListView):
    model = User
    template_name = 'main/users_view.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Список всех клиентов, зарегистрированных в системе'

        return context_data

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.annotate(mails_count=Count('mails'))

        return queryset

class UserDeleteView(DeleteView):
    model = User

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Подтвердите удаление клиента'
        context_data['page_info'] = 'После удаления клиента все рассылки, которые ссылаются на email клиента будут отменены'

        return context_data

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('main:users')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Внесите желаемые изменения'
        context_data['page_info'] = ''

        return context_data

class MailCreateView(CreateView):
    model = Mails
    form_class = MailForm
    success_url = reverse_lazy('main:home')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Создать рассылку'
        context_data['page_info'] = 'Время необходимо вводить в формате GMT+0'
        context_data['info'] = 'При неуказывании запланированной даты, рассылка начнется мгновенно'
        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        users = form.cleaned_data["users"]

        self.object.users.set(users)

        return response

class MailListView(ListView):
    model = Mails
    template_name = 'main/mails_view.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Все рассылки, включая созданные'
        context_data['is_success'] = False

        return context_data

class SuccessMailListView(ListView):
    model = Mails
    template_name = 'main/mails_view.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(status=True)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Список всех проведенных рассылок'
        context_data['is_success'] = True

        return context_data


class MailDeleteView(DeleteView):
    model = Mails
    success_url = reverse_lazy('main:mails')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Подтвердите отмену рассылки'
        context_data['page_info'] = 'После подтверждения все запланированные рассылки будут отменены'

        return context_data

class MailDetailView(DetailView):
    model = Mails

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = f'Информация о рассылке'

        if self.object.scheduled and self.object.scheduled <= timezone.now():
            context_data['zapusheno'] = 'Запущена'
        else:
            context_data['zapusheno'] = ''

        return context_data
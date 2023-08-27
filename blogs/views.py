from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from blogs.forms import BlogCreateForm
from blogs.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogCreateForm
    success_url = reverse_lazy('blogs:blogs')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.date = timezone.now()
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['title'] = 'Создайте свой блог'

        return context_data

class BlogListView(ListView):
    model = Blog
    template_name = 'blogs/blogs.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['is_manager'] = False
        if Group.objects.get(name='Менеджеры') in self.request.user.groups.all():
            context_data['is_manager'] = True
        context_data['title'] = 'Блоги'

        return context_data

class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['title'] = 'Блог'

        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogCreateForm
    success_url = reverse_lazy(f'blogs:blogs')

    def test_func(self):
        mail = self.get_object()

        return mail.author == self.request.user or Group.objects.get(name='Менеджеры') in self.request.user.groups.all()

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['title'] = 'Измените блог по своему усмотрению'

        return context_data

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blogs:blogs')

    def test_func(self):
        mail = self.get_object()
        return mail.author == self.request.user or Group.objects.get(name='Менеджеры') in self.request.user.groups.all()


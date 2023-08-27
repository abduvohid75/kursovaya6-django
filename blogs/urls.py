from django.urls import path
from django.views.decorators.cache import cache_page

from blogs.apps import BlogsConfig
from blogs.views import BlogCreateView, BlogListView, BlogDeleteView, BlogDetailView, BlogUpdateView

app_name = BlogsConfig.name

urlpatterns = [
    path('blogs', cache_page(15)(BlogListView.as_view()), name='blogs'),
    path('create_blogs', BlogCreateView.as_view(), name='blogs_create'),
    path('update_blog/<int:pk>', BlogUpdateView.as_view(), name='update_blog'),
    path('detail_blog/<int:pk>', BlogDetailView.as_view(), name='detail_blog'),
    path('delete_blog/<int:pk>', BlogDeleteView.as_view(), name='delete_blog'),
]
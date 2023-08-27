from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy

from users.views import RegisterView, ProfileView, send_verification_email, verify_email, UsersListView, \
    UsersDetailView, block_user, unblock_user
from users.apps import UsersConfig


app_name = UsersConfig.name

urlpatterns = [
    path('login', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', LogoutView.as_view(next_page=reverse_lazy('main:home')), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('verify', send_verification_email, name='verify'),
    path('verification/verify/<str:uid64>/<str:token>', verify_email, name='verify_email'),
    path('view_users', UsersListView.as_view(), name='view_users'),
    path('detail_users/<int:pk>', UsersDetailView.as_view(), name='detail_users'),
    path('block_users/<int:pk>', block_user, name='block_users'),
    path('unblock_users/<int:pk>', unblock_user, name='unblock_users'),
]
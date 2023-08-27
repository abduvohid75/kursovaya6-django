from django.urls import path

from main.apps import MainConfig
from main.views import home, UserCreateView, MailCreateView, MailListView, MailDeleteView, MailDetailView, UserListView, \
    UserUpdateView, UserDeleteView, SuccessMailListView, MailUpdateView

app_name = MainConfig.name

urlpatterns = [
    path('', home, name="home"),
    path('create_user', UserCreateView.as_view(), name="create_user"),
    path('create_mail', MailCreateView.as_view(), name="create_mail"),
    path('mails', MailListView.as_view(), name="mails"),
    path('success_mails', SuccessMailListView.as_view(), name="success_mails"),
    path('users', UserListView.as_view(), name="users"),
    path('delete_mail/<int:pk>', MailDeleteView.as_view(), name="delete_mails"),
    path('detail_mail/<int:pk>', MailDetailView.as_view(), name="detail_mails"),
    path('delete_user/<int:pk>', UserDeleteView.as_view(), name="delete_users"),
    path('edit_user/<int:pk>', UserUpdateView.as_view(), name="edit_users"),
    path('edit_mail/<int:pk>', MailUpdateView.as_view(), name="edit_mails"),
]
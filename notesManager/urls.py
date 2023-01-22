from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', auth_views.LoginView.as_view(), name="login"),
    path('logout', auth_views.LogoutView.as_view(), name="logout"),
    path("register", views.register_request, name="register"),
    path("create_note", views.create_note, name="create_note"),
    path("create_reminder", views.create_reminder, name="create_reminder"),
    path("reminders", views.view_reminders, name="reminders"),
    path('note/<int:primary_key>', views.note_details, name='note-detail'),
    path('update_note/<int:primary_key>', views.modify_note, name='modify-note'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('reset_password', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='reset_password'),
    path('password_reset_done',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/set_password.html'
    ), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_complete.html'
    ), name='password_reset_complete'),
]

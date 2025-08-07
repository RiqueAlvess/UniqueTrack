from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from . import views

urlpatterns = [
    # páginas principais
    path('', views.home,                    name='home'),
    path('dashboard/',  views.dashboard,    name='dashboard'),

    # relatórios
    path('relatorios/',           views.relatorio_list,      name='relatorio_list'),
    path('relatorios/novo/',      views.relatorio_create,    name='relatorio_create'),
    path('relatorios/<int:pk>/enviar/', views.relatorio_send_email, name='relatorio_send_email'),

    # e-mails
    path('emails/',               views.emails,        name='emails'),
    path('emails/delete/<int:pk>/', views.email_delete, name='email_delete'),

    # perfil / smtp
    path('perfil/',               views.perfil,        name='perfil'),
    path('perfil/testar-smtp/',   views.testar_smtp,   name='testar_smtp'),

    # autenticação
    path('login/',  auth_views.LoginView.as_view(
            template_name='login.html',
            authentication_form=LoginForm),             name='login'),
    path('logout/', auth_views.LogoutView.as_view(),    name='logout'),
    path('relatorios/<int:pk>/copiar/', views.relatorio_copy, name='relatorio_copy'),
]


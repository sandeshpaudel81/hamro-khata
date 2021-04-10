from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    
    #AUTHENTICATION
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),
    path('change-password', auth_views.PasswordChangeView.as_view(
        template_name='change-password.html',
        success_url='login'
    ), name='change-password'),

    path('update_profile/', views.ProfileUpdateView.as_view(), name='update_profile'),
    path('add_party/', views.PartyCreateView.as_view(), name='add_party'),
    path('add_transaction/', views.TransactionCreateView.as_view(), name='add_transaction'),
    path('party_statement/<int:id>', views.party_statement, name='party-statement'),
]
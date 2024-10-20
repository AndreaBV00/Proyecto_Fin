
from django.urls import path
from django.contrib.auth import views as auth_views
from App_Artista import views
urlpatterns = [
    path('', views.Inicio, name='Inicio'),
    path('Detalle_Artistas/', views.Detalle_Artista, name='Detalle_Artistas'),
    path('Detalle_Obras/', views.lista_obras, name='Detalle_Obras'),
    path('Exposiciones/', views.detalle_exposicion, name='Exposiciones'),
    path('Artista_Invitado/', views.Artista_Invitado, name='Artista_invitado'),
    path('Registro/', views.register, name='Registro'),
    path('Login/', views.CustomLoginView.as_view(), name='Login'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='Inicio'), name='logout'),
    path('votos/', views.mostrar_votos, name='mostrar_votos'),
]



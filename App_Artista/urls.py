
from django.urls import path
from App_Artista import views
urlpatterns = [
    path('', views.Inicio, name='Inicio'),
    path('Detalle_Artistas/', views.Detalle_Artista, name='Detalle_Artistas'),
    path('Detalle_Obras/', views.lista_obras, name='Detalle_Obras'),
    path('Exposiciones/', views.detalle_exposicion, name='Exposiciones'),
    path('Artista_Invitado/', views.Artista_Invitado, name='Artista_invitado'),
    path('Gracias/', views.pagina_gracias, name='Gracias'),
    path('Login/', views.Login, name='Login'),
]

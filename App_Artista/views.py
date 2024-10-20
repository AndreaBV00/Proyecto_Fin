from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Artista_invitado, Artista, Obra, Exposicion, VotoArtista
from .forms import Artista_invitadoForm, CustomUserCreationForm, ExposicionSeleccionForm, CustomLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def Artista_Invitado(request):
    if request.method == 'POST':
        mi_form = Artista_invitadoForm(request.POST)
        
        if mi_form.is_valid():
            data = mi_form.cleaned_data
            nuevo_artista = Artista_invitado(
                nombre = data['nombre'],
                nacionalidad = data['nacionalidad'],
                fecha_nacimiento = data['fecha_nacimiento'],
                texto_motivacional = data['texto_motivacional'],
                link_obras = data['link_obras'],
                exposicion_anfitriona = data['exposicion_anfitriona'],
                Email_contacto = data['Email_contacto'],
            )
            nuevo_artista.save()
            
            return redirect('Gracias')
        else:
            mi_form = Artista_invitadoForm()
    else:
        mi_form = Artista_invitadoForm()
    return render(request, 'Artista_Invitado.html', {'mi_form': mi_form})


def Inicio(request):
    return render(request, 'Inicio.html', {})
                  
"""def Detalle_Artista(request, id):
    artista = Artista.objects.get(id=id)
    return render(request, 'Detalle_artistas.html', {})"""

# Vista para mostrar todas las obras y los detalles de una obra seleccionada
def lista_obras(request):
    obras = Obra.objects.all()
    obra_detalle = None

    # Si se ha seleccionado una obra (por ejemplo, mediante el ID en GET)
    if 'obra_id' in request.GET:
        obra_id = request.GET.get('obra_id')
        obra_detalle = get_object_or_404(Obra, id=obra_id)

    context = {
        'obras': obras,
        'obra_detalle': obra_detalle
    }
    return render(request, 'Detalle_Obras.html', context)

def Detalle_Artista(request):
    artistas = Artista.objects.all()
    artista_detalle = None
    
    if 'artista_id' in request.GET:
        artista_id = request.GET.get('artista_id')
        artista_detalle = get_object_or_404(Artista, id=artista_id)
    
    context = {
        'artistas': artistas,
        'artista_detalle': artista_detalle
    }
    return render(request, 'Detalle_artistas.html', context)


def pagina_gracias(request):
    return render(request, 'Gracias.html')

def detalle_exposicion(request):
    exposicion_detalle = None
    if request.method == 'POST':
        form = ExposicionSeleccionForm(request.POST)
        if form.is_valid():
            exposicion = form.cleaned_data['exposicion']
            # Obtenemos los detalles de la exposición seleccionada
            exposicion_detalle = Exposicion.objects.get(id=exposicion.id)
    else:
        form = ExposicionSeleccionForm()
    
    return render(request, 'Exposiciones.html', {'form': form, 'exposicion_detalle': exposicion_detalle})


def register(request):
    if request.method == 'POST':
        log_form = CustomUserCreationForm(request.POST)
        if log_form.is_valid():
            log_form.save()
            return redirect('Login')  # Redirige a la página de inicio de sesión o a donde quieras
    else:
        log_form = CustomUserCreationForm()

    return render(request, 'Registro.html', {'form': log_form})


class CustomLoginView(LoginView):
    template_name = 'Login.html'  # Nombre de la plantilla de inicio de sesión
    form_class = CustomLoginForm


@login_required

def profile_view(request):
    artistas = Artista_invitado.objects.all()
   
    if request.user.is_staff:
        return redirect('mostrar_votos')  # Redirige a la página de votos

    if request.method == 'POST':
        # Obtén el ID del artista favorito del formulario
        artista_id = request.POST.get('artista_favorito')
        
        if artista_id:  # Verifica que se haya recibido un ID
            artista_favorito = Artista_invitado.objects.get(id=artista_id)

            # Guarda el voto en la tabla VotoArtista
            voto, created = VotoArtista.objects.get_or_create(artista=artista_favorito)
            voto.cantidad_votos += 1  # Incrementar el contador de votos
            voto.save()

            # Muestra un mensaje de confirmación
            messages.success(request, 'Tu voto ha sido guardado exitosamente.')
            return redirect('profile')  # Redirige para evitar reenvíos de formulario
        else:
            messages.error(request, 'No se ha seleccionado ningún artista.')

    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'artistas': artistas,
    })
# Decorador para verificar si el usuario es un administrador
def is_admin(user):
    return user.is_staff  # Verifica si el usuario es un miembro del personal

@user_passes_test(is_admin)
def mostrar_votos(request):
    votos = VotoArtista.objects.all()  # Obtén todos los votos
    return render(request, 'votos_artistas.html', {'votos': votos})

@user_passes_test(is_admin)
def eliminar_artista(request, artista_id):
    if request.method == 'POST':  # Verifica si se ha enviado un formulario POST
        artista = get_object_or_404(Artista_invitado, id=artista_id)
        artista.delete()
        return redirect('artista_eliminado')  # Cambia esto a la vista que deseas redirigir después de eliminar
    
def artista_eliminado(request):
    return render(request, 'Artista_Eliminado.html')
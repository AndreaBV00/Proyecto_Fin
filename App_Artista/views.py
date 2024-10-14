from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Artista_invitado, Artista, Obra, Exposicion
from .forms import Artista_invitadoForm, CustomUserCreationForm, ExposicionSeleccionForm, CustomLoginForm
from django.contrib.auth.forms import AuthenticationForm

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
                  
def Detalle_Artista(request, id):
    artista = Artista.objects.get(id=id)
    return render(request, 'Detalle_artistas.html', {})

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
            return redirect('Artista_invitado')  # Redirige a la página de inicio de sesión o a donde quieras
    else:
        log_form = CustomUserCreationForm()

    return render(request, 'Inicio.html', {'log_form': log_form})


class CustomLoginView(LoginView):
    template_name = 'Login.html'  # Nombre de la plantilla de inicio de sesión
    form_class = CustomLoginForm


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')  # Asegúrate de que esta plantilla exista
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Artista_invitado, Artista, Obra, Exposicion


class Artista_invitadoForm(forms.Form):
    nombre = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nombre completo'
        })
    )
    
    nacionalidad = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nacionalidad'
        })
    )
    
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control', 
            'placeholder': 'YYYY-MM-DD', 
            'type': 'date'
        })
    )
    
    texto_motivacional = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Escribe tu mensaje aquí...', 
            'style': 'height: 10rem'
        })
    )
    
    link_obras = forms.URLField(
        widget=forms.URLInput(attrs={
            'class': 'form-control', 
            'placeholder': 'https://www.example.com'
        })
    )
    
    exposicion_anfitriona = forms.ModelChoiceField(
        queryset=Exposicion.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    Email_contacto = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'name@example.com'
        })
    )

class ExposicionSeleccionForm(forms.Form):
    exposicion = forms.ModelChoiceField(
        queryset=Exposicion.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label=''  # Esto ocultará la etiqueta del campo en el formulario
    )



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = True  # El usuario puede iniciar sesión
        if commit:
            user.save()
        return user
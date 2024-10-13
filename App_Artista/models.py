from django.db import models

# Create your models here.
class Artista(models.Model):
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    fecha_defuncion = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to='artistas', null=True, blank=True)
    biografia = models.TextField()
    def __str__(self):
        return self.nombre
    
class Obra(models.Model):   
    nombre = models.CharField(max_length=100)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    tecnica = models.CharField(max_length=100)
    dimensiones = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='obras', null=True, blank=True)
    def __str__(self):
        return self.nombre

class Exposicion(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    obras = models.ManyToManyField(Obra)
    def __str__(self):
        return self.nombre
    
class Artista_invitado(models.Model):
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    texto_motivacional = models.TextField()
    link_obras = models.URLField()
    exposicion_anfitriona = models.ForeignKey(Exposicion, on_delete=models.CASCADE)
    Email_contacto = models.EmailField(default='default@example.com')
  
    def __str__(self):
        return self.nombre

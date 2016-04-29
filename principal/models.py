from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Palabra_Clave(models.Model):
	nombre = models.TextField(max_length=20, unique=True)
	
	def __unicode__(self):
		return self.nombre

class VideoH(models.Model):
	titulo = models.CharField(max_length=100, unique=True)
	descripcion = models.TextField(max_length=400)
	archivo = models.FileField(upload_to='media/videos', blank=True)
	careta = models.ImageField(upload_to='media/imagenes', blank=True)
	fecha = models.DateField()
	usuario = models.ForeignKey(User, null=True, blank=True)
	etiquetas = models.ManyToManyField(Palabra_Clave, blank=False)
	

	def __unicode__(self):
		return self.titulo

class Comentario(models.Model):
	tiempo_registro = models.DateField(auto_now=True)
	autor = models.ForeignKey(User, null=True, blank=True)
	videoH = models.ForeignKey(VideoH)
	texto = models.TextField(blank=False)
	
	def __unicode__(self):
		return ("%s %s" % (self.videoH, self.texto[:60]))
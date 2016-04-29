from django.forms import ModelForm
from django import forms
from principal.models import VideoH, Palabra_Clave, Comentario

class VideoForm(ModelForm):
		class Meta:
			model = VideoH
			exclude = ['usuario']

class Palabra_ClaveForm(ModelForm):
	class Meta:
		model = Palabra_Clave

class ComentarioForm(ModelForm):
	class Meta:
		model = Comentario
		exclude = ['videoH']
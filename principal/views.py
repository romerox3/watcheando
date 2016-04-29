# Create your views here.

from principal.models import Palabra_Clave, VideoH, Comentario
# Formularios
from django.views.generic import TemplateView
from principal.forms import VideoForm, Palabra_ClaveForm, ComentarioForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.context_processors import csrf
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.utils.encoding import force_text
def index(request):
	return render_to_response('base.html',context_instance=RequestContext(request))

def inicio(request):
	usuario = request.user
	videos = VideoH.objects.all()
	cont = 2;
	return render_to_response('inicio.html',{'cont':cont, 'datos':videos, 'usuario': usuario}, context_instance=RequestContext(request))



	# ======= Parte de video ==========

@login_required(login_url='/acceder')
def videoVer(request, pk):
	idvideo = VideoH.objects.get(pk=int(pk))
	etiquetacion = idvideo.etiquetas.all()
	comentar = Comentario.objects.filter(videoH = idvideo)
	videosRel = VideoH.objects.filter(etiquetas = etiquetacion)
	d = dict(vvideo = idvideo, comentar = comentar, form=ComentarioForm(), usuario=request.user)
	d.update(csrf(request))

	return render_to_response('videos.html', d, context_instance=RequestContext(request))

@login_required(login_url='/acceder')
def nuevo_video(request, id_usuario):
	usuario = request.user
	if request.method=='POST':
		formulario = VideoForm(request.POST, request.FILES)
		if formulario.is_valid():
			VideoH=formulario.save(commit=False)
			VideoH.usuario=request.user
			VideoH.save()
			return HttpResponseRedirect('/')
	else:
		formulario = VideoForm()
		return render_to_response('videoform.html',{'formulario':formulario, 'usuario':usuario}, context_instance=RequestContext(request))


def poncomentario(request, pk):
	p = request.POST
	autor = request.user

	comentario = Comentario(videoH = VideoH.objects.get(pk=pk))
	cf = ComentarioForm(p, instance=comentario)

	cf.fields['autor'].required=False

	comentario = cf.save(commit=False)
	comentario.autor = autor
	comentario.save()

	return HttpResponseRedirect (reverse("principal.views.videoVer", kwargs={'pk': pk}))

	# ======= Gestion de Usuarios =======

def acceder(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/privado')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/privado')
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('acceder.html',{'formulario':formulario}, context_instance=RequestContext(request))

def nuevo_usuario(request):
    if request.method=='POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario = UserCreationForm()
    return render_to_response('nuevousuario.html',{'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/acceder')
def perfil(request, id_usuario):
	usuario = request.user
	videos = VideoH.objects.filter(usuario_id=int(id_usuario))
	return render_to_response('perfil.html',{'usuario':usuario, 'videos':videos}, context_instance=RequestContext(request))

@login_required(login_url='/acceder')
def privado(request):
	usuario = request.user
	return render_to_response('privado.html',{'usuario':usuario}, context_instance=RequestContext(request))

@login_required(login_url='/')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/')

# --------------- PalabraClave --------

@login_required(login_url='/acceder')
def nueva_Palabra_Clave(request,id_usuario):
	usuario = request.user
	referer = force_text(request.META.get('HTTP_REFERER', ''), errors='replace')
	etiquetas = Palabra_Clave.objects.all()
	if request.method=='POST':
		formulario = Palabra_ClaveForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect(referer)
	else:
		formulario = Palabra_ClaveForm()
	return render_to_response('Palabra_Claveform.html',{'formulario':formulario, 'etiquetas':etiquetas, 'usuario':usuario}, context_instance=RequestContext(request))

#--------------- Parte Buscar -------

class BuscarView(TemplateView):

	def post(self, request, *args, **kwargs):
		buscar = request.POST['buscalo'] # Lo que ha enviado el formulario es lo que guardo
		if buscar:
			palabrasClave = Palabra_Clave.objects.filter(nombre__contains=buscar) # busco "Palabras clave" donde aparezca la palabra que busco
			
			videos = VideoH.objects.all()
			datos = []
			for video in videos:
				etiquetas = video.etiquetas.all()
				datos.append(dict([(video,etiquetas)]))
			return render(request, "buscar.html", {'palabrasClave':palabrasClave, 'datos':datos}, context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect("/")

#------------ Edicion de objetos ------

@login_required(login_url='/acceder')
def editar_video(request, id_video):
	video = VideoH.objects.get(id=id_video)
	if request.method=='POST':
		formulario = VideoForm(request.POST, request.FILES, instance=video)
		if formulario.is_valid():
			#lineas para que no aparezca en authentication
			formulario.save()
			return HttpResponseRedirect('/')
	else:
		formulario = VideoForm(instance=video)
	return render_to_response('videoform.html',{'formulario':formulario}, context_instance=RequestContext(request))

def eliminar_video(request, id_video):
	referer = force_text(request.META.get('HTTP_REFERER', ''), errors='replace')
	video = VideoH.objects.get(id=id_video)
	video.delete()
	return HttpResponseRedirect(referer)

def eliminar_comentario(request, id_comentario):
	usuario = request.user
	referer = force_text(request.META.get('HTTP_REFERER', ''), errors='replace')
	
	comentario=Comentario.objects.get(id=id_comentario)
	comentario.delete()
	return HttpResponseRedirect (referer)
	
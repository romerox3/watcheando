from django.conf.urls import patterns, include, url
from django.contrib import admin 
from principal import views
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from principal.views import BuscarView


admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$','principal.views.inicio'),
	url(r'^(?P<pk>\d+)','principal.views.videoVer'),
	url(r'^nuevoV/(?P<id_usuario>\d+)/subir/$','principal.views.nuevo_video'),
	url(r'^nuevoV/(?P<id_usuario>\d+)/subir/nuevaPalabra/$','principal.views.nueva_Palabra_Clave'),
	url(r'^acceder/$','principal.views.acceder'),
	url(r'^privado/$','principal.views.privado'),
	url(r'^cerrar/$','principal.views.cerrar'),
	url(r'^usuario/nuevo/$','principal.views.nuevo_usuario'),
	url(r'^perfil/(?P<id_usuario>\d+)','principal.views.perfil'),
    url(r'^poncomentario/(\d+)/$', 'principal.views.poncomentario'),
    url(r'^editar/(?P<id_video>\d+)/$', 'principal.views.editar_video'),
    url(r'^eliminar/(?P<id_video>\d+)/$', 'principal.views.eliminar_video'),
    url(r'^eliminar_comentario/(?P<id_comentario>\d+)/$','principal.views.eliminar_comentario'),   
    # Examples:
    # url(r'^$', 'wacheando.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    url(r'^buscar/$', BuscarView.as_view(), name='buscar'),

)



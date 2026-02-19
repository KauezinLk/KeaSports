from django.contrib import admin
from django.urls import path, include
# Importa as configurações de mídia para servir arquivos durante o desenvolvimento
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api_s.urls')),
]

# Responsavel por exibir arquivos de mídia (imagns). Somente em modo DEBUG (desenvolvimento)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

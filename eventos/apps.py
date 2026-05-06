from django.apps import AppConfig


class EventosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eventos'
    label = 'api_s'

    def ready(self):
        import eventos.signals  # importa o arquivo signals.py quando o app é carregado

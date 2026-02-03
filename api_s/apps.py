from django.apps import AppConfig


class ApiSConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_s'

    def ready(self):
        import api_s.signals  # importa o arquivo signals.py quando o app é carregado
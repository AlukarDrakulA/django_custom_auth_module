from django.apps import AppConfig


class SingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sing'

    def ready(self):
        import sing.signals
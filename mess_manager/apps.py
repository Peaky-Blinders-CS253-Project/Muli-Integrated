from django.apps import AppConfig


class MessManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mess_manager'

    def ready(self):
        import mess_manager.signals  # Import signals module
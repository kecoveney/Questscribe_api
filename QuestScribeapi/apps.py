from django.apps import AppConfig

class QuestScribeapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'QuestScribeapi'

    def ready(self):
        import QuestScribeapi.signals  # Import your signals here

from django.apps import AppConfig


class AthsysAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'athsys_app'

    def ready(self):
        import athsys_app.signals








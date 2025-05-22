from django.apps import AppConfig



class RideAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'   #this is the app name, change when we find a proper name 

    def ready(self):
        import app.signal
        # Import the signals module to ensure the signal handlers are registered
        # when the app is ready.

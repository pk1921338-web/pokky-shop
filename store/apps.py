from django.apps import AppConfig

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    # 👇 This function is vital for Signals (Profile creation) to work
    def ready(self):
        import store.models
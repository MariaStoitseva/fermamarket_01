from django.apps import AppConfig


class CustomusersConfig(AppConfig):
    name = 'fermamarket.customusers'

    def ready(self):
        import fermamarket.customusers.signals

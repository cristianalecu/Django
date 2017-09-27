from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "financ"

    def ready(self):
        import_module("financ.receivers")

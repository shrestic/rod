from django.apps import AppConfig


class EtlConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rod.etl"

    def ready(self) -> None:
        import rod.etl.signals.handlers  # noqa: F401

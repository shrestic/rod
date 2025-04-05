from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rod.accounts"

    def ready(self):
        import rod.accounts.signals.handlers  # noqa: F401

"""Django AppConfig for Roya."""
import logging
from django.apps import AppConfig

logger = logging.getLogger("roya.apps")


class RoyaConfig(AppConfig):
    name = "roya"
    verbose_name = "Roya Material Design Components"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        logger.info("Roya library ready")
        from roya.core.registry import registry
        from roya.components import register_all
        register_all(registry)
        logger.info("Registered %d components", registry.count())
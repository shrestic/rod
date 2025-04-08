import logging
import uuid

from celery import shared_task

from rod.etl.connectors.connection_status_enum import ConnectionStatus
from rod.etl.connectors.loaders import get_connector_class
from rod.etl.models.connector_model import ConnectorInstance

logger = logging.getLogger(__name__)


def _get_runtime_connector(connector_instance: ConnectorInstance):
    connector_class = get_connector_class(connector_instance.connector.code)
    config = connector_instance.decrypted_config
    return connector_class(config)


@shared_task
def run_connector_instance_check(connector_instance_id: uuid.UUID):
    logger.info("[CELERY] Checking connector instance ID: %s", connector_instance_id)
    try:
        connector_instance = ConnectorInstance.objects.get(id=connector_instance_id)
        logger.info(
            "[CELERY] Loaded connector instance: %s",
            connector_instance,
        )

        connector = _get_runtime_connector(connector_instance)
        logger.info("[CELERY] Initialized connector: %s", connector.__class__.__name__)

        status = connector.check(config=connector_instance.decrypted_config)
        logger.info("[CELERY] Check result: %s", status)

        if status == ConnectionStatus.VALID:
            connector_instance.status = ConnectorInstance.StatusChoices.VALID
        else:
            connector_instance.status = ConnectorInstance.StatusChoices.INVALID

        connector_instance.save(update_fields=["status"])
        logger.info("[CELERY] Updated status to: %s", connector_instance.status)

    except ConnectorInstance.DoesNotExist:
        logger.warning(
            "[CELERY] ConnectorInstance with ID %s does not exist.",
            connector_instance_id,
        )
    except Exception:
        logger.exception(
            "[CELERY] Error checking connector instance %s",
            connector_instance_id,
        )
        try:
            connector_instance.status = ConnectorInstance.StatusChoices.INVALID
            connector_instance.save(update_fields=["status"])
            logger.warning(
                "[CELERY] Fallback: Set status=INVALID for instance %s",
                connector_instance_id,
            )
        except Exception:
            logger.exception(
                "[CELERY] FATAL: Fallback save failed for instance %s",
                connector_instance_id,
            )


@shared_task
def run_connector_instance_discover_schema(connector_instance_id: uuid.UUID):
    logger.info(
        "[CELERY] Discovering schema for connector instance ID: %s",
        connector_instance_id,
    )
    try:
        connector_instance = ConnectorInstance.objects.get(id=connector_instance_id)
        logger.info("[CELERY] Loaded connector instance: %s", connector_instance)

        connector = _get_runtime_connector(connector_instance)
        logger.info("[CELERY] Initialized connector: %s", connector.__class__.__name__)

        schema = connector.discover_schema(config=connector_instance.decrypted_config)
        logger.info("[CELERY] Schema discovered: %s", schema)

        connector_instance.schema_snapshot = schema
        connector_instance.schema_status = ConnectorInstance.SchemaStatusChoices.READY
        connector_instance.save(update_fields=["schema_snapshot", "schema_status"])
        logger.info(
            "[CELERY] Schema snapshot saved for instance %s",
            connector_instance_id,
        )

    except ConnectorInstance.DoesNotExist:
        logger.warning(
            "[CELERY] ConnectorInstance with ID %s does not exist.",
            connector_instance_id,
        )
    except Exception:
        logger.exception(
            "[CELERY] Error discovering schema for instance %s",
            connector_instance_id,
        )
        try:
            connector_instance.status = ConnectorInstance.StatusChoices.INVALID
            connector_instance.schema_status = (
                ConnectorInstance.SchemaStatusChoices.FAILED
            )
            connector_instance.save(update_fields=["schema_status", "status"])
            logger.warning(
                "[CELERY] Fallback: Set status=INVALID for instance %s",
                connector_instance_id,
            )
        except Exception:
            logger.exception(
                "[CELERY] FATAL: Fallback save failed for instance %s",
                connector_instance_id,
            )

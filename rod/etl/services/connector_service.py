import json

from rod.billing.models.subscription_model import Subscription
from rod.common.services import model_update
from rod.etl.models.connector_model import Connector
from rod.etl.models.connector_model import ConnectorInstance
from rod.etl.tasks.connector_tasks import run_connector_instance_check
from rod.etl.tasks.connector_tasks import run_connector_instance_discover_schema
from rod.etl.utils.utils import KMSUtil


class ConnectorService:
    def __init__(self):
        pass

    def connector_create(
        self,
        *,
        label: str,
        code: str,
        config_form: dict,
        input_type: str,
    ) -> Connector:
        return Connector.objects.create(
            label=label,
            code=code,
            config_form=config_form,
            input_type=input_type,
        )

    def connector_update(
        self,
        *,
        connector: Connector,
        data: dict,
    ) -> Connector:
        fields: list[str] = [
            "label",
            "code",
            "config_form",
            "input_type",
        ]
        connector, has_updated = model_update(
            instance=connector,
            fields=fields,
            data=data,
        )
        return connector

    def connector_delete(self, *, connector: Connector) -> None:
        connector.delete()


class ConnectorInstanceService:
    def __init__(self):
        pass

    def connector_instance_create(
        self,
        *,
        subscription: Subscription,
        connector: Connector,
        config: dict,
    ) -> ConnectorInstance:
        plaintext = json.dumps(config)
        customer_key_id = subscription.customer_key_id
        encrypted_config = KMSUtil().encrypt(customer_key_id, plaintext)

        return ConnectorInstance.objects.create(
            subscription=subscription,
            connector=connector,
            schema_snapshot={},
            encrypted_config=encrypted_config,
            status=ConnectorInstance.StatusChoices.NONE,
        )

    def connector_instance_update_config(
        self,
        *,
        connector_instance: ConnectorInstance,
        new_config: dict,
    ) -> ConnectorInstance:
        plaintext = json.dumps(new_config)
        customer_key_id = connector_instance.customer_key_id
        encrypted_config = KMSUtil().encrypt(customer_key_id, plaintext)
        connector_instance.encrypted_config = encrypted_config
        connector_instance.save(update_fields=["encrypted_config"])

        return connector_instance

    def connector_instance_delete(
        self,
        *,
        connector_instance: ConnectorInstance,
    ) -> None:
        connector_instance.delete()

    def connector_instance_check(
        self,
        connector_instance: ConnectorInstance,
    ) -> None:
        run_connector_instance_check.delay(connector_instance.id)

    def connector_instance_discover_schema(
        self,
        connector_instance: ConnectorInstance,
    ) -> None:
        connector_instance.schema_status = (
            ConnectorInstance.SchemaStatusChoices.DISCOVERING
        )
        connector_instance.save(update_fields=["schema_status"])

        run_connector_instance_discover_schema.delay(connector_instance.id)

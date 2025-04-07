import json

from rod.billing.models.subscription_model import Subscription
from rod.common.services import model_update
from rod.etl.models.connector_model import Connector
from rod.etl.models.connector_model import ConnectorInstance
from rod.etl.utils.kms_helper import KMSHelper


class ConnectorService:
    def __init__(self):
        pass

    def connector_create(
        self,
        *,
        name: str,
        description: str,
        type: str,  # noqa: A002
    ) -> Connector:
        return Connector.objects.create(
            name=name,
            description=description,
            type=type,
        )

    def connector_update(
        self,
        *,
        connector: Connector,
        data: dict,
    ) -> Connector:
        fields: list[str] = [
            "name",
            "description",
            "type",
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
        status: str,
        config: dict,
    ) -> ConnectorInstance:
        connector_instance = ConnectorInstance(
            subscription=subscription,
            connector=connector,
            status=status,
        )
        plaintext = json.dumps(config)
        connector_instance.encrypted_config = KMSHelper().encrypt(plaintext)
        connector_instance.save()

        return connector_instance

    def connector_instance_update(
        self,
        connector_instance: ConnectorInstance,
        status: str,
        config: dict,
    ) -> ConnectorInstance:
        plaintext = json.dumps(config)
        connector_instance.encrypted_config = KMSHelper().encrypt(plaintext)
        connector_instance.save()
        return connector_instance

    def connector_instance_delete(
        self,
        *,
        config: dict,
        connector_instance: ConnectorInstance,
    ) -> None:
        connector_instance.delete()

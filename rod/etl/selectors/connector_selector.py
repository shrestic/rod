import uuid

from rod.billing.models.subscription_model import Subscription
from rod.etl.models.connector_model import Connector
from rod.etl.models.connector_model import ConnectorInstance


class ConnectorSelector:
    def __init__(self):
        pass

    def connector_list(self) -> list:
        return Connector.objects.all().order_by("label")

    def connector_get(self, *, code: str) -> Connector:
        return Connector.objects.get(code=code)

    def connector_get_by_code(self, *, code: str) -> Connector:
        return Connector.objects.get(code=code)


class ConnectorInstanceSelector:
    def __init__(self):
        pass

    def connector_instance_list(self, *, subscription) -> list:
        return (
            ConnectorInstance.objects.select_related("connector")
            .all()
            .filter(subscription=subscription)
            .order_by("connector__label")
        )

    def connector_instance_get(
        self,
        connector_instance_id: uuid.UUID,
        subscription: Subscription,
    ) -> ConnectorInstance:
        return ConnectorInstance.objects.filter(
            id=connector_instance_id,
            subscription=subscription,
        ).first()

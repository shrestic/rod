import uuid

from rod.etl.models.connector_model import Connector
from rod.etl.models.connector_model import ConnectorInstance


class ConnectorSelector:
    def __init__(self):
        pass

    def connector_list(self) -> list:
        return Connector.objects.all().order_by("name")

    def connector_get(self, *, connector_id: int) -> Connector:
        return Connector.objects.get(id=connector_id)


class ConnectorInstanceSelector:
    def __init__(self):
        pass

    def connector_instance_list(self) -> list:
        return (
            ConnectorInstance.objects.select_related("connector")
            .all()
            .order_by("connector__name")
        )

    def connector_instance_get(
        self,
        *,
        connector_instance_id: uuid.UUID,
    ) -> ConnectorInstance:
        return ConnectorInstance.objects.select_related("connector").get(
            id=connector_instance_id,
        )

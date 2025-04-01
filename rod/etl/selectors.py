import uuid

from django.db.models.query import QuerySet

from rod.common.utils import get_object
from rod.etl.filters import CustomerFilter
from rod.etl.models import Customer


class CustomerSelector:
    def __init__(self) -> None:
        pass

    def customer_get(self, *, user_id: uuid.UUID) -> Customer:
        return get_object(Customer, user_id=user_id)

    def customer_list(self, filters=None) -> QuerySet[Customer]:
        filters = filters or {}

        qs = Customer.objects.select_related("user").all()

        return CustomerFilter(filters, qs).qs

import uuid

from rod.common.utils import get_object
from rod.etl.models import Customer


class CustomerSelector:
    def __init__(self) -> None:
        pass

    def customer_get(self, *, user_id: uuid.UUID) -> Customer:
        return get_object(Customer, user_id=user_id)

    def customer_list(self) -> list[Customer]:
        return Customer.objects.all()

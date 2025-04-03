from rod.common.services import model_update
from rod.etl.models.customer import Customer
from rod.users.models import BaseUser


class CustomerService:
    def __init__(self) -> None:
        pass

    def customer_create(self, *, user: BaseUser) -> Customer:
        customer = Customer(user=user)
        customer.full_clean()
        customer.save()
        return customer

    def customer_update(self, *, customer: Customer, data) -> Customer:
        fields: list[str] = [
            "phone",
            "address",
            "birth_date",
            "image",
        ]
        customer, has_updated = model_update(
            instance=customer,
            fields=fields,
            data=data,
        )
        return customer

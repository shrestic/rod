import uuid

from rod.accounts.models.employee_model import Employee
from rod.common.utils import get_object


class EmployeeSelector:
    def __init__(self) -> None:
        pass

    def employee_get(self, *, user_id: uuid.UUID) -> Employee | None:
        queryset = Employee.objects.select_related("user")
        return get_object(queryset, user_id=user_id)

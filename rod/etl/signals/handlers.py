from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rod.etl.services import CustomerService
from rod.etl.services import EmployeeService


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        user = kwargs["instance"]
        if user.is_staff and not user.is_superuser:
            EmployeeService().employee_create(user=user)
        elif not user.is_staff:
            CustomerService().customer_create(user=user)

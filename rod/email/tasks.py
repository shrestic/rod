from celery import shared_task
from celery.utils.log import get_task_logger

from rod.core.exceptions import ApplicationError
from rod.email.models import Email

logger = get_task_logger(__name__)


def _email_send_failure(self, exc, task_id, args, kwargs, einfo):  # noqa: PLR0913
    email_id = args[0]
    email = Email.objects.get(id=email_id)

    from rod.email.services import email_failed

    email_failed(email)


@shared_task(bind=True, on_failure=_email_send_failure)
def email_send(self, email_id):
    email = Email.objects.get(id=email_id)

    from rod.email.services import email_send

    try:
        email_send(email)
    except ApplicationError as exc:
        # https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying
        logger.warning("Exception occurred while sending email: %s", exc)
        self.retry(exc=exc, countdown=5)

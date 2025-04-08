import uuid

from django.core.files.storage import default_storage
from django.utils.text import slugify
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rod.accounts.selectors.customer_selector import CustomerSelector
from rod.billing.selectors.subscription_selector import SubscriptionSelector
from rod.core.exceptions import ApplicationError
from rod.core.permissions import IsCustomer


class FileUploadApi(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsCustomer]
    EXTENSIONS_BY_CODE = {
        "csv": ["csv"],
        "json": ["json"],
        "xlsx": ["xlsx"],
        "sqlite": ["sqlite", "db"],
    }

    def post(self, request, code):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            raise ApplicationError(message="Customer not found")

        subscription = SubscriptionSelector().subscription_get_by_customer(
            customer_id=customer.id,
            is_active=True,
        )
        if not subscription:
            raise ApplicationError(message="Subscription not found")
        allowed_exts = self.EXTENSIONS_BY_CODE.get(code)
        if not allowed_exts:
            raise ApplicationError(
                message=(
                    "Invalid file type. Only CSV, JSON, XLSX and SQLite are allowed."
                ),
            )

        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            raise ApplicationError(message="File not found")

        ext = uploaded_file.name.split(".")[-1].lower()
        if ext not in allowed_exts:
            raise ApplicationError(
                message=(
                    f"Invalid file extension '.{ext}'. "
                    f"Allowed: {', '.join(allowed_exts)}"
                ),
            )

        filename = f"{slugify(uploaded_file.name)}-{uuid.uuid4()}.{ext}"
        path = default_storage.save(f"data-upload/{filename}", uploaded_file)

        return Response({"path": default_storage.url(path)})

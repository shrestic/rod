from django.contrib import admin

from .models import customer
from .models import employee


# Register your models here.
@admin.register(customer.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "phone", "address", "birth_date"]
    list_per_page = 10
    list_select_related = ["user"]
    ordering = ["user__first_name", "user__last_name"]
    search_fields = ["user__first_name__istartswith", "user__last_name__istartswith"]


@admin.register(employee.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "phone",
        "address",
        "birth_date",
        "position",
        "department",
        "start_date",
    ]
    list_per_page = 10
    list_select_related = ["user"]
    ordering = ["user__first_name", "user__last_name"]
    search_fields = [
        "user__first_name__istartswith",
        "user__last_name__istartswith",
        "position",
        "department",
    ]

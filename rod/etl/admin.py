from django.contrib import admin

from .models import customer
from .models import employee
from .models import plan


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


@admin.register(plan.Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "max_rows_processed",
        "cost_per_million_rows",
        "base_cost",
    ]
    list_per_page = 10
    ordering = ["name"]


@admin.register(plan.PlanFeature)
class PlanFeatureAdmin(admin.ModelAdmin):
    list_display = ["plan", "feature_name", "feature_description"]
    list_per_page = 10
    ordering = ["plan__name", "feature_name"]

from django.contrib import admin

from rod.plan.models.plan_model import Plan
from rod.plan.models.plan_model import PlanFeature


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "cost",
    ]
    list_per_page = 10
    ordering = ["name"]


@admin.register(PlanFeature)
class PlanFeatureAdmin(admin.ModelAdmin):
    list_display = [
        "plan",
        "name",
        "description",
    ]
    list_per_page = 10
    ordering = ["plan__name", "name"]
    list_select_related = ["plan"]

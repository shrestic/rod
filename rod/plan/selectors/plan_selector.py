from rod.common.utils import get_object
from rod.plan.models.plan_model import Plan
from rod.plan.models.plan_model import PlanFeature


class PlanSelector:
    def __init__(self) -> None:
        pass

    def plan_list(self) -> list[Plan]:
        return Plan.objects.prefetch_related("features").all().order_by("code")

    def plan_get(self, *, code: str) -> Plan:
        qs = Plan.objects.prefetch_related("features")
        return get_object(qs, pk=code)

    def plan_features_list(self, *, plan_code: str) -> list[PlanFeature]:
        return PlanFeature.objects.filter(plan__code=plan_code).order_by("plan__code")

    def plan_feature_get(self, *, id: int) -> PlanFeature:  # noqa: A002
        return get_object(PlanFeature, id=id)

    def plan_feature_get_by_code(self, *, code: str) -> PlanFeature:
        return get_object(PlanFeature, code=code)

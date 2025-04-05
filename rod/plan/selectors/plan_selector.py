from rod.common.utils import get_object
from rod.plan.models.plan_model import Plan
from rod.plan.models.plan_model import PlanFeature


class PlanSelector:
    def __init__(self) -> None:
        pass

    def plan_list(self) -> list[Plan]:
        return Plan.objects.prefetch_related("features").all().order_by("id")

    def plan_get(self, *, plan_id: str) -> Plan:
        qs = Plan.objects.prefetch_related("features")
        return get_object(qs, pk=plan_id)

    def plan_features_list(self, *, plan_id: str) -> list[PlanFeature]:
        return PlanFeature.objects.filter(plan_id=plan_id).order_by("id")

    def plan_feature_get(self, *, feature_id: str) -> PlanFeature:
        return get_object(PlanFeature, id=feature_id)

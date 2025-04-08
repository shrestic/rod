from rod.common.services import model_update
from rod.plan.models.plan_model import Plan
from rod.plan.models.plan_model import PlanFeature


class PlanService:
    def __init__(self) -> None:
        pass

    def plan_create(
        self,
        *,
        name: str,
        code: str,
        description: str,
        cost: float,
    ) -> Plan:
        return Plan.objects.create(
            name=name,
            code=code,
            description=description,
            cost=cost,
        )

    def plan_update(self, *, plan: Plan, data: dict) -> Plan:
        fields: list[str] = [
            "name",
            "code",
            "description",
            "cost",
        ]
        plan, has_updated = model_update(
            instance=plan,
            fields=fields,
            data=data,
        )
        return plan

    def plan_delete(self, *, plan: Plan) -> None:
        plan.delete()


class PlanFeatureService:
    def __init__(self) -> None:
        pass

    def plan_feature_create(
        self,
        *,
        plan: Plan,
        code: str,
        name: str,
        description: str,
    ) -> PlanFeature:
        return PlanFeature.objects.create(
            plan=plan,
            code=code,
            name=name,
            description=description,
        )

    def plan_feature_bulk_create(
        self,
        *,
        plan: Plan,
        features_data: list[dict],
    ) -> list[PlanFeature]:
        features = [
            PlanFeature(
                plan=plan,
                code=item["code"],
                name=item["name"],
                description=item["description"],
            )
            for item in features_data
        ]
        return PlanFeature.objects.bulk_create(features)

    def plan_feature_update(
        self,
        *,
        plan_feature: PlanFeature,
        data: dict,
    ) -> PlanFeature:
        fields: list[str] = [
            "code",
            "name",
            "description",
        ]
        plan_feature, has_updated = model_update(
            instance=plan_feature,
            fields=fields,
            data=data,
        )
        return plan_feature

    def plan_feature_delete(self, *, plan_feature: PlanFeature) -> None:
        plan_feature.delete()

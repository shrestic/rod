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
        description: str,
        max_rows_processed: int,
        cost_per_million_rows: float,
        base_cost: float,
    ) -> Plan:
        return Plan.objects.create(
            name=name,
            description=description,
            max_rows_processed=max_rows_processed,
            cost_per_million_rows=cost_per_million_rows,
            base_cost=base_cost,
        )

    def plan_update(self, *, plan: Plan, data: dict) -> Plan:
        fields: list[str] = [
            "name",
            "description",
            "max_rows_processed",
            "cost_per_million_rows",
            "base_cost",
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
        feature_name: str,
        feature_description: str,
    ) -> PlanFeature:
        return PlanFeature.objects.create(
            plan=plan,
            feature_name=feature_name,
            feature_description=feature_description,
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
                feature_name=item["feature_name"],
                feature_description=item["feature_description"],
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
            "feature_name",
            "feature_description",
        ]
        plan_feature, has_updated = model_update(
            instance=plan_feature,
            fields=fields,
            data=data,
        )
        return plan_feature

    def plan_feature_delete(self, *, plan_feature: PlanFeature) -> None:
        plan_feature.delete()

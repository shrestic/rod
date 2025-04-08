from django.utils import timezone

from rod.common.services import model_update
from rod.etl.models.connector_model import ConnectorInstance
from rod.etl.models.pipeline_model import Pipeline
from rod.etl.selectors.pipeline_selector import PipelineSelector


class PipelineService:
    def __init__(self) -> None:
        self.selector = PipelineSelector()

    def pipeline_create(
        self,
        *,
        subscription,
        source_instance: ConnectorInstance,
        destination_instance: ConnectorInstance,
        sync_frequency: str,
        notes: str = "",
    ) -> Pipeline:
        return Pipeline.objects.create(
            subscription=subscription,
            source_connector=source_instance,
            destination_connector=destination_instance,
            sync_frequency=sync_frequency,
            status=Pipeline.StatusChoices.ACTIVE,
            deployed_at=timezone.now(),
            notes=notes,
        )

    def pipeline_update(
        self,
        *,
        pipeline: Pipeline,
        data: dict,
    ) -> Pipeline:
        fields = ["sync_frequency", "status", "notes"]
        pipeline, has_updated = model_update(
            instance=pipeline,
            fields=fields,
            data=data,
        )
        return pipeline

    def pipeline_delete(self, *, pipeline: Pipeline) -> None:
        pipeline.status = Pipeline.StatusChoices.DELETED
        pipeline.save()

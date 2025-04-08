from django.urls import include
from django.urls import path

from rod.etl.apis.connector_api import ConnectorCreateApi
from rod.etl.apis.connector_api import ConnectorDeleteApi
from rod.etl.apis.connector_api import ConnectorDetailApi
from rod.etl.apis.connector_api import ConnectorListApi
from rod.etl.apis.connector_api import ConnectorUpdateApi
from rod.etl.apis.connector_instance_api import ConnectorInstanceCheckApi
from rod.etl.apis.connector_instance_api import ConnectorInstanceCreateApi
from rod.etl.apis.connector_instance_api import ConnectorInstanceDetailApi
from rod.etl.apis.connector_instance_api import ConnectorInstanceDiscoverSchemaApi
from rod.etl.apis.connector_instance_api import ConnectorInstanceListApi
from rod.etl.apis.connector_instance_api import ConnectorInstanceUpdateConfigApi
from rod.etl.apis.file_upload_api import FileUploadApi

connector_patterns = [
    path("", ConnectorListApi.as_view(), name="list"),
    path("create/", ConnectorCreateApi.as_view(), name="create"),
    path("<str:code>/", ConnectorDetailApi.as_view(), name="detail"),
    path("<str:code>/update/", ConnectorUpdateApi.as_view(), name="update"),
    path("<str:code>/delete/", ConnectorDeleteApi.as_view(), name="delete"),
    path("<str:code>/upload/", FileUploadApi.as_view(), name="upload"),
]

connector_instance_patterns = [
    path("", ConnectorInstanceListApi.as_view(), name="list"),
    path("create/", ConnectorInstanceCreateApi.as_view(), name="create"),
    path("<uuid:pk>/", ConnectorInstanceDetailApi.as_view(), name="detail"),
    path(
        "<uuid:pk>/update-config/",
        ConnectorInstanceUpdateConfigApi.as_view(),
        name="update-config",
    ),
    path("<uuid:pk>/check", ConnectorInstanceCheckApi.as_view(), name="check"),
    path(
        "<uuid:pk>/discover-schema",
        ConnectorInstanceDiscoverSchemaApi.as_view(),
        name="discover-schema",
    ),
]

urlpatterns = [
    path("connectors/", include((connector_patterns, "connectors"))),
    path(
        "connector-instances/",
        include((connector_instance_patterns, "connector-instances")),
    ),
]

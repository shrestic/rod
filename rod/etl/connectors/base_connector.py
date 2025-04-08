from abc import ABC
from abc import abstractmethod
from typing import Any


class BaseConnector(ABC):
    def __init__(self, config: dict[str, Any]):
        self.config = config

    @abstractmethod
    def check(self, config: dict[str, Any]) -> str:
        pass

    @abstractmethod
    def discover_schema(self, config: dict[str, Any]) -> dict[str, Any]:
        pass

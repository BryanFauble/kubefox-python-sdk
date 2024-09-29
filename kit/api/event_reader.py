from dataclasses import dataclass
from typing import Any, Optional

from kit.api.kit_types import EventType
from kit.proto.protobuf_msgs_pb2 import Event


@dataclass
class EventReader:
    # params: dict[str, str] = None
    # param_vs: dict[str, Any] = None
    # url: str = None
    # path_suffix: str = None
    # queries: dict[str, str] = None
    # query_vs: dict[str, Any] = None
    # headers: dict[str, str] = None
    # header_vs: dict[str, Any] = None
    # status: int = None
    # status_v: Optional[Any] = None
    event: Event = None

    @property
    def event_type(self) -> EventType:
        return EventType(self.event.type)

    def param(self, key: str) -> str:
        raise NotImplementedError

    def param_v(self, key: str) -> Any:
        raise NotImplementedError

    def param_def(self, key: str, default: str) -> str:
        raise NotImplementedError

    def url(self) -> str:
        raise NotImplementedError

    def path_suffix(self) -> str:
        raise NotImplementedError

    def query(self, key: str) -> str:
        raise NotImplementedError

    def query_v(self, key: str) -> Any:
        raise NotImplementedError

    def query_def(self, key: str, default: str) -> str:
        raise NotImplementedError

    def query_all(self, key: str) -> list[str]:
        raise NotImplementedError

    def header(self, key: str) -> str:
        raise NotImplementedError

    def header_v(self, key: str) -> Any:
        raise NotImplementedError

    def header_def(self, key: str, default: str) -> str:
        raise NotImplementedError

    def header_all(self, key: str) -> list[str]:
        raise NotImplementedError

    def status(self) -> int:
        raise NotImplementedError

    def status_v(self) -> Optional[Any]:
        raise NotImplementedError

    def bind(self, v: Any) -> None:
        raise NotImplementedError

    def str(self) -> str:
        raise NotImplementedError

    def bytes(self) -> bytes:
        raise NotImplementedError

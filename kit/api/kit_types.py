from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List

from dataclasses_json import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Object:
    def get_namespace(self) -> str:
        pass

    def get_name(self) -> str:
        pass

    def get_resource_version(self) -> str:
        pass

    def get_generation(self) -> int:
        pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class EnvVarDefinition:
    type: str
    required: bool


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class EnvSchema:
    vars: Dict[str, EnvVarDefinition]
    secrets: Dict[str, EnvVarDefinition]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ComponentDefinition:
    type: str
    routes: List["RouteSpec"]
    default_handler: bool
    env_var_schema: Dict[str, EnvVarDefinition]
    dependencies: Dict[str, "Dependency"]
    hash: str
    image: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RouteSpec:
    id: int
    rule: str
    env_var_schema: Dict[str, EnvVarDefinition]
    priority: int = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Dependency:
    type: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Details:
    title: str
    description: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ProblemSource:
    kind: str
    name: str
    observed_generation: int
    path: str
    value: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Problem:
    type: str
    message: str
    causes: List[ProblemSource]


class EventType(str, Enum):
    Cron = "io.kubefox.cron"
    Dapr = "io.kubefox.dapr"
    HTTP = "io.kubefox.http"
    KubeFox = "io.kubefox.kubefox"
    Kubernetes = "io.kubefox.kubernetes"
    Ack = "io.kubefox.ack"
    Bootstrap = "io.kubefox.bootstrap"
    Error = "io.kubefox.error"
    Health = "io.kubefox.health"
    Metrics = "io.kubefox.metrics"
    Nack = "io.kubefox.nack"
    Register = "io.kubefox.register"
    Rejected = "io.kubefox.rejected"
    Telemetry = "io.kubefox.telemetry"
    Unknown = "io.kubefox.unknown"

    def __str__(self) -> str:
        return self.value


class ComponentType(Enum):
    Broker = "Broker"
    HTTPAdapter = "HTTPAdapter"
    KubeFox = "KubeFox"
    NATS = "NATS"


class EnvVarType(Enum):
    Array = "Array"
    Boolean = "Boolean"
    Number = "Number"
    String = "String"


@dataclass
class EnvVarDep:
    name: str
    type: EnvVarType


@dataclass
class ComponentDep:
    name: str
    app: str
    type: ComponentType
    event_type: EventType


# @dataclass
# class RouteSpec:
#     pass


@dataclass
class Route:
    route_spec: RouteSpec
    # Swap this out for a better type
    handler: Any


# @dataclass
# class Dependency:
#     type: ComponentType
#     app: str
#     name: str

#     def name(self) -> str:
#         return self.name

#     def app(self) -> str:
#         return self.app

#     def type(self) -> ComponentType:
#         return self.type

#     def event_type(self) -> EventType:
#         if self.type == ComponentType.HTTPAdapter:
#             return EventType.HTTP
#         else:
#             return EventType.KubeFox

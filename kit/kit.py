import logging
from dataclasses import dataclass
import os
from typing import Any, Callable, Generator, List, Optional, Self, Union
from enum import Enum
from urllib.parse import urlparse
from enum import Enum

from grpc import StatusCode, insecure_channel, secure_channel, ssl_channel_credentials
from kit.api.types import ComponentDefinition, Dependency, EnvVarDefinition, EnvVarSchema, RouteSpec
from dataclasses_json import dataclass_json, LetterCase
from kit.api.vars import DEFAULT_MAX_EVENT_SIZE_BYTES
from proto.broker_svc_pb2_grpc import BrokerStub
from proto.protobuf_msgs_pb2 import Event, MatchedEvent, EventContext

logger = logging.getLogger(__name__)

# TODO: https://www.python-httpx.org/advanced/transports/#custom-transports
# Implement a custom transport for HTTPX to handle putting data into and pulling data out of an event


class EventType(Enum):
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


class Val:
    pass


class URL:
    pass


class Logger:
    pass


class FS:
    pass


class Client:
    pass


class RoundTripper:
    pass


class Context:
    pass


class Template:
    pass


class HTMLTemplate:
    pass


# EventHandler = Callable[['Kontext'], None]


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
    # handler: EventHandler


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

def make_event() -> Generator[Event, None, None]:
    my_context = EventContext(platform="debug", virtual_environment="virtual_environment",
                              app_deployment="hello-world", release_manifest="release_manifest")
    yield Event(context=my_context, id="1234")


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Kit:
    routes: List[Route]
    comp_def: Any
    max_event_size: int
    num_workers: int
    export: bool
    log: Logger
    brk: Any

    def start(self):
        # Alternative to a context managed instance is to use `.close()`
        # open ca.crt and read into string:
        with open("/tmp/kubefox/ca.crt", "r") as file:
            root_ca = file.read()
        creds = ssl_channel_credentials(root_certificates=root_ca.encode(),
                                        private_key=None, certificate_chain=None)

        # TODO: Implement this config:
        # grpcCfg := `{
        # "methodConfig": [{
        #   "name": [{"service": "", "method": ""}],
        #   "waitForReady": false,
        #   "retryPolicy": {
        # 	  "MaxAttempts": 3,
        # 	  "InitialBackoff": "3s",
        # 	  "MaxBackoff": "6s",
        # 	  "BackoffMultiplier": 2.0,
        # 	  "RetryableStatusCodes": [ "UNAVAILABLE" ]
        #   }
        # }]}`
        with secure_channel("127.0.0.1:6060", credentials=creds) as channel:
            # TODO: See if I can just hit the broker directly:
            # This is the golang code to create a new client:
            # broker := grpc.NewClient(grpc.ClientOpts{
            #     Platform:      adapter.Platform,
            #     Component:     comp,
            #     Pod:           pod,
            #     BrokerAddr:    adapter.BrokerAddr,
            #     HealthSrvAddr: adapter.HealthSrvAddr,
            #     TokenPath:     tokenPath,
            # })
            print("-------------- BrokerStub --------------")
            stub = BrokerStub(channel)
            result = stub.Subscribe(make_event())
            if not result.is_active():
                logger.error(result.exception())
                raise RuntimeError(result.details)
            logger.debug(result.details())

    # def route(self, rule: str, handler: EventHandler):
    #     pass

    # def static(self, path_prefix: str, fs_prefix: str, fs: FS):
    #     pass

    # def default(self, handler: EventHandler):
    #     pass

    # def env_var(self, name: str, opts: List[Any]) -> EnvVarDep:
    #     pass

    # def component(self, name: str) -> ComponentDep:
    #     pass

    # def http_adapter(self, name: str) -> ComponentDep:
    #     pass

    # def title(self, title: str):
    #     pass

    # def description(self, description: str):
    #     pass

    # def log(self) -> Logger:
    #     pass

    @classmethod
    def new(cls) -> Self:

        # svc = cls(
        #     routes=[],
        #     comp_def=ComponentDefinition(
        #         type=ComponentType.KubeFox,
        #         routes=[],
        #         env_var_schema={},
        #         dependencies={}
        #     ),
        #     max_event_size=vars.DEFAULT_MAX_EVENT_SIZE_BYTES,
        #     num_workers=os.cpu_count(),
        #     export=False,
        #     # log=logkf.Global,
        #     brk=grpc.NewClient(grpc.ClientOpts(
        #         Platform=platform,
        #         Component=comp,
        #         BrokerAddr=brokerAddr,
        #         HealthSrvAddr=healthAddr
        #     ))
        # )

        # return svc

        svc = cls(
            routes=[],
            comp_def=ComponentDefinition(
                type=ComponentType.KubeFox,
                default_handler=False,
                hash="123",
                image="abc",
                routes=[],
                env_var_schema={},
                dependencies={}
            ),
            max_event_size=DEFAULT_MAX_EVENT_SIZE_BYTES,
            num_workers=os.cpu_count(),
            export=False,
            # log=logkf.Global,
            # brk=grpc.NewClient(grpc.ClientOpts(
            #     Platform=platform,
            #     Component=comp,
            #     BrokerAddr=brokerAddr,
            #     HealthSrvAddr=healthAddr
            # ))
            log=None,
            brk=None
        )

        return svc


# class Kontext:
#     def env(self, v: EnvVarDep) -> str:
#         pass

#     def env_v(self, v: EnvVarDep) -> Val:
#         pass

#     def env_def(self, v: EnvVarDep, def: str) -> str:
#         pass

#     def env_def_v(self, v: EnvVarDep, def: Val) -> Val:
#         pass

#     def resp(self) -> 'Resp':
#         pass

#     def req(self, target: ComponentDep) -> 'Req':
#         pass

#     def forward(self, target: ComponentDep) -> 'Req':
#         pass

#     def http(self, target: ComponentDep) -> Client:
#         pass

#     def transport(self, target: ComponentDep) -> RoundTripper:
#         pass

#     def context(self) -> Context:
#         pass

#     def log(self) -> Logger:
#         pass


# class Req:
#     def send_str(self, s: str) -> ('EventReader', Optional[Exception]):
#         pass

#     def send_html(self, h: str) -> ('EventReader', Optional[Exception]):
#         pass

#     def send_json(self, v: Any) -> ('EventReader', Optional[Exception]):
#         pass

#     def send_bytes(self, content_type: str, content: bytes) -> ('EventReader', Optional[Exception]):
#         pass

#     def send_reader(self, content_type: str, reader: Any) -> ('EventReader', Optional[Exception]):
#         pass

#     def send(self) -> ('EventReader', Optional[Exception]):
#         pass


# class Resp:
#     def forward(self, evt: 'EventReader') -> Optional[Exception]:
#         pass

#     def send_str(self, s: str) -> Optional[Exception]:
#         pass

#     def send_html(self, h: str) -> Optional[Exception]:
#         pass

#     def send_json(self, v: Any) -> Optional[Exception]:
#         pass

#     def send_accepts(self, json: Any, html: str, str: str) -> Optional[Exception]:
#         pass

#     def send_bytes(self, content_type: str, b: bytes) -> Optional[Exception]:
#         pass

#     def send_reader(self, content_type: str, reader: Any) -> Optional[Exception]:
#         pass

#     def send_template(self, tpl: Template, name: str, data: Any) -> Optional[Exception]:
#         pass

#     def send_html_template(self, tpl: HTMLTemplate, name: str, data: Any) -> Optional[Exception]:
#         pass

#     def send(self) -> Optional[Exception]:
#         pass


# class EventReader:
#     def event_type(self) -> EventType:
#         pass

#     def param(self, key: str) -> str:
#         pass

#     def param_v(self, key: str) -> Val:
#         pass

#     def param_def(self, key: str, def: str) -> str:
#         pass

#     def url(self) -> (URL, Optional[Exception]):
#         pass

#     def path_suffix(self) -> str:
#         pass

#     def query(self, key: str) -> str:
#         pass

#     def query_v(self, key: str) -> Val:
#         pass

#     def query_def(self, key: str, def: str) -> str:
#         pass

#     def query_all(self, key: str) -> List[str]:
#         pass

#     def header(self, key: str) -> str:
#         pass

#     def header_v(self, key: str) -> Val:
#         pass

#     def header_def(self, key: str, def: str) -> str:
#         pass

#     def header_all(self, key: str) -> List[str]:
#         pass

#     def status(self) -> int:
#         pass

#     def status_v(self) -> Val:
#         pass

#     def bind(self, v: Any) -> Optional[Exception]:
#         pass

#     def str(self) -> str:
#         pass

#     def bytes(self) -> bytes:
#         pass


# class EventWriter(EventReader):
#     def set_param(self, key: str, value: str):
#         pass

#     def set_param_v(self, key: str, value: Val):
#         pass

#     def set_url(self, u: URL):
#         pass

#     def rewrite_path(self, path: str):
#         pass

#     def set_query(self, key: str, value: str):
#         pass

#     def set_query_v(self, key: str, value: Val):
#         pass

#     def del_query(self, key: str):
#         pass

#     def set_header(self, key: str, value: str):
#         pass

#     def set_header_v(self, key: str, value: Val):
#         pass

#     def add_header(self, key: str, value: str):
#         pass

#     def del_header(self, key: str):
#         pass

#     def set_status(self, code: int):
#         pass

#     def set_status_v(self, val: Val):
#         pass

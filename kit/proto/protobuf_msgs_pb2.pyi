from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from opentelemetry.proto.logs.v1 import logs_pb2 as _logs_pb2
from opentelemetry.proto.metrics.v1 import metrics_pb2 as _metrics_pb2
from opentelemetry.proto.trace.v1 import trace_pb2 as _trace_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class Category(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[Category]
    MESSAGE: _ClassVar[Category]
    REQUEST: _ClassVar[Category]
    RESPONSE: _ClassVar[Category]

UNKNOWN: Category
MESSAGE: Category
REQUEST: Category
RESPONSE: Category

class Component(_message.Message):
    __slots__ = ("type", "app", "name", "hash", "id", "broker_id")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    BROKER_ID_FIELD_NUMBER: _ClassVar[int]
    type: str
    app: str
    name: str
    hash: str
    id: str
    broker_id: str
    def __init__(
        self,
        type: _Optional[str] = ...,
        app: _Optional[str] = ...,
        name: _Optional[str] = ...,
        hash: _Optional[str] = ...,
        id: _Optional[str] = ...,
        broker_id: _Optional[str] = ...,
    ) -> None: ...

class EventContext(_message.Message):
    __slots__ = (
        "platform",
        "virtual_environment",
        "app_deployment",
        "release_manifest",
    )
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    APP_DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    RELEASE_MANIFEST_FIELD_NUMBER: _ClassVar[int]
    platform: str
    virtual_environment: str
    app_deployment: str
    release_manifest: str
    def __init__(
        self,
        platform: _Optional[str] = ...,
        virtual_environment: _Optional[str] = ...,
        app_deployment: _Optional[str] = ...,
        release_manifest: _Optional[str] = ...,
    ) -> None: ...

class SpanContext(_message.Message):
    __slots__ = ("trace_id", "span_id", "trace_state", "flags")
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    TRACE_STATE_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    trace_id: bytes
    span_id: bytes
    trace_state: str
    flags: int
    def __init__(
        self,
        trace_id: _Optional[bytes] = ...,
        span_id: _Optional[bytes] = ...,
        trace_state: _Optional[str] = ...,
        flags: _Optional[int] = ...,
    ) -> None: ...

class Event(_message.Message):
    __slots__ = (
        "id",
        "parent_id",
        "parent_span",
        "type",
        "category",
        "create_time",
        "ttl",
        "context",
        "source",
        "target",
        "params",
        "values",
        "content_type",
        "content",
    )

    class ParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    class ValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_SPAN_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    id: str
    parent_id: str
    parent_span: SpanContext
    type: str
    category: Category
    create_time: int
    ttl: int
    context: EventContext
    source: Component
    target: Component
    params: _containers.ScalarMap[str, str]
    values: _containers.ScalarMap[str, str]
    content_type: str
    content: bytes
    def __init__(
        self,
        id: _Optional[str] = ...,
        parent_id: _Optional[str] = ...,
        parent_span: _Optional[_Union[SpanContext, _Mapping]] = ...,
        type: _Optional[str] = ...,
        category: _Optional[_Union[Category, str]] = ...,
        create_time: _Optional[int] = ...,
        ttl: _Optional[int] = ...,
        context: _Optional[_Union[EventContext, _Mapping]] = ...,
        source: _Optional[_Union[Component, _Mapping]] = ...,
        target: _Optional[_Union[Component, _Mapping]] = ...,
        params: _Optional[_Mapping[str, str]] = ...,
        values: _Optional[_Mapping[str, str]] = ...,
        content_type: _Optional[str] = ...,
        content: _Optional[bytes] = ...,
    ) -> None: ...

class MatchedEvent(_message.Message):
    __slots__ = ("event", "route_id", "env")

    class EnvEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    EVENT_FIELD_NUMBER: _ClassVar[int]
    ROUTE_ID_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    event: Event
    route_id: int
    env: _containers.ScalarMap[str, str]
    def __init__(
        self,
        event: _Optional[_Union[Event, _Mapping]] = ...,
        route_id: _Optional[int] = ...,
        env: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class Telemetry(_message.Message):
    __slots__ = ("trace_id", "log_records", "metrics", "spans")
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    LOG_RECORDS_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    SPANS_FIELD_NUMBER: _ClassVar[int]
    trace_id: bytes
    log_records: _containers.RepeatedCompositeFieldContainer[_logs_pb2.LogRecord]
    metrics: _containers.RepeatedCompositeFieldContainer[_metrics_pb2.Metric]
    spans: _containers.RepeatedCompositeFieldContainer[_trace_pb2.Span]
    def __init__(
        self,
        trace_id: _Optional[bytes] = ...,
        log_records: _Optional[_Iterable[_Union[_logs_pb2.LogRecord, _Mapping]]] = ...,
        metrics: _Optional[_Iterable[_Union[_metrics_pb2.Metric, _Mapping]]] = ...,
        spans: _Optional[_Iterable[_Union[_trace_pb2.Span, _Mapping]]] = ...,
    ) -> None: ...

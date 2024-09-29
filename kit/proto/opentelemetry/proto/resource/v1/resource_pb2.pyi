from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from opentelemetry.proto.common.v1 import common_pb2 as _common_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class Resource(_message.Message):
    __slots__ = ("attributes", "dropped_attributes_count")
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    DROPPED_ATTRIBUTES_COUNT_FIELD_NUMBER: _ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[_common_pb2.KeyValue]
    dropped_attributes_count: int
    def __init__(
        self,
        attributes: _Optional[_Iterable[_Union[_common_pb2.KeyValue, _Mapping]]] = ...,
        dropped_attributes_count: _Optional[int] = ...,
    ) -> None: ...

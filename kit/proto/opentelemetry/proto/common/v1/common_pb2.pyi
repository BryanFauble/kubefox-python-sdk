from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class AnyValue(_message.Message):
    __slots__ = (
        "string_value",
        "bool_value",
        "int_value",
        "double_value",
        "array_value",
        "kvlist_value",
        "bytes_value",
    )
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    KVLIST_VALUE_FIELD_NUMBER: _ClassVar[int]
    BYTES_VALUE_FIELD_NUMBER: _ClassVar[int]
    string_value: str
    bool_value: bool
    int_value: int
    double_value: float
    array_value: ArrayValue
    kvlist_value: KeyValueList
    bytes_value: bytes
    def __init__(
        self,
        string_value: _Optional[str] = ...,
        bool_value: bool = ...,
        int_value: _Optional[int] = ...,
        double_value: _Optional[float] = ...,
        array_value: _Optional[_Union[ArrayValue, _Mapping]] = ...,
        kvlist_value: _Optional[_Union[KeyValueList, _Mapping]] = ...,
        bytes_value: _Optional[bytes] = ...,
    ) -> None: ...

class ArrayValue(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[AnyValue]
    def __init__(
        self, values: _Optional[_Iterable[_Union[AnyValue, _Mapping]]] = ...
    ) -> None: ...

class KeyValueList(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[KeyValue]
    def __init__(
        self, values: _Optional[_Iterable[_Union[KeyValue, _Mapping]]] = ...
    ) -> None: ...

class KeyValue(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: AnyValue
    def __init__(
        self,
        key: _Optional[str] = ...,
        value: _Optional[_Union[AnyValue, _Mapping]] = ...,
    ) -> None: ...

class InstrumentationScope(_message.Message):
    __slots__ = ("name", "version", "attributes", "dropped_attributes_count")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    DROPPED_ATTRIBUTES_COUNT_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: str
    attributes: _containers.RepeatedCompositeFieldContainer[KeyValue]
    dropped_attributes_count: int
    def __init__(
        self,
        name: _Optional[str] = ...,
        version: _Optional[str] = ...,
        attributes: _Optional[_Iterable[_Union[KeyValue, _Mapping]]] = ...,
        dropped_attributes_count: _Optional[int] = ...,
    ) -> None: ...

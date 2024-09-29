from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from opentelemetry.proto.logs.v1 import logs_pb2 as _logs_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class ExportLogsServiceRequest(_message.Message):
    __slots__ = ("resource_logs",)
    RESOURCE_LOGS_FIELD_NUMBER: _ClassVar[int]
    resource_logs: _containers.RepeatedCompositeFieldContainer[_logs_pb2.ResourceLogs]
    def __init__(
        self,
        resource_logs: _Optional[
            _Iterable[_Union[_logs_pb2.ResourceLogs, _Mapping]]
        ] = ...,
    ) -> None: ...

class ExportLogsServiceResponse(_message.Message):
    __slots__ = ("partial_success",)
    PARTIAL_SUCCESS_FIELD_NUMBER: _ClassVar[int]
    partial_success: ExportLogsPartialSuccess
    def __init__(
        self,
        partial_success: _Optional[_Union[ExportLogsPartialSuccess, _Mapping]] = ...,
    ) -> None: ...

class ExportLogsPartialSuccess(_message.Message):
    __slots__ = ("rejected_log_records", "error_message")
    REJECTED_LOG_RECORDS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    rejected_log_records: int
    error_message: str
    def __init__(
        self,
        rejected_log_records: _Optional[int] = ...,
        error_message: _Optional[str] = ...,
    ) -> None: ...

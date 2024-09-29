import json
import traceback
from enum import Enum
from typing import Optional

# Define the error codes as an enumeration


class Code(Enum):
    UNEXPECTED = 0
    BROKER_MISMATCH = 1
    BROKER_UNAVAILABLE = 2
    COMPONENT_GONE = 3
    COMPONENT_MISMATCH = 4
    CONTENT_TOO_LARGE = 5
    INVALID = 6
    NOT_FOUND = 7
    PORT_UNAVAILABLE = 8
    ROUTE_INVALID = 9
    ROUTE_NOT_FOUND = 10
    TIMEOUT = 11
    UNAUTHORIZED = 12
    UNKNOWN_CONTENT_TYPE = 13
    UNSUPPORTED_ADAPTER = 14


# Global variable to control stack trace recording
RECORD_STACK_TRACES = False


class KubeFoxError(Exception):
    def __init__(
        self,
        msg: str,
        code: Code,
        grpc_code: int,
        http_code: int,
        cause: Optional[str] = None,
    ) -> None:
        self.msg = msg
        self.code = code
        self.grpc_code = grpc_code
        self.http_code = http_code
        self.cause = cause
        self.stack = (
            traceback.format_stack()
            if RECORD_STACK_TRACES or code == Code.UNEXPECTED
            else None
        )

    def __str__(self):
        if self.cause:
            return f"{self.msg}: {self.cause}"
        return self.msg

    def to_dict(self):
        return {
            "msg": self.msg,
            "code": self.code.value,
            "grpc_code": self.grpc_code,
            "http_code": self.http_code,
            "cause": self.cause,
            "stack": self.stack,
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(
            msg=data["msg"],
            code=Code(data["code"]),
            grpc_code=data["grpc_code"],
            http_code=data["http_code"],
            cause=data["cause"],
        )


class KubeFoxErrorBrokerMismatch(KubeFoxError):
    def __init__(self, cause: Optional[str] = None) -> None:
        super().__init__("broker mismatch", Code.BROKER_MISMATCH, 9, 502, cause)


class KubeFoxErrorBrokerUnavailable(KubeFoxError):
    def __init__(self, cause: Optional[str] = None) -> None:
        super().__init__("broker unavailable", Code.BROKER_UNAVAILABLE, 14, 502, cause)


class KubeFoxErrorComponentGone(KubeFoxError):
    def __init__(self, cause: Optional[str] = None) -> None:
        super().__init__("component gone", Code.COMPONENT_GONE, 9, 502, cause)


class KubeFoxErrorComponentMismatch(KubeFoxError):
    def __init__(self, cause: Optional[str] = None) -> None:
        super().__init__("component mismatch", Code.COMPONENT_MISMATCH, 9, 502, cause)


class KubeFoxErrorContentTooLarge(KubeFoxError):
    def __init__(self, cause: Optional[str] = None) -> None:
        super().__init__("content too large", Code.CONTENT_TOO_LARGE, 8, 413, cause)


class KubeFoxErrorInvalid(KubeFoxError):
    def __init__(self, cause: Optional[str] = None) -> None:
        super().__init__("invalid", Code.INVALID, 3, 400, cause)


class KubeFoxErrorNotFound(KubeFoxError):
    def __init__(self, cause: Optional[str] = None) -> None:
        super().__init__("not found", Code.NOT_FOUND, 12, 404, cause)


class KubeFoxErrorPortUnavailable(KubeFoxError):
    def __init__(self, cause: Optional[str] = None) -> None:
        super().__init__("port unavailable", Code.PORT_UNAVAILABLE, 14, 409, cause)


class KubeFoxErrorRouteInvalid(KubeFoxError):
    def __init__(self, cause: Optional[str] = None) -> None:
        super().__init__("route invalid", Code.ROUTE_INVALID, 3, 400, cause)


class KubeFoxErrorRouteNotFound(KubeFoxError):
    def __init__(self, cause: Optional[str] = None) -> None:
        super().__init__("route not found", Code.ROUTE_NOT_FOUND, 12, 404, cause)


class KubeFoxErrorTimeout(KubeFoxError):
    def __init__(self, cause: Optional[str] = None) -> None:
        super().__init__("time out", Code.TIMEOUT, 4, 504, cause)


class KubeFoxErrorUnauthorized(KubeFoxError):
    def __init__(self, cause: Optional[str] = None) -> None:
        super().__init__("component unauthorized", Code.UNAUTHORIZED, 7, 403, cause)


class KubeFoxErrorUnexpected(KubeFoxError):
    def __init__(self, cause: Optional[str] = None) -> None:
        super().__init__("unexpected error", Code.UNEXPECTED, 2, 500, cause)


class KubeFoxErrorUnknownContentType(KubeFoxError):
    def __init__(self, cause: Optional[str] = None) -> None:
        super().__init__(
            "unknown content type", Code.UNKNOWN_CONTENT_TYPE, 3, 400, cause
        )


class KubeFoxErrorUnsupportedAdapter(KubeFoxError):
    def __init__(self, cause: Optional[str] = None) -> None:
        super().__init__(
            "unsupported adapter", Code.UNSUPPORTED_ADAPTER, 12, 400, cause
        )

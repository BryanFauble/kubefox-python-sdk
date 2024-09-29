from dataclasses import dataclass
from typing import Any, Optional, Union
from urllib.parse import urlparse, urlunparse

from kit.api.event_reader import EventReader


@dataclass
class EventWriter(EventReader):
    def SetParam(self, key: str, value: str) -> None:
        """Set a parameter with a string value."""
        raise NotImplementedError

    def SetParamV(self, key: str, value: Any) -> None:
        """Set a parameter with a value of any type."""
        raise NotImplementedError

    def SetURL(self, u: str) -> None:
        """Set the URL."""
        raise NotImplementedError

    def RewritePath(self, path: str) -> None:
        """Rewrite the path."""
        raise NotImplementedError

    def SetQuery(self, key: str, value: str) -> None:
        """Set a query parameter with a string value."""
        raise NotImplementedError

    def SetQueryV(self, key: str, value: Any) -> None:
        """Set a query parameter with a value of any type."""
        raise NotImplementedError

    def DelQuery(self, key: str) -> None:
        """Delete a query parameter."""
        raise NotImplementedError

    def SetHeader(self, key: str, value: str) -> None:
        """Set a header with a string value."""
        raise NotImplementedError

    def SetHeaderV(self, key: str, value: Any) -> None:
        """Set a header with a value of any type."""
        raise NotImplementedError

    def AddHeader(self, key: str, value: str) -> None:
        """Add a header with a string value."""
        raise NotImplementedError

    def DelHeader(self, key: str) -> None:
        """Delete a header."""
        raise NotImplementedError

    def SetStatus(self, code: int) -> None:
        """Set the status code."""
        raise NotImplementedError

    def SetStatusV(self, val: Any) -> None:
        """Set the status code with a value of any type."""
        raise NotImplementedError

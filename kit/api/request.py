from io import IOBase
from typing import Any


class Req:
    """
    Req interface.

    This interface provides methods for sending requests to a target Component and
    returning the response.
    """

    def SendStr(self, s: str) -> tuple["EventReader", Exception]:
        """
        SendStr sends the request to the target Component and returns the response.
        The given string is used as the content of the request Event, content-type
        is set to 'text/plain'.

        Args:
            s (str): The string to be sent.

        Returns:
            tuple['EventReader', Exception]: A tuple containing the EventReader
                and any error that occurred.
        """
        raise NotImplementedError

    def SendHTML(self, h: str) -> tuple["EventReader", Exception]:
        """
        SendHTML sends the request to the target Component and returns the response.
        The given HTML is used as the content of the request Event, content-type
        is set to 'text/html'.

        Args:
            h (str): The HTML to be sent.

        Returns:
            tuple['EventReader', Exception]: A tuple containing the EventReader
                and any error that occurred.
        """
        raise NotImplementedError

    def SendJSON(self, v: Any) -> tuple["EventReader", Exception]:
        """
        SendJSON sends the request to the target Component and returns the response.
        The given object is marshalled to JSON and the output is used as the
        content of the request Event, content-type is set to 'application/json'.

        Args:
            v (Any): The object to be sent.

        Returns:
            tuple['EventReader', Exception]: A tuple containing the EventReader
                and any error that occurred.
        """
        raise NotImplementedError

    def SendBytes(
        self, content_type: str, content: bytes
    ) -> tuple["EventReader", Exception]:
        """
        SendBytes sends the request to the target Component using the given
        content-type and content and returns the response.

        Args:
            content_type (str): The content type of the request.
            content (bytes): The content of the request.

        Returns:
            tuple['EventReader', Exception]: A tuple containing the EventReader
                and any error that occurred.
        """
        raise NotImplementedError

    def SendReader(
        self, content_type: str, reader: IOBase
    ) -> tuple["EventReader", Exception]:
        """
        SendReader sends the request to the target Component and returns the response.
        All data is read from the given reader and is used as the content of the
        request Event. If the reader implements io.ReadCloser then it will be
        automatically closed.

        Args:
            content_type (str): The content type of the request.
            reader (IOBase): The reader to read the content from.

        Returns:
            tuple['EventReader', Exception]: A tuple containing the EventReader
                and any error that occurred.
        """
        raise NotImplementedError

    def Send(self) -> tuple["EventReader", Exception]:
        """
        Send sends the request to the target Component and returns the response.

        Returns:
            tuple['EventReader', Exception]: A tuple containing the EventReader
                and any error that occurred.
        """
        raise NotImplementedError

"""Test running the Python Kit SDK"""

import asyncio
import logging

from proto.protobuf_msgs_pb2 import Event as ProtoEvent
from proto.protobuf_msgs_pb2 import EventContext, MatchedEvent

from kit import Kit
from kit.api.event import Event
from kit.proto.protobuf_msgs_pb2 import Category

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(module)s:%(lineno)d - %(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# TODO: Extract this out into a "nice to use" interface that exposes the same functionality as the golang client
def return_response(event: MatchedEvent) -> Event:
    my_context = EventContext(
        platform="debug",
        virtual_environment="qa",
        app_deployment="hello-world-main",
        release_manifest="",
    )
    target_component = event.event.target
    target_component.id = "1234"
    target_component.hash = "976e059"
    my_event = Event(
        proto_object=ProtoEvent(
            context=my_context,
            type="io.kubefox.kubefox",
            content_type="text/plain; charset=UTF-8",
            ttl=event.event.ttl,
            source=target_component,
            target=event.event.source,
            content=b"hello world",
            category=Category.RESPONSE,
            parent_id=event.event.id,
            parent_span=event.event.parent_span,
        )
    )
    return my_event


async def my_cool_function(event: MatchedEvent) -> Event:
    return return_response(event)


if __name__ == "__main__":
    instance = Kit.new()
    instance.event_request_handlers = my_cool_function
    asyncio.run(instance.start())

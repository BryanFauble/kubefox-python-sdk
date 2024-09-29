"""Test running the Python Kit SDK"""

import asyncio
import logging
import random

from opentelemetry import trace

from kit import Kit
from kit.proto.protobuf_msgs_pb2 import Category, Event, EventContext, MatchedEvent

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(module)s:%(lineno)d - %(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

tracer = trace.get_tracer(__name__)

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
    return my_event


async def my_cool_function(event: MatchedEvent) -> Event:
    with tracer.start_as_current_span("my_cool_function"):
        await asyncio.sleep(random.uniform(0.01, 1))
        return return_response(event)


if __name__ == "__main__":
    instance = Kit.new()
    instance.export = False
    instance.route("Path(`/{{.Vars.subPath}}/hello`)", my_cool_function)
    asyncio.run(instance.start())

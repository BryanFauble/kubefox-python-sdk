import asyncio
import logging
import os
import random
from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, Coroutine, Dict, List, Self, Tuple

from dataclasses_json import LetterCase, dataclass_json
from grpc import aio, ssl_channel_credentials
from opentelemetry import trace

from kit.api import exceptions as KitExceptions
from kit.api import vars as KitVars
from kit.api.env_template import EnvTemplate
from kit.api.kit_types import (
    ComponentDefinition,
    ComponentType,
    EventType,
    Route,
    RouteSpec,
)
from kit.proto.broker_svc_pb2_grpc import BrokerStub
from kit.proto.protobuf_msgs_pb2 import (
    Category,
    Component,
    Event,
    EventContext,
    MatchedEvent,
)
from kit.telemetry.trace import (
    attach_event_attributes,
    extract_otel_context,
    setup_trace_provder,
)

tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)
max_attempts = 5

# TODO: https://www.python-httpx.org/advanced/transports/#custom-transports
# Implement a custom transport for HTTPX to handle putting data into and pulling data out of an event


def set_json(event: Event, v) -> None:
    if v is None:
        v = {}
    b = v.to_json().encode("utf-8")

    event.content_type = f"{
        KitVars.CONTENT_TYPE_JSON}; {KitVars.CHARSET_UTF8}"
    event.content = b


def create_subscription() -> Event:
    my_context = EventContext(
        platform="debug",
        virtual_environment="virtual_environment",
        app_deployment="hello-world",
        release_manifest="release_manifest",
    )
    my_event = Event(
        context=my_context,
        id="1234",
        type=EventType.Register.value,
        content_type="application/json",
        ttl=1,
    )
    component_def = ComponentDefinition(
        type=ComponentType.KubeFox,
        default_handler=False,
        hash="123",
        image="abc",
        # TODO: Pass along the routes to the initial subscription event
        routes=[],
        env_var_schema={},
        dependencies={},
    )
    set_json(event=my_event, v=component_def)
    return my_event


async def yield_event_queue(
    initial_subscription: Event, request_queue: asyncio.Queue
) -> AsyncGenerator[Event, Any]:
    yield initial_subscription
    while True:
        new_request: Event = await request_queue.get()
        with tracer.start_as_current_span(
            name=f"Send {Category.Name(new_request.category)} to broker",
            context=extract_otel_context(new_request.parent_span),
        ) as root_span:
            attach_event_attributes(event=new_request, span=root_span)
            yield new_request
            request_queue.task_done()


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Kit:
    max_event_size: int
    num_workers: int
    export: bool
    log: logging.Logger
    broker_component: Component = None
    routes: Dict[int, Route] = field(default_factory=dict)
    comp_def: ComponentDefinition = field(default_factory=ComponentDefinition)
    # TODO: Update the typing here to be more specific than Any
    default_request_handler: Coroutine[Any, Any, Any] = None

    to_broker_queue: asyncio.Queue = asyncio.Queue()
    from_broker_queue: asyncio.Queue = asyncio.Queue()

    def __post_init__(self) -> None:
        # TODO: Pull data to pass along to the initial setup of the tracer instead of hard coding
        metadata = {
            "id": "1234",
            "hash": "976e059",
            "name": "hello-world",
            "component": "frontend",
        }
        setup_trace_provder(
            component_id=metadata["id"],
            component_hash=metadata["hash"],
            name=metadata["name"],
            component=metadata["component"],
        )

    def register_default_request_handler(
        self, handler: Coroutine[Any, Any, Any]
    ) -> None:
        self.default_request_handler = handler
        self.comp_def.default_handler = handler is not None

    def route(self, rule: str, handler: Coroutine[Any, Any, Any]) -> None:
        r = EnvTemplate("route", rule)
        kit_route_spec = RouteSpec(
            id=len(self.routes), rule=rule, env_var_schema=r.env_schema.vars
        )
        kit_route = Route(route_spec=kit_route_spec, handler=handler)
        self.routes.update({len(self.routes): kit_route})
        self.comp_def.routes.append(kit_route_spec)

    async def handle_subscription(
        self,
        initial_sub: AsyncGenerator[Event, Any],
        stub: BrokerStub,
        metadata_sequence: List[Tuple[str, str]],
    ) -> None:
        response = stub.Subscribe(initial_sub, metadata=metadata_sequence)
        subscribed = False
        async for res in response:
            res_event: MatchedEvent = res
            if not subscribed:
                subscribed = True
                self.broker_component = res_event.event.source
                print(f"Initial subscription event response: {res_event}")
            else:
                print("Got message from broker")
                self.from_broker_queue.put_nowait(res_event)

    async def process_responses(self, worker_name: str) -> None:
        """
        Handles the responses from the broker. This is one of the two main loops of
        kit.

        TODO: Add some more documentation here
        TODO: Implement all categories and exception handling
        """
        try:
            while True:
                # Wait until there is an event in the queue
                matched_event: MatchedEvent = await self.from_broker_queue.get()

                with tracer.start_as_current_span(
                    name=f"Handle {Category.Name(matched_event.event.category)}",
                    context=extract_otel_context(matched_event.event.parent_span),
                ) as root_span:
                    attach_event_attributes(matched_event=matched_event, span=root_span)

                    print(
                        f"Worker: {worker_name}, "
                        + f"Processing event: {matched_event.event.id}"
                    )

                    if matched_event.event.category == Category.REQUEST:
                        route_id = matched_event.route_id
                        route = self.routes.get(route_id, None)
                        if route is None:
                            handler = self.default_request_handler
                            if handler is None:
                                raise KitExceptions.KubeFoxErrorNotFound(
                                    "default handler not found"
                                )
                        else:
                            handler = route.handler
                        result_of_response_to_request = await handler(matched_event)
                        print(
                            f"Got result from handler for worker: {
                              worker_name}"
                        )
                        await self.to_broker_queue.put(result_of_response_to_request)
                    elif matched_event.event.category == Category.RESPONSE:
                        print("Response received")

                self.from_broker_queue.task_done()

        except Exception as e:
            logger.exception(f"Error in process_responses")
        finally:
            raise KitExceptions.KubeFoxErrorUnexpected("Shutting down worker")

    async def start(self, attempt: int = 0):
        if attempt >= max_attempts:
            raise KitExceptions.KubeFoxErrorTimeout("broker subscription timed out")

        if self.export:
            # TODO: Write out in JSON the component definition
            print(self.comp_def.to_json())
            return
            # TODO: Code for starting up broker in "dry-run" mode is needed. This is used to generate the ApplicationManifest k8s resource definition
            # Extracting env vars from routes: https://github.com/xigxog/kubefox/blob/main/api/env_template.go#L53

        # open ca.crt and read into string:
        with open("/tmp/kubefox/ca.crt", "r") as file:
            root_ca = file.read()
        with open("/tmp/kubefox/hello-world-token", "r") as file:
            token = file.read()
        creds = ssl_channel_credentials(
            root_certificates=root_ca.encode(), private_key=None, certificate_chain=None
        )

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

        logger.info("subscribing to broker, attempt %d/%d", attempt + 1, max_attempts)
        async with aio.secure_channel(
            target="127.0.0.1:6060", credentials=creds
        ) as channel:
            stub = BrokerStub(channel)

            # A CallCredentials has to be used with secure Channel, otherwise the metadata will not be transmitted to the server.
            metadata = {
                "id": "1234",
                "hash": "976e059",
                "name": "hello-world",
                "app": "hello-world",
                "type": "KubeFox",
                "platform": "debug",
                "pod": "hello-world",
                "token": token,
                "component": "frontend",
            }
            metadata_sequence = [(k, v) for k, v in metadata.items()]
            my_event = create_subscription()
            response_workers = []
            for i in range(os.cpu_count()):
                response_workers.append(asyncio.create_task(self.process_responses(i)))
            try:
                await asyncio.gather(
                    *[
                        self.handle_subscription(
                            yield_event_queue(
                                initial_subscription=my_event,
                                request_queue=self.to_broker_queue,
                            ),
                            stub,
                            metadata_sequence,
                        ),
                        *response_workers,
                    ]
                )
            except (asyncio.exceptions.CancelledError, ConnectionRefusedError):
                logger.warning("broker subscription closed", exc_info=True)
                await asyncio.sleep(random.randint(1, 2))
                await self.start(attempt + 1)
            except Exception as e:
                print(f"Error: {e}")
                raise
            finally:
                # Should probably make sure we empty out the event queues
                # print("Done - To clean up anything here?")
                pass

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
            # routes=[],
            comp_def=ComponentDefinition(
                type=ComponentType.KubeFox,
                default_handler=False,
                hash="123",
                image="abc",
                routes=[],
                env_var_schema={},
                dependencies={},
            ),
            max_event_size=KitVars.DEFAULT_MAX_EVENT_SIZE_BYTES,
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
        )

        return svc

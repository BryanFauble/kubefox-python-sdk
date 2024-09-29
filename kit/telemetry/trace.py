from typing import List, Optional

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import SpanProcessor, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Context, Span, SpanContext, get_current_span
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from kit.proto.protobuf_msgs_pb2 import Event, MatchedEvent
from kit.proto.protobuf_msgs_pb2 import SpanContext as ProtoSpanContext
from kit.telemetry import vars as TelemetryVars


class AttributePropagatingSpanProcessor(SpanProcessor):
    """Class used to propagate attributes from parent spans to child spans if
    the attributes exist in the parent span."""

    def __init__(self, attributes_to_propagate: Optional[List[str]] = None) -> None:
        """Initializes the AttributePropagatingSpanProcessor with a number of
        attributes to propagate."""
        self.attributes_to_propagate = attributes_to_propagate or [
            TelemetryVars.ATTR_KEY_EVENT_ID,
            TelemetryVars.ATTR_KEY_EVENT_PARENT_ID,
            TelemetryVars.ATTR_KEY_EVENT_TYPE,
            TelemetryVars.ATTR_KEY_EVENT_CATEGORY,
            TelemetryVars.ATTR_KEY_EVENT_TTL,
            TelemetryVars.ATTR_KEY_ROUTE_ID,
            TelemetryVars.ATTR_KEY_EVENT_VIRTUAL_ENV,
            TelemetryVars.ATTR_KEY_EVENT_APP_DEPLOYMENT,
            TelemetryVars.ATTR_KEY_EVENT_REL_MANIFEST,
            TelemetryVars.ATTR_KEY_PLATFORM,
            TelemetryVars.ATTR_KEY_EVENT_SOURCE_ID,
            TelemetryVars.ATTR_KEY_EVENT_SOURCE_HASH,
            TelemetryVars.ATTR_KEY_EVENT_SOURCE_NAME,
            TelemetryVars.ATTR_KEY_EVENT_SOURCE_TYPE,
            TelemetryVars.ATTR_KEY_EVENT_TARGET_ID,
            TelemetryVars.ATTR_KEY_EVENT_TARGET_HASH,
            TelemetryVars.ATTR_KEY_EVENT_TARGET_NAME,
            TelemetryVars.ATTR_KEY_EVENT_TARGET_TYPE,
            TelemetryVars.ATTR_KEY_COMPONENT_APP,
            TelemetryVars.ATTR_KEY_COMPONENT_HASH,
            TelemetryVars.ATTR_KEY_COMPONENT_ID,
            TelemetryVars.ATTR_KEY_COMPONENT_NAME,
            TelemetryVars.ATTR_KEY_COMPONENT_TYPE,
        ]

    def on_start(self, span: Span, parent_context: SpanContext) -> None:
        """Propagates attributes from the parent span to the child span.

        Arguments:
            span: The child span to which the attributes should be propagated.
            parent_context: The context of the parent span.

        Returns:
            None
        """
        parent_span = get_current_span()
        if parent_span is not None and parent_span.is_recording():
            for attribute in self.attributes_to_propagate:
                if attribute in parent_span.attributes:
                    span.set_attribute(attribute, parent_span.attributes[attribute])

    def on_end(self, span: Span) -> None:
        """No-op method that does nothing when the span ends."""
        pass

    def shutdown(self) -> None:
        """No-op method that does nothing when the span processor is shut down."""
        pass

    def force_flush(self, timeout_millis: int = 30000) -> None:
        """No-op method that does nothing when the span processor is forced to flush."""
        pass


def extract_otel_context(protobuf_message: ProtoSpanContext) -> Context:
    """Utility function to extract an OpenTelemetry context from a protobuf message.

    Arguments:
        protobuf_message: The protobuf message containing the span context.

    Returns:
        The OpenTelemetry context.
    """

    carrier = {"traceparent": construct_traceparent(protobuf_message)}
    return TraceContextTextMapPropagator().extract(carrier)


def construct_traceparent(protobuf_message: ProtoSpanContext) -> str:
    """Utility function to construct a traceparent string from a protobuf message."""
    # Extract fields from the protobuf message
    trace_id = protobuf_message.trace_id
    span_id = protobuf_message.span_id
    # flags = protobuf_message.flags

    # Convert trace_id and span_id from bytes to hex strings
    trace_id_hex = trace_id.hex()
    span_id_hex = span_id.hex()

    if protobuf_message.trace_state == "kf=1":
        # Convert flags to a 2-digit hex string
        flags_hex = f"{1:02x}"
    else:
        # Convert flags to a 2-digit hex string
        flags_hex = f"{0:02x}"

    # Construct the traceparent string
    traceparent = f"00-{trace_id_hex}-{span_id_hex}-{flags_hex}"

    return traceparent


def attach_event_attributes(
    span: Span,
    matched_event: Optional[MatchedEvent] = None,
    event: Optional[Event] = None,
) -> None:
    """Utility function to attach event attributes to a span. match_event or event
    must be provided. If both are provided, the event attributes from the matched_event
    will be attached to the span.

    Arguments:
        span: The span to which the event attributes should be attached.
        matched_event: The matched event containing the event attributes.
        event: The event containing the event attributes. This is an optional
            alternative to the matched_event.

    Returns:
        None
    """
    if matched_event is None and matched_event is None:
        return

    event = event or matched_event.event

    # Set basic event attributes
    span.set_attributes(
        attributes={
            TelemetryVars.ATTR_KEY_EVENT_ID: event.id,
            TelemetryVars.ATTR_KEY_EVENT_PARENT_ID: event.parent_id,
            TelemetryVars.ATTR_KEY_EVENT_TYPE: event.type,
            TelemetryVars.ATTR_KEY_EVENT_CATEGORY: event.category,
            TelemetryVars.ATTR_KEY_EVENT_TTL: event.ttl,
            # TODO: We do not have this data
            # TelemetryVars.ATTR_KEY_INSTANCE: ,
        }
    )

    if matched_event is not None:
        span.set_attributes(
            attributes={
                TelemetryVars.ATTR_KEY_ROUTE_ID: matched_event.route_id,
            }
        )

    # Set context attributes if available
    if event.context is not None:
        span.set_attributes(
            attributes={
                TelemetryVars.ATTR_KEY_EVENT_VIRTUAL_ENV: event.context.virtual_environment,
                TelemetryVars.ATTR_KEY_EVENT_APP_DEPLOYMENT: event.context.app_deployment,
                TelemetryVars.ATTR_KEY_EVENT_REL_MANIFEST: event.context.release_manifest,
                TelemetryVars.ATTR_KEY_PLATFORM: event.context.platform,
            }
        )

    # Set source attributes if available
    if event.source is not None:
        span.set_attributes(
            attributes={
                TelemetryVars.ATTR_KEY_EVENT_SOURCE_ID: event.source.id,
                TelemetryVars.ATTR_KEY_EVENT_SOURCE_HASH: event.source.hash,
                TelemetryVars.ATTR_KEY_EVENT_SOURCE_NAME: event.source.name,
                TelemetryVars.ATTR_KEY_EVENT_SOURCE_TYPE: event.source.type,
            }
        )

    # Set target attributes if available
    if event.target is not None:
        span.set_attributes(
            attributes={
                TelemetryVars.ATTR_KEY_EVENT_TARGET_ID: event.target.id,
                TelemetryVars.ATTR_KEY_EVENT_TARGET_HASH: event.target.hash,
                TelemetryVars.ATTR_KEY_EVENT_TARGET_NAME: event.target.name,
                TelemetryVars.ATTR_KEY_EVENT_TARGET_TYPE: event.target.type,
            }
        )

        # TODO: These should come from our own component definition:
        span.set_attributes(
            attributes={
                TelemetryVars.ATTR_KEY_COMPONENT_APP: event.target.app,
                TelemetryVars.ATTR_KEY_COMPONENT_HASH: event.target.hash,
                TelemetryVars.ATTR_KEY_COMPONENT_ID: event.target.id,
                TelemetryVars.ATTR_KEY_COMPONENT_NAME: event.target.name,
                TelemetryVars.ATTR_KEY_COMPONENT_TYPE: event.target.type,
            }
        )


def setup_trace_provder(
    component_id: str, component_hash: str, name: str, component: str
) -> None:
    """
    Utility function to setup the trace provider with the necessary span processors.
    With this setup, the trace provider will propagate attributes from parent spans to
    child spans.

    Arguments:
        component_id: The ID of the component.
        component_hash: The hash of the component.
        name: The name of the component.
        component: The type of the component.

    Returns:
        None
    """
    service_name = f"{name}-{component}-{component_hash}-{component_id}"
    trace.set_tracer_provider(
        TracerProvider(resource=Resource(attributes={SERVICE_NAME: service_name}))
    )
    processor = BatchSpanProcessor(OTLPSpanExporter())
    attribute_propogator = AttributePropagatingSpanProcessor()
    trace.get_tracer_provider().add_span_processor(attribute_propogator)
    trace.get_tracer_provider().add_span_processor(processor)

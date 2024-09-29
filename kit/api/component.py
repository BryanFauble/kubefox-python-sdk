from dataclasses import dataclass
from typing import Self

from kit.proto.protobuf_msgs_pb2 import Component as ProtoObject
from kit.utils import utils


@dataclass
class Component:
    proto_object: ProtoObject

    @classmethod
    def new_component(cls, typ, app, name, component_hash) -> Self:
        return cls(
            ProtoObject(
                Type=str(typ),
                App=utils.clean_name(app),
                Name=utils.clean_name(name),
                Hash=component_hash,
            )
        )

    @classmethod
    def new_target_component(cls, typ, name) -> Self:
        return cls(ProtoObject(Type=str(typ), Name=utils.clean_name(name)))

    @classmethod
    def new_platform_component(cls, typ, name, component_hash) -> Self:
        return cls(
            ProtoObject(Type=str(typ), Name=utils.clean_name(name), Hash=component_hash)
        )

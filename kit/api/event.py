from dataclasses import dataclass

from kit.api import constants
from kit.proto.protobuf_msgs_pb2 import Event as ProtoObject

# TODO: Take a look at the following and see what we want to extract out from other implementations:
# https://fastapi.tiangolo.com/
# https://docs.djangoproject.com/en/5.1/ref/request-response/
# https://flask.palletsprojects.com/en/3.0.x/quickstart/


# TODO: Replace this Event class with an EventReader/EventWriter class
@dataclass
class Event:
    proto_object: ProtoObject

    def set_json(self, v):
        if v is None:
            v = {}
        # TODO: Some clever typing is needed here since `.to_json()` is a method of https://pypi.org/project/dataclasses-json/ and added via `@dataclass_json`
        # TODO: Re-work this to be wrapped by EventReader/EventWriter
        b = v.to_json().encode("utf-8")

        self.proto_object.content_type = f"{
            constants.CONTENT_TYPE_JSON}; {constants.CHARSET_UTF8}"
        self.proto_object.content = b

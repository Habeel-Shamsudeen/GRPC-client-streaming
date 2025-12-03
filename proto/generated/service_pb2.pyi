import data_model_pb2 as _data_model_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class StreamResonse(_message.Message):
    __slots__ = ("success", "message_received", "message_dropped", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_RECEIVED_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_DROPPED_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message_received: int
    message_dropped: int
    message: str
    def __init__(self, success: bool = ..., message_received: _Optional[int] = ..., message_dropped: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

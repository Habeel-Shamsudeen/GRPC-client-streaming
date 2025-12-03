import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOT_STARTED: _ClassVar[Status]
    IN_PROGRESS: _ClassVar[Status]
    COMPLETED: _ClassVar[Status]
NOT_STARTED: Status
IN_PROGRESS: Status
COMPLETED: Status

class WorkItem(_message.Message):
    __slots__ = ("id", "username", "payload", "status", "priority", "timestamp", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    username: str
    payload: str
    status: Status
    priority: bool
    timestamp: _timestamp_pb2.Timestamp
    metadata: _any_pb2.Any
    def __init__(self, id: _Optional[str] = ..., username: _Optional[str] = ..., payload: _Optional[str] = ..., status: _Optional[_Union[Status, str]] = ..., priority: bool = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., metadata: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

import random
import uuid
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from proto.generated.data_model_pb2 import WorkItem, Status

DUMMY_IDS = [
    str(uuid.uuid4()) for _ in range(50)
]

DUMMY_USERNAMES = [
    "alice_johnson", "bob_smith", "charlie_brown", "diana_prince", "eve_wilson",
    "frank_miller", "grace_kelly", "henry_davis", "ivy_chen", "jack_taylor",
    "karen_white", "liam_martinez", "mia_rodriguez", "noah_anderson", "olivia_thomas",
    "paul_walker", "quinn_foster", "rachel_green", "sam_wilson", "tina_turner",
    "user_001", "admin_user", "test_account", "demo_user", "guest_access"
]

DUMMY_PAYLOADS = [
    "Process payment transaction",
    "Generate monthly report",
    "Send email notification",
    "Update user profile",
    "Create backup snapshot",
    "Validate authentication token",
    "Calculate analytics metrics",
    "Sync data to external service",
    "Generate PDF document",
    "Process image upload",
    "Update inventory levels",
    "Send push notification",
    "Process order fulfillment",
    "Generate invoice",
    "Validate form submission",
    "Process refund request",
    "Update search index",
    "Send SMS notification",
    "Generate API response",
    "Process webhook event",
    "Update cache entries",
    "Process subscription renewal",
    "Generate audit log",
    "Validate API key",
    "Process batch job"
]

STATUS_OPTIONS = [Status.NOT_STARTED, Status.IN_PROGRESS, Status.COMPLETED]


def get_random_data() -> WorkItem:
    item_id = str(uuid.uuid4())
    
    username = random.choice(DUMMY_USERNAMES)
    payload = random.choice(DUMMY_PAYLOADS)
    status = random.choice(STATUS_OPTIONS)
    priority = random.random() < 0.3
    
    timestamp = create_timestamp(datetime.now())
    
    work_item = WorkItem(
        id=item_id,
        username=username,
        payload=payload,
        status=status,
        priority=priority,
        timestamp=timestamp
    )
    
    return work_item


def create_timestamp(dt: datetime) -> Timestamp:
    timestamp = Timestamp()
    timestamp.FromDatetime(dt)
    return timestamp
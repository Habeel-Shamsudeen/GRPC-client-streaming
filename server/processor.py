import asyncio
import logging
import time
from proto.generated.data_model_pb2 import WorkItem

async def process_message(batch : list[WorkItem]):
    # Processing the messages one by one
    start_time = time.time()
    down_stream_data = []
    for message in batch:
        # simulate processing of message
        data = {
            "uuid" : message.id,
            "payload" : message.payload
        }
        down_stream_data.append(data)
        await asyncio.sleep(0.05) # can be transformation, db call etc
    
    # simulate sending the transformed message downstream
    asyncio.create_task(send_downstream(down_stream_data))
    end_time = time.time()
    logging.info(f"Finished Processing message took {(end_time-start_time)*1000:.1f}ms for {len(batch)}")


async def send_downstream(data):
    # simulate sending data to downstream services or kafka
    await asyncio.sleep(0.3)

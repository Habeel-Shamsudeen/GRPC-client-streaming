import asyncio
import logging
import time
from proto.generated.data_model_pb2 import WorkItem, Status
from redis.asyncio import Redis
from aiokafka import AIOKafkaProducer

async def process_message(batch : list[WorkItem], redis_client:Redis, kafka_producer:AIOKafkaProducer):
    # Processing the messages one by one
    start_time = time.time()
    down_stream_data = []
    fetch_message_ids_pipe = redis_client.pipeline()
    message_ids = []
    for message in batch:
        # simulate processing of message
        message_ids.append(message.id)
        fetch_message_ids_pipe.hgetall(message.id)
    
    message_ids_data = await fetch_message_ids_pipe.execute()
    await asyncio.sleep(0.05)
    logging.info(f"Finished fetching message ids took {(time.time()-start_time)*1000:.1f}ms for {len(batch)}")
    new_messages_pipeline = redis_client.pipeline()
    for message_id, result in zip(message_ids, message_ids_data):
        if result:
            down_stream_data.append(result)
        else:
            data = {
                "uuid" : message_id,
                "payload" : message.payload,
                "status" : Status.NOT_STARTED
            }
            new_messages_pipeline.hset(message_id, mapping=data)
            down_stream_data.append(data)
    asyncio.create_task(new_messages_pipeline.execute())
    # simulate sending the transformed message downstream
    asyncio.create_task(send_downstream(down_stream_data, kafka_producer))
    end_time = time.time()
    logging.info(f"Finished Processing message took {(end_time-start_time)*1000:.1f}ms for {len(batch)}")


async def send_downstream(data, kafka_producer:AIOKafkaProducer):
    # simulate sending data to downstream services or kafka
    asyncio.create_task(asyncio.sleep(0.5))

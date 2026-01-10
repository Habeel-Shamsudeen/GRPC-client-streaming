import logging
import os
from redis.asyncio import Redis
from aiokafka import AIOKafkaProducer

async def start_redis_client() -> Redis:
    try:
        redis = Redis.from_url(os.getenv("REDIS_URL","redis://redis:6379"))
        logging.info(f"Redis client connected: {os.getenv('REDIS_URL','redis://redis:6379')}")
        return redis
    except Exception as e:
        logging.error("Error connecting to Redis", exc_info=True)
        raise e

async def start_kafka_producer() -> AIOKafkaProducer:
    try:
        kafka_producer = AIOKafkaProducer(
            bootstrap_servers="kafka:9092",
            max_request_size=2_097_152,
            max_batch_size=2_097_152,
        )
        await kafka_producer.start()
        logging.info("Kafka producer started")
        return kafka_producer
    except Exception as e:
        logging.error("Error starting Kafka producer", exc_info=True)
        raise e
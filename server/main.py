import asyncio
import logging
from server.consumer import GrpcServer
from server.connections import start_redis_client, start_kafka_producer

logging.basicConfig(level=logging.INFO)

async def main():
    logging.info("Server starting")
    redis_client = await start_redis_client()
    kafka_producer = await start_kafka_producer()
    grpc_server = GrpcServer(
        port=50051,
        no_of_workers=1
    )
    try:
        await grpc_server.start_server()
    except KeyboardInterrupt:
        logging.info("Received interrupt signal")
        await grpc_server.stop()

if __name__ == "__main__":
    asyncio.run(main())
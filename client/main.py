import asyncio
from client.client import grpc_client
from client.producer import start_producer
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    await grpc_client.initialize()
    try:

        while True:
            await start_producer()
            await asyncio.sleep(5)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received, stopping producer")
        await grpc_client.cleanup()
        exit(0)
    

if __name__ == "__main__":
    asyncio.run(main())
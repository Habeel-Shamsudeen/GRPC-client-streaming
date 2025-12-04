import asyncio
from client.client import grpc_client
from client.producer import start_producer
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    await grpc_client.initialize()
    
    await start_producer()

if __name__ == "__main__":
    asyncio.run(main())
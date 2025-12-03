import asyncio
import logging
from server.consumer import GrpcServer


logging.basicConfig(level=logging.INFO)

async def main():
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
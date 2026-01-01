import grpc
from proto.generated.service_pb2_grpc import ConsumerServiceStub
import asyncio
import logging
import os

class GrpcClient:
    GRPC_SERVER = os.getenv('GRPC_SERVER', 'localhost:50051')

    def __init__(self, pool_size: int = 6):
        self.pool_size = pool_size
        self.channel = None
        self.stub = None
        self.streams = []
        self.current_index = 0
        self.lock = asyncio.Lock()
        self._initialized = False

    async def initialize(self):
        async with self.lock:
            if not self._initialized:
                try:
                    self.channel = grpc.aio.insecure_channel(
                        f"dns:///{self.GRPC_SERVER}", # dns resolves to ips (if multiple) of our server instances
                        options=[
                            ('grpc.keepalive_time_ms', 30000),
                            ('grpc.keepalive_timeout_ms', 5000),
                            ('grpc.max_send_message_length', 50 * 1024 * 1024),
                            ('grpc.keepalive_permit_without_calls', 1),
                            ('grpc.lb_policy_name', 'round_robin'), # Client side loadbalancing policy
                        ]
                    )

                    await self.channel.channel_ready()

                    self.stub = ConsumerServiceStub(self.channel)

                    for i in range(self.pool_size):
                        stream = self.stub.StreamWork()
                        self.streams.append(stream)
                    self._initialized = True
                    logging.info("Initialized gRPC client and streams")
                except Exception as e:
                    logging.error(f"Failed to initialize gRPC client: {e}")
                    await self.cleanup()
                    raise

    async def get_stream(self):
        if not self._initialized:
            await self.initialize()
        
        async with self.lock:
            stream = self.streams[self.current_index]
            self.current_index = (self.current_index + 1) % self.pool_size
        return stream

    async def cleanup(self):
        responses = []
        for stream in self.streams:
            try:
                await stream.done_writing()
                response = await stream
                responses.append(response)
            except:
                responses.append(None)
                pass
        self.streams = []
        
        if self.channel:
            try:
                await self.channel.close()
            except:
                pass
            self.channel = None
        
        self.stub = None
        self._initialized = False
        return responses

    async def reset_connection(self):
        async with self.lock:
            logging.info("Resetting gRPC connection")
            await self.cleanup()

    async def is_healthy(self):
        if not self._initialized or self.channel is None:
            return False
        
        try:
            state = self.channel.get_state(try_to_connect=False)
            return state not in (
                grpc.ChannelConnectivity.TRANSIENT_FAILURE,
                grpc.ChannelConnectivity.SHUTDOWN
            )
        except Exception as e:
            logging.warning(f"Error checking health: {e}")
            return False


grpc_client = GrpcClient()
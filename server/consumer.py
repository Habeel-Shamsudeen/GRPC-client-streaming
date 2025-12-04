import asyncio
import logging
import grpc.aio
import time
import proto.generated.service_pb2_grpc as service_pb2_grpc
from  proto.generated.service_pb2 import StreamResonse
from server.processor import process_message

class ConsumerService(service_pb2_grpc.ConsumerServiceServicer):
    def __init__(self):
        self.background_tasks = set()
        self.max_concurrent_tasks = 5
        self.priority_queue = asyncio.Queue(maxsize=15)
        self.normal_queue = asyncio.Queue(maxsize=25)

    async def StreamWork(self, request_iterator, context):
        message_received = 0
        message_dropped = 0

        async for message in request_iterator:
            try:
                if message.priority:
                    self.priority_queue.put_nowait(message)
                else:
                    self.normal_queue.put_nowait(message)
                message_received += 1
            except asyncio.QueueFull:
                queue_name = "priority" if message.priority else "normal"
                queue_size = self.priority_queue.qsize() if message.priority else self.normal_queue.qsize()
                logging.warning(f"{queue_name} queue FULL (size: {queue_size}) - dropping message {message.id[:8]}...")
                message_dropped += 1

        if message_dropped > 0:
            logging.warning(f"Stream Summary: {message_received} received, {message_dropped} DROPPED "
                          f"(Priority queue: {self.priority_queue.qsize()}, Normal queue: {self.normal_queue.qsize()})")
        else:
            logging.info(f"Stream Summary: {message_received} received, {message_dropped} dropped "
                        f"(Priority queue: {self.priority_queue.qsize()}, Normal queue: {self.normal_queue.qsize()})")
        
        return StreamResonse(
            success=True,
            message_received=message_received,
            message_dropped=message_dropped,
            message="Upload successful"
        )
    
    async def priority_worker(self):
        while True:
            try:
                first_item = await self.priority_queue.get()
                queue_size = self.priority_queue.qsize()

                # Dynamic batching ( faster batching )
                if queue_size < 3:
                    max_batch_size = 3
                    deadline_seconds = 0.5
                    
                elif queue_size < 7:
                    max_batch_size = 5
                    deadline_seconds = 0.8
                    
                else:
                    max_batch_size = 7
                    deadline_seconds = 1
                
                batch = [first_item]
                deadline = time.monotonic() + deadline_seconds

                while len(batch) < max_batch_size:
                    now = time.monotonic()
                    remaining = deadline - now

                    if remaining <= 0:
                        break
                    
                    try:
                        item = await asyncio.wait_for(self.priority_queue.get(),timeout=min(0.5,remaining))
                        batch.append(item)
                    except asyncio.TimeoutError:
                        break
                
                if batch:
                    if len(self.background_tasks) >= self.max_concurrent_tasks:
                        logging.warning(f"MAX CONCURRENT TASKS REACHED ({self.max_concurrent_tasks}) - waiting for task completion. "
                                      f"Priority queue: {self.priority_queue.qsize()}, "
                                      f"Normal queue: {self.normal_queue.qsize()}")
                        await asyncio.sleep(0.5)
                    
                    logging.info(f"Processing {len(batch)} priority messages (active tasks: {len(self.background_tasks)})")
                    task = asyncio.create_task(process_message(batch.copy()))
                    self.background_tasks.add(task)
                    task.add_done_callback(self.background_tasks.discard)
                    batch.clear()

            except Exception as e:
                logging.error(f"Worker error: {e}", exc_info=True)

    async def normal_worker(self):
        while True:
            try:
                first_item = await self.normal_queue.get()
                queue_size = self.normal_queue.qsize()

                # Slower batching
                if queue_size < 8:
                    max_batch_size = 5
                    deadline_seconds = 2
                    
                else:
                    max_batch_size = 8
                    deadline_seconds = 3
                
                batch = [first_item]
                deadline = time.monotonic() + deadline_seconds

                while len(batch) < max_batch_size:
                    now = time.monotonic()
                    remaining = deadline - now

                    if remaining <= 0:
                        break
                    
                    try:
                        item = await asyncio.wait_for(self.normal_queue.get(),timeout=min(1,remaining))
                        batch.append(item)
                    except asyncio.TimeoutError:
                        break
                
                if batch:
                    if len(self.background_tasks) >= self.max_concurrent_tasks:
                        logging.warning(f"MAX CONCURRENT TASKS REACHED ({self.max_concurrent_tasks}) - waiting for task completion. "
                                      f"Priority queue: {self.priority_queue.qsize()}, "
                                      f"Normal queue: {self.normal_queue.qsize()}")
                        await asyncio.sleep(1)
                    
                    logging.info(f"Processing {len(batch)} normal messages (active tasks: {len(self.background_tasks)})")
                    task = asyncio.create_task(process_message(batch.copy()))
                    self.background_tasks.add(task)
                    task.add_done_callback(self.background_tasks.discard)
                    batch.clear()

            except Exception as e:
                logging.error(f"Worker error: {e}", exc_info=True)



class GrpcServer:
    def __init__(self, port:int = 50051, no_of_workers:int =1):
        self.port = port
        self.no_of_workers = no_of_workers
        self.server = None

    async def start_server(self):
        logging.info(f"Starting GRPC server at port {self.port}")
        consumer_service = ConsumerService()
        for i in range(self.no_of_workers):
            asyncio.create_task(consumer_service.priority_worker(),name=f"Priority Worker {i}")
            asyncio.create_task(consumer_service.normal_worker(),name=f"Normal Worker {i}")
        self.server = grpc.aio.server(
            options=[
                ("grpc.max_concurrent_streams", 50),
                ("grpc.keepalive_time_ms", 30_000),
                ("grpc.keepalive_timeout_ms", 5_000),
            ]
        )
        service_pb2_grpc.add_ConsumerServiceServicer_to_server(consumer_service,self.server)
        self.server.add_insecure_port(f"[::]:{self.port}")
        await self.server.start()
        logging.info(f"gRPC server started on port {self.port}")
        await self.server.wait_for_termination()
    
    async def stop(self) -> None:
        if self.server:
            logging.info("Stopping gRPC server")
            await self.server.stop(grace=30)
            logging.info("gRPC server stopped")

        

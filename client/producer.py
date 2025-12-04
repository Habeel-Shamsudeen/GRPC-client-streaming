import logging
import asyncio
from proto.generated.data_model_pb2 import WorkItem
from client.client import grpc_client
from client.data import get_random_data
import grpc

MAX_MESSAGES = 300

async def start_producer():
    logging.info("Starting Producer")
    messages_sent = 0
    while True:
        if messages_sent >= MAX_MESSAGES:
            logging.info(f"{MAX_MESSAGES} messages sent")
            responses = await grpc_client.cleanup()
            break
        data = get_random_data()
        await asyncio.sleep(0.005)
        uploaded = await upload_to_stream(data)
        if uploaded:
            messages_sent += 1
        else:
            logging.warning("Data upload error")
    
    if responses:
        total_received = 0
        total_dropped = 0
        for i, response in enumerate(responses):
            if response:
                total_received += response.message_received
                total_dropped += response.message_dropped
                logging.info(f"Stream {i+1} response: success={response.success}, "
                           f"messages_received={response.message_received}, "
                           f"messages_dropped={response.message_dropped}, "
                           f"message='{response.message}'")
        logging.info(f"Total across all streams: {total_received} received, {total_dropped} dropped")
    else:
        logging.warning("No responses received from any stream")

async def upload_to_stream(data: WorkItem):
    try:
        if not grpc_client._initialized:
            logging.warning(f"Grpc client not initialized")
            await asyncio.wait_for(grpc_client.initialize(), timeout=0.1)

       
        stream = await grpc_client.get_stream()    
        if stream is None:
            raise RuntimeError("Stream is None after initialization")
            
        await stream.write(data)
        return True
    except asyncio.TimeoutError:
        logging.warning("Timeout waiting for gRPC connection/stream, dropping message")
        return False
        
    except (asyncio.InvalidStateError, grpc.aio.AioRpcError) as e:
        logging.warning(f"gRPC error: {str(e)}, dropping message")
        await grpc_client.reset_connection()
        return False
        
    except Exception as e:
        logging.warning(f"Unexpected error uploading to ingest: {str(e)}", exc_info=True)
        await grpc_client.reset_connection()
        return False
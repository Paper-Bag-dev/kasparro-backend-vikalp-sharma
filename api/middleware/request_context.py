import time
import uuid
from fastapi import Request

async def request_context_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    start = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start) * 1000
    
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-ms"] = str(round(duration_ms, 2))
    return response
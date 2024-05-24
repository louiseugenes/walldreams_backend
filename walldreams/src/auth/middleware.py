
from fastapi import Request, HTTPException, FastAPI
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.middleware.cors import CORSMiddleware

# Defina a chave API válida
VALID_API_KEYS = ["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"]

async def api_key_middleware(request: Request, call_next):
    api_key = request.headers.get("x-api-key")
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API key")

    response = await call_next(request)
    return response

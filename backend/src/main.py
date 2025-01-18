from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.endpoints import api_router

API_PORT = 8000

app = FastAPI(
    title="SPEECH RECOGNITION API",
    description="SPEECH RECOGNITION API",
    version="0.1.0",
)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=API_PORT)

from fastapi import APIRouter

from api.v1 import speech_recognition, webpage

api_router = APIRouter()

api_router.include_router(speech_recognition.router, prefix="/api/v1", tags=["v1/speech_recognition"])
api_router.include_router(webpage.router, tags=["webpage"])

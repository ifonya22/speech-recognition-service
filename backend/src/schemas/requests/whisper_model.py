from pydantic import BaseModel


class WhisperModelRequest(BaseModel):
    model: str
    filename: str

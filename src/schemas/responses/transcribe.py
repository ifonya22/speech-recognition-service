from pydantic import BaseModel


class TranscribeResponse(BaseModel):
    type: str
    text: str

import os

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydub import AudioSegment

from schemas.enums.model_list import ModelList
from schemas.requests.whisper_model import WhisperModelRequest
from schemas.responses.transcribe import TranscribeResponse
from services.speech_recognition.main import SpeechRecognitionService

router = APIRouter()


@router.websocket("/ws/transcribe")
async def websocket_transcribe(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connected")
    try:
        metadata = await websocket.receive_text()
        metadata = WhisperModelRequest.model_validate_json(metadata)
        model = metadata.model
        filename = metadata.filename
        print(model)

        file_path = os.path.join("tmp", filename)
        os.makedirs("tmp", exist_ok=True)

        file_bytes = await websocket.receive_bytes()
        with open(file_path, "wb") as f:
            f.write(file_bytes)

        srs = SpeechRecognitionService(model=model)

        audio = AudioSegment.from_file(file_path)
        segment_duration = 30 * 1000
        segments = [audio[i : i + segment_duration] for i in range(0, len(audio), segment_duration)]

        for i, segment in enumerate(segments):
            segment_path = os.path.join("tmp", f"segment_{i}.wav")
            segment.export(segment_path, format="wav")

            result_text = srs.transcribe(segment_path)
            text = TranscribeResponse(type="transcription", text=result_text).model_dump_json()
            await websocket.send_text(text)

        processing_complete = TranscribeResponse(type="done", text="Processing complete").model_dump_json()
        await websocket.send_text(processing_complete)
    except WebSocketDisconnect:
        await websocket.send_text("Connection closed.")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        _on_close(file_path, segments)
        await websocket.close()


def _on_close(file_path, segments):
    if os.path.exists(file_path):
        os.remove(file_path)
    for idx in range(len(segments)):
        segment_path = os.path.join("tmp", f"segment_{idx}.wav")
        if os.path.exists(segment_path):
            os.remove(segment_path)


@router.get("/models/required_vram")
def get_models_required_vram() -> dict:
    return ModelList.get_models_required_vram()

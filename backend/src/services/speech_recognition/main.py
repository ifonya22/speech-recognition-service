import whisper

from schemas.enums.model_list import ModelList


class SpeechRecognitionService:
    def __init__(self, model: ModelList):
        self.model = whisper.load_model(model)

    def transcribe(self, audio_file_path: str) -> str:
        audio = whisper.load_audio(audio_file_path)
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio, n_mels=self.model.dims.n_mels).to(self.model.device)

        _, probs = self.model.detect_language(mel)
        print(f"Detected language: {max(probs, key=probs.get)}")

        options = whisper.DecodingOptions()
        result = whisper.decode(self.model, mel, options)

        return result.text

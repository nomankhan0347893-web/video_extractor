from dotenv import load_dotenv
load_dotenv()   # MUST be before any core/ imports

from utils.audio_processor import process_input
from core.transcribe import transcribe_all

source = "https://www.youtube.com/watch?v=mPd_MokU6s0"
language = "hinglish"   # "english" → Whisper, "hinglish" → Sarvam



chunks = process_input(source)
transcript=transcribe_all(chunks,language=language)

print("\n++++ Transcription ++++")
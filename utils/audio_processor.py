import yt_dlp
from pydub import AudioSegment
import os

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_youtube_audio(url: str) -> str:
    # Use %(id)s instead of %(title)s -> avoids special characters (：, ?, /, etc.)
    # that break Windows filenames and trigger AV/rename locking issues.
    output_path = os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s")
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': output_path,
    'restrictfilenames': True,
    'retries': 10,
    'fragment_retries': 10,
    'nocheckcertificate': True,   # skip cert verification (helps w/ SSL-inspecting networks)
    'socket_timeout': 30,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
    'quiet': True,
}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        # After FFmpegExtractAudio postprocessing, the extension becomes .wav
        filename = os.path.splitext(filename)[0] + '.wav'

    return filename


def convert_to_wav(input_path: str) -> str:
    """Convert any video or audio file to wav format using pydub"""
    output_path = os.path.splitext(input_path)[0] + '_converted.wav'
    sound = AudioSegment.from_file(input_path)
    sound = sound.set_channels(1).set_frame_rate(16000)  # 16kHz
    sound.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path: str, chunk_minute: int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunks_ms = chunk_minute * 60 * 1000

    chunks = []
    for i, start in enumerate(range(0, len(audio), chunks_ms)):
        chunk = audio[start:start + chunks_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks

def process_input(source: str)->list:
    if source.startswith('http://') or source.startswith('https://'):
        print("Detected Youtube URl .Download audio...")
        wav_path = download_youtube_audio(source)
        wav_path = convert_to_wav(wav_path)
    else:
        print("detected local file .Converting to wav...")
        wav_path = convert_to_wav(source)


    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready - {len(chunks)} chunks created")
    return chunks

if __name__ == "__main__":
    process_input("")
from pathlib import Path
from typing import List, Tuple

import whisperx

def transcribe_and_align_with_whisperx(audio_path: Path, model, device: str = "cpu", lang: str = "en") -> List[Tuple[float, str]]:
    """Transcribe with Whisper then align with WhisperX; return list of (timestamp_seconds, text) by segment.

    Requires `whisperx` to be installed.
    """
    if whisperx is None:
        raise RuntimeError("whisperx is not installed. Install with: pip install whisperx")

    result = model.transcribe(str(audio_path), task="transcribe")

    # load align model
    align_model, metadata = whisperx.load_align_model(language_code=result["language"], device=device)

    # align the previously generated segments
    result_aligned = whisperx.align(result["segments"], align_model, metadata, str(audio_path), device)

    entries: List[Tuple[float, str]] = []
    for seg in result_aligned["segments"]:
        start = seg.get("start", 0.0)
        text = seg.get("text", "").strip()
        if text:
            entries.append((start, text))
    return entries

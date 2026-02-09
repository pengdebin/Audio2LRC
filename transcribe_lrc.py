import argparse
import os

from pathlib import Path
from lrc_generator import write_lrc_file
from demucs_separate import extract_vocals
from whisperx_align import transcribe_and_align_with_whisperx


def main():
    parser = argparse.ArgumentParser(description="Transcribe an English MP3 (or a directory) and generate bilingual LRC files (EN + ZH)")
    parser.add_argument("--input", "-i", default="input", help="Directory containing audio files to process")
    parser.add_argument("--ext", default=".mp3", help="Comma-separated audio file extensions to find in batch mode (e.g. .mp3,.wav)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing .lrc files")
    parser.add_argument("--model", default="large-v3", help="Whisper model to use (tiny, base, small, medium, large, large-v2, large-v3)")
    parser.add_argument("--sep", default="demucs", help="Source separation method to extract vocals before alignment")
    parser.add_argument("--aligner", default="whisperx", help="Alignment tool to use after transcription")
    parser.add_argument("--output", default = "output", help="Output LRC path")
    args = parser.parse_args()

    if not args.input:
        parser.error("Either an audio file or --input directory must be provided.")

    if args.aligner != "whisperx":
        print(f"Unsupported aligner: {args.aligner}.")
        return

    if args.sep != "demucs":
        print(f"Unsupported separation method: {args.sep}.")

    src = Path(args.input)
    if not src.exists():
        print(f"Input directory not found: {src}")
        return

    target = Path(args.output)
    if not target.exists():
        print(f"Output directory not found: {target}")
        return

    exts = []
    for e in args.ext.split(","):
        e = e.strip()
        if not e:
            continue
        if not e.startswith("."):
            e = "." + e
        exts.append(e.lower())

    files = [p for p in src.glob("*") if p.suffix.lower() in exts]
    files = sorted(files)
    if not files:
        print(f"No audio files found in {src} with extensions: {', '.join(exts)}")
        return

    print(f"Found {len(files)} files in {src}. Starting processing...")

    # Import heavy libs and load model now that we know there are files to process.
    print(f"Loading Whisper model '{args.model}' (this may take a while)...")
    try:
        import whisper
    except Exception as e:
        print("Error: 'whisper' is not available. Install with: pip install openai-whisper")
        print(f"Detailed error: {e}")
        return

    try:
        import torch
    except Exception:
        torch = None
        print("Warning: 'torch' not available; running on CPU only (if Whisper supports it).")

    model = whisper.load_model(args.model)

    # decide device
    if torch is not None and torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    for f in files:
        try:
            target_audio = f
            entries = []

            if args.sep == "demucs":
                try:
                    print(f"Extracting vocals for {f} ...")
                    vocals = extract_vocals(f, device=device)
                    print(f"Extracted vocals to {vocals}")
                    target_audio = vocals
                except Exception as e:
                    print(f"Vocal extraction failed for {f}: {e}. Skipping file.")
                    continue
            else:
                print(f"Unsupported separation method: {args.sep}. Skipping file: {f}")
                continue

            if args.aligner == "whisperx":
                try:
                    entries = transcribe_and_align_with_whisperx(target_audio, model, device=device)
                except Exception as e:
                    print(f"Alignment failed for {f}: {e}")
            else:
                print(f"Unsupported aligner: {args.aligner}. Skipping file: {f}")
                continue
            
            write_lrc_file(entries, target / f.with_suffix(".lrc").name)

        except Exception as e:
            print(f"Error processing {f}: {e}")

    print("Processing complete.")


if __name__ == "__main__":
    main()

import subprocess
from pathlib import Path
import shutil

def extract_vocals(input_path: Path, out_dir: Path = "temp", model: str = "htdemucs", device = "cpu") -> Path:
    """Use demucs CLI to extract the vocals stem. Returns path to vocals wav file.

    Requires `demucs` to be installed (pip install demucs).
    """
    input_path = Path(input_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Call demucs: `demucs --two-stems vocals -o out_dir input_path`
    cmd = ["demucs", "--mp3", "--two-stems", "vocals", "-d", device, "-o", str(out_dir), str(input_path)]
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        raise RuntimeError("demucs not found. Please install it: pip install demucs")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"demucs failed: {e}")

    # demucs output structure: out_dir/<model>/<basename>/vocals.wav
    # Since model name may vary, search for vocals.wav under out_dir
    vocals_files = list(out_dir.rglob("vocals.*"))
    if not vocals_files:
        raise RuntimeError(f"Failed to find extracted vocals in {out_dir}")

    # Prefer wav
    for p in vocals_files:
        if p.suffix.lower() == ".wav":
            return p
    return vocals_files[0]

from typing import List, Tuple

def format_timestamp(t: float) -> str:
    """Format seconds as [mm:ss.xx] (centiseconds)
    """
    total_centis = int(round(t * 100))
    minutes = total_centis // 6000
    seconds = (total_centis % 6000) // 100
    centis = total_centis % 100
    return f"[{minutes:02d}:{seconds:02d}.{centis:02d}]"


def write_lrc_file(entries: List[Tuple[float, str]], out_path: str):
    # Sort by timestamp and write: [mm:ss.xx]EN text
    entries_sorted = sorted(entries, key=lambda x: x[0])
    with open(out_path, "w", encoding="utf-8") as f:
        for ts, en in entries_sorted:
            tag = format_timestamp(ts)
            f.write(f"{tag}{en}\n")

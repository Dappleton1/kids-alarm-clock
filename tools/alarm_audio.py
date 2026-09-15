"""Shared audio helpers for the alarm clock cards.

DFPlayer Mini clones (YX5200) crackle on VBR / high-bitrate MP3s, so everything that goes on a card
passes through encode(): 128 kbps CBR, 44.1 kHz, stereo, loudness-normalised, no Xing/ID3 headers.
"""
import subprocess
from pathlib import Path

SOUNDS_ROOT = Path(__file__).resolve().parent.parent / "sounds"   # 001.mp3 .. 010.mp3 go here
MAX_TRACKS = 99          # /01/001.mp3 .. /01/099.mp3


def encode(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-i", str(src),
        "-vn", "-map", "0:a:0",          # drop embedded cover art (breaks the no-ID3 output)
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "2",
        "-c:a", "libmp3lame", "-b:a", "128k", "-map_metadata", "-1", "-id3v2_version", "0", "-write_xing", "0",
        str(dst),
    ], check=True)


def slot_name(n: int) -> str:
    return f"{n:03d}.mp3"


def write_tracks_md(folder: Path, title: str, rows: list[tuple[str, str, str]]) -> None:
    """rows = (file, HA name, detail). Copied onto the card by prep-card.ps1."""
    lines = [f"# {title}", "", "Folder `01` on the card, copied in this order. HA selector position N plays `/01/0NN.mp3`.", "",
             "| File | HA name | Detail |", "|------|---------|--------|"]
    lines += [f"| {f} | {name} | {detail} |" for f, name, detail in rows]
    (folder / "TRACKS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

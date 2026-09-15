#!/usr/bin/env python3
"""Re-encode the alarm sounds (001-010.mp3 in sounds/) into sounds/dfplayer/.
DFPlayer-safe settings, see alarm_audio.encode. Originals are left alone."""
from alarm_audio import SOUNDS_ROOT, encode

for src in sorted(SOUNDS_ROOT.glob("0[0-9][0-9].mp3")):
    encode(src, SOUNDS_ROOT / "dfplayer" / src.name)
    print("encoded", src.name)

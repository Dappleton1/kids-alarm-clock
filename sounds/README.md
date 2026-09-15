# Sounds

The MP3s are not in this repo (licence terms), but they are free and take five minutes to collect.
`docs/tracks.md` lists the ten we use with their Mixkit and Pixabay IDs. Any MP3s will do.

1. Save them here as `001.mp3` … `010.mp3` in the order you want on the clock.
2. `python tools/encode_tracks.py` writes DFPlayer-safe copies to `sounds/dfplayer/`
   (128 kbps CBR, 44.1 kHz, loudness-matched). **Do not skip this**: YX5200 clones crackle and
   stutter on the high-bitrate or variable-bitrate files most sites hand out. Needs `ffmpeg` on PATH.
3. Put the names in the same order in `esphome/tracks.yaml`, then `tools\prep-card.ps1 -Drive E`
   formats the microSD and copies them.

Short clips loop until dismissed, so a 4-second rooster works as well as a 3-minute song.

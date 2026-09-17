# Sounds

The MP3s are not in this repo (licence terms), but they are free and take five minutes to collect.
`docs/tracks.md` lists the ten we use with where to find them. Any MP3s will do, including your kid's
favourite songs. Short clips loop until dismissed, so a 4-second rooster works as well as a 3-minute song.

## 1. Collect

Save them here as `001.mp3` … `010.mp3` in the order you want on the clock.

## 2. Re-encode (do not skip)

YX5200 DFPlayer clones crackle and stutter on the high-bitrate or variable-bitrate files most sites hand
out. `python tools/encode_tracks.py` writes DFPlayer-safe copies (128 kbps CBR, 44.1 kHz, loudness-matched)
to `sounds/dfplayer/`. Needs Python and `ffmpeg` on PATH.

No Python? The equivalent ffmpeg command per file is:

```
ffmpeg -i 001.mp3 -vn -ac 1 -ar 44100 -b:a 128k -af loudnorm dfplayer/001.mp3
```

## 3. Put them on the card

**The DFPlayer plays tracks in the order they were written to the card, not by filename.** Select ten
files and drag them together and the copy order is whatever the OS felt like, so "track 3" may be the
farm animals. Always start from a freshly formatted card and copy one file at a time, 001 first.

- **Windows:** `tools\prep-card.ps1 -Drive E` formats the card FAT32 and copies them in order. Check the
  drive letter twice, it erases the card.
- **macOS / Linux, by hand:** format the card FAT32 (32 GB or smaller), create a folder named `01`, then
  copy `001.mp3`, `002.mp3`, … one at a time in a terminal:

  ```
  for f in dfplayer/0*.mp3; do cp "$f" /Volumes/ALARM/01/; done      # macOS
  for f in dfplayer/0*.mp3; do cp "$f" /media/$USER/ALARM/01/; done  # Linux
  ```

  Linux users can also run `fatsort` on the card afterwards to force directory order.

## 4. Tell the clock the names

The "Alarm Track" selector in Home Assistant lists the sounds by name; position N plays `/01/0NN.mp3`,
so the list order must match the card.

- **One-file firmware** (`alarm-clock-single.yaml`): edit the `options:` list under `select:` at the
  bottom of the file.
- **Packaged firmware**: edit `esphome/tracks.yaml`.

Re-flash after changing names. Changing the MP3s on the card alone does not need a re-flash as long as
the count and order still match the list.

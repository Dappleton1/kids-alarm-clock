"""Build esphome/alarm-clock-single.yaml: the whole clock in one file, no packages, no secrets.yaml.

Run from the repo root after any change to kids_alarm_common.yaml or tracks.yaml:
    python tools/build_single.py
"""
import io, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "esphome"
COMMON = (ROOT / "kids_alarm_common.yaml").read_text(encoding="utf-8")
TRACKS = (ROOT / "tracks.yaml").read_text(encoding="utf-8")
OUT = ROOT / "alarm-clock-single.yaml"

HEADER = '''# Kids Alarm Clock - ONE-FILE VERSION. Edit the "substitutions" block, then: esphome run alarm-clock-single.yaml
# Building a second clock: copy this file, change name / friendly_name / api_key.
# Source, wiring sheet, parts list, dashboard: https://github.com/Dappleton1/kids-alarm-clock
#
# GENERATED from kids_alarm_common.yaml + tracks.yaml by tools/build_single.py. Edit below the line only if
# you are not going to regenerate.

substitutions:
  # ---- Your settings -------------------------------------------------------------------------
  name: alarm-clock-1                  # lowercase, digits and dashes only. Becomes the hostname.
  friendly_name: Alarm Clock 1         # what Home Assistant shows
  wifi_ssid: "your-wifi"
  wifi_password: "your-wifi-password"
  ota_password: "pick-a-password"      # protects over-the-air updates
  ap_fallback_password: "pick-a-password"  # the clock's own hotspot if it can't find your WiFi
  # 32 random bytes as base64. Generate with `openssl rand -base64 32`, or in the ESPHome dashboard
  # (Secrets -> Generate). Home Assistant asks for this when it discovers the clock.
  api_key: "PASTE-A-BASE64-KEY-HERE"
  timezone: America/Edmonton           # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
  # ---- Hardware (leave alone for the parts in the BOM) ---------------------------------------
'''

API = '''
api:
  encryption:
    key: ${api_key}
'''


def top_level_blocks(text):
    """Split a yaml doc into (key, block_text) at top-level keys; leading comments stay with the first key."""
    parts = re.split(r"(?m)^(?=[a-z_]+:)", text)
    return parts


def main():
    body = COMMON
    # 1. lift the hardware substitutions out of the common file
    m = re.search(r"(?ms)^substitutions:\n(.*?)(?=^[a-z_]+:)", body)
    hw_subs = m.group(1)
    body = body[: m.start()] + body[m.end():]
    # 2. drop the common file's own header comment (the single file has its own)
    body = re.sub(r"\A(#.*\n)+\n?", "", body)
    # 3. secrets -> substitutions, timezone -> substitution
    body = re.sub(r"!secret (\w+)", r"${\1}", body)
    body = body.replace("timezone: America/Edmonton", "timezone: ${timezone}")
    assert "!secret" not in body and "!include" not in body
    # 4. tracks: strip the file comment, keep the select block
    tracks = re.sub(r"\A(#.*\n)+", "", TRACKS)
    out = HEADER + hw_subs.rstrip("\n") + "\n" + API + "\n" + body.rstrip("\n") + "\n\n" + tracks.rstrip("\n") + "\n"
    OUT.write_text(out, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(ROOT.parent)} ({out.count(chr(10))} lines)")


if __name__ == "__main__":
    main()

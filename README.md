# Kids' Alarm Clock — Home Assistant edition

**A bedside alarm clock for kids that parents control from their phone.** One button to stop it, a
touch strip to pick the wake-up sound, and every setting lives in Home Assistant: school-day time,
weekend time, holiday mode, skip-tomorrow, volume, the lot. Built from an ESP32, a 16x2 LCD, a
DFPlayer MP3 module and an arcade button, in a 3D-printed case.

> **Why this exists.** Our kids' alarm clocks kept going off on holidays and PD days, and there was no
> way to cancel or change them without walking into a dark bedroom at 6:55 AM. We wanted alarms we could
> set, skip or silence from the couch, that the kids could still stop themselves with one thump.
> Wake-up times are now a family setting, not a fight.

## What it does

- **Two alarm times**: school days and weekends. **Holiday mode** makes every day a weekend.
- **Skip next** swallows one ring and turns itself off. Set it from bed the night before a snow day.
- **Arcade button = stop.** No snooze on the clock. A tired six-year-old only needs one button.
- **Touch pads**: next wake-up sound with a 5-second preview, volume down, volume up. One pad spare.
- **Real sounds from a microSD**: ten ringers, or full songs, encoded so the DFPlayer plays them cleanly.
- **Runs on the clock, not the server.** Time comes from Home Assistant with an internet fallback, every
  setting is saved to flash. If Home Assistant is down at 7 AM the alarm still rings.
- **The screen shows the next ring**, not just today's setting: `Alarm 7:00a Mon` on a Sunday afternoon.
- **Backlight schedule** on the device: dark between lights-off and lights-on, any press lights it briefly.
- **Home Assistant dashboard** with one column per kid, plus optional notifications when a kid gets up
  or sleeps through.

## Parts, per clock

The case is cut for these exact footprints. Substitutes will fit the wiring but not the holes.

| Part | Exact fit | Notes | ~Cost |
|------|-----------|-------|------:|
| ESP32 dev board | **30-pin** ESP32 DevKit (WROOM-32), **USB-C** | The 38-pin board is too wide. A CP2102 USB bridge auto-resets for flashing; CH340 boards need the BOOT button held. | $5 |
| 16x2 LCD | LCD1602 with **PCF8574T** I2C backpack fitted, 5 V | PCF8574T = address 0x27 (firmware default). Blue or yellow-green, your call. | $4 |
| DFPlayer Mini | **YX5200** chip, standard DFPlayer Mini footprint | Held by one M3 bolt, so wider clones won't clamp. Clones vary, buy two. | $2 |
| microSD card | any, 32 GB or smaller | FAT32. | $5 |
| Speaker | **32 mm (1 inch) full-range, 8 Ω 3 W**, neodymium | Sold in pairs, one pair does two clocks. | $2 |
| Touch strip | **TTP224** "touch four button switch module" | The "V G 1 2 3 4" board. Most clones idle HIGH; firmware default handles it. | $2 |
| Arcade button | **Sanwa OBSF-24**, 24 mm snap-in | Hole is cut for the OBSF-24 flange. 30 mm and screw-ring buttons don't fit. Any colour. | $4 |
| USB-C panel mount | USB-C female to male **panel-mount extension, 0.3 m** | Male end into the ESP32, flange screws into the rear opening. | $3 |
| Power supply | any 5 V 2 A USB-C supply | The ESP32 plus LCD plus WiFi browns out on a 1 A adapter. | $6 |
| 1 kΩ resistor | | On the DFPlayer RX line. Required, kills the hiss. | |
| Passive piezo buzzer | optional | Click feedback on pad presses. | $1 |
| Rubber feet | 4 × 12 mm self-adhesive | Under the base. | $1 |
| Printed case | base + bezel from MakerWorld, see `case/` | ABS or PETG. | |

Fasteners per clock: **16 × M2 × 6 mm Phillips round-head self-tapping screws** (case) and **1 × M3 × 8 mm bolt**
(clamps the DFPlayer). Plus Dupont wires or a small perfboard, and a soldering iron for the button and speaker.

## Wiring

Print `docs/wiring-sheet.pdf` (or open `docs/wiring-sheet.html` in a browser): two pages, colour-coded schematic on one, pin table and
bench checks on the other. The short version:

```
 5V USB ──> ESP32 dev board
             ├─ VIN (5V) ─┬──> LCD backpack VCC       (LCD needs 5 V for contrast)
             │            └──> DFPlayer VCC
             ├─ 3V3 ──────> TTP224 V                  (3V3 so its outputs are 3.3 V)
             ├─ GND ──────┬──> LCD GND
             │            ├──> TTP224 G
             │            ├──> DFPlayer GND
             │            └──> piezo (−)
             ├─ GPIO21 ──> LCD SDA
             ├─ GPIO22 ──> LCD SCL
             ├─ GPIO17 ──[1k]──> DFPlayer RX          (ESP TX)
             ├─ GPIO16 <──────── DFPlayer TX          (ESP RX)
             ├─ GPIO25 ──> passive piezo (+)          (optional)
             ├─ GPIO27 <── TTP224 pad 1  = spare
             ├─ GPIO32 <── arcade button NO  = Stop   (COM -> GND, internal pull-up)
             ├─ GPIO33 <── TTP224 pad 2  = Next sound (5 s preview)
             ├─ GPIO34 <── TTP224 pad 3  = Volume down
             └─ GPIO35 <── TTP224 pad 4  = Volume up

 DFPlayer Mini    SPK_1 ──> speaker ──> SPK_2   (8 Ω, direct, no extra amp)
```

Gotchas we hit so you don't have to:

- **LCD on 3V3 = brownout reboot loop.** It must be on VIN / 5 V.
- **DFPlayer VCC on 5 V**, and the **1 kΩ on RX** is not optional on clone modules.
- **Touch pads all show ON when untouched?** Your TTP224 idles HIGH like ours. `btn_inverted: "true"`
  in the clock's yaml is the default; set it to `"false"` if your pads never trigger instead.
- **Crackly speaker?** Nine times out of ten it's the MP3, not the wiring. Run `tools/encode_tracks.py`.
- **LCD lit but blank?** Contrast pot on the backpack. **I2C not found?** Address 0x3F instead of 0x27.

## Build it

Step by step with photos in `docs/assembly.md`. In short: wire it on the bench, flash, test the button
and pads from the Home Assistant device page, then fit it in the case.

## Flash it

You need Home Assistant with the **ESPHome Device Builder** add-on (or `pip install esphome` on a PC).

**Easiest: the one-file firmware.** `esphome/alarm-clock-single.yaml` is the whole clock in a single file,
no secrets file, no includes. Also attached to the MakerWorld listing as a `.txt`.

1. Copy `alarm-clock-single.yaml` into your ESPHome config folder (or paste it into a new device in the dashboard).
2. Edit the `substitutions` block at the top: WiFi, an OTA password, a timezone, and an API key
   (`openssl rand -base64 32`, or let the ESPHome dashboard generate one).
3. Plug the ESP32 into USB, **Install** the file **Plug into this computer**. The first flash is over USB.
   Every later update is over WiFi.
4. Home Assistant will discover the clock. Add it, paste its API key, put it in the kid's room.
5. Second clock: copy the file, change `name`, `friendly_name` and `api_key`, flash again.

**Maintaining several clocks:** the packaged layout (`alarm-clock-1.yaml` + `kids_alarm_common.yaml` +
`tracks.yaml` + `secrets.yaml`) keeps one copy of the firmware for all of them. Copy `secrets.yaml.example`
to `secrets.yaml`, fill it in, install `alarm-clock-1.yaml`. The single file is generated from the
packaged one by `tools/build_single.py`, so edit the packaged files and regenerate.

## Sounds and the microSD card

See `sounds/README.md`. Ten free ringers are listed in `docs/tracks.md`, or use your kid's favourite
songs. The encode script and card-prep script make the DFPlayer happy.

## Home Assistant

- **Dashboard**: `ha/dashboard.yaml`, paste into a new dashboard's raw editor. Uses the Mushroom cards
  from HACS. Each column shows the next ring in plain words, on/skip/holiday chips, both times, the sound
  picker, a volume slider, stop and snooze buttons that appear only while ringing, and the backlight
  schedule. Rename the headings to your kids.
- **Helper**: a toggle called `school_holiday` drives holiday mode on both clocks through the first
  automation in `ha/automations.yaml`.
- **Notifications**: the other two automations tell your phone when a kid stops the alarm, and when
  one is still ringing after ten minutes. Point them at your own notify service.

## Entities per clock

`time` weekday_alarm, weekend_alarm, lights_off_at, lights_on_at · `switch` alarm_enabled, holiday_mode,
skip_next_alarm, backlight, auto_backlight · `number` snooze_minutes, max_ring_minutes, volume (3 to 30),
backlight_timeout · `select` alarm_track · `sensor` alarm_state (idle / ringing / snoozed) · `button`
test_alarm, snooze, dismiss · `binary_sensor` dismiss_button, pad_1 … pad_4.

## Behaviour details

- Weekday time rings Monday to Friday, weekend time Saturday and Sunday. Holiday mode: weekend time daily.
- Skip Next hides the next ring and shows the one after on the LCD, then clears itself.
- Snooze exists on the Home Assistant card for parents, not on the clock. Default 9 minutes.
- The track loops until stopped, or auto-stops after Max Ring Minutes (default 10).
- Volume floor is 3 so a kid can't mute it from the pads. The LCD shows the level for two seconds.
- Pad 2 steps through the sounds and previews five seconds of each. It's ignored while ringing.

## Files

| Path | What |
|------|------|
| `esphome/kids_alarm_common.yaml` | All the logic, shared by both clocks |
| `esphome/alarm-clock-1.yaml`, `-2.yaml` | Per-clock name and API key |
| `esphome/tracks.yaml` | The sound names in card order |
| `esphome/alarm-clock-single.yaml` | The whole clock in one file, easiest way to flash |
| `esphome/secrets.yaml.example` | What your secrets file needs (packaged layout only) |
| `ha/dashboard.yaml`, `ha/automations.yaml` | Home Assistant side |
| `docs/wiring-sheet.html` | Printable wiring sheet |
| `docs/assembly.md` | Build walkthrough |
| `docs/tracks.md` | The ten free ringers with sources |
| `tools/encode_tracks.py`, `tools/prep-card.ps1` | Make the MP3s DFPlayer-safe, write the card |
| `case/` | Where the printed parts come from |

## Ideas for v2

Stream songs straight from the server on an ESP32-S3 with an I2S amp, so no card swaps. Sleep sounds
through the same speaker. An OK-to-wake light. We're working on the first one.

MIT licence. Built in Alberta by a dad who was tired of 6:55 AM on a Saturday.

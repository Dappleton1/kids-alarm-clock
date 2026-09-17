# MakerWorld listing text

Paste into the model description. Swap the repo link once it's live.

---

## Kids' Alarm Clock that parents control from Home Assistant

Our kids' alarm clocks kept going off on holidays and PD days, and the only way to stop it was a walk
into a dark bedroom at 6:55 AM. So I built alarm clocks where every setting lives in Home Assistant.
Set school-day and weekend times from the couch, flip Holiday Mode for the whole break, hit Skip Next
the night before a snow day. The kids get one arcade button that stops it and a touch strip to pick
their wake-up sound. Wake-up times became a family setting instead of a morning argument.

**What's inside:** ESP32, 16x2 LCD, DFPlayer Mini MP3 module with a real speaker, TTP224 touch strip,
a Sanwa arcade button, all running ESPHome. About $30 in parts per clock.

**Features**
- School-day and weekend alarm times, Holiday Mode, Skip Next, all from your phone
- Arcade button = stop. No snooze for kids, snooze for parents on the dashboard
- Touch pads: next sound with a 5-second preview, volume down, volume up
- Any MP3 on the microSD: ten free ringers included in the docs, or their favourite songs
- Runs on the clock. If your server is down at 7 AM it still rings
- LCD shows the next ring ("Alarm 7:00a Mon"), backlight follows a bedtime schedule
- Home Assistant dashboard with one column per kid, plus "kid is up" and "slept through" notifications

**Print:** ABS or PETG. Base prints flat with no supports, bezel face down. Openings for the Sanwa OBSF-24 button,
the LCD, the touch strip, a microSD slot in the top so you can change songs without opening it, and USB-C
power out the back.

**Firmware, wiring sheet, dashboard and a step-by-step build guide:** https://github.com/Dappleton1/kids-alarm-clock
The firmware is one ESPHome file (attached here as .txt, rename to .yaml): fill in WiFi and a key at the top, flash, done.
The wiring sheet is a two-page PDF (docs/wiring-sheet.pdf) with a colour-coded schematic and a pin table.

**Parts list** (per clock, about $30). The case is cut for these exact parts, substitutes won't fit the holes:
- ESP32 DevKit, **30 pin**, **USB-C** (38-pin boards are too wide)
- LCD1602 16x2 with **PCF8574T** I2C backpack fitted, 5 V (blue or yellow-green)
- DFPlayer Mini, **YX5200** chip, standard footprint (buy two, clones vary)
- microSD card, 32 GB or smaller
- **32 mm (1 inch) full-range speaker, 8 Ω 3 W**, neodymium (sold in pairs)
- **TTP224** touch four-button module (the "V G 1 2 3 4" board)
- **Sanwa OBSF-24** arcade button, 24 mm snap-in, any colour
- **USB-C female to male panel-mount extension, 0.3 m**
- 5 V 2 A USB-C power supply
- 1 kΩ resistor, optional passive piezo
- Fasteners: **16 × M2 × 6 mm** Phillips round-head self-tapping screws, **1 × M3 × 8 mm** bolt for the DFPlayer

**Gotchas covered in the guide:** LCD must be on 5 V or the ESP brownouts, the 1 kΩ on the DFPlayer RX
line is required, some TTP224 clones idle HIGH (one line in the yaml fixes it), and crackly audio is
almost always the MP3 encoding, not the wiring. There's a script that fixes the files.

Built in Alberta, Canada. MIT licensed. Happy to answer build questions in the comments.

## Maker's Supply parts for the BOM tool

Only the fasteners and the power brick exist in Maker's Supply. Add these by product ID in the upload page's BOM
section; everything else (ESP32, LCD, DFPlayer, speaker, TTP224, Sanwa OBSF-24, USB-C panel-mount cable, microSD)
has no Maker's Supply equivalent and goes in as a custom part.

| Part | Maker's Supply item | Product ID | Qty per clock | Page |
|------|--------------------|------------|---------------|------|
| Case screws (16 x 2 x 6 mm) | BT2x6 BHCS Self Tapping Screw (20PCS) | AA128 | 1 pack | https://ca.store.bambulab.com/products/bt2-button-head-cap-self-tapping-screw-bhcs |
| Same, hex socket head instead of button head | BT2x6 SHCS Self Tapping Screw (20PCS) | AA093 | 1 pack | https://ca.store.bambulab.com/products/bt2-socket-head-cap-self-tapping-screws-shcs |
| DFPlayer clamp bolt (M3 x 8 mm) | M3x8 BHCS Machine Screw | AA058 | 1 pack | https://ca.store.bambulab.com/products/m3-button-head-cap-machine-screws-bhcs |
| 5 V 2 A supply | 20W Dual Port Fast Charger (USB-C 5 V 3 A) | B-XB006 | 1 | https://ca.store.bambulab.com/products/20w-dual-port-fast-charger-1pcs |

Bambu's screws are hex-socket, not Phillips; same thread and length, they fit the same holes.

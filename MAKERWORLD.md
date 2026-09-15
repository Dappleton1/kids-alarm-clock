# MakerWorld listing text

Paste into the model description. Swap the repo link once it's live.

---

## Kids' Alarm Clock that parents control from Home Assistant

Our kids' alarm clocks kept going off on holidays and PD days, and the only way to stop it was a walk
into a dark bedroom at 6:55 AM. So I built alarm clocks where every setting lives in Home Assistant.
Set school-day and weekend times from the couch, flip Holiday Mode for the whole break, hit Skip Next
the night before a snow day. The kids get one big arcade button that stops it and a touch strip to pick
their wake-up sound. Wake-up times became a family setting instead of a morning argument.

**What's inside:** ESP32, 16x2 LCD, DFPlayer Mini MP3 module with a real speaker, TTP224 touch strip,
a 60 mm arcade button, all running ESPHome. About $30 in parts per clock.

**Features**
- School-day and weekend alarm times, Holiday Mode, Skip Next, all from your phone
- Big button = stop. No snooze for kids, snooze for parents on the dashboard
- Touch pads: next sound with a 5-second preview, volume down, volume up
- Any MP3 on the microSD: ten free ringers included in the docs, or their favourite songs
- Runs on the clock. If your server is down at 7 AM it still rings
- LCD shows the next ring ("Alarm 7:00a Mon"), backlight follows a bedtime schedule
- Home Assistant dashboard with one column per kid, plus "kid is up" and "slept through" notifications

**Print:** ABS or PETG. Base prints flat with no supports, bezel face down. Openings for the 60 mm button,
the LCD, the touch strip, a side microSD slot so you can change songs without opening it, and USB-C
power out the back.

**Firmware, wiring sheet, dashboard and a step-by-step build guide:** REPO_LINK
The wiring sheet is a printable two-page PDF-style page with a colour-coded schematic and a pin table.

**Parts list** (per clock): ESP32 dev board · 16x2 LCD with I2C backpack · DFPlayer Mini · microSD ≤32 GB ·
8 Ω speaker · TTP224 4-pad touch module · 60 mm arcade button · 5 V 2 A USB supply · 1 kΩ resistor ·
optional passive piezo.

**Gotchas covered in the guide:** LCD must be on 5 V or the ESP brownouts, the 1 kΩ on the DFPlayer RX
line is required, some TTP224 clones idle HIGH (one line in the yaml fixes it), and crackly audio is
almost always the MP3 encoding, not the wiring. There's a script that fixes the files.

Built in Alberta, Canada. MIT licensed. Happy to answer build questions in the comments.

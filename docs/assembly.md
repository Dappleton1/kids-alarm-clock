# Assembly

Budget an evening for the first clock and an hour for the second. Bench-test before the case goes on.
Everything below assumes the printed parts from MakerWorld and the parts list in the README.

## 1. Bench wiring

Breadboard or loose dupont leads, nothing in the case yet.

1. **Power first, nothing else.** ESP32 on USB, confirm it boots (the onboard LED blinks).
2. **LCD.** Backpack VCC to **VIN**, not 3V3. GND, SDA to GPIO21, SCL to GPIO22. Power up: you should
   see the backlight. Blank boxes means turn the contrast pot on the back of the backpack.
3. **DFPlayer.** VCC to VIN, GND to GND. ESP GPIO17 through a **1 kΩ resistor** to DFPlayer RX. DFPlayer
   TX straight to ESP GPIO16. Speaker across SPK_1 and SPK_2. Card in. The player's blue LED lights
   while a track plays.
4. **Touch module.** TTP224 V to **3V3**, G to GND, outputs 1 to 4 to GPIO27, 33, 34, 35.
5. **Arcade button.** Microswitch COM to GND, NO to GPIO32. NC stays empty. If it has an LED, leave it.
6. **Piezo**, if you have one: + to GPIO25, − to GND.

Power the whole thing from a **2 A** adapter, not a laptop port. The LCD plus WiFi radio draws enough
to brown out a weak port and the ESP will reboot in a loop.

## 2. First flash

1. Copy the `esphome/` folder into ESPHome, make `secrets.yaml` from the example.
2. Dashboard, `alarm-clock-1.yaml`, Install, Plug into this computer. Pick the COM port.
   - CH340 boards without auto-reset: hold **BOOT** while it says "Connecting".
3. Watch the log. You want `Syncing time...` on the LCD, then the clock, then `Alarm 7:00a on`.

## 3. Bench checks, in this order

Each of these is visible on the clock's device page in Home Assistant once it's added.

| Check | What you should see |
|-------|--------------------|
| Nobody touching anything | All four pads **off**, dismiss button **off** |
| Touch pad 4 | Pad 4 flips on, LCD shows `Volume 19 of 30` |
| Touch pad 2 | Next sound name on the LCD, 5 seconds of audio |
| Press Test Alarm in HA | `** WAKE UP! **`, sound plays and loops |
| Thump the arcade button | Silence, back to `Alarm 7:00a on` |

- All four pads showing **on** with nobody touching them: the module idles HIGH, keep
  `btn_inverted: "true"`. Pads never triggering: set it to `"false"`.
- Dismiss button showing **on** at rest: wire is on NC not NO, or the microswitch is jammed.
- No sound, no blue LED: card not read. Re-format FAT32, folder `01`, files `001.mp3` up, copied in order.
- Crackle: encode the files with `tools/encode_tracks.py` before blaming the wiring.

## 4. Into the case

1. Solder the speaker and arcade button leads, heat-shrink the button terminals.
2. Mount the LCD in the front bezel, the touch strip below it, the arcade button on top.
3. The DFPlayer and ESP sit on the base. Keep the DFPlayer's speaker leads short and away from the
   touch module's inputs.
4. Clamp the DFPlayer with the M3x8 bolt so its microSD slot lines up with the opening in the top,
   so you can change songs without opening the case.
5. USB power out the back. Close it up.

## 5. Home Assistant

1. Settings, Devices, the clock appears as discovered. Add it, paste its API key, assign the room.
2. Create the toggle helper `school_holiday`.
3. New dashboard, raw editor, paste `ha/dashboard.yaml`. Rename the headings.
4. Add the automations from `ha/automations.yaml`, pointing the two notify actions at your phone.
5. Set the two times, pick a sound, set the volume. Press the Ring button once so the kid hears it in
   daylight and knows what the big button does.

Second clock: same steps with `alarm-clock-2.yaml`.

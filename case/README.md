# Case

The printed parts are on MakerWorld (link on the top-level README once the listing is up); firmware and docs at https://github.com/Dappleton1/kids-alarm-clock.
Printed in ABS on a Bambu Lab; PETG is fine too. No supports on the base, the bezel prints face down.

## Exact-fit parts

The openings are cut for specific boards. See the parts table in the top-level README for the full list.

| Opening | Cut for |
|---------|---------|
| Top button | Sanwa OBSF-24 snap-in flange (24 mm). Not 30 mm, not screw-ring buttons. |
| Front bezel | LCD1602 with PCF8574T backpack fitted, and the TTP224 four-pad module |
| Main board | 30-pin ESP32 DevKit. The 38-pin board is too wide. |
| Side grille | 32 mm (1 inch) full-range driver |
| Rear | USB-C panel-mount extension flange (female to male, 0.3 m). The ESP32's own USB-C plugs into the male end. |
| Top slot | DFPlayer Mini microSD, so songs swap without opening the case |

## Fasteners, per clock

- 16 × M2 × 6 mm Phillips round-head self-tapping screws (case)
- 1 × M3 × 8 mm bolt, clamps the DFPlayer Mini snug in its pocket
- 4 × 12 mm self-adhesive rubber feet under the base

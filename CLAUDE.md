# CLAUDE.md

Guidance for working in this repo.

## What this is

Firmware for an e-ink conference badge: a **Pimoroni Badger 2040** (RP2040 + 296×128
1-bit e-paper display) running **CircuitPython**. The badge shows the wearer's name,
job title, and a company logo, plus three interactive modes triggered by the front
buttons: Emoji Party, Dad Joke, and Cat Fact. After 2 minutes of inactivity it returns
to badge mode and deep-sleeps until the UP button wakes it.

This is not a packaged application — there is no build step, no test suite, and no
package manager. The "repo" is a mirror of the files that live on the badge's `CIRCUITPY`
USB drive. Deploying = copying files onto that drive.

## Hardware / runtime facts

- Board: `pimoroni_badger2040` (RP2040). Board ID is in `boot_out.txt`.
- Display: 296×128 monochrome e-paper, driven via `board.DISPLAY`. Code sets
  `display.rotation = 270` so it renders landscape.
- Buttons used: `SW_A`, `SW_B`, `SW_C` (mode buttons, pull-down + `Debouncer`),
  `SW_DOWN` (back to badge), `SW_UP` (reserved as the deep-sleep wake pin).
- e-paper refresh is **slow and rate-limited**. `display.refresh()` raises if called
  too soon; the code catches that and prints "Too soon, please try again." Expect a
  visible full-screen flash on every update — this is normal for e-ink.
- **Memory is tight.** Display groups for each mode are appended/removed on every screen
  change and `gc.collect()` is called aggressively. When adding UI, follow the existing
  append-then-remove pattern in `clear_ui()` rather than keeping everything resident.

## CircuitPython version

- The badge runs CircuitPython **10.x** (see `boot_out.txt` on the device for the exact
  build). The libraries in `lib/` must come from the **matching** CircuitPython bundle
  (10.x-mpy). Mixing bundle major versions with the firmware will fail to import.
- **API note:** `display.show(group)` was removed in CircuitPython 9. This code uses the
  current API, `display.root_group = group`. Do not reintroduce `display.show()`.

## Files

| File | Purpose |
|------|---------|
| `code.py` | The entire app. CircuitPython auto-runs `code.py` on boot. |
| `catfacts` | One cat fact per line. Plain text, no delimiters. |
| `dadjokes` | One joke per line, `question < answer` format (`<` separates Q and A). |
| `harness.bmp` | Company wordmark bitmap (1-bit, 141×30), shown top of badge. |
| `harness_mark.bmp` | Company logo mark (1-bit, 82×82), shown left of badge. |
| `canary.bmp` | Canary bird icon (1-bit, 46×46), shown bottom-right of badge. |
| `*.bdf` | Bitmap fonts. `luRS19`/`luRS14`/`luIS14` = Lucida (regular/italic sizes); `streamline_all` = icon/emoji glyphs; `emoticons` = smiley set (currently unused). |
| `examples.py` | Scratch snippets for shapes/emoji. Not loaded at runtime. |
| `boot_out.txt` | Written by CircuitPython at boot; records firmware version + board. Read-only reference. |
| `lib/` | Adafruit libraries copied from the CircuitPython bundle (see below). |
| `settings.toml` | CircuitPython env/secrets file. Currently empty. |

`code.py` personalization lives at the top of the file: `username`, `jobtitle`, and an
optional `fonticon` (a glyph from `streamline_all.bdf`; comment it out for a random icon).

## Dependencies (`lib/`)

Managed with **circup** (`pip install --upgrade circup`). The board must be plugged in
and mounted as `CIRCUITPY`. From the repo or anywhere:

```sh
circup list                 # show installed vs. outdated libs on the device
circup update --all         # update every installed lib to the current bundle
circup install <name>       # add a library
circup freeze               # list what's installed on the device
```

If circup can't auto-detect the drive, pass it explicitly: `circup --path D:\ ...`
(the drive letter is whatever `CIRCUITPY` mounts as).

Libraries this project imports: `adafruit_bitmap_font`, `adafruit_display_text`,
`adafruit_display_shapes`, `adafruit_debouncer` (+ its dep `adafruit_ticks`).

## Deploying a change

There is no build. To run new code, copy it onto the `CIRCUITPY` drive:

```sh
cp code.py /d/            # or the drive letter CIRCUITPY mounted as
```

CircuitPython restarts and runs the new `code.py` automatically on file save. To watch
output / tracebacks, open the USB serial REPL (e.g. `screen`, PuTTY, or the Mu editor).
Keep this repo and the drive in sync — the drive is the source of truth for what's
actually running.

## Updating firmware (rare)

1. Back up the whole `CIRCUITPY` drive first — flashing **erases** it.
2. Put the board in bootloader mode: it remounts as `RPI-RP2`.
3. Copy the CircuitPython `.uf2` for `pimoroni_badger2040` onto `RPI-RP2`; it flashes and
   reboots to a blank `CIRCUITPY`.
4. Restore `code.py`, fonts, `.bmp`s, `catfacts`, `dadjokes`, then `circup install` the
   libraries from the bundle matching the new firmware major version.

## Gotchas

- Test on the physical badge — there is no emulator, and the e-paper timing/memory
  behavior only shows up on real hardware.
- The two logo bitmaps must be **1-bit** BMPs at their expected pixel sizes, or
  `OnDiskBitmap` placement will be wrong. Regenerate at the same dimensions when
  rebranding. Rendering a wordmark to a 1-bit BMP (as `harness.bmp` was, from the
  Inter font) is far lighter on RAM than shipping another `.bdf` font.
- Font files are large; adding more `.bdf`s eats both flash and RAM.

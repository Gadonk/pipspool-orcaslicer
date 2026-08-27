# PipSpool

![PipSpool logo](assets/pipspool_logo.png)

**Spoolman synchronization plugin for OrcaSlicer**

PipSpool synchronizes active [Spoolman](https://github.com/Donkie/Spoolman) spools into OrcaSlicer filament presets. It is maintained by **Donko** and designed for printers where Klipper, Moonraker, and Happy Hare handle real-time filament usage.

## PipSpool 2.0 development features

- Imports active Spoolman spools as OrcaSlicer filament presets.
- Updates existing presets by stable Spoolman spool ID instead of creating duplicates after renames.
- Preserves Orca-specific profile adjustments during synchronization.
- Writes the correct `SET_SPOOL_ID ID=<id>` command into managed filament start G-code.
- Uses Spoolman's nozzle and bed temperatures for Orca's nozzle and all supported build-plate temperature fields.
- Opens a simple settings dialog when the plugin activates.
- Includes an offline embedded PipSpool logo and a connection test.
- Does not deduct filament during G-code export.
- Does not create duplicate `- SpoolMan` process profiles.
- Includes focused cleanup for artifacts created by older bridge versions.
- Uses a clean implementation built around public OrcaSlicer, Spoolman, and Moonraker interfaces.

## Compatibility

The working development build is confirmed on OrcaSlicer 2.5.0 nightly build `142c63ab` on Windows with Spoolman, Klipper, Moonraker, and Happy Hare.

OrcaSlicer's Python plugin API is experimental. Test development builds before production use.

## Development installation

1. Download [`pipspool_v2_0_5_dev.py`](pipspool_v2_0_5_dev.py).
2. Open **File → Plugins** in OrcaSlicer.
3. Choose **Install local plugin** and select the Python file.
4. Activate PipSpool. Its settings dialog opens automatically.
5. Confirm the Spoolman URL, use **Test connection**, and save.
6. Run **Sync Spoolman Profiles**, then restart OrcaSlicer to load changed presets.

Do not enable PipSpool and the older Spoolman Bridge plugin simultaneously.

## Release safety

The public source uses `http://localhost:7912`. Set the address of your Spoolman server in the PipSpool settings dialog. GitHub Actions rejects private development addresses.

## Provenance and license

PipSpool 2.0 is a clean architectural replacement for the inherited 1.1.x development line. Its documented comparison found no substantial matching algorithmic block. See [PROVENANCE.md](PROVENANCE.md) for the implementation boundaries, comparison results, and tests.

The repository currently retains the earlier MIT notice while the maintainer completes the final licensing reassessment. Historical inherited builds are not distributed from this repository.

The PipSpool logo is original artwork based on Donko's Pip character and an independently designed filament-spool/database motif. It does not reproduce the official Spoolman logo or wordmark.

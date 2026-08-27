# PipSpool

![PipSpool logo](assets/pipspool_logo.png)

**Spoolman synchronization plugin for OrcaSlicer**

PipSpool synchronizes active [Spoolman](https://github.com/Donkie/Spoolman) spools into OrcaSlicer filament presets. It is maintained by **Donko** and designed for printers where Klipper, Moonraker, and Happy Hare handle real-time filament usage.

## Features

- Imports active Spoolman spools as OrcaSlicer filament presets.
- Removes generated Orca profiles when their spools are archived in Spoolman.
- Names profiles with the spool ID first, for example `(#42) Manufacturer Filament - PipSpool`.
- Updates existing presets by stable Spoolman spool ID instead of creating duplicates after renames.
- Preserves Orca-specific profile adjustments during synchronization.
- Writes the correct `SET_SPOOL_ID ID=<id>` command into managed filament start G-code.
- Uses Spoolman's nozzle and bed temperatures for Orca's nozzle and all supported build-plate temperature fields.
- Opens a simple settings dialog when the plugin activates.
- Includes an offline embedded PipSpool logo and a connection test.
- Does not deduct filament during G-code export.
- Does not create duplicate `- SpoolMan` process profiles.
- Includes focused cleanup for artifacts created by older bridge versions.

## Compatibility

PipSpool 2.0.6 is confirmed on OrcaSlicer 2.5.0 nightly build `142c63ab` on Windows x86-64 with Spoolman, Klipper, Moonraker, and Happy Hare.

OrcaSlicer's Python plugin API is new and may change in future OrcaSlicer builds.

## Installation

1. Download [`pipspool_v2_0_6_win_x86_64.py`](pipspool_v2_0_6_win_x86_64.py).
2. Open **File → Plugins** in OrcaSlicer.
3. Choose **Install local plugin** and select the Python file.
4. Activate PipSpool. Its settings dialog opens automatically.
5. Enter the address of your Spoolman server, use **Test connection**, and save.
6. Run **Sync Spoolman Profiles**, then restart OrcaSlicer to load changed presets.

Do not enable PipSpool and the older Spoolman Bridge plugin simultaneously.

## Release safety

The public source defaults to `http://localhost:7912`. Configure the actual Spoolman server address in PipSpool Settings. GitHub Actions rejects private development addresses.

## License

PipSpool is maintained and copyrighted by **Donko** and distributed under the [MIT License](LICENSE).

The PipSpool logo is original artwork based on Donko's Pip character and an independently designed filament-spool/database motif. It does not reproduce the official Spoolman logo or wordmark.

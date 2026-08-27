# PipSpool

![PipSpool logo](assets/pipspool_logo.png)

**Spoolman synchronization plugin for OrcaSlicer**

PipSpool synchronizes active [Spoolman](https://github.com/Donkie/Spoolman) spools into OrcaSlicer filament presets. It is maintained by **Donko** and designed for printers where Klipper, Moonraker, and Happy Hare handle real-time filament usage.

## Current development features

- Imports active Spoolman spools as OrcaSlicer filament presets.
- Updates existing presets by stable Spoolman spool ID instead of creating duplicates after renames.
- Preserves Orca-specific profile adjustments during synchronization.
- Writes the correct `SET_SPOOL_ID ID=<id>` command into managed filament start G-code.
- Does not deduct filament during G-code export.
- Does not create duplicate `- SpoolMan` process profiles.
- Includes focused cleanup for artifacts created by older bridge versions.

## Compatibility

Development currently targets OrcaSlicer 2.5.0 nightly build `142c63ab` on Windows with Spoolman, Klipper, Moonraker, and Happy Hare.

OrcaSlicer's Python plugin API is experimental. Test development builds before production use.

## Development installation

1. Download the latest versioned `pipspool_*_dev.py` file.
2. Open **File → Plugins** in OrcaSlicer.
3. Choose **Install local plugin** and select the Python file.
4. Activate PipSpool and restart OrcaSlicer when requested.
5. Configure the Spoolman URL and run **Sync Spoolman Profiles**.

Do not enable PipSpool and the older Spoolman Bridge plugin simultaneously.

## Release safety

Development builds may use a private development Spoolman address. Publishable releases must restore the default to `http://localhost:7912`.

## License and attribution

PipSpool is derived from Zao Soula's [OrcaSlicer Spoolman Bridge](https://github.com/zaosoula/orcaslicer-plugin-spoolman), licensed under the MIT License. The original copyright and permission notice are retained in [LICENSE](LICENSE).

The PipSpool logo is original artwork based on Donko's Pip character and an independently designed filament-spool/database motif. It does not reproduce the official Spoolman logo or wordmark.

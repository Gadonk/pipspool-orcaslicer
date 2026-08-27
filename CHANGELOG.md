# Changelog

All notable PipSpool changes are documented here.

## [2.0.5-dev] - 2026-08-27

- Published the working clean 2.0 development build confirmed on OrcaSlicer nightly `142c63ab` for Windows.
- Corrected dependency metadata for Orca's bundled installer.
- Added a simple settings dialog with connection testing and automatic opening on activation.
- Embedded the original PipSpool logo directly in the single-file plugin.
- Added stable spool-ID preset updating and rename migration.
- Added managed `SET_SPOOL_ID ID=<id>` filament start G-code.
- Corrected Spoolman temperature fields to `settings_extruder_temp` and `settings_bed_temp`.
- Applied Spoolman temperatures to Orca's nozzle and all supported build-plate temperature fields.
- Removed Orca-side filament deduction and duplicate process-profile generation.
- Added focused cleanup for legacy pipeline profiles and references.
- Expanded automated verification to eight behavior and architecture tests.

## [1.1.4-dev] - 2026-08-27

- Rebranded the maintained fork as PipSpool.
- Added an original PipSpool logo.
- Added stable spool-ID preset updating and rename migration.
- Added managed `SET_SPOOL_ID ID=<id>` filament start G-code.
- Removed Orca-side filament deduction.
- Removed duplicate SpoolMan process-profile generation.
- Added focused cleanup for legacy pipeline profiles and references.
- Centralized the development Spoolman URL with a release reminder.

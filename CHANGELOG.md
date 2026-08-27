# Changelog

All notable PipSpool changes are documented here.

## [2.0.7] - 2026-08-27

- Added optional per-spool Start G-code synchronized from Spoolman.
- Automatically creates the spool-level Spoolman `start_gcode` text field when needed.
- Falls back to the managed `SET_SPOOL_ID ID=<id>` command when custom Start G-code is blank.
- Preserves unrelated OrcaSlicer filament Start G-code while updating PipSpool's managed block.
- Added compatibility with JSON-encoded and double-encoded Spoolman extra-field values.
- Changed automatic setup so the settings window opens only when no valid saved configuration exists.
- Expanded automated verification to 17 behavior and architecture tests.

## [2.0.6] - 2026-08-27

- Released the first stable PipSpool improvement build for Windows x86-64.
- Adopted Orca Cloud's target-platform filename convention.
- Removed development markers from the release filename and plugin metadata.
- Removed generated Orca profiles when their Spoolman spools are archived.
- Added a defensive client-side archive check in addition to `allow_archived=false`.
- Moved the spool number to the beginning of profile names for spool-ID sorting.
- Confirmed all ten behavior and architecture tests pass.
- Added trusted GitHub Release publishing to Orca Cloud with OIDC and release-safety checks.

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

- Rebranded the maintained plugin as PipSpool.
- Added an original PipSpool logo.
- Added stable spool-ID preset updating and rename migration.
- Added managed `SET_SPOOL_ID ID=<id>` filament start G-code.
- Removed Orca-side filament deduction.
- Removed duplicate process-profile generation.
- Added focused cleanup for legacy pipeline profiles and references.
- Centralized the development Spoolman URL with a release reminder.

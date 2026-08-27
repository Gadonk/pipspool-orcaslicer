# Changelog

All notable PipSpool changes are documented here.

## [2.2.0] - 2026-08-27

- Added an integrated PipSpool page to OrcaSlicer's main interface.
- Added clear green/red connection artwork with Happy and Sad Pip states.
- Added live connection status, active-spool count, and a searchable spool table.
- Added **Refresh** and **Synchronize now** actions with an immediate synchronization report.
- Added page controls for Filament, Cooling, and Multimaterial field selection.
- Added deliberate cleanup controls for obsolete unselected PipSpool fields.
- Rendered initial data directly from Python so the page remains informative before its live bridge initializes.
- Repaired the page's generated JavaScript newline escaping, which had prevented all interactive controls from loading.
- Reworked the page script for compatibility with OrcaSlicer's Windows webview backend.
- Confirmed all 33 behavior, dashboard, configuration, and architecture tests pass.

## [2.1.0] - 2026-08-27

- Added Orca-master synchronization for selected Filament, Cooling, and Multimaterial settings.
- Added a grouped opt-in Plugin configuration checklist; advanced fields are disabled by default.
- Creates, initializes, and reads only the advanced fields selected by the user.
- Added an explicit warned option to remove unselected PipSpool fields and their values from Spoolman.
- Uses exact material-type inheritance so PLA, ASA, composites, and other families do not cross.
- Retains Spoolman text-field values through their required encoded round trip.
- Reset Filament Settings now follows the most recently synchronized field selection.
- Confirmed all 26 behavior, configuration, and architecture tests pass.

## [2.0.8] - 2026-08-27

- Moved the filament material immediately after the spool number in generated profile names.
- Changed the remaining name order to filament name, manufacturer, and PipSpool.
- Avoided duplicate material text when the Spoolman filament name already begins with its material.
- Existing profiles continue to be renamed by stable spool ID without creating duplicates.
- Confirmed all 17 behavior and architecture tests pass.

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

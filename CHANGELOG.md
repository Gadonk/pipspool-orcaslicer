# Changelog

All notable PipSpool changes are documented here.

## [2.2.17] - 2026-10-23

### 2.2.17

- Reduced embedded artwork size by about 91% while retaining full-resolution wallpapers and transparent, appropriately sized Pip artwork. The complete five-platform payload is now about 27 MB instead of 294 MB, addressing the upload-size failure affecting 2.2.16.
- Fixed gate/toolhead cards retaining blue Classic styling when another theme is selected. Loaded and empty cards now follow built-in and custom palettes, including their labels and borders.
- Fixed unreadable gate-material and printer labels in Light theme; empty-slot labels remain readable without fading the entire card.
- Preserved filament-path colours, remaining-weight gauges, low-stock indicators and problem borders when switching themes. Classic restores its original appearance.
- Updated the theme guide with the palette keys controlling loaded and empty toolhead cards.
- Added aggregate upload-size checks before draft creation and Orca Cloud publishing, with headroom below the release limit.
- Passed 198 automated tests and populated-dashboard browser checks across all built-in themes and a custom palette. Spool identification, synchronization and shared-Filament conflict protection are unchanged.
- Further sync-back reports in existing profiles remain under investigation in [#17](https://github.com/Gadonk/pipspool-orcaslicer/issues/17); this update does not claim to fix that follow-up.
- Included Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel and macOS Apple Silicon packages.

### Included from 2.2.16

These features are included here because the 2.2.16 upload did not reach Orca Cloud:

- Saved dashboard theme selector beside Feedback, with Classic, Light, Forest, rich-red Rosewood and Bonus Treat.
- Custom JSON palettes and optional local PNG, JPEG or WebP wallpapers, with colours and wallpaper settings together in one JSON file.
- Editable starter theme and a theme guide covering default paths on all five supported platforms, image limits and sharing instructions.
- Improved dashboard colour coverage for dropdowns, selected filters, advanced-field tabs and reports; the active-spool table fills its card's scrolling area.
- Theme changes remain separate from spool identity, synchronization and shared-Filament conflict handling. Custom themes do not execute code or download remote images.

Full history: https://github.com/Gadonk/pipspool-orcaslicer/blob/main/CHANGELOG.md

## [2.2.16] - 2026-10-23

- Added a saved dashboard theme selector beside Feedback, with Classic, Light, Forest, rich-red Rosewood and a Bonus Treat appearance.
- Added custom JSON palettes and optional local PNG, JPEG or WebP wallpapers. Colours and wallpaper settings share one JSON file; custom options show the filename for easy editing.
- Included an editable starter theme and a GitHub-ready theme guide with default installation paths for all five supported platforms, image limits and sharing instructions.
- Improved dashboard colour coverage and readable controls, including dropdowns, selected filters, advanced-field tabs and reports. The active-spool table now fills its card's available scrolling area.
- Kept theme changes separate from spool identification, profile synchronization and shared-Filament conflict handling. Custom theme data never executes code or downloads remote images.
- Passed 195 automated tests, rendered-dashboard checks and text-contrast checks. All five stable packages share the same verified source and numeric 2.2.16 metadata.
- Known issue: further reports of sync-back failures in some existing profiles are being investigated in [#17](https://github.com/Gadonk/pipspool-orcaslicer/issues/17); this theme release does not claim to fix that follow-up.
- Included Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel and macOS Apple Silicon packages.

## [2.2.15] - 2026-10-23

- Fixed a synchronization precedence defect investigated for issue #17: live parent-preset defaults no longer mask explicit values saved in an individual spool profile; matching live spool-profile values remain authoritative.
- Preserved per-field shared-Filament reconciliation and conflicting sibling edits. Conflicted advanced nozzle/plate temperatures retain their original override or inheritance instead of falling back to ordinary generated Spoolman temperatures.
- Fixed the manual synchronization action's restart notice to use direction-aware tracking: pure exports need no restart, while sibling imports or other profile changes can still require one.
- Passed 117 private regression tests and 44 focused tests, including multi-field edits, exact live-profile matching, sibling conflicts, temperature preservation and restart behavior. Reporter-specific manual OrcaSlicer validation remains pending.
- Included matching Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel and macOS Apple Silicon packages.

## [2.2.14] - 2026-10-20

- Added a configurable spool-ID command in PipSpool Settings for issue #16, keeping `SET_ACTIVE_SPOOL ID={spool_id}` as the default.
- Replaced `{spool_id}` with each physical Spoolman spool ID when generating profiles; templates are validated as single-line commands with exactly one spool-ID placeholder.
- Added an example preview, reset-to-default control and durable command preferences through Orca configuration and the existing settings mirror.
- Added printer/firmware examples for Klipper/Moonraker, issue-reported Anycubic GoKlipper M555 bridges, custom macro aliases, and setups where spool-ID injection should be disabled.
- Retained per-spool custom Start G-code overrides and added literal `{spool_id}` substitution while preserving other Orca/Klipper expressions.
- Preserved the existing dashboard off switch, including removal of configured managed commands while retaining unrelated Start G-code. Changing the template does not re-enable disabled output.
- Applied managed spool identity after advanced/shared Start G-code so sibling data cannot restore the wrong spool ID or defeat the off switch.
- Passed 117 regression tests and 39 focused tests; validated Settings preview/reset/save/reload behavior and all five stable packages for Python syntax, numeric metadata, matching contents and the localhost default.
- Included Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel and macOS Apple Silicon packages.

## [2.2.13] - 2026-10-20

- Added a per-spool **Sync** action. When advanced fields are selected, the action reconciles the selected spool's shared-Filament group with existing sibling conflict protection; unrelated Filaments and archived-profile cleanup remain outside its scope.
- Added configurable profile naming for issue #15, with a live example, reset control and durable saved preferences. The default remains `(#42) PETG Galaxy Black - Prusament - PipSpool`.
- Kept one mandatory spool-ID marker and the managed suffix, prevented descriptive text from introducing another identity, and strengthened managed-profile lookup and safe rename/collision handling.
- Preserved unrelated Orca settings during profile renames; the new naming format is applied only during synchronization.
- Distinguished denied network operations from an offline Spoolman server, with recoverable approval-and-retry guidance.
- Stopped full and per-spool synchronization before profile writes when field setup or shared-Filament reconciliation is denied, without automatically replaying mutating network requests.
- Documented Orca's upstream permission fix #16658 (`6626377`), included in nightly `069bd402`. The original Orca 2.5.0 Alpha predates the fix; upgrading PipSpool alone does not resolve repeated prompts in older Orca builds.
- Passed 117 regression tests and 26 focused tests, and validated all five packages for syntax, numeric stable metadata, matching contents and the localhost default.
- Included Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel and macOS Apple Silicon packages.

## [2.2.12] - 2026-10-18

- Aligned PipSpool with the public OrcaSlicer 2.5.0 Alpha plugin contract.
- Declared OrcaSlicer's bundled Python 3.12 runtime in the PEP 723 plugin metadata.
- Added recoverable handling for Orca 2.5's audited background-thread permission when synchronizing, resetting filament fields, using dashboard actions or testing the Spoolman connection.
- Prevented a deferred lifecycle worker permission from leaking an unhandled `PermissionError`; PipSpool skips that single refresh and retries normally on the next event.
- Retained compatibility guards for older Orca builds and did not bypass Orca's permission storage.
- Kept the recurring targetless `socket.__new__` prompt documented as upstream OrcaSlicer issue #15724.
- Validated 117 synchronization, dashboard, lifecycle, persistence, packaging and architecture tests.
- Added stable packages for Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel and macOS Apple Silicon.

## [2.2.11] - 2026-10-12

- Fixed the **Select all** and **Clear** controls in every Advanced field synchronization tab so they update the checkboxes in the complete active tab panel.
- Added regression coverage for the field-group action scope and validated Python syntax for all five stable packages.
- Added stable packages for Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel and macOS Apple Silicon.

## [2.2.10] - 2026-10-06

- Added debounced Orca lifecycle-event integration from issue #10 so supported filament-preset and project events refresh PipSpool without performing network or UI work inside Orca's callback thread.
- Added concrete synchronization reasons for saved Orca filament presets while keeping preset selection informational and retaining the compatibility path for Orca builds without lifecycle events.
- Made the Settings window reload-safe after Orca restores its HTML on Linux/WebKit by requesting the current Python/backend state whenever the document is recreated.
- Stored the Spoolman address, dashboard visibility and low-stock threshold through Orca's supported capability configuration, automatically migrating existing settings and retaining PipSpool's shared JSON file as a compatibility mirror.
- Removed PipSpool's eager startup request for installation-specific Python IDNA files, avoiding an inherently unstable permission target on Linux AppImage launches.
- Corrected the automatic Moonraker command from `SET_SPOOL_ID` to `SET_ACTIVE_SPOOL` for issue #12.
- Migrated older PipSpool-managed G-code blocks on synchronization while preserving unrelated filament Start G-code and explicit per-spool custom G-code.
- Renamed the dashboard control to **Active spool G-code** and retained its existing enabled/disabled setting.
- Documented that Orca's recurring `socket.__new__`/IDNA permission prompt remains upstream issue #15724; PipSpool does not suppress a legitimate security prompt.
- Validated 112 synchronization, dashboard, lifecycle, persistence, packaging and architecture tests.
- Added stable packages for Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel and macOS Apple Silicon.

## [2.2.9] - 2026-09-24

- Added live Orca system-preset discovery for vendor `.opc` caches while preserving the JSON fallback for older Orca installations, based on the approach contributed by JP-Reitsma in PR #7.
- Improved parent selection for exact vendors, portable generic presets and custom material families.
- Synchronized shared Spoolman Filament settings across every associated physical-spool profile, based on JP-Reitsma's issue #9.
- Propagated a single Orca-side sibling edit to the other profiles while preserving and clearly reporting conflicting simultaneous edits.
- Added dashboard filters with live counts for all, loaded, low-filament, synchronization-needed and profile-problem spools.
- Added ascending and descending sorting by spool number, material, remaining weight, manufacturer and gate/toolhead.
- Made synchronization warnings diagnostic by naming affected spools and the specific missing, renamed, duplicate or changed profile data.
- Fixed persistent synchronization warnings after successful synchronization, Orca restarts and shared-Filament conflicts.
- Excluded Orca-only profile inheritance from Spoolman change detection while retaining manual parent repair.
- Removed the unnecessary vertical scrollbar from Advanced field tabs and retained horizontal access on narrow windows.
- Preserved the 2.2.8 compatibility-list recovery and validated 104 synchronization, dashboard, configuration, packaging and architecture tests.
- Added stable packages for Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel and macOS Apple Silicon.

## [2.2.8] - 2026-09-20

- Fixed a critical regression that could hide every PipSpool filament profile in OrcaSlicer after synchronizing Compatible Printers.
- Repaired malformed quoted-empty compatibility lists created by 2.2.7.
- Prevented inherited printer and print compatibility restrictions from being copied into every filament.
- Added automatic recovery: synchronize once and restart OrcaSlicer to restore affected profiles.
- Preserved valid explicitly selected dependency values and bidirectional advanced-field synchronization.
- Validated the recovery through repeated synchronization and OrcaSlicer restart.
- Added stable packages for Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel and macOS Apple Silicon.

## [2.2.7] - 2026-09-17

- Added a prominent **Spool ID G-code** toggle to the Printer Gates/Toolheads card.
- Kept managed `SET_SPOOL_ID` generation enabled by default for existing users.
- Allowed `SET_SPOOL_ID` to be disabled for printers and firmware that do not support the command while preserving unrelated filament start G-code.
- Fixed HTTP 400 errors when synchronizing list-valued dependency fields such as Compatible Printers and Compatible Prints.
- Preserved dependency lists through their complete Spoolman-to-Orca round trip.
- Removed PipSpool's external Python networking dependency and retained the public localhost default.
- Added mandatory Python syntax and embedded-image validation for every generated platform package.
- Validated stable packages for Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel and macOS Apple Silicon.

## [2.2.6] - 2026-09-13

- Redesigned Advanced field synchronization with Orca-style tabs instead of expanding lists.
- Added Setting Overrides, Advanced, Dependencies and Notes alongside Filament, Cooling and Multimaterial.
- Added synchronization support and matching Spoolman units for retraction, Z-hop, wiping and ironing settings.
- Added explicit synchronization for filament start, change and end G-code plus filament notes.
- Added opt-in synchronization for compatible printers, compatible print profiles and their conditions.
- Kept Orca dependency restrictions untouched unless the corresponding dependency field is explicitly selected.
- Added stable packages for Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel and macOS Apple Silicon.
- Validated all five packages for Python syntax, stable metadata and public-safe defaults.

## [2.2.5] - 2026-09-02

- Added stable bidirectional synchronization for selected Filament, Cooling and Multimaterial fields.
- Added native Spoolman field types and units for numbers, temperatures, percentages, booleans and choices.
- Added safe migration of older PipSpool text fields while preserving existing values.
- Filled newly selected Spoolman fields from Orca's resolved filament profiles.
- Persisted PipSpool settings, field selections and synchronization history across plugin updates.
- Added pending-change detection to Refresh with separate synchronize and restart notices.
- Prevented repeated profile updates, false restart notices and synchronization loops.
- Improved portable material inheritance so generated profiles remain visible across printers.
- Added optional Gate/Toolhead and Profile status columns, remaining-weight gauges and direct Spoolman links.
- Simplified synchronization totals to count each changed spool once with clear field-level details.
- Added stable packages for Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel and macOS Apple Silicon.
- Confirmed all 94 synchronization, dashboard, configuration, packaging and architecture tests pass.

## [2.2.4] - 2026-08-30

- Added a compact **Columns** menu to the Active spools table.
- Added saved visibility choices for Filament, Manufacturer, Colour, Nozzle, Bed and Remaining.
- Added Spoolman Location as an optional searchable column, hidden by default.
- Kept Spool and Material permanently visible for a clear minimum table layout.
- Fixed synchronization freezing after changing visible columns.
- Fixed unchecked columns remaining visible until the page was reopened.
- Kept Active spools column headings visible while scrolling through the spool list.
- Added stable packages for Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel and macOS Apple Silicon.
- Confirmed all 66 synchronization, dashboard, configuration, packaging and architecture tests pass.

## [2.2.3] - 2026-08-30

- Added optional dashboard visibility while keeping all core synchronization actions active.
- Added configurable low-filament warnings and compact remaining-weight gauges to gate/toolhead tiles.
- Added duplicate gate-assignment warnings with clear hover explanations.
- Added per-spool profile health for synced, missing, outdated and error states.
- Added detailed synchronization bullets describing which profiles and fields changed.
- Preserved exact custom Spoolman material types, including arbitrary names such as PLA-XS.
- Added stable packages for Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel and macOS Apple Silicon.
- Confirmed all 62 synchronization, dashboard, configuration, packaging and architecture tests pass.

## [2.2.1] - 2026-08-28

- Added a colour-aware Printer Gates/Toolheads overview based entirely on gate assignments already stored in Spoolman.
- Added compact toolhead tiles with gate number, spool number, material, printer name and remaining weight, arranged eight per row with support for larger systems.
- Added nozzle and bed temperatures to the searchable Active spools table.
- Added PipSpool's native pinstripe icon to the OrcaSlicer page tab.
- Reworked the dashboard into a deep navy and electric-blue Pip theme, including a full-height page background and a 75/25 Active spools/Last synchronization layout.
- Added a direct Feedback action that opens PipSpool GitHub Issues in the user's default browser.
- Added clear, stable connection-loss text instead of exposing raw HTTP exceptions.
- Added version, copyright and project information to the dashboard footer.
- Improved the first-open and refresh handshake so connection state and spool data populate reliably.
- Added regression protection for stable metadata, runtime version and the public localhost default.
- Confirmed all 44 synchronization, dashboard, configuration, packaging and architecture tests pass.

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

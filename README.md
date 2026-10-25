# PipSpool

![PipSpool — from spool inventory to OrcaSlicer profiles](https://github.com/Gadonk/pipspool-orcaslicer/blob/main/assets/pipspool_logo.png)

**Spoolman synchronization for OrcaSlicer**

PipSpool turns every active [Spoolman](https://github.com/Donkie/Spoolman) spool
into a clear, individual OrcaSlicer filament profile. It keeps spool identity,
material, colour, manufacturer, temperatures and selected filament settings
synchronized—without performing a second filament deduction.

PipSpool is maintained by **Donko** and designed for printers where Klipper,
Moonraker, Happy Hare or another Spoolman integration already handles real-time
filament usage.

## Current release: 2.2.19

The dashboard now shows spool inventory before background profile checks finish,
reduces repeated loading work, and offers a themed diagnostic preview/export.
Shared Filament settings remain the default; Settings also offers independent
advanced values per spool. See the [changelog](CHANGELOG.md#2219---2026-10-25).

## At a glance

- One OrcaSlicer filament profile for each active Spoolman spool.
- Stable spool-ID matching, so updates and renames do not create duplicates.
- Lifecycle-aware refreshes after supported Orca preset and project events, with
  a compatibility path for older Orca builds.
- Automatic removal of the matching profile when a spool is archived.
- Configurable profile naming, with `(#42) PLA Galaxy Blue - Manufacturer - PipSpool`
  retained as the default and a mandatory spool ID for safe matching.
- Nozzle and bed temperatures imported from the correct Spoolman material.
- Configurable spool-ID command with `{spool_id}` substitution, retaining
  `SET_ACTIVE_SPOOL ID={spool_id}` as the default, optional per-spool Start G-code,
  and the existing dashboard off switch.
- Optional synchronization for selected fields across every Orca filament tab.
- Bidirectional advanced-field updates: one-sided Spoolman changes can update
  Orca, while Orca remains master if both sides changed differently.
- Shared Spoolman Filament values propagate across all associated physical-spool
  profiles without silently overwriting conflicting sibling edits.
- Native Spoolman field types and units for temperatures, percentages, numbers,
  booleans and supported choices.
- No slicer-side filament deduction and no duplicate process profiles.

## PipSpool dashboard

The integrated PipSpool page brings daily controls and useful information into
one place:

- Clear connection health with Happy or Sad Pip artwork.
- A saved theme selector beside **Feedback**, with built-in palettes and optional local wallpaper.
- Searchable active-spool overview with remaining weight, nozzle temperature and
  bed temperature.
- A compact **Columns** menu with saved visibility choices for Filament,
  Manufacturer, Colour, Nozzle, Bed and Remaining.
- Optional Gate/Toolhead and Profile status columns, plus direct spool-number
  links that open the corresponding Spoolman record.
- Optional searchable Spoolman Location column, hidden by default.
- Live-count filters for all, loaded, low-filament, synchronization-needed and
  profile-problem spools.
- Ascending or descending sorting by spool number, material, remaining weight,
  manufacturer and gate/toolhead.
- Sticky table headings that remain visible while scrolling through active
  spools.
- Colour-aware **Printer Gates/Toolheads** overview using assignments already
  reported by Spoolman.
- **Feedback**, **Refresh** and **Synchronize now** actions, plus a **Sync**
  button beside each active spool.
- A prominent **Active spool G-code** toggle that is enabled by default and removes
  PipSpool-managed spool-ID output, including the configured command, when switched off.
- A diagnostic pending-synchronization notice that identifies affected spools
  and changed fields, kept separate from the restart-required notice.
- Last synchronization metrics, report and visible errors.
- A detailed change list showing which spool profiles and fields were updated.
- Optional page visibility without disabling PipSpool's core synchronization.
- Remaining-weight gauges, configurable low-filament warnings, duplicate-gate
  warnings and per-spool profile health on gate/toolhead tiles.
- Orca-style tabs for advanced Filament, Cooling, Multimaterial, Setting
  Overrides, Advanced, Dependencies and Notes fields.
- Deliberate cleanup controls for obsolete PipSpool fields.

Advanced field synchronization is opt-in. No advanced fields are selected by
default, and ordinary spool details, temperatures and spool-ID G-code continue
to work without enabling it. List-valued dependency settings such as Compatible
Printers and Compatible Prints retain their full values in both directions.

## Dashboard themes

Choose **PipSpool Classic**, **Light**, **Forest**, **Rosewood** or **Bonus Treat**
from the dropdown beside **Feedback**. Changes apply immediately and your
selection is remembered. Rosewood uses rich red surfaces and ruby actions;
Bonus Treat adds pumpkin-orange accents and matching Pip artwork. Loaded and
empty gate/toolhead cards follow the selected palette too, while filament colours
and remaining-weight gauges keep their meaning. Light theme uses readable
labels on matching light toolhead cards.

For a custom theme, open the dashboard once to create `example.json` in your
themes folder. Copy or edit that file to set colours and optional wallpaper
properties together in one JSON file. Put a referenced PNG, JPEG or WebP in the
folder's `images` subfolder, then click **Refresh**. Hover over the dropdown for
the exact folder path. Custom options show their JSON filename beside the name.

See the [theme guide](THEME_GUIDE.md) for default paths on every supported
platform, a complete example, image limits and sharing instructions. A
[starter theme file](themes/example.json) is also included. Themes change the
dashboard appearance; selecting a theme does not synchronize or rename profiles.

## Install and connect

### Orca Cloud

1. Subscribe to **PipSpool** in Orca Cloud.
2. In OrcaSlicer, open **File → Plugins**.
3. Select **Refresh**, then activate **PipSpool**.
4. Enter the complete address of your Spoolman server—for example,
   `http://192.168.1.50:7912`.
5. Select **Test connection**, then **Save settings**.
6. Open the **PipSpool** page and select **Synchronize now**.
7. Restart OrcaSlicer when the report says filament profiles changed.

### Manual installation

1. Download `pipspool-2.2.19-py3-none-any.whl` from the
   [latest GitHub release](https://github.com/Gadonk/pipspool-orcaslicer/releases/latest).
   The same wheel supports Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel
   and macOS Apple Silicon. Select the wheel directly; do not unpack it or run pip.
2. Open **File → Plugins** in OrcaSlicer.
3. Choose **Install local plugin** and select the downloaded file.
4. Disable any previous locally installed PipSpool or development copy, then
   activate the new copy and follow the connection steps above. Local packages
   have their own Orca identity; only one PipSpool copy should be active.

The setup window opens automatically only when no valid settings have been
saved. It remains available through the dashboard's **Settings** button or PipSpool's setup action. PipSpool stores
critical user settings through Orca's supported capability configuration and
keeps its existing settings file as a compatibility mirror.

> Do not run PipSpool alongside another plugin that creates Orca profiles from
> the same Spoolman spools.

## How synchronization works

PipSpool matches generated profiles by numeric Spoolman ID. Adding, editing or
archiving a spool therefore updates the correct Orca profile instead of creating
another copy.

Generated profiles use this order by default:

```text
(#spool) MATERIAL Filament name - Manufacturer - PipSpool
```

### Synchronize one spool

Select **Sync** beside an active spool. With no advanced fields selected, only
that spool is synchronized. With advanced fields enabled, the confirmation
explains that all active profiles sharing its Spoolman Filament are reconciled
together, preserving sibling conflict protection. Unrelated Filaments are left
unchanged. Use **Synchronize now** for the full inventory and archived-profile
cleanup. The last synchronization report lists the checked scope and changes.

### Choose the spool-ID command

Open **PipSpool Settings → Active spool G-code**. The default template is:

```gcode
SET_ACTIVE_SPOOL ID={spool_id}
```

PipSpool replaces `{spool_id}` with the physical Spoolman spool number when it
writes the filament profile. Spool #42 therefore gets `SET_ACTIVE_SPOOL ID=42`.
The template must be a single line containing `{spool_id}` exactly once. The
Settings example preview and **Reset command to default** help you check it.
The command is saved through Orca's capability configuration and the existing
settings-file mirror.

The right command depends on installed firmware and macros, not the printer
brand alone. The same examples are available beside the setting:

| Printer / firmware setup | Command or setting | Requirement |
| --- | --- | --- |
| Klipper + Moonraker + Spoolman | `SET_ACTIVE_SPOOL ID={spool_id}` | Install the macro from [Moonraker's Spoolman setup](https://moonraker.readthedocs.io/en/stable/configuration/#setting-the-active-spool-from-klipper). |
| Anycubic GoKlipper with an M555 Spoolman bridge | `M555 S={spool_id}` | Reported in issue #16; use only if your firmware or macro implements it. This is not a universal Anycubic command. |
| Klipper with a custom SET_SPOOL_ID macro | `SET_SPOOL_ID ID={spool_id}` | Your printer must define that macro with an ID parameter. This is not Moonraker's documented default. |
| Happy Hare / MMU managing active-spool selection | Turn **Active spool G-code** off | Use this when the configured MMU integration already selects the correct active Spoolman spool on tool changes. |
| Printer without a compatible Spoolman command | Turn **Active spool G-code** off | Continue using the printer's own filament-selection workflow; profile synchronization remains available. |

Per-spool Spoolman `start_gcode` remains an explicit override of the automatic
command and now supports literal `{spool_id}` replacement too. Other Orca or
Klipper expressions in that custom text are preserved, not evaluated by PipSpool.

The dashboard **Active spool G-code** switch still disables managed spool-ID
output. During synchronization PipSpool removes the managed block, filters the
configured/standard spool commands and token-bearing lines from its custom
managed text, and preserves unrelated user-authored Start G-code. Saving a new
command does not turn the switch back on. Advanced/shared Start G-code cannot
restore another spool's managed ID or defeat the off switch.

After saving or toggling, synchronize the affected profiles and restart
OrcaSlicer when prompted. Use full synchronization to apply the change to all
active profiles. Changing this setting does not execute a command on the printer
or configure the printer's macros.

### Choose your profile naming

Open **PipSpool Settings → Profile naming** and reorder these placeholders:

- `{spool_id}`: required exactly once; renders as `(#42)`.
- `{material}`: the Spoolman material.
- `{name}`: the filament name without a repeated leading material.
- `{vendor}`: the manufacturer.

The default format is `{spool_id} {material} {name} - {vendor}`. For example,
`{vendor} - {material} {name} {spool_id}` gives
`Prusament - PETG Galaxy Black (#42) - PipSpool`.

A live example and **Reset to default** are available. PipSpool always appends
` - PipSpool` and validates the format to keep spool identification unambiguous.
Saving the setting does not rename profiles immediately: synchronize to apply it,
then restart OrcaSlicer when prompted. Full synchronization applies the format
to all active spools. Existing profiles are matched by spool ID and renamed while
preserving unrelated Orca adjustments. Unreadable or mismatched existing files
are preserved with a visible error instead of being overwritten.

PipSpool preserves unrelated Orca-specific profile adjustments. Advanced-field
synchronization remembers the last agreed value so it can identify which side
changed. A one-sided Spoolman edit is imported into Orca; a one-sided Orca edit
is exported to Spoolman. If both sides changed differently, Orca remains the
master.

## Features I’m working on

These are active areas of investigation and improvement, not release promises:

- Reloading changed filament profiles inside OrcaSlicer without requiring a
  restart, if the evolving plugin API provides a safe supported method.
- More useful dashboard feedback and controls while keeping the page simple.
- Broader compatibility testing as OrcaSlicer's plugin API changes.
- Improving material-profile matching and advanced-field coverage based on
  real-world filament libraries.
- Refining cross-platform diagnostics based on Windows, Linux and macOS user
  feedback.

Suggestions and reproducible test cases are welcome in
[GitHub Issues](https://github.com/Gadonk/pipspool-orcaslicer/issues).

## Compatibility

PipSpool 2.2.19 supports Windows x86-64, Linux x86-64, Linux ARM64, macOS Intel
and macOS Apple Silicon. It is aligned with the public OrcaSlicer 2.5.0 Alpha
Python-plugin metadata, lifecycle-event, hosted-page and background-worker APIs.
Compatibility guards keep manual synchronization and the established fallback
behavior available on older Orca plugin builds.

OrcaSlicer 2.5 may ask once for permission when PipSpool creates a background
worker. If permission is denied, PipSpool now reports a recoverable message:
approve the request and repeat the action. PipSpool never edits or bypasses
OrcaSlicer's saved permission decisions.

Linux/WebKit Settings-window reload recovery requires an Orca build containing
[OrcaSlicer PR #15737](https://github.com/OrcaSlicer/OrcaSlicer/pull/15737).
PipSpool does not eagerly request access to installation-specific Python IDNA
files at startup; this avoids an unstable Linux AppImage permission target.
Orca fixed the recurring network permission prompt across restarts in
[PR #16658](https://github.com/OrcaSlicer/OrcaSlicer/pull/16658), merged as
`6626377` on 20 October 2026. Use an Orca build containing that fix; nightly
`069bd402` includes it, while the original 2.5.0 Alpha release predates it.
PipSpool alone cannot fix the host permission system in older Orca builds.

PipSpool distinguishes a denied network operation from a disconnected server.
If Orca refuses an attempt while posting an approval prompt, approve the trusted
request and repeat the action. Permission denial during field setup or shared
Filament reconciliation stops synchronization before profile writes and does
not save a new successful synchronization baseline. Requests that change data
are never automatically replayed. A new plugin identity or a different host may
legitimately require approval. PipSpool does not edit or bypass Orca's grants.

OrcaSlicer's Python plugin API is new and may change in future builds.

## Advanced setting scope and diagnostics

Open **Settings → Advanced setting scope** to choose shared Filament settings
(the default) or independent settings for each spool. Shared mode propagates
selected values to sibling profiles using the same Spoolman Filament. Independent
mode stores selected values on each Spoolman spool. Returning to shared mode with
differing sibling values reports a conflict rather than choosing a silent winner.

Click **Diagnostics** to open a window matching the selected theme. Review the
anonymous numeric comparisons before exporting. Enter your chosen absolute path
and `.json` filename in an existing folder; the exact reviewed report is saved
there and existing files are preserved. The current Orca plugin API has no native
Save As picker, so export uses a path field. Nothing is sent automatically. Reports
omit raw logs, credentials, server addresses, paths, profile names, original IDs
and G-code. Collect reports before and after a suspected reset; after-only data
cannot recover the preceding values. Historical error logs are not included.

The first dashboard connection uses a real read-only request through Orca's UI
callback so the released alpha can show its permission prompts. If refused, use
**Allow connection** to retry explicitly. Automatic attempts pause after denial.
The first request may pause the interface while the server responds or you answer
an approval prompt. After a successful read, spools appear and profile checks
continue in the background. Timing details are written to the local PipSpool log.
This does not require a PR test build or bypass Orca's permissions; older-host
permission persistence limitations described above still apply.

## Privacy and release safety

Version 2.2.19 uses one universal wheel of about 4 MB, with bundled artwork stored
as separate local package resources. Release workflows validate the wheel's
metadata, file hashes, source, artwork and upload size before creating a draft or
contacting Orca Cloud. Packaging does not determine Orca Cloud's security rating;
that rating comes from Orca Cloud's own review.

PipSpool synchronizes with the Spoolman address saved in its settings. Its
installed-version notice also checks the public GitHub release API. The public
source defaults to `http://localhost:7912`; configure your actual server address
during setup. GitHub Actions rejects private development addresses from release
artifacts. The universal wheel is checked for valid Python syntax and complete
bundled artwork before release.

## License

PipSpool is maintained and copyrighted by **Donko** and distributed under the
[MIT License](LICENSE).

The PipSpool logo is original artwork based on Donko's Pip character and an
independently designed filament-spool/database motif. It does not reproduce the
official Spoolman logo or wordmark.

### Synchronization corrections in 2.2.15

Saved per-spool advanced values are preserved over live parent-preset defaults.
Only the matching live spool profile can override those effective values. Selected
fields still synchronize through the shared Spoolman Filament; conflicting sibling
edits remain preserved and reported, including nozzle and plate temperatures.
Pure Orca-to-Spoolman exports no longer request a restart from the manual sync
action. Imports into sibling profiles and other disk-profile changes can still
require a restart. The reporter has since described remaining sync-back failures
in some existing profiles; investigation continues in [issue #17](https://github.com/Gadonk/pipspool-orcaslicer/issues/17).
The new safeguards and diagnostics improve investigation of that follow-up; issue #17 remains open pending confirmation.

# PipSpool

(https://raw.githubusercontent.com/Gadonk/pipspool-orcaslicer/main/assets/pipspool_orcacloud_hero_v1.png)

**Spoolman synchronization for OrcaSlicer**

PipSpool turns every active [Spoolman](https://github.com/Donkie/Spoolman) spool
into a clear, individual OrcaSlicer filament profile. It keeps spool identity,
material, colour, manufacturer, temperatures and selected filament settings
synchronized—without performing a second filament deduction.

PipSpool is maintained by **Donko** and designed for printers where Klipper,
Moonraker, Happy Hare or another Spoolman integration already handles real-time
filament usage.

## At a glance

- One OrcaSlicer filament profile for each active Spoolman spool.
- Stable spool-ID matching, so updates and renames do not create duplicates.
- Automatic removal of the matching profile when a spool is archived.
- Sortable names such as `(#42) PLA Galaxy Blue - Manufacturer - PipSpool`.
- Nozzle and bed temperatures imported from the correct Spoolman material.
- Automatic `SET_SPOOL_ID ID=42` or optional per-spool custom Start G-code.
- Optional Orca-master synchronization for selected Filament, Cooling and
  Multimaterial fields.
- No slicer-side filament deduction and no duplicate process profiles.

## PipSpool dashboard

The integrated PipSpool page brings daily controls and useful information into
one place:

- Clear connection health with Happy or Sad Pip artwork.
- Searchable active-spool overview with remaining weight.
- **Refresh** and **Synchronize now** actions.
- Last synchronization metrics, report and visible errors.
- Grouped selection of advanced Filament, Cooling and Multimaterial fields.
- Deliberate cleanup controls for obsolete PipSpool fields.

Advanced field synchronization is opt-in. No advanced fields are selected by
default, and ordinary spool details, temperatures and spool-ID G-code continue
to work without enabling it.

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

1. Download the Windows `pipspool_v*_win_x86_64.py` file from the
   [latest GitHub release](https://github.com/Gadonk/pipspool-orcaslicer/releases/latest).
2. Open **File → Plugins** in OrcaSlicer.
3. Choose **Install local plugin** and select the downloaded file.
4. Activate PipSpool and follow the connection steps above.

The setup window opens automatically only when no valid settings have been
saved. It remains available through PipSpool's setup action.

> Do not run PipSpool alongside another plugin that creates Orca profiles from
> the same Spoolman spools.

## How synchronization works

PipSpool matches generated profiles by numeric Spoolman ID. Adding, editing or
archiving a spool therefore updates the correct Orca profile instead of creating
another copy.

Generated profiles use this order:

```text
(#spool) MATERIAL Filament name - Manufacturer - PipSpool
```

PipSpool preserves unrelated Orca-specific profile adjustments. When advanced
field synchronization is enabled, OrcaSlicer is the master for the selected
Filament, Cooling and Multimaterial values.

## Features I’m working on

These are active areas of investigation and improvement, not release promises:

- Reloading changed filament profiles inside OrcaSlicer without requiring a
  restart, if the evolving plugin API provides a safe supported method.
- More useful dashboard feedback and controls while keeping the page simple.
- Broader compatibility testing as OrcaSlicer's plugin API changes.
- Improving material-profile matching and advanced-field coverage based on
  real-world filament libraries.
- Evaluating additional operating-system packages after the Windows version is
  stable and testable on those platforms.

Suggestions and reproducible test cases are welcome in
[GitHub Issues](https://github.com/Gadonk/pipspool-orcaslicer/issues).

## Compatibility

PipSpool 2.2.0 is confirmed on OrcaSlicer 2.5.0 nightly build `142c63ab` on
Windows x86-64 with Spoolman, Klipper, Moonraker and Happy Hare.

OrcaSlicer's Python plugin API is new and may change in future builds.

## Privacy and release safety

PipSpool connects only to the Spoolman address saved in its settings. The public
source defaults to `http://localhost:7912`; configure your actual server address
during setup. GitHub Actions rejects private development addresses from release
artifacts.

## License

PipSpool is maintained and copyrighted by **Donko** and distributed under the
[MIT License](LICENSE).

The PipSpool logo is original artwork based on Donko's Pip character and an
independently designed filament-spool/database motif. It does not reproduce the
official Spoolman logo or wordmark.

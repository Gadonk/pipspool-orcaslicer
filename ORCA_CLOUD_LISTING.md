# PipSpool

![PipSpool â from spool inventory to OrcaSlicer profiles](https://raw.githubusercontent.com/Gadonk/pipspool-orcaslicer/main/assets/pipspool_orcacloud_hero_v1.png)

**Spoolman synchronization plugin for OrcaSlicer**

PipSpool brings your active Spoolman inventory into OrcaSlicer as individual,
easy-to-find filament profiles. Each physical spool keeps its own profile,
Spoolman ID, temperatures, colour and optional Start G-code.

It is designed for Klipper and Moonraker systems where filament usage is already
deducted in real time. PipSpool does not perform a second deduction during
slicing and does not create duplicate process profiles.

## Key features

- Creates one OrcaSlicer filament profile for every active Spoolman spool.
- Updates an existing profile by its stable Spoolman ID instead of duplicating it.
- Removes the generated Orca profile when its spool is archived in Spoolman.
- Uses readable names such as `(#42) PLA Blue - Manufacturer - PipSpool`.
- Adds the correct `SET_SPOOL_ID ID=42` command to filament Start G-code.
- Supports optional custom Start G-code for individual physical spools.
- Imports nozzle and bed temperatures from Spoolman.
- Applies the bed temperature to OrcaSlicer's supported build-plate types.
- Lets the user choose which advanced Orca Filament, Cooling, and Multimaterial
  parameters are synchronized through Spoolman.
- Keeps advanced synchronization opt-in through a grouped Plugin configuration
  checklist, so Spoolman remains clean and readable.
- Preserves Orca-specific profile adjustments when synchronizing again.
- Includes a simple connection test and an embedded offline logo.
- Opens setup automatically only on the first launch.
- Performs no slicer-side filament deduction.

## Requirements

- A current OrcaSlicer nightly build with plugin support.
- Windows x86-64.
- A reachable Spoolman server.
- Active spools configured in Spoolman.

PipSpool has been confirmed with OrcaSlicer 2.5.0 nightly build `142c63ab`.
OrcaSlicer's plugin API is new and may change in later nightly builds.

## Installation

1. Subscribe to PipSpool in Orca Cloud.
2. Open **File â Plugins** in OrcaSlicer.
3. Click **Refresh** if PipSpool is not visible yet.
4. Activate **PipSpool**.
5. The setup window opens automatically if PipSpool has no saved settings.

Do not activate PipSpool alongside another plugin that synchronizes the same
Spoolman spools into OrcaSlicer.

## First-time setup

1. Enter the complete address of your Spoolman server, including `http://` or
   `https://` and its port when required. Example: `http://192.168.1.50:7912`.
2. Select **Test connection**.
3. Confirm that PipSpool reports the number of active spools it found.
4. Select **Save settings**.
5. Run **Sync Spoolman Profiles** from PipSpool's plugin actions.
6. Restart OrcaSlicer when the synchronization report says profiles changed.

The settings window remains available through **PipSpool Settings** if the
server address changes later.

## Advanced filament field selection

Open PipSpool's **Plugin configuration** for **Sync Spoolman Profiles** and
choose only the Filament, Cooling, and Multimaterial settings you want exposed
in Spoolman. No advanced fields are selected by default; ordinary spool data,
temperatures and spool-ID G-code continue working normally.

The optional removal checkbox deletes unselected PipSpool field definitions and
their saved values for every filament. Enable it only when intentionally cleaning
up old fields, run one synchronization, and then disable it again.

## What synchronization does

PipSpool reads the active spool list from Spoolman and matches profiles using
the numeric spool ID. This allows a profile to be renamed or refreshed without
losing its identity or producing another copy.

Generated profiles are named in this order:

```text
(#spool) MATERIAL Filament name - Manufacturer - PipSpool
```

Example:

```text
(#42) PLA Galaxy Blue - Example Filaments - PipSpool
```

After adding, editing or archiving spools in Spoolman, run **Sync Spoolman
Profiles** again. Restart OrcaSlicer if the report shows created, updated,
renamed or removed profiles.

## Per-spool Start G-code

On synchronization, PipSpool ensures that Spoolman has a spool-level text field
named **Start G-code**.

- Leave the field empty to use `SET_SPOOL_ID ID=<spool number>` automatically.
- Enter custom G-code to use it for that physical spool instead.
- PipSpool replaces only its own managed block and preserves unrelated Start
  G-code already stored in the Orca filament profile.

Use custom machine commands only when they are supported by your Klipper setup.

## Temperatures

PipSpool reads Spoolman's filament nozzle and bed temperature settings. The
nozzle temperature is applied to Orca's normal and initial-layer nozzle fields.
The bed temperature is applied to the supported Orca build-plate temperature
fields so the synced profile does not rely solely on generic filament values.

## Archived spools

Archiving a spool in Spoolman marks it as inactive. On the next PipSpool sync,
the matching generated Orca profile is removed. Profiles for active spools and
unrelated user-created filament profiles are left in place.

## Troubleshooting

### Connection test fails

- Confirm that the server address opens from the same Windows computer.
- Include the protocol and port, for example `http://192.168.1.50:7912`.
- Check the Windows firewall and the network connection to the Spoolman host.

### Profiles do not appear

- Confirm that the spools are active rather than archived in Spoolman.
- Run **Sync Spoolman Profiles** again.
- Restart OrcaSlicer after profiles have changed.

### PipSpool is missing after subscribing

- Sign in to OrcaSlicer with the same Orca Cloud account.
- Open **File â Plugins** and select **Refresh**.
- Confirm that you are using a current nightly build with plugin support.

### Filament usage is not deducted by PipSpool

This is intentional. PipSpool synchronizes profiles only. Klipper, Moonraker or
your spool-management integration should handle real-time usage accounting.

## Privacy and network access

PipSpool connects only to the Spoolman address configured in its settings. The
public plugin defaults to `http://localhost:7912`; replace it with your own
server address during first-time setup.

## Support and source

Source code, releases and issue reporting:
[github.com/Gadonk/pipspool-orcaslicer](https://github.com/Gadonk/pipspool-orcaslicer)

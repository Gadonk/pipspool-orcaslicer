# PipSpool provenance record

## Purpose

PipSpool 2.0 is a clean architectural replacement for the inherited 1.1.x
development line. This record tracks whether substantial implementation from
Zao Soula's OrcaSlicer Spoolman Bridge remains.

## Compared artifacts

- Inherited baseline: `pipspool_v1_1_4_dev.py` (1,417 lines)
- Clean implementation: `pipspool_v2_0_5_dev.py` (based on the independently rewritten 2.0 series)
- Comparison date: 2026-08-27

## Implementation boundaries

The clean implementation was written around public interfaces:

- OrcaSlicer PEP 723 plugin metadata and script capability API
- Spoolman `GET /api/v1/spool?allow_archived=false`
- OrcaSlicer JSON filament-preset fields
- Moonraker/Klipper `SET_SPOOL_ID ID=<id>` behavior

It does not register a slicing-pipeline capability, parse G-code, deduct
filament, create Spoolman extra fields, or generate duplicate process presets.

## Textual comparison

A line-oriented `difflib.SequenceMatcher` comparison reported:

- 71 exact sequence-matched lines in the 533-line clean file (13.321%)
- 7.282% overall line-sequence similarity
- Largest exact block: 5 lines

The exact blocks of three or more lines were limited to:

- required plugin metadata
- generic Python imports
- a two-count return used by legacy cleanup
- the public capability name `Remove Legacy Double Profiles`
- the required `@orca.plugin` declaration

No substantial algorithmic block was found as an exact textual match.

## Behavioral verification

`tests/test_pipspool.py` verifies:

- stable spool-ID rename/update behavior
- preservation of Orca-only preset overrides
- managed spool-ID G-code replacement without deleting custom G-code
- cleanup of inactive generated presets
- absence of slicing-pipeline and HTTP deduction code
- automatic settings opening through Orca's capability-load lifecycle
- clear settings actions and an embedded offline logo
- Spoolman nozzle and bed temperatures across every Orca build-plate type

All eight tests passed on 2026-08-27.

## Attribution status

The technical comparison supports a licensing reassessment for the clean 2.0
implementation. The inherited 1.1.x file remains subject to its original MIT
notice and must not be distributed without it. The repository-level notice
should remain until the inherited file is removed from distributed artifacts
and the maintainer has completed the final licensing review.

This record is technical evidence, not legal advice.

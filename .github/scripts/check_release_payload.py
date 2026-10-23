"""Reject oversized five-platform uploads before contacting Orca Cloud."""
from pathlib import Path
import sys

MAX_PAYLOAD_BYTES = 50_000_000  # Headroom below Orca's 100 MB release limit.
MULTIPART_ALLOWANCE_BYTES = 64 * 1024
TARGETS = {"win_x86_64", "linux_x86_64", "linux_arm64", "macosx_x86_64", "macosx_arm64"}


def validate_payload(files):
    files = list(files)
    targets = {target for file in files for target in TARGETS
               if file.name.endswith(f"_{target}.py")}
    if len(files) != 5 or targets != TARGETS:
        raise ValueError("Expected exactly one artifact for each of the five supported platforms")
    total = sum(file.stat().st_size for file in files) + MULTIPART_ALLOWANCE_BYTES
    if total > MAX_PAYLOAD_BYTES:
        raise ValueError(f"Five-platform payload {total:,} bytes exceeds the {MAX_PAYLOAD_BYTES:,}-byte safety budget")
    return total


def main():
    files = [Path(arg) for arg in sys.argv[1:]] or sorted(Path(".").glob("pipspool_v*.py"))
    try:
        size = validate_payload(files)
    except (ValueError, OSError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"Five-platform payload including framing allowance: {size:,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

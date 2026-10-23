"""Validate the stable universal wheel before draft creation or Cloud upload."""
import ast
import base64
import csv
from email.parser import BytesParser
import hashlib
import io
from pathlib import Path, PurePosixPath
import re
import sys
import zipfile

MAX_PAYLOAD_BYTES = 50_000_000
MULTIPART_ALLOWANCE_BYTES = 64 * 1024


def validate_payload(files):
    files = list(files)
    if len(files) != 1:
        raise ValueError("Expected exactly one universal wheel")
    wheel = files[0]
    match = re.fullmatch(r"pipspool-([0-9]+\.[0-9]+\.[0-9]+)-py3-none-any\.whl", wheel.name)
    if not match:
        raise ValueError("Expected a numeric stable version and py3-none-any wheel")
    version = match[1]
    size = wheel.stat().st_size + MULTIPART_ALLOWANCE_BYTES
    if size > MAX_PAYLOAD_BYTES:
        raise ValueError("Wheel upload exceeds the 50 MB safety budget")
    info = f"pipspool-{version}.dist-info"
    expected = {"pipspool/__init__.py", "pipspool/artwork.py",
                f"{info}/METADATA", f"{info}/WHEEL", f"{info}/RECORD", f"{info}/top_level.txt", f"{info}/LICENSE"}
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Duplicate wheel paths")
        assets = {name for name in names if re.fullmatch(r"pipspool/assets/[0-9a-f]{64}\.webp", name)}
        if len(assets) != 27 or set(names) != expected | assets:
            raise ValueError("Unexpected wheel contents or missing artwork")
        if sum(entry.file_size for entry in archive.infolist()) > MAX_PAYLOAD_BYTES:
            raise ValueError("Uncompressed wheel exceeds safety budget")
        for name in names:
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError("Unsafe wheel path")
        metadata = BytesParser().parsebytes(archive.read(f"{info}/METADATA"))
        if (metadata["Name"] != "PipSpool" or metadata["Version"] != version
                or metadata["Requires-Python"] != ">=3.12" or metadata.get_all("Requires-Dist")):
            raise ValueError("Invalid plugin metadata")
        wheel_meta = BytesParser().parsebytes(archive.read(f"{info}/WHEEL"))
        if wheel_meta.get_all("Tag") != ["py3-none-any"] or wheel_meta["Root-Is-Purelib"] != "true":
            raise ValueError("Wheel is not pure Python and universal")
        if archive.read(f"{info}/top_level.txt").strip() != b"pipspool":
            raise ValueError("Incorrect entry package")
        rows = list(csv.reader(io.StringIO(archive.read(f"{info}/RECORD").decode("utf-8"))))
        if len(rows) != len(names) or {row[0] for row in rows} != set(names):
            raise ValueError("Incomplete wheel RECORD")
        for name, digest, count in rows:
            if name == f"{info}/RECORD":
                if digest or count:
                    raise ValueError("Invalid RECORD self entry")
                continue
            payload = archive.read(name)
            hashed = base64.urlsafe_b64encode(hashlib.sha256(payload).digest()).rstrip(b"=").decode()
            if digest != "sha256=" + hashed or count != str(len(payload)):
                raise ValueError("RECORD integrity check failed")
            if name in assets:
                if payload[:4] != b"RIFF" or payload[8:12] != b"WEBP":
                    raise ValueError("Invalid WebP resource")
                if Path(name).stem != hashlib.sha256(payload).hexdigest():
                    raise ValueError("Resource filename does not match content")
            if name.endswith(".py"):
                source = payload.decode("utf-8")
                ast.parse(source, filename=name)
                if "-dev" in source or "192.168.0.3" in source:
                    raise ValueError("Development data in stable source")
        source = archive.read("pipspool/__init__.py").decode("utf-8")
        if f'PLUGIN_VERSION = "{version}"' not in source or f'# version = "{version}"' not in source:
            raise ValueError("Runtime version mismatch")
        if 'DEFAULT_SPOOLMAN_URL = "http://localhost:7912"' not in source:
            raise ValueError("Incorrect public default")
        if "data:image/webp;base64," in source:
            raise ValueError("Artwork should be separate resources")
    return size, version


def main():
    files = sorted(Path(".").glob("pipspool*.whl"))
    if list(Path(".").glob("pipspool_v*.py")):
        raise ValueError("Superseded root Python packages remain")
    size, version = validate_payload(files)
    print(version if "--version-only" in sys.argv else
          f"Stable {version}: universal wheel validated; upload with framing {size:,} bytes")


if __name__ == "__main__":
    main()

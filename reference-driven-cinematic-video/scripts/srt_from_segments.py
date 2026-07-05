#!/usr/bin/env python3
"""Create an SRT file from simple JSON caption segments."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def timestamp(seconds: float) -> str:
    millis = round(seconds * 1000)
    hours, remainder = divmod(millis, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{ms:03}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("segments", type=Path, help="JSON list with start, end, text fields")
    parser.add_argument("output", type=Path, help="Output .srt path")
    args = parser.parse_args()

    data = json.loads(args.segments.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("segments JSON must be a list")

    blocks: list[str] = []
    previous_end = 0.0
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise SystemExit(f"segment {index} is not an object")
        try:
            start = float(item["start"])
            end = float(item["end"])
            text = str(item["text"]).strip()
        except KeyError as exc:
            raise SystemExit(f"segment {index} missing field: {exc}") from exc
        if not text:
            raise SystemExit(f"segment {index} has empty text")
        if start < previous_end - 0.001:
            raise SystemExit(f"segment {index} starts before previous segment ends")
        if end <= start:
            raise SystemExit(f"segment {index} end must be after start")
        blocks.append(f"{index}\n{timestamp(start)} --> {timestamp(end)}\n{text}")
        previous_end = end

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
    print(str(args.output.resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

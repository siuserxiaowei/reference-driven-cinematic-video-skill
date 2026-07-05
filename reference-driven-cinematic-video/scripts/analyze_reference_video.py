#!/usr/bin/env python3
"""Analyze a reference video and produce FFmpeg evidence artifacts."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def run(command: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--out", type=Path, default=Path("reference-analysis"))
    parser.add_argument("--frames", default="0,3,6,9,13,18,24,30,36")
    args = parser.parse_args()

    video = args.video.expanduser().resolve()
    out = args.out.expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    if not video.exists():
        raise SystemExit(f"Video not found: {video}")

    probe = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size,bit_rate:stream=index,codec_name,codec_type,width,height,r_frame_rate,bit_rate",
            "-of",
            "json",
            str(video),
        ]
    )
    (out / "probe.json").write_text(probe.stdout, encoding="utf-8")

    volume = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-nostats",
            "-i",
            str(video),
            "-af",
            "volumedetect",
            "-vn",
            "-f",
            "null",
            "-",
        ],
        check=False,
    )
    (out / "volume.txt").write_text(volume.stderr, encoding="utf-8")

    silence = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-nostats",
            "-i",
            str(video),
            "-af",
            "silencedetect=noise=-50dB:d=0.5",
            "-vn",
            "-f",
            "null",
            "-",
        ],
        check=False,
    )
    (out / "silence.txt").write_text(silence.stderr, encoding="utf-8")

    contact_sheet = out / "contact-sheet.jpg"
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-nostats",
            "-i",
            str(video),
            "-vf",
            "fps=1/4,scale=320:-1,tile=5x3:padding=8:margin=8:color=black",
            "-frames:v",
            "1",
            "-update",
            "1",
            str(contact_sheet),
            "-y",
        ],
        check=False,
    )

    keyframes_dir = out / "keyframes"
    keyframes_dir.mkdir(exist_ok=True)
    for raw_time in args.frames.split(","):
        timestamp = raw_time.strip()
        if not timestamp:
            continue
        safe_name = timestamp.replace(".", "_")
        run(
            [
                "ffmpeg",
                "-hide_banner",
                "-nostats",
                "-ss",
                timestamp,
                "-i",
                str(video),
                "-frames:v",
                "1",
                str(keyframes_dir / f"t{safe_name}.png"),
                "-y",
            ],
            check=False,
        )

    summary = {
        "video": str(video),
        "out": str(out),
        "probe": str(out / "probe.json"),
        "volume": str(out / "volume.txt"),
        "silence": str(out / "silence.txt"),
        "contact_sheet": str(contact_sheet),
        "keyframes_dir": str(keyframes_dir),
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

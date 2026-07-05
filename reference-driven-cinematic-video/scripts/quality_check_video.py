#!/usr/bin/env python3
"""Run delivery gates for a rendered product video."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


def run(command: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def parse_db(pattern: str, text: str) -> float | None:
    match = re.search(pattern, text)
    return float(match.group(1)) if match else None


def has_detector_hit(text: str, marker: str) -> bool:
    return marker in text


def gate(status: str, message: str) -> dict[str, str]:
    return {"status": status, "message": message}


def score_gates(gates: dict[str, dict[str, str]]) -> int:
    weights = {
        "decode": 20,
        "streams": 15,
        "audio_loudness": 15,
        "subtitles": 10,
        "black_frames": 15,
        "silence": 10,
        "freezes": 10,
        "artifacts": 5,
    }
    total = 0.0
    for name, weight in weights.items():
        status = gates.get(name, {}).get("status", "warn")
        if status == "pass":
            total += weight
        elif status == "warn":
            total += weight * 0.5
    return round(total)


def stream_types(probe_data: dict[str, Any]) -> set[str]:
    return {stream.get("codec_type", "") for stream in probe_data.get("streams", [])}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--expect-audio", action="store_true")
    parser.add_argument("--expect-subtitles", action="store_true")
    parser.add_argument("--srt", type=Path, help="Expected sidecar SRT file")
    parser.add_argument("--min-score", type=int, default=0)
    parser.add_argument("--allow-black", action="store_true")
    parser.add_argument("--allow-freeze", action="store_true")
    args = parser.parse_args()

    video = args.video.expanduser().resolve()
    if not video.exists():
        raise SystemExit(f"Video not found: {video}")

    out = (args.out or video.with_suffix("")).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    probe = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size,bit_rate:stream=index,codec_name,codec_type,width,height,pix_fmt,color_range,r_frame_rate,avg_frame_rate,bit_rate,channels,channel_layout,duration",
            "-of",
            "json",
            str(video),
        ]
    )
    probe_data = json.loads(probe.stdout)

    decode = run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"], check=False)
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
    silence = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-nostats",
            "-i",
            str(video),
            "-af",
            "silencedetect=noise=-45dB:d=0.8",
            "-vn",
            "-f",
            "null",
            "-",
        ],
        check=False,
    )
    black = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-nostats",
            "-i",
            str(video),
            "-vf",
            "blackdetect=d=0.4:pic_th=0.98",
            "-an",
            "-f",
            "null",
            "-",
        ],
        check=False,
    )
    freeze = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-nostats",
            "-i",
            str(video),
            "-vf",
            "freezedetect=n=-60dB:d=1.0",
            "-an",
            "-f",
            "null",
            "-",
        ],
        check=False,
    )

    duration = float(probe_data.get("format", {}).get("duration") or 0)
    cols, rows = 5, 3
    step = max(duration / (cols * rows), 0.5) if duration else 4
    contact_sheet = out / "contact-sheet.jpg"
    contact = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-nostats",
            "-i",
            str(video),
            "-vf",
            (
                f"fps=1/{step:.3f},scale=360:-1,"
                "drawtext=text='%{pts\\:hms}':x=8:y=8:fontsize=18:"
                "fontcolor=white:box=1:boxcolor=black@0.55,"
                f"tile={cols}x{rows}:padding=8:margin=8:color=black"
            ),
            "-frames:v",
            "1",
            "-update",
            "1",
            str(contact_sheet),
            "-y",
        ],
        check=False,
    )
    if contact.returncode != 0 or not contact_sheet.exists():
        contact = run(
            [
                "ffmpeg",
                "-hide_banner",
                "-nostats",
                "-i",
                str(video),
                "-vf",
                f"fps=1/{step:.3f},scale=360:-1,tile={cols}x{rows}:padding=8:margin=8:color=black",
                "-frames:v",
                "1",
                "-update",
                "1",
                str(contact_sheet),
                "-y",
            ],
            check=False,
        )

    (out / "probe.json").write_text(probe.stdout, encoding="utf-8")
    (out / "decode-errors.txt").write_text(decode.stderr, encoding="utf-8")
    (out / "volume.txt").write_text(volume.stderr, encoding="utf-8")
    (out / "silencedetect.txt").write_text(silence.stderr, encoding="utf-8")
    (out / "blackdetect.txt").write_text(black.stderr, encoding="utf-8")
    (out / "freezedetect.txt").write_text(freeze.stderr, encoding="utf-8")
    (out / "contact-sheet-log.txt").write_text(contact.stderr, encoding="utf-8")

    types = stream_types(probe_data)
    mean_volume = parse_db(r"mean_volume:\s*(-?\d+(?:\.\d+)?) dB", volume.stderr)
    max_volume = parse_db(r"max_volume:\s*(-?\d+(?:\.\d+)?) dB", volume.stderr)

    gates: dict[str, dict[str, str]] = {}
    gates["decode"] = (
        gate("pass", "ffmpeg decode produced no errors")
        if decode.returncode == 0 and not decode.stderr.strip()
        else gate("fail", "ffmpeg decode reported errors")
    )

    if "video" not in types:
        gates["streams"] = gate("fail", "missing video stream")
    elif args.expect_audio and "audio" not in types:
        gates["streams"] = gate("fail", "expected audio stream is missing")
    elif args.expect_audio and "audio" in types:
        gates["streams"] = gate("pass", "video and expected audio streams present")
    else:
        gates["streams"] = gate("pass", "video stream present")

    if "audio" not in types:
        gates["audio_loudness"] = gate("fail" if args.expect_audio else "warn", "no audio stream")
    elif mean_volume is None or max_volume is None:
        gates["audio_loudness"] = gate("warn", "could not parse volumedetect output")
    elif mean_volume < -22 or mean_volume > -16 or max_volume > -1:
        gates["audio_loudness"] = gate(
            "warn",
            f"volume outside target: mean={mean_volume} dB, max={max_volume} dB",
        )
    else:
        gates["audio_loudness"] = gate(
            "pass",
            f"volume in target: mean={mean_volume} dB, max={max_volume} dB",
        )

    srt = args.srt.expanduser().resolve() if args.srt else None
    if args.expect_subtitles and srt and srt.exists() and srt.stat().st_size > 0:
        gates["subtitles"] = gate("pass", f"sidecar SRT exists: {srt}")
    elif args.expect_subtitles:
        gates["subtitles"] = gate("fail", "expected subtitles but no non-empty SRT was provided")
    else:
        gates["subtitles"] = gate("pass", "subtitle gate not requested")

    black_hit = has_detector_hit(black.stderr, "black_start:")
    gates["black_frames"] = (
        gate("warn" if args.allow_black else "fail", "blackdetect found black interval")
        if black_hit
        else gate("pass", "no blackdetect intervals")
    )

    silence_hit = has_detector_hit(silence.stderr, "silence_start:")
    gates["silence"] = (
        gate("warn", "silencedetect found audio silence interval")
        if silence_hit
        else gate("pass", "no long silence intervals")
    )

    freeze_hit = has_detector_hit(freeze.stderr, "freeze_start:")
    gates["freezes"] = (
        gate("warn" if args.allow_freeze else "fail", "freezedetect found frozen interval")
        if freeze_hit
        else gate("pass", "no freezedetect intervals")
    )

    gates["artifacts"] = (
        gate("pass", f"contact sheet created: {contact_sheet}")
        if contact_sheet.exists() and contact_sheet.stat().st_size > 0
        else gate("warn", "contact sheet was not created")
    )

    score = score_gates(gates)
    hard_fail = any(item["status"] == "fail" for item in gates.values())
    score_fail = args.min_score > 0 and score < args.min_score

    summary = {
        "video": str(video),
        "out": str(out),
        "decode_ok": gates["decode"]["status"] == "pass",
        "hard_fail": hard_fail,
        "score": score,
        "min_score": args.min_score,
        "passed": not hard_fail and not score_fail,
        "gates": gates,
        "metrics": {
            "duration": duration,
            "mean_volume_db": mean_volume,
            "max_volume_db": max_volume,
        },
        "contact_sheet": str(contact_sheet),
        "probe": str(out / "probe.json"),
        "volume": str(out / "volume.txt"),
        "blackdetect": str(out / "blackdetect.txt"),
        "silencedetect": str(out / "silencedetect.txt"),
        "freezedetect": str(out / "freezedetect.txt"),
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "quality-report.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

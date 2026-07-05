# Voice And Captions

Use this when a video needs Chinese narration, user-like timbre, cloned voice, subtitles, or TTS cleanup.

## Voice Gate

Prefer this order:

1. Clean user or client recording.
2. User-authorized voice clone from a clean sample.
3. Premium neural TTS such as MiniMax, Alibaba/Qwen/CosyVoice, ElevenLabs, Azure Custom Neural Voice, Tencent Cloud TTS, or OpenAI TTS when configured and auditioned.
4. Edge TTS only for draft or internal preview.
5. No-voice/music-first cut when available voices hurt the product.

Never claim voice cloning worked unless a usable sample was actually used. Do not upload a voice sample until ownership/permission, provider, purpose, audience, retention risk, and deletion needs are clear.

## Sample Requirements

A user-timbre sample should be:

- 20-60 seconds of continuous clean speech.
- Same language and approximate delivery style as the final video.
- No background music, heavy room echo, loud keyboard noise, or overlapping voices.
- Not silent or near-silent. Check with `ffmpeg -af volumedetect`; a sample with mean/max around -90 dB is unusable.

If the reference video is silent, say it is silent and ask for a real sample. Do not synthesize a "same timbre" voice from silence.

## Chinese Narration Style

Write 5-8 spoken sentences. Keep them short.

Avoid:

- "赋能", "全链路", "多维度", "效率闭环", "不止是...更是..."
- long written-language clauses
- generic openings such as "在数字化浪潮下"
- reading every on-screen feature aloud

Prefer:

- one punchy hook
- concrete work scenes
- one sentence for the product reveal
- two or three proof lines
- one closing memory line

## Audio Processing

Run a quick voice sample before final render when possible.

Typical FFmpeg cleanup:

```bash
ffmpeg -y -i voice.raw.mp3 \
  -af "highpass=f=80,lowpass=f=12000,acompressor=threshold=-20dB:ratio=1.5:attack=12:release=180,loudnorm=I=-18.5:TP=-2.0:LRA=10" \
  -ar 48000 -c:a aac -b:a 192k voice.m4a
```

Target:

- final web mix around -16 to -14 LUFS when measured with `loudnorm` or `ebur128`
- true peak at or below -1.5 dBTP
- `volumedetect` mean roughly -22 dB to -16 dB as a coarse check
- max volume below -1 dB as a coarse check
- no clipping, harsh sibilance, or unreadable music bed

Useful validation:

```bash
ffmpeg -hide_banner -i final.mp4 -af loudnorm=I=-16:LRA=7:TP=-1.5:print_format=json -f null -
ffmpeg -hide_banner -i final.mp4 -filter_complex ebur128=peak=true -f null -
```

## Captions

When narration exists, create captions unless the user explicitly says no.

Deliver:

- burned-in captions in the MP4
- sidecar `.srt` when possible
- caption segments aligned to voice beats, not arbitrary scene boundaries

In Remotion projects, normalize subtitle inputs to `@remotion/captions` `Caption[]` when possible, then render burned-in captions and/or export SRT. Candidate sources include `@remotion/install-whisper-cpp`, `@remotion/whisper-web`, `@remotion/openai-whisper`, or ElevenLabs transcript conversion. For short social/product clips, TikTok-style grouping can help, but only if it fits the brand.

Caption style:

- one or two lines only
- bottom safe-zone unless it covers key product UI
- high-contrast text with subtle backing
- no subtitle over final brand/product lockup unless it is the closing line

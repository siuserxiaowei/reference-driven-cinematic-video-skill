# Quality Gates

Use this file when a video is close to delivery or when the user has complained about low quality. Also use `production-upgrade-playbook.md` for the 100-point scorecard.

## Reference Match

- Candidate and reference contact sheets should have visibly related composition, density, typography, color, and rhythm.
- If the reference is mostly full-screen type, do not deliver a small centered product mockup.
- If the reference uses sparse text, do not add paragraphs.
- If the reference has hard cuts and flashes, avoid slow corporate fades.
- If the reference uses a curved screen, the candidate's primary surface must be large, bright, and carrying real content; small floating cards are a fail.

## Voice

Fail the voice gate if:

- it is macOS `say`
- it has obvious robotic prosody, unnatural pauses, or generic news-reader cadence
- it reads like a brochure instead of spoken narration
- the voice is louder than the mix or clips

Pass target:

- mean volume roughly between -22 dB and -16 dB in `volumedetect`
- max volume below about -1 dB
- no obvious clipping or harsh sibilance
- music/SFX support the cut without swallowing speech

If the user asks for their own voice, pass only when a clean user sample was used or when the final response clearly labels the voice as a non-cloned draft.

## Captions

Fail the caption gate if:

- narration exists but there are no captions and no explicit user opt-out
- captions overlap important UI/product text
- captions run beyond the spoken line by more than a beat
- the final video has burned-in captions but no sidecar SRT when the workflow can reasonably create one

## Images And Visual Assets

Fail the visual gate if:

- image looks like generic stock filler
- product PNG is pasted without lighting, scale, shadow, or visual role
- screenshots are unreadable or too dense
- generated images have broken text, warped UI, or inconsistent logo/product identity

## Render

Always run:

```bash
ffprobe -v error -show_entries format=duration,size,bit_rate:stream=index,codec_name,codec_type,width,height,r_frame_rate,bit_rate -of json final.mp4
ffmpeg -v error -i final.mp4 -f null -
ffmpeg -hide_banner -nostats -i final.mp4 -af volumedetect -vn -f null -
```

Render or extract a contact sheet:

```bash
ffmpeg -hide_banner -nostats -i final.mp4 -vf "fps=1/4,scale=320:-1,tile=5x2:padding=8:margin=8:color=black" -frames:v 1 -update 1 contact-sheet.jpg -y
```

Do not call it final if FFmpeg decode fails, if the contact sheet has accidental blank shots, or if audio is missing when voice/music was expected.

When using the bundled checker, prefer:

```bash
scripts/quality_check_video.py final.mp4 --expect-audio --expect-subtitles --srt captions.srt --min-score 80
```

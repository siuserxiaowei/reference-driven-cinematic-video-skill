---
name: reference-driven-cinematic-video
description: Use when Codex must turn a product intro, product brief, website, app, feature list, or reference video into a researched and narrated promo, launch film, kinetic typography video, curved-screen/cyclorama video, product demo, or motion-graphics clip. Also use when the user wants Codex to search the web, think through positioning, fill missing video content, or when prior output looks like PPT, AI voice, weak images, poor rhythm, or low production value.
---

# Reference Driven Cinematic Video

## Standard

Treat this as a production workflow, not a prompt-to-video shortcut. The job is to take a product intro or reference style, research and reason about what is missing, turn it into a sharp video concept, make or collect stronger assets, produce acceptable audio, add captions when narration exists, render, and verify. If the available voice, product images, or screenshots are not good enough for a final cut, say so and ship a clearly labeled draft or no-voice/music-first cut instead of pretending it is final.

Default quality target: a 30-60 second product intro should feel like an edited launch film, not slides with transitions. Use the reference to extract shot grammar, but use the user's product as the hero. If the first render feels like a 60/100 cut, keep iterating on the three bottlenecks that usually matter most: visual carrier, voice, and rhythm.

## Related Stack

Before implementation, choose the smallest stack that fits the reference:

- Load `$cyclorama-curved-screen` when the shot uses a concave screen, curved projection, parabolic media panel, or screen-as-hero language.
- Load `$remotion-video` and `remotion:remotion-best-practices` for React/Remotion implementation, timing, assets, audio, 3D, and render verification.
- Load `$ffmpeg` for media analysis, trimming, contact sheets, loudness checks, silence/black-frame checks, and final decode validation.
- Load `$humanizer-zh` for Chinese voiceover scripts. Video narration must sound spoken, not like a product brochure.
- Use image-generation or design skills for hero assets only after writing a precise art direction. Do not use random product PNGs or stock-like images as final art.
- Consider HyperFrames for HTML/GSAP-heavy kinetic references, Motion Canvas for explanatory vector animation with audio sync, and Remotion/Three for reusable product templates or 3D/screen texture work. See `references/related-stack.md`.
- Read `references/production-upgrade-playbook.md` when the user wants a reusable high-quality product-video skill, complains about PPT-like output, or asks for cooler effects.
- Read `references/voice-and-captions.md` when the output needs Chinese voiceover, subtitles, user voice matching, cloned voice, or TTS cleanup.

## Workflow

### 0. Product Brief Expansion

Use this step whenever the user gives a product introduction, feature list, website, app, brand name, or rough idea. Do not merely animate the supplied text.

Create a concise creative brief:

- product: what it is, who it is for, what job it does
- audience: buyer/user, pain level, familiarity with category
- promise: one sentence that could sit at the center of the video
- proof: concrete features, screenshots, workflows, stats, testimonials, demos, or public evidence
- objections: what the audience will doubt
- narrative angle: problem-solution, before-after, reference-led style, demo-first, founder/product story, category education
- missing assets: product images, logo, UI screenshots, screen recordings, brand colors, voice sample

Use search when the brief is thin, market/category context matters, or the product/company info may be current. Prefer official product pages, docs, GitHub repos, app stores, launch pages, founder posts, public demos, and credible competitor pages. Cite sources in the final response when web research affects claims.

If the user gives only a rough intro, proceed with a best-effort script and storyboard, but label assumptions. For product briefs, produce a "video packet" before coding: brief, claim ledger, category context, visual proof board, scene plan, voice script, asset list, and quality risks. See `references/product-brief-intake.md` and `references/research-to-storyboard.md`.

### 1. Reference Audit

Run `scripts/analyze_reference_video.py <reference-video> --out <analysis-dir>` or equivalent FFmpeg commands.

Capture:

- duration, dimensions, frame rate, codecs, bitrate
- audio reality: silent, music-only, speech, clipping, mean/max volume
- contact sheet across the full video
- 8-12 keyframes if the edit has distinct shots
- shot list: timestamp, composition, typography, color, camera movement, transition, audio event

Do not start building until the reference has a written shot grammar. If the user gives no reference video, create a reference board from searched examples or the related stack, then choose one primary visual direction. If the reference is silent or its audio is effectively silence, do not claim the target includes a reference voice. Add voice only because the user asked for it.

### 2. Style And Asset Plan

Write a short production plan before coding:

- visual grammar: e.g. full-frame black cyclorama, editorial giant type, card rail, 3D mesh, documentary B-roll, UI macro shots
- typography: 1-2 font families, size hierarchy, max words per frame
- palette: 2 neutrals plus 1-2 accents; avoid dusty gray, one-note purple/blue, beige defaults, and low-contrast "AI dashboard" mush unless the reference uses them
- assets needed: real product screenshot, generated hero image, UI mock, logo, footage, 3D model, texture, sound effects
- failure risks: weak voice, low-res image, no product screenshots, time too short, reference too complex

If assets are weak, make better ones before animating. A polished edit cannot rescue placeholder images.

Write a scene plan that maps product content to visuals:

- Scene purpose: hook, pain, product reveal, proof, workflow, close
- On-screen text: short, visual, not a paragraph
- Visual asset: screenshot, generated scene, UI mock, product render, code/card rail, footage
- Voice line: spoken, short, with room for pauses
- Motion reference: cut, sweep, flash, mesh bend, card rail, zoom, match cut

For cinematic product videos, choose one primary visual carrier and make it carry most shots: curved screen, product render, UI macro, code/data stream, or kinetic type. Do not build separate slide-like scenes unless the reference itself is slide-based.

### 3. Voiceover Gate

Voice is a quality gate, not decoration.

Provider order:

1. real user/client recording
2. cloned or premium neural voice with permission
3. MiniMax/ElevenLabs-class neural TTS if configured
4. Edge TTS only for draft or low-stakes preview
5. no-voice/music-first cut if voice quality harms the video

Never ship macOS `say` as final. Avoid generic TTS cadences by:

- writing 5-8 short spoken sentences
- removing brochure phrases and AI patterns
- adding pause marks in the script
- rendering an audio sample before final video
- loudness-normalizing and mixing with a restrained bed

If the user asks for their own timbre, first verify the supplied sample is usable: it should contain clean speech, not background music or silence. If the sample is silent, clipped, noisy, or not the user's voice, say so plainly and request a 20-60 second clean sample. If the voice still sounds fake after one serious attempt, stop and state the voice blocker. Offer a no-voice cut or ask for a real voice sample.

When a voiceover is present, subtitles are required unless the user explicitly says no subtitles. Create both burned-in captions for the MP4 and a sidecar `.srt` when possible.

### 4. Motion Build

Choose one implementation route:

- **Reference-faithful Remotion**: use for reusable templates, frame-accurate motion, products, UI, audio, and 3D.
- **Remotion + Three**: use when real curved mesh, camera, video textures, GLTF, or parabolic panels matter.
- **HyperFrames**: use when the reference is mostly HTML, typography, GSAP-like timeline, browser layout, or agent-friendly composition.
- **Motion Canvas**: use when the video explains a process and needs narration-synced vector construction.

Hard visual rules:

- Make one strong visual idea per shot. Do not stack a dashboard, paragraph, mascot, subtitle, and product card at once.
- Do not build a landing page or slide deck unless requested.
- Do not leave long accidental black gaps. Treat more than 12 frames of unintended blank screen as a fail.
- Keep reference-specific proportions. If the reference is 1280x624, do not silently switch to 1920x1080.
- Keep text inside the frame. Intentional crop is okay only when it matches the reference's giant-type style.
- For curved-screen shots, the screen should carry the frame; small floating panels fail.
- For high-tech product intros, use fast evidence shots, parallax, light sweeps, mesh/video textures, hard cuts, and restrained flashes instead of slow corporate fades.
- For generated images, avoid warped text, broken logos, fake UI claims, and one-off art that cannot be reused across scenes.

### 5. Verification

Run `scripts/quality_check_video.py <final-video> --expect-audio --min-score 80` or equivalent checks. Add `--expect-subtitles --srt <captions.srt>` when narration exists.

Required gates before saying "done":

- render stills or contact sheet for the candidate
- compare candidate contact sheet against the reference contact sheet
- decode final MP4 with FFmpeg
- inspect audio: duration, codec, mean/max volume, clipping risk
- verify subtitles: burned-in by visual inspection, sidecar `.srt` exists when requested, no missing opening or closing lines
- verify no unintended black gap, blank canvas, broken image, missing audio, or text clipping
- score the cut against `references/production-upgrade-playbook.md`; anything below 80 is a draft unless the user explicitly accepts it
- report exact final path and exact caveat if a gate is only partially satisfied

If any gate fails, fix it before final response. Do not describe an unfinished render as final.

## Output Contract

Final response must include:

- the final video path
- the contact sheet path
- the main source files changed
- validation results
- sources used for product claims or reference research
- explicit note if voice or assets are still draft quality

Use links or citations for external projects researched during the run. Keep the final short; the artifacts should do the talking.

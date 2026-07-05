# Production Upgrade Playbook

Use this when the user wants the skill itself improved, says the cut looks like PPT, or asks for a cooler reference-style product video.

## Scorecard

Score the candidate before final delivery. Treat less than 80 as a draft unless the user explicitly accepts it.

| Area | Points | Pass signal |
|---|---:|---|
| Reference match | 15 | Composition, rhythm, typography, transitions, and density visibly relate to the reference. |
| Product clarity | 15 | A viewer understands what the product is and why it matters within 10 seconds. |
| Visual carrier | 15 | One strong visual system carries the edit: curved screen, UI macro, product render, code/data stream, or kinetic type. |
| Asset quality | 10 | Product visuals are real, staged, or deliberately generated; no stock filler or warped text. |
| Motion quality | 15 | Camera, cuts, parallax, flashes, light sweeps, or mesh moves are timed; no slow slide-deck fades. |
| Voice and mix | 10 | Voice is natural enough for the intended use; mean volume roughly -22 to -16 dB, no clipping. |
| Subtitles | 8 | Narrated videos have readable burned-in captions and a sidecar SRT when possible. |
| Technical delivery | 12 | Decode passes, no unintended black gaps, correct dimensions/fps/codecs, contact sheet inspected. |

## Product-Video Packet

Before coding a product video from a thin description, write this packet in the working notes:

```markdown
Product:
Audience:
One-line promise:
Safe claims:
Risky claims:
Primary visual carrier:
Reference direction:
Shot rhythm:
Voice approach:
Subtitle approach:
Asset upgrades:
Quality risks:
```

## Claim Ledger

Use a claim ledger when web research affects the script or the product brief is thin:

```text
claim | claim_type | source_url | evidence_summary | confidence | allowed_wording | scene_id | risk
```

Claim types:

- `factual`: product has X, integrates with Y.
- `comparative`: faster, cheaper, or better than Z.
- `category`: common user pain or market pattern.
- `inferred`: reasonable positioning from evidence.
- `creative`: visual metaphor, not factual.

Rules:

- Comparative claims require direct evidence or must be removed.
- Quantified claims require source, date, and exact context.
- Inferred claims must be softened.
- No scene may contain unsupported factual or comparative claims.

## Visual Proof Board

Collect or specify proof assets before storyboard:

```text
asset | source | proves | visual use | quality | replacement_needed
```

Acceptable proof:

- real product screenshots
- workflow captures
- docs or API examples
- dashboard states
- before/after outputs
- credible public screenshots

Generated visuals are fine for metaphor and staging, but not as factual proof.

## Visual Pattern Library

Choose one primary pattern and one secondary pattern. More than two usually feels unfocused.

- **Cyclorama product reveal**: line draw -> bend into a curved screen -> product/workflow broadcasts -> collapse or final brand lockup. Use for reference videos like curved-screen demos.
- **Kinetic typography launch**: giant type, hard cuts, 2-4 words per frame, monochrome base with one accent. Use for abstract SaaS or category reframing.
- **UI macro proof**: close-up crops of real or mocked product screens, cursor trails, highlighted actions, fast zooms. Use when workflow proof matters.
- **Data/code stream**: terminal logs, cards, graph lines, structured records, and agent traces as motion texture. Use for developer/AI infrastructure products.
- **Product hero orbit**: 3D product render or staged PNG with parallax, rim light, shadow, and device-like camera moves. Use when hardware or mascot identity matters.
- **Shader/glass montage**: blur, refraction, scanlines, bloom, Lottie, and short sub-compositions. Use sparingly; it should support proof, not hide weak content.

## Upgrade Moves

- Replace feature bullets with proof shots: UI card, real screenshot crop, task log, generated doc, before/after output.
- Replace dusty gray with clean dark neutral plus controlled accent. If the scene feels muddy, raise local contrast and reduce grain/vignette.
- Replace long dissolves with hard cuts, flash cuts, match cuts, whip wipes, line wipes, or mesh transitions that echo the reference.
- Make subtitles part of the design: bottom safe-zone, high contrast, 1-2 lines, no overlap with product text.
- Use music and SFX as timing glue: hit reveals, whooshes, soft risers, and low beds; never let them swallow speech.

## Routing Defaults

- Use Remotion + Three for reusable curved-screen/product-render templates.
- Use HyperFrames when most of the look is HTML/CSS/GSAP/Lottie/shader montage and fast agent authoring matters.
- Use Motion Canvas when the video is an explanatory vector build synced to narration.
- Use plain Remotion DOM when typography, UI cards, captions, and audio timing are the main work.

## Cyclorama Preset

Use this preset when the user references a Cyclorama-style curved screen.

Geometry:

- Use a real bent mesh. Do not fake the effect with CSS perspective, flat DOM layers, border-radius panels, or 2D screenshots.
- Baseline panel: `PlaneGeometry(3.2, 1.8, 64, 20)`.
- Bend per vertex: `z = bend * 0.42 * nx * nx`, where `nx` is normalized x in `[-1, 1]`.
- Main act panel should occupy roughly 65-85% of frame width.
- Precompose product scenes into 16:9 textures, ideally 1280x720 or higher.

Material and texture:

- Use `MeshBasicMaterial` for mapped media so the screen stays self-lit.
- Crossfade stacked mesh materials on the same geometry using opacity and render order.
- In current Remotion + Three, prefer `@remotion/media` `<Video headless />` plus `onVideoFrame` to update a Three.js `CanvasTexture`. Treat `useVideoTexture()` and `useOffthreadVideoTexture()` as legacy/deprecated fallback paths.
- Use `<ThreeCanvas width={width} height={height}>`, drive motion with `useCurrentFrame()`, and pass `layout="none"` for any `<Sequence>` inside Three scenes.
- Do not add floor, wall, chrome, monitor bezel, or decorative 3D rooms unless the reference has them.

Shot rhythm:

```text
0.0-0.6s   black hold
0.6-2.8s   white horizontal line draws in
3.2-6.0s   line expands vertically while bend rises 0 -> 1
6.4-8.0s   white surface fades out while first media fades in
8.0-33.0s  4-6 broadcasts, each 4-6s, with slow crossfades and gentle parallax
33.2-40.0s final media fades to white surface; bend/height collapse; line retracts; title appears
```

Camera:

- Default composition: 1920x1080 or reference aspect ratio.
- Camera `fov=46`, `z=4.2-4.25`, slow push toward `z=3.8` during the media act.
- Gentle motion only: yaw about `-0.14` to `+0.16` rad, pitch about `-0.05` to `+0.045` rad, roll drift around `0.012` rad.

Render preflight:

- For WebGL/Three renders, use `--gl=angle` locally, `angle-egl` on GPU Linux, and `swangle` on Lambda or no-GPU machines.
- If long WebGL renders leak memory or fail, split the video into shorter parts and join with FFmpeg.

Verification:

- Contact sheet must include black hold, line, half-expanded panel, first media, 2-3 broadcast frames, fold-back, and title.
- Fail if the candidate reads as slides, the panel is small, media is flat DOM overlay, text lives mostly outside the mesh, or the line-to-screen transition is a cut instead of a continuous morph.

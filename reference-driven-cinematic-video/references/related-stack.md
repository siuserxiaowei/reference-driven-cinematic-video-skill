# Related Stack

Use this file when deciding which project, skill, or framework to combine for a reference-driven video.

## Local Skills

- `cyclorama-curved-screen`: curved screen, parabolic media surface, line-to-screen reveal, 3D texture stack.
- `remotion-video`: Remotion project workflow, audio-driven scene timing, 3D patterns, render commands.
- `remotion:remotion-best-practices`: official Remotion rules; read relevant rules for 3D, animations, timing, assets, audio, compositions, and video.
- `ffmpeg`: reference analysis, still extraction, contact sheets, silence/volume checks, final decode validation.
- `humanizer-zh`: rewrite Chinese voiceover into spoken language and remove AI writing patterns.
- `generate-image`, `imagegen`, `gemini-image`, `brand-guidelines`, `frontend-design`: use only when the video needs stronger visuals or a brand-consistent art direction.
- `hyperframes:hyperframes` / `hyperframes:gsap`: use when the reference is closer to HTML/GSAP kinetic typography than React component logic.

## Implementation Capabilities

Use this as a routing map, not as a public list of reference projects.

- Programmatic video rendering: reusable templates, timeline control, audio sync, props, preview, MP4 render.
- Three-dimensional screen work: product/device shots, curved screens, self-lit media textures, parallax, WebGL render preflight.
- HTML/CSS motion rendering: kinetic typography, web-style layouts, shader accents, vector inserts, fast social clips.
- Explanatory vector animation: process explainers, diagrams, system flows, and narration-synced construction.
- Caption and transcript tooling: import, generate, normalize, burn in, and export `.srt`.
- Voice provider routing: user recording, user API, authorized voice clone, premium TTS, or default Mandarin neural voice.
- FFmpeg delivery checks: decode, loudness, silence, black frames, freezes, contact sheets, and final artifact validation.

## Routing

- If the reference has 3D camera, meshes, curved screens, or video textures: use Remotion + Three.
- If the reference is flat editorial kinetic typography: use Remotion DOM or HyperFrames; avoid unnecessary 3D.
- If the reference is a process explainer with narration: use Motion Canvas or a Remotion scene registry.
- If the user wants many future variants: build a Remotion template with props and a repeatable render script.
- If the user wants one fast social clip: HyperFrames may be faster, but still run FFmpeg checks.
- If the user wants agent-friendly product launch videos from a URL or brief: study HyperFrames `/product-launch-video` and its render loop, then decide whether to port the pattern or call HyperFrames directly.
- If the reference is Cyclorama-style: use a real bent mesh and texture stack, not CSS perspective or flat DOM layers.
- If using external templates or code, check the license before copying. Prefer learning patterns over vendoring unknown assets.

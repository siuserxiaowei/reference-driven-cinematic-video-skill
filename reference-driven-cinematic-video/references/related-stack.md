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

## External Projects To Consider

- `YPAAAAAAAAAAAAA/cyclorama-curved-screen`: source inspiration for concave screens and projection surface behavior. https://github.com/YPAAAAAAAAAAAAA/cyclorama-curved-screen
- `remotion-dev/remotion`: React-based programmatic video engine. https://github.com/remotion-dev/remotion
- `remotion-dev/template-three`: Remotion + React Three Fiber starter for 3D scenes and screens. https://github.com/remotion-dev/template-three
- `remotion.dev/docs/three`: official rules for `@remotion/three`, video textures, and OpenGL renderer. https://www.remotion.dev/docs/three
- `remotion.dev/docs/videos/as-threejs-texture`: current Remotion video-texture route using `@remotion/media` `<Video headless />` and `onVideoFrame`. https://www.remotion.dev/docs/videos/as-threejs-texture
- `remotion.dev/docs/gl-options`: renderer backend guidance for WebGL/Three renders. https://www.remotion.dev/docs/gl-options
- `remotion.dev/docs/captions`: official caption import, transcription, display, and subtitle export docs. https://www.remotion.dev/docs/captions/
- `remotion-dev/template-prompt-to-motion-graphics-saas`: prompt-to-motion-graphics architecture with validation, skill detection, constants-first code, and live preview. https://github.com/remotion-dev/template-prompt-to-motion-graphics-saas
- `lifeprompt-team/remotion-scenes`: reusable Remotion motion-graphics scene library; useful for text reveals, transitions, and After Effects-like patterns. https://github.com/lifeprompt-team/remotion-scenes
- `reactvideoeditor/remotion-templates`: many self-contained Remotion templates for charts, text, transitions, branding, images, and media. https://github.com/reactvideoeditor/remotion-templates
- `ali-abassi/remotion-templates`: AI-agent-oriented Remotion template index and SKILL.md patterns. https://github.com/ali-abassi/remotion-templates
- `motion-canvas/motion-canvas`: TypeScript motion graphics with generator timelines and editor; useful for explainer videos synced to voice. https://github.com/motion-canvas/motion-canvas
- `motion-canvas/examples`: runnable Motion Canvas examples for parallax, code, diagrams, and explanatory motion. https://github.com/motion-canvas/examples
- `redotvideo/revideo`: Motion Canvas-style TypeScript scenes with headless/API-oriented rendering; treat as experimental until locally proven. https://github.com/redotvideo/revideo
- `Manim Community`: precise programmatic diagrams and technical explainers; use as insert clips, not default cinematic layer. https://docs.manim.community/en/stable/
- `airbnb/lottie-web`: browser-rendered AE/Bodymovin vector animation for icon loops, loaders, and motion accents. https://github.com/airbnb/lottie-web
- `Rive runtimes`: stateful vector/brand animations when a `.riv` asset exists. https://rive.app/docs/runtimes/getting-started
- `heygen-com/hyperframes`: plain HTML to video for agents; useful when a reference is mostly DOM layout, typography, GSAP, and browser-native composition. https://github.com/heygen-com/hyperframes
- `heygen-com/hyperframes-launch-video`: full production example with sub-compositions, GSAP, Lottie, shaders, Three.js, captions, SFX, script, and storyboard. https://github.com/heygen-com/hyperframes-launch-video
- `nexu-io/html-video`: agentic HTML-to-video project with templates and FFmpeg MP4 output; use as pattern source or experimental prototype route. https://github.com/nexu-io/html-video
- `nateherkai/hyperframes-student-kit`: HyperFrames example workbench; useful as a source of HTML/GSAP timeline patterns. https://github.com/nateherkai/hyperframes-student-kit
- `faster-whisper`: local ASR route for transcripts and SRT QA when available. https://github.com/SYSTRAN/faster-whisper
- `ElevenLabs TTS / voice cloning docs`: premium TTS and authorized voice-clone route when configured. https://elevenlabs.io/docs/overview/capabilities/text-to-speech

## Routing

- If the reference has 3D camera, meshes, curved screens, or video textures: use Remotion + Three.
- If the reference is flat editorial kinetic typography: use Remotion DOM or HyperFrames; avoid unnecessary 3D.
- If the reference is a process explainer with narration: use Motion Canvas or a Remotion scene registry.
- If the user wants many future variants: build a Remotion template with props and a repeatable render script.
- If the user wants one fast social clip: HyperFrames may be faster, but still run FFmpeg checks.
- If the user wants agent-friendly product launch videos from a URL or brief: study HyperFrames `/product-launch-video` and its render loop, then decide whether to port the pattern or call HyperFrames directly.
- If the reference is Cyclorama-style: use a real bent mesh and texture stack, not CSS perspective or flat DOM layers.
- If using external templates or code, check the license before copying. Prefer learning patterns over vendoring unknown assets.

# Reference Driven Cinematic Video

一个面向 Codex 的产品视频生产 skill：把产品介绍、网站、文档、功能清单或参考视频，转成带研究补全、分镜、配音、字幕、特效路线和质量闸门的产品介绍片工作流。

它不是“把文字塞进 PPT 模板”。这个 skill 的目标是让 Codex 像一个小型视频制片流程一样工作：先理解产品和参考风格，再补全事实与视觉证据，最后用 Remotion、Three.js、HyperFrames、Motion Canvas、FFmpeg 等工具生成并校验成片。

## 适合什么场景

- 给一段产品说明，自动补全 30-60 秒中文/英文产品介绍片。
- 给一个参考视频，复刻它的镜头语法、节奏、色彩和特效结构。
- 做科技感、曲面屏、Cyclorama、UI macro、代码流、动效字体类产品片。
- 修正“像 PPT”“AI 配音味太重”“没字幕”“画面灰尘”“节奏很散”的视频产出。
- 让 Codex 在最终交付前跑音频、字幕、黑屏、冻帧、解码和 contact sheet 检查。

## 核心流程

1. **Product Brief Expansion**
   从产品介绍、飞书文档、网站或功能清单里提取产品、用户、痛点、承诺、证据、疑虑和缺失素材。

2. **Research Sidecar**
   对薄弱产品介绍做搜索补全，生成 claim ledger、category context、visual proof board，避免写出无证据的夸张文案。

3. **Reference Audit**
   用 FFmpeg 拆参考视频：时长、分辨率、帧率、音频现实、contact sheet、关键帧和镜头语法。

4. **Style And Asset Plan**
   选择主视觉载体，例如曲面屏、产品 render、UI macro、代码流、动效字体或数据流，而不是堆叠多个幻灯片场景。

5. **Voiceover Gate**
   中文配音必须先过口播稿、样音、音量、LUFS、峰值和授权检查。用户音色必须有干净人声样本，不能从静音视频硬说成克隆。

6. **Captions Gate**
   有旁白就默认要字幕：烧录字幕进 MP4，并尽量同时输出 `.srt`。

7. **Motion Build**
   根据参考风格路由到 Remotion、Remotion + Three、HyperFrames 或 Motion Canvas。

8. **Quality Gate**
   交付前必须跑 `quality_check_video.py`，低于 80 分默认只能叫 draft。

## Cyclorama 曲面屏标准

如果参考是 `YPAAAAAAAAAAAAA/cyclorama-curved-screen` 这类效果，skill 会要求：

- 使用真实 bent mesh，不用 CSS 假透视。
- 默认 `PlaneGeometry(3.2, 1.8, 64, 20)`。
- 弯曲公式：`z = bend * 0.42 * nx * nx`。
- 产品场景先预合成为 16:9 texture，再贴到曲面屏上。
- 主屏占画面 65-85% 宽度。
- 走 line draw -> expand -> bend -> media broadcast -> collapse 的连续几何变形。

## 配音与字幕标准

配音优先级：

1. 真实用户/客户录音。
2. 用户授权的自定义/克隆音色。
3. MiniMax、Alibaba/Qwen/CosyVoice、ElevenLabs、Azure、Tencent、OpenAI 等可用且试音通过的神经 TTS。
4. Edge TTS 只能作为草稿。
5. macOS `say` 不允许作为最终成片。

中文口播规则：

- 5-10 句短口语。
- 少讲抽象价值，多讲真实工作场景。
- 避免“赋能、无缝、革命性、生态闭环、行业领先”等广告腔。
- 先出 10-15 秒样音，听起来不行就停，不把烂配音硬塞进最终片。

## 质量检查脚本

skill 自带：

- `scripts/analyze_reference_video.py`：分析参考视频，输出 probe、音量、静音、contact sheet、关键帧。
- `scripts/quality_check_video.py`：检查最终视频，输出 `quality-report.json`。
- `scripts/srt_from_segments.py`：从 JSON 字幕片段生成 SRT。

示例：

```bash
python3 reference-driven-cinematic-video/scripts/quality_check_video.py final.mp4 \
  --expect-audio \
  --expect-subtitles \
  --srt captions.srt \
  --min-score 80
```

它会检查：

- FFmpeg decode 是否通过。
- 视频/音频流是否存在。
- 音量是否在目标区间。
- SRT 是否存在。
- 是否有长黑屏、长静音、冻帧。
- 是否生成 contact sheet。
- 最终 `score` 是否达到阈值。

## 安装

克隆后把 skill 目录同步到 Codex skill 目录：

```bash
git clone https://github.com/siuserxiaowei/reference-driven-cinematic-video-skill.git
mkdir -p ~/.codex/skills
rsync -a reference-driven-cinematic-video-skill/reference-driven-cinematic-video/ \
  ~/.codex/skills/reference-driven-cinematic-video/
```

验证：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  ~/.codex/skills/reference-driven-cinematic-video
```

## 使用示例

```text
用 $reference-driven-cinematic-video

这是我的产品介绍：
<产品文档或网站链接>

目标：30-40 秒产品介绍片，中文配音，偏高级科技感。
参考这个视频风格：
<参考视频路径或链接>

你自己搜索补全，最后给我成片。
```

## 依赖建议

基础依赖：

- Python 3
- FFmpeg / ffprobe
- Node.js

常用视频栈：

- Remotion
- Three.js / React Three Fiber
- `@remotion/media`
- `@remotion/captions`
- HyperFrames
- Motion Canvas

配音能力取决于你本地或云端可用的 TTS/voice-clone provider。没有高质量人声或授权音色时，skill 会把最终成片降级为草稿或建议无旁白版本。

## 参考项目

- [YPAAAAAAAAAAAAA/cyclorama-curved-screen](https://github.com/YPAAAAAAAAAAAAA/cyclorama-curved-screen)
- [Remotion](https://github.com/remotion-dev/remotion)
- [Remotion Three.js texture docs](https://www.remotion.dev/docs/videos/as-threejs-texture)
- [Remotion captions docs](https://www.remotion.dev/docs/captions/)
- [HyperFrames](https://github.com/heygen-com/hyperframes)
- [HyperFrames launch video](https://github.com/heygen-com/hyperframes-launch-video)
- [Motion Canvas](https://github.com/motion-canvas/motion-canvas)

## 许可证

暂未指定许可证。公开仓库可供查看与学习，但复用、分发、商用授权需要仓库所有者后续明确。

# Chat Distill · 聊天记录提纯器

> 将杂乱的多轮微信 / 即时通讯聊天记录，蒸馏成结构化的 **6-Scheme Prompt** 蓝图。
> 
> Distill messy multi-turn WeChat / IM chat logs into a structured **6-Scheme Prompt** blueprint.

---

## 简介 · Overview

**中文**
Chat Distill 是一个 Prompt 工程技能包。它从碎片化的群聊、语音转文字、对话截图里滤掉寒暄与跑题噪音，提取核心需求、约束与偏好，编译成一份生产级、可直接喂给任意 LLM 执行的 6-Scheme Prompt。典型场景：群聊头脑风暴落地成方案、老板零散布置任务编译成需求文档、多人讨论提炼成 PRD / SOP、会议记录结构化。

**English**
Chat Distill is a prompt-engineering skill package. It strips greetings and off-topic noise from fragmented group chats, voice-to-text transcripts, and screenshots, then extracts core requirements, constraints, and preferences into a production-ready 6-Scheme Prompt that can be fed directly to any LLM. Typical use cases: turning a group brainstorm into a spec, compiling a boss's scattered instructions into a requirements doc, distilling multi-party discussions into a PRD / SOP, or structuring meeting notes.

---

## 6-Scheme 框架 · The 6-Scheme Framework

**中文**
最终输出是一份包含六个正交支柱的 Prompt，保证生成质量的一致性与可复现性：

| #   | 支柱  | 作用  |
| --- | --- | --- |
| 1   | **Role** 角色与人设 | 定义高度具体的专家身份（禁用"助手""AI"等泛化标签） |
| 2   | **Context** 背景与意图 | 合成业务场景、痛点、目标受众与触发动因 |
| 3   | **Task** 核心指令与流水线 | 按时间顺序拆解为强动词开头的 SOP 步骤 |
| 4   | **Output Format** 输出格式 | 指定精确响应布局（表格 / JSON / 列表 / 标签） |
| 5   | **Constraints** 约束与红线 | 列出硬边界：字数、禁用词、强制语气、数据范围 |
| 6   | **Examples** Few-Shot 示例 | 提取或生成 Input/Output 对以锚定输出质量 |

**English**
The output is a Prompt with six orthogonal pillars that guarantee consistent, reproducible generation:

| #   | Pillar | Purpose |
| --- | --- | --- |
| 1   | **Role** | Define a highly specific expert identity (no generic tags like "assistant" or "AI") |
| 2   | **Context** | Synthesize the business scenario, pain points, audience, and triggers |
| 3   | **Task** | Break the work into a chronological SOP of strong-verb steps |
| 4   | **Output Format** | Specify the exact response layout (table / JSON / list / tags) |
| 5   | **Constraints** | List hard boundaries: length, forbidden phrases, mandatory tone, data scope |
| 6   | **Examples** | Extract or generate Input/Output pairs to anchor output quality |

详细框架指南见 `references/6-scheme-guide.md`。
See `references/6-scheme-guide.md` for the full framework guide.

---

## 安装 · Installation

**中文**
双击 `chat-distill.skill` 文件，或将其拖入 QClaw 窗口，即可自动安装该技能包。

**English**
Double-click the `chat-distill.skill` file, or drag it into the QClaw window, to install the skill package automatically.

---

## 快速开始 · Quick Start

### 方式一：直接对话 · Mode A — Conversational

**中文**
把聊天记录粘贴到对话中，说"聊天记录提纯"或"chat-distill"即可触发。

**English**
Paste your chat log into the conversation and say "聊天记录提纯" or "chat-distill" to trigger it.

### 方式二：脚本批量处理 · Mode B — Batch Script

**中文**
使用配套脚本对聊天记录文件做批量提纯：

```bash
python scripts/distill.py 聊天记录.txt [输出.md]
```

**English**
Use the bundled script to batch-distill chat-log files:

```bash
python scripts/distill.py input.txt [output.md]
```

---

## 脚本用法 · Script Usage

**中文**
`scripts/distill.py` 是一个独立命令行工具，无需 LLM 即可完成基础提纯：

- **输入**：`.txt` / `.md` / `.json` 聊天导出文件；自动识别编码（utf-8 → gbk → utf-8-sig 回退）。
- **功能**：发言人识别、噪音过滤、约束提取（字数 / 语气 / 禁用词 / 必含项 / 参考案例）、角色推断、6-Scheme 生成。
- **输出**：默认打印到终端；传入第二个参数则写入 `.md` 文件（含提纯报告头注释）。

```bash
# 打印到终端
python scripts/distill.py chat-distill-test_input_cn.txt

# 写入文件
python scripts/distill.py chat-distill-test_input.txt 我的方案.md
```

**English**
`scripts/distill.py` is a standalone CLI that performs basic distillation without an LLM:

- **Input**: `.txt` / `.md` / `.json` chat exports; auto-detects encoding (utf-8 → gbk → utf-8-sig fallback).
- **Features**: speaker detection, noise filtering, constraint extraction (length / tone / forbidden / must-include / references), role inference, 6-Scheme generation.
- **Output**: printed to terminal by default; pass a second argument to write a `.md` file (with a distillation-report header comment).

```bash
# Print to terminal
python scripts/distill.py chat-distill-test_input_cn.txt

# Write to file
python scripts/distill.py chat-distill-test_input.txt my-spec.md
```

---

## 工作原理 · How It Works

**中文**
技能执行一条六步流水线：

1. **预处理** — 读取文本/文件/截图 OCR，标注发言人，识别噪音类型。
2. **意图挖掘** — 提取目标、约束、偏好信号，并把批评反转为正向约束。
3. **噪音过滤** — 移除寒暄、情绪填充、冗余确认、跑题与语音错别字。
4. **6-Scheme 编译** — 将提纯信息填入六柱框架。
5. **质量校验** — 零信息丢失、去口语化、隐含推断、可执行性检查。
6. **输出** — 生成包裹在 Markdown 代码块中的最终 Prompt。

**English**
The skill runs a six-step pipeline:

1. **Preprocess** — read text/file/screenshot OCR, tag speakers, classify noise types.
2. **Mine intent** — extract objectives, constraints, preference signals; invert criticism into positive constraints.
3. **Filter noise** — remove greetings, emotional filler, redundant ack, off-topic, and ASR typos.
4. **Compile 6-Scheme** — fill the purified info into the six pillars.
5. **Quality check** — zero information loss, de-colloquialization, implicit inference, executability.
6. **Output** — emit the final Prompt wrapped in a Markdown code block.

---

## 文件结构 · Project Structure

```
chat-distill/
├── chat-distill.skill              # 可安装的技能包 (installable skill package)
├── SKILL.md                        # 技能主文件 (skill definition)
├── chat-distill-readme.md          # 本文件 (this README)
├── 聊天记录提纯.md                  # 原始 Prompt 规范 (raw prompt spec)
├── scripts/
│   ├── distill.py                  # 批量提纯命令行工具 (batch CLI)
│   └── example.py                  # 示例脚本 (example script)
├── references/
│   ├── 6-scheme-guide.md           # 6-Scheme 框架详解 (framework guide)
│   ├── examples.md                 # 完整示例库 (example library)
│   ├── api_reference.md            # API 参考 (API reference)
│   └── original-spec.md            # 原始规范文档 (original spec)
├── assets/
│   └── example_asset.txt           # 资源样例 (sample asset)
├── chat-distill-test_input.txt     # 英文测试样例 (EN test sample)
└── chat-distill-test_input_cn.txt  # 中文测试样例 (CN test sample)
```

---

## 测试样例 · Test Samples

**中文**
仓库内置两组样例，可直接用来验证提纯效果：

- `chat-distill-test_input.txt` — 英文：新能源汽车落地页文案需求。
- `chat-distill-test_input_cn.txt` — 中文：会员积分等级体系简化需求。

运行：`python scripts/distill.py chat-distill-test_input_cn.txt`

**English**
Two built-in samples let you validate distillation immediately:

- `chat-distill-test_input.txt` — English: NEV landing-page copy requirements.
- `chat-distill-test_input_cn.txt` — Chinese: membership tier-system simplification requirements.

Run: `python scripts/distill.py chat-distill-test_input_cn.txt`

---

## 参考资源 · References

- `references/6-scheme-guide.md` — 六柱的设计原则、正反示例与检查清单。
- `references/examples.md` — 端到端完整示例库。
- `references/original-spec.md` — 6-Scheme 框架的原始规范来源。
- `references/api_reference.md` — 脚本 / 接口参考。

---

## 许可证 · License

**中文**
本技能包按项目约定分发的内部工具，使用前请确认所在组织的合规要求。

**English**
This skill package is distributed as an internal tool under project conventions; confirm your organization's compliance requirements before use.

---

*Created: 2026-06-29 · Updated bilingual README: 2026-07-20*

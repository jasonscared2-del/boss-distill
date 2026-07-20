---
name: chat-distill
description: 聊天记录提纯器——将杂乱的多轮微信/即时通讯聊天记录蒸馏成结构化的 6-Scheme Prompt 蓝图。当用户提供聊天记录、对话截图、语音转文字内容，并希望从中提取核心需求、生成 AI Agent 提示词、或将碎片化讨论整理成可执行方案时触发。典型场景：(1) 微信群聊头脑风暴后想落地成方案 (2) 老板在群里零散布置任务需要编译成完整需求文档 (3) 多人讨论的产品/项目需求需要提炼成 PRD 或 SOP (4) 语音转文字的会议记录需要结构化 (5) 任何需要从对话噪音中提取信号并输出 6-Scheme Prompt 的场景。触发词：聊天记录提纯、聊天记录蒸馏、群聊提纯、对话整理、微信记录变方案、聊天变 prompt、chat-distill、6-Scheme。
description_en: "Chat Distill — distills messy multi-turn WeChat / IM chat logs into a structured 6-Scheme Prompt blueprint. Triggers when the user provides chat logs, screenshots, or voice transcripts and wants to extract core requirements, generate AI Agent prompts, or turn fragmented discussion into an executable spec. Scenarios: (1) brainstorm to spec, (2) boss scattered instructions to requirements doc, (3) multi-party discussion to PRD/SOP, (4) voice-transcript meeting notes to structured, (5) any noise-to-signal to 6-Scheme Prompt. Trigger words: 聊天记录提纯, 聊天记录蒸馏, 群聊提纯, 对话整理, 微信记录变方案, 聊天变 prompt, chat-distill, 6-Scheme."
---

# 聊天记录提纯器 (Chat Distill)

将杂乱的多轮聊天记录（微信、飞书、dingtalk、Slack、Facebook、message、link 等）蒸馏成高精度、生产级的 6-Scheme Prompt 蓝图。

Distill messy multi-turn chat logs (WeChat, Feishu, DingTalk, Slack, etc.) into a high-precision, production-ready 6-Scheme Prompt blueprint.

---

## 核心能力 · Core Capability

**中文**
从碎片化的对话中识别发言人、滤除噪音、提炼真实意图，输出一份可直接输入任意 LLM 执行而无歧义的 6-Scheme Prompt。

**English**
Identify speakers from fragmented dialogue, filter out noise, extract true intent, and emit a 6-Scheme Prompt that can be fed directly to any LLM with zero ambiguity.

---

## 执行流水线 · Execution Pipeline

### 第一步：原始数据预处理 · Step 1 — Raw Data Preprocessing

**中文**

1. 读取用户提供的聊天记录（文本粘贴、文件上传、截图 OCR 均可）。
2. 标注发言人身份（A/B/C 或姓名），保留时间线顺序。
3. 识别并标记噪音类型：寒暄、表情包描述、语音转文字错别字、重复确认、跑题闲聊。

**English**

1. Read the chat log provided by the user (pasted text, uploaded file, or screenshot OCR).
2. Tag speaker identities (A/B/C or names) while preserving timeline order.
3. Identify and flag noise types: greetings, emoji descriptions, ASR typos, redundant ack, off-topic chatter.

### 第二步：核心意图挖掘 · Step 2 — Core Intent Mining

**中文**

1. **目标识别**：从对话中提取最终想要交付的资产/动作（文案、方案、代码、报告等）。
2. **约束提取**：字数、语气、格式、deadline、禁止事项等硬性要求。
3. **偏好信号**：用户提及的参考案例、风格倾向、"不要 XX 要 XX"类对比表达。
4. **隐含推理**：老板对草稿的批评 → 反转为正向约束；讨论中的犹豫/妥协 → 标记为低置信度。

**English**

1. **Objective identification**: extract the final asset/action the user wants (copy, spec, code, report, etc.).
2. **Constraint extraction**: hard requirements like length, tone, format, deadline, forbidden items.
3. **Preference signals**: referenced cases, style leanings, "don't want X, want Y" contrasts.
4. **Implicit inference**: a boss critiquing a draft → invert into positive constraints; hesitation/compromise → mark as low confidence.

### 第三步：噪音过滤 · Step 3 — Noise Filtering

**中文**
完全移除以下内容：

- 寒暄问候（"在吗""哈喽""谢谢"）
- 情绪填充（"哈哈""牛""6"）
- 冗余确认（"收到""好的""明白"）
- 跑题闲聊（与核心目标无关的支线对话）
- 语音转文字的明显错别字（自动修正）

**English**
Completely remove the following:

- Greetings ("在吗" / "hi" / "thanks")
- Emotional filler ("哈哈" / "nice" / "lol")
- Redundant ack ("收到" / "ok" / "got it")
- Off-topic chatter (threads unrelated to the core goal)
- Obvious ASR typos (auto-corrected)

### 第四步：6-Scheme 结构化编译 · Step 4 — 6-Scheme Structured Compilation

**中文**
将提纯后的信息填入六柱框架：

#### 1. Role（角色与人设）

- 根据业务领域定义高度具体的专家身份。
- 禁用泛化标签（"助手""AI"），使用精准人设（"资深汽车文案""敏捷产品经理"）。

#### 2. Context（背景与意图）

- 合成业务场景、市场痛点、目标受众。
- 提取对话中触发此任务的显性/隐性动因。

#### 3. Task（核心指令与流水线）

- 按时间顺序拆解执行步骤为 SOP。
- 每步用强动词开头（"撰写""分析""生成"）。

#### 4. Output Format（输出格式）

- 指定精确的响应布局（Markdown 表格、JSON schema、编号列表、特定标签等）。
- 若对话未明确，根据任务类型推断最佳视觉与结构格式。

#### 5. Constraints（约束与红线）

- 列出所有硬边界：长度限制、禁用措辞、强制语气、数据范围。
- 将口语化要求翻译为可执行参数（"别太枯燥" → "保持活泼有力的语气，避免行业术语"）。

#### 6. Examples（Few-Shot 示例）

- 提取对话中提及的参考案例、已接受的草稿、模板。
- 若对话缺少示例，根据业务上下文生成一组高质量的 Input/Output 对。

**English**
Fill the purified info into the six-pillar framework:

#### 1. Role

- Define a highly specific expert identity from the business domain.
- Forbid generic tags ("assistant" / "AI"); use precise personas ("Senior Auto Copywriter" / "Agile PM").

#### 2. Context

- Synthesize the business scenario, market pain points, target audience.
- Extract the explicit/implicit trigger that initiated this task.

#### 3. Task

- Break execution steps into a chronological SOP.
- Start each step with a strong verb ("Write" / "Analyze" / "Generate").

#### 4. Output Format

- Specify the exact response layout (Markdown table, JSON schema, numbered list, tags, etc.).
- If unspecified, infer the best visual/structural format for the task type.

#### 5. Constraints

- List all hard boundaries: length limits, forbidden phrases, mandatory tone, data scope.
- Translate casual requests into actionable params ("don't make it boring" → "keep a vibrant tone, avoid jargon").

#### 6. Examples

- Extract referenced cases, accepted drafts, or templates mentioned in the chat.
- If the chat lacks examples, generate a high-quality Input/Output pair from the business context.

### 第五步：质量校验 · Step 5 — Quality Check

**中文**
编译完成后执行以下检查：

- **零信息丢失**：所有具体数字、deadline、专有名词、功能列表、负面约束 100% 保留。
- **去口语化**：最终 prompt 中不得出现任何口语俚语、结巴、对话填充词。
- **隐含推断**：批评反转为正向标准、模糊表述具体化。
- **可执行性**：生成的 prompt 应可直接输入任意 LLM 执行而无歧义。

**English**
After compilation, run these checks:

- **Zero information loss**: all specific numbers, deadlines, proper nouns, feature lists, negative constraints 100% preserved.
- **De-colloquialization**: no slang, stutters, or conversational fillers in the final prompt.
- **Implicit inference**: criticism inverted to positive criteria; vague phrasing made concrete.
- **Executability**: the prompt must run in any LLM directly with no ambiguity.

### 第六步：输出 · Step 6 — Output

**中文**
生成最终 prompt，包裹在单个 Markdown 代码块中，使用以下精确结构：

**English**
Emit the final prompt wrapped in a single Markdown code block using this exact structure:

```
# 1. Role (角色与人设)
- [精准专家身份]

# 2. Context (背景与意图)
- [业务场景、痛点、触发动因]

# 3. Task (核心指令与流水线)
- [SOP 步骤列表]

# 4. Output Format (输出格式)
- [精确结构要求]

# 5. Constraints (约束与红线)
- [硬边界列表]

# 6. Examples (Few-Shot 示例)
- **Input**: [示例输入]
- **Output**: [示例理想输出]
```

---

## 使用方式 · Usage

### 输入格式 · Input Formats

**中文**
用户可通过以下方式提供聊天记录：

1. **直接粘贴**：将聊天记录文本粘贴到对话中。
2. **文件上传**：上传 .txt / .md / .json 格式的聊天导出文件。
3. **截图**：提供聊天截图（通过 OCR 识别）。
4. **语音转文字**：粘贴语音转文字结果（自动修正错别字）。

**English**
Users can supply chat logs via:

1. **Direct paste**: paste the chat text into the conversation.
2. **File upload**: upload a .txt / .md / .json chat export.
3. **Screenshot**: provide a chat screenshot (recognized via OCR).
4. **Voice-to-text**: paste ASR results (typos auto-corrected).

### 辅助工具 · Helper Tool

**中文**
配套脚本 `scripts/distill.py` 可用于批量处理聊天记录文件：

```bash
python scripts/distill.py input.txt [output.md]
```

**English**
The bundled script `scripts/distill.py` batch-processes chat files:

```bash
python scripts/distill.py input.txt [output.md]
```

---

## 特殊场景处理 · Special Scenarios

### 多人会议记录 · Multi-party Meeting Notes

**中文**：识别主持人、汇报人、参与者角色；按议题分组而非时间线组织；决策项和待办项单独标注。
**English**: Identify host/reporter/participant roles; group by topic rather than timeline; flag decisions and action items separately.

### 老板批评型对话 · Boss-Critique Dialogue

**中文**：将所有批评反转为目标约束（"太技术了" → "避免工程术语，面向非专业读者"；"不够吸引人" → "使用情感化语言，增强场景代入感"）。
**English**: Invert all criticism into target constraints ("too technical" → "avoid engineering jargon, address non-experts"; "not engaging" → "use emotional language, strengthen scene immersion").

### 多轮迭代型对话 · Multi-iteration Dialogue

**中文**：只保留最新版本的反馈；标注版本演进路径（v1→v2→v3 的关键变更点）；最终 prompt 基于最新版本生成。
**English**: Keep only the latest round of feedback; mark the version path (key changes v1→v2→v3); generate the final prompt from the latest version.

### 跨语言对话 · Cross-language Dialogue

**中文**：若聊天记录中混合中英文，输出 prompt 的语言跟随用户最终交付目标；专有名词保留原文，不强行翻译。
**English**: If the chat mixes Chinese and English, the output prompt's language follows the user's final delivery goal; proper nouns stay in the original, not force-translated.

---

## 参考资源 · References

**中文**
详细框架指南见 `references/6-scheme-guide.md`；完整示例库见 `references/examples.md`；原始规范文档见 `references/original-spec.md`。

**English**
See `references/6-scheme-guide.md` for the full framework guide, `references/examples.md` for the example library, and `references/original-spec.md` for the original spec.

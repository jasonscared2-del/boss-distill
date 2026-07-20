"""
聊天记录提纯器 (Chat Distill)
将原始聊天记录文件转换为结构化 6-Scheme Prompt

用法：
  python distill.py input.txt [output.md]

示例：
  python distill.py 聊天记录.txt
  python distill.py 聊天记录.txt 我的方案.md
"""

import re
import sys
import json
from pathlib import Path

# ============================================================
# 噪音模式定义
# ============================================================

NOISE_PATTERNS = [
    # 寒暄问候
    r"^(在吗|你好|您好|hi|hello|哈喽|嗨| hey)[\s,，.。]*$",
    r"^(收到|好的|好的好的|好的哈|OK|ok|好嘞|收到！)$",
    r"^(谢谢|感谢|多谢|3Q|3q)$",
    r"^(哈哈|哈哈哈|哈哈哈哈|hhhh|haha|😂|😄|👍)$",
    r"^(明白|了解|知道了|清楚)$",
    r"^(请问一下|问一下|想请教)$",
    r"^(抱歉|不好意思|打扰了)$",
    r"^(没问题|没问题没问题)$",
    # 确认类
    r"^(对|是的|对对|对对对|没错|是的是的)$",
    r"^(我也是|同感|我也是这么想的)$",
    # 重复确认
    r"^(收到收到|好的好的|明白了明白了)$",
]

# 口语化表达映射表
SLANG_CORRECTIONS = {
    "这个": "该",
    "那会": "当时",
    "整": "处理",
    "搞": "实施",
    "弄": "制作",
    "啥": "什么",
    "咋": "怎么",
    "肿么": "怎么",
    "为啥": "为什么",
    "酱紫": "这样子",
    "这样子": "这样",
    "介个": "这个",
    "银家": "人家",
    "神马": "什么",
    "木有": "没有",
    "有滴": "有点",
}


def is_noise(line: str) -> bool:
    """判断一行是否为噪音"""
    line = line.strip()
    if not line:
        return True
    if len(line) <= 2:
        return True
    for pattern in NOISE_PATTERNS:
        if re.match(pattern, line, re.IGNORECASE):
            return True
    return False


def extract_speakers(lines: list[str]) -> dict[str, list[str]]:
    """按发言人分组"""
    speakers = {}
    current_speaker = None

    # 发言人识别模式：中文冒号、"Name:"、"[Name]"、"Name -" 等
    speaker_patterns = [
        r"^([A-Za-z\u4e00-\u9fa5]{1,20})[：:]\s*(.*)",
        r"^\[([A-Za-z\u4e00-\u9fa5]{1,20})\]\s*(.*)",
        r"^<([A-Za-z\u4e00-\u9fa5]{1,20})>\s*(.*)",
        r"^([A-Za-z\u4e00-\u9fa5]{1,20})\s+[0-9]{2}:\d{2}\s*-\s*(.*)",
    ]

    for line in lines:
        line = line.strip()
        if not line:
            continue

        speaker_found = False
        for pattern in speaker_patterns:
            m = re.match(pattern, line)
            if m:
                speaker = m.group(1).strip()
                content = m.group(2).strip()
                if speaker not in speakers:
                    speakers[speaker] = []
                if content:
                    speakers[speaker].append(content)
                current_speaker = speaker
                speaker_found = True
                break

        if not speaker_found and current_speaker:
            speakers[current_speaker].append(line)

    return speakers


def extract_constraints(speakers: dict[str, list[str]]) -> dict:
    """从聊天记录中提取约束和偏好"""
    all_text = " ".join([" ".join(msgs) for msgs in speakers.values()])

    constraints = {
        "length": None,
        "tone": [],
        "forbidden": [],
        "must_include": [],
        "format": None,
        "deadline": None,
        "audience": None,
        "references": [],
    }

    # 长度约束
    length_patterns = [
        (r"不超过?\s*(\d+)\s*字", lambda m: f"不超过 {m.group(1)} 字"),
        (r"(\d+)\s*字以内", lambda m: f"{m.group(1)} 字以内"),
        (r"(\d+)\s*字左右", lambda m: f"约 {m.group(1)} 字"),
    ]
    for pattern, fmt in length_patterns:
        m = re.search(pattern, all_text)
        if m:
            constraints["length"] = fmt(m)

    # 语气约束
    tone_keywords = {
        "专业": "专业严谨",
        "活泼": "活泼有力",
        "轻松": "轻松易懂",
        "正式": "正式规范",
        "学术": "学术规范",
        "情感": "情感化",
        "场景化": "场景化描写",
    }
    for keyword, tone in tone_keywords.items():
        if keyword in all_text:
            constraints["tone"].append(tone)

    # 禁用词
    forbid_patterns = [
        r"不要\s+([^，,。\n]{1,50})",
        r"别\s+([^，,。\n]{1,30})",
        r"禁止\s+([^，,。\n]{1,30})",
        r"不得\s+([^，,。\n]{1,30})",
    ]
    for pattern in forbid_patterns:
        for match in re.finditer(pattern, all_text):
            item = match.group(1).strip()
            if item and item not in constraints["forbidden"]:
                constraints["forbidden"].append(item)

    # 必须包含
    must_patterns = [
        r"必须\s+([^，,。\n]{1,30})",
        r"要提到\s+([^，,。\n]{1,30})",
        r"包含\s+([^，,。\n]{1,30})",
    ]
    for pattern in must_patterns:
        for match in re.finditer(pattern, all_text):
            item = match.group(1).strip()
            if item and item not in constraints["must_include"]:
                constraints["must_include"].append(item)

    # 参考案例
    ref_patterns = [
        r"像\s+([^样那样]{1,20})\s+那样",
        r"参考\s+([^，,。\n]{1,30})",
        r"和\s+([^样那样]{1,20})\s+一样",
    ]
    for pattern in ref_patterns:
        for match in re.finditer(pattern, all_text):
            ref = match.group(1).strip()
            if ref and ref not in constraints["references"]:
                constraints["references"].append(ref)

    return constraints


def identify_core_objective(speakers: dict[str, list[str]]) -> str:
    """识别核心目标"""
    all_text = "\n".join(["\n".join(msgs) for msgs in speakers.values()])

    # 意图关键词分析
    intent_keywords = {
        "写": "撰写/生成",
        "做": "制作/完成",
        "生成": "生成",
        "整理": "整理/提炼",
        "分析": "分析",
        "设计": "设计",
        "策划": "策划",
        "规划": "规划",
        "评审": "评审",
        "落地": "落地实施",
    }

    intents_found = []
    for keyword, intent in intent_keywords.items():
        if keyword in all_text:
            intents_found.append(intent)

    if intents_found:
        # 取最常见的意图
        return f"基于聊天记录内容，{max(set(intents_found), key=intents_found.count)}"

    return "整理聊天记录中的讨论内容"


def generate_6scheme_prompt(
    speakers: dict[str, list[str]],
    constraints: dict,
    core_objective: str,
) -> str:
    """生成 6-Scheme Prompt"""

    # 从聊天内容推断角色
    all_text = " ".join([" ".join(msgs) for msgs in speakers.values()])
    role_map = {
        ("文案", "落地页", "宣传"): "资深品牌文案策划",
        ("产品", "需求", "PRD", "功能"): "资深产品经理",
        ("技术", "开发", "代码", "接口"): "高级技术架构师",
        ("运营", "推广", "增长", "留存"): "资深运营策略专家",
        ("会议", "评审", "纪要"): "项目管理助理",
        ("报告", "分析", "数据"): "高级数据分析专家",
        ("法律", "合同", "合规"): "企业法务顾问",
    }

    detected_role = "专业顾问"
    for keywords, role in role_map.items():
        if any(k in all_text for k in keywords):
            detected_role = role
            break

    # 构建输出
    output = []

    output.append("# 1. Role (角色与人设)")
    output.append(f"- {detected_role}，精通聊天记录中涉及的业务领域，能准确理解多方讨论的真实意图。")

    output.append("")
    output.append("# 2. Context (背景与意图)")
    output.append(f"- {core_objective}。")
    output.append("- 以下为相关人员的讨论记录：")
    for name, msgs in speakers.items():
        preview = "；".join(msgs[:2]) if msgs else ""
        if len(preview) > 80:
            preview = preview[:77] + "..."
        output.append(f"  * {name}：{preview}")

    output.append("")
    output.append("# 3. Task (核心指令与流水线)")
    output.append("基于上述聊天记录，执行以下步骤：")
    output.append("1. 过滤对话噪音（寒暄、确认、跑题），提取有效信息")
    output.append("2. 识别核心需求和约束条件")
    output.append("3. 按任务类型生成对应的结构化输出")
    output.append("4. 校验输出是否符合所有约束条件")

    output.append("")
    output.append("# 4. Output Format (输出格式)")

    format_hints = constraints.get("format") or "结构化 Markdown 文档，根据任务类型采用合适的表格、列表或分节格式"
    output.append(f"- {format_hints}")

    output.append("")
    output.append("# 5. Constraints (约束与红线)")

    if constraints.get("length"):
        output.append(f"- **字数限制**：{constraints['length']}")

    if constraints.get("tone"):
        tones = "、".join(constraints["tone"])
        output.append(f"- **语气要求**：{tones}")

    if constraints.get("forbidden"):
        forbids = "；".join(constraints["forbidden"])
        output.append(f"- **禁用内容**：{forbids}")

    if constraints.get("must_include"):
        musts = "、".join(constraints["must_include"])
        output.append(f"- **必须包含**：{musts}")

    if constraints.get("deadline"):
        output.append(f"- **截止时间**：{constraints['deadline']}")

    if not any([constraints.get("length"), constraints.get("tone"),
                constraints.get("forbidden"), constraints.get("must_include")]):
        output.append("- 根据聊天记录中的隐含要求自行推断合理的约束条件")

    output.append("")
    output.append("# 6. Examples (Few-Shot 示例)")
    output.append("以下为参考案例：")
    if constraints.get("references"):
        for ref in constraints["references"]:
            output.append(f"- 参考风格：{ref}")
    else:
        output.append("- 本次无明确参考案例，请根据业务领域自行生成高质量示例")
    output.append("")
    output.append("**Input**: 聊天记录中的原始讨论内容")
    output.append("**Output**: 提纯后的核心需求与执行方案")

    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"[ERROR] 文件不存在: {input_file}")
        sys.exit(1)

    output_file = Path(sys.argv[2]) if len(sys.argv) >= 3 else None

    # 读取文件
    try:
        content = input_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            content = input_file.read_text(encoding="gbk")
        except UnicodeDecodeError:
            content = input_file.read_text(encoding="utf-8-sig")

    lines = content.split("\n")

    # 提纯流程
    speakers = extract_speakers(lines)
    constraints = extract_constraints(speakers)
    core_objective = identify_core_objective(speakers)
    prompt = generate_6scheme_prompt(speakers, constraints, core_objective)

    # 输出
    final_output = f"""<!--
聊天记录提纯报告
========================================
输入文件：{input_file.name}
发言人：{len(speakers)} 人
约束识别：{len([c for c in constraints.values() if c]) } 项
========================================
-->

{prompt}
"""

    if output_file:
        output_file.write_text(final_output, encoding="utf-8")
        print(f"[OK] 已生成: {output_file}")
    else:
        print(final_output)


if __name__ == "__main__":
    main()

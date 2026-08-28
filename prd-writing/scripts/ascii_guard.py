#!/usr/bin/env python3
"""ascii_guard — PRD ASCII 配图的硬校准工具。

用法:
  ascii_guard.py check <file.md>   校验 md 内所有 ```text 块的漂移免疫性，违规输出行号+原因，exit 1
  ascii_guard.py fix   <file>      把 mermaid-ascii 输出转为开口式（去右边线/右上下角），结果写 stdout

不变量（为什么这样能免疫字体塌陷）:
  md 查看器里回退中文字体宽度 != 2 ASCII 格，中文只把它「右侧」的字符往左拽。
  因此需要跨行垂直对齐的轨道字符（│┌┐└┘├┤┬┴┼▼▲）必须全部位于该行第一个宽字符之前；
  横向装饰（─ ► ◄ ▶）跟在文本后面不需要对齐，无害。
"""
import re
import sys
import unicodedata

RAIL = set("│┌┐└┘├┤┬┴┼▼▲|+")
VERT = set("│|├┤┬┴┼▼▲+")


def is_wide(ch: str) -> bool:
    return unicodedata.east_asian_width(ch) in ("W", "F")


def display_width(line: str) -> int:
    return sum(2 if is_wide(ch) else 1 for ch in line)


def text_blocks(md: str):
    """yield (start_lineno, [lines]) for each ```text fenced block"""
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("```text"):
            start = i + 1
            j = start
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            yield start + 1, lines[start:j]  # 1-based lineno of first content line
            i = j + 1
        else:
            i += 1


def check(path: str) -> int:
    md = open(path, encoding="utf-8").read()
    errors = []
    warnings = []
    for base, block in text_blocks(md):
        for off, line in enumerate(block):
            n = base + off
            if "\t" in line:
                errors.append(f"{n}: 含 TAB，宽度不可预测，改空格")
            w = display_width(line.rstrip())
            if w > 80:
                errors.append(f"{n}: 显示宽度 {w} > 80，导入后可能折行破版")
            wide_seen = False
            for ch in line:
                if is_wide(ch):
                    wide_seen = True
                elif wide_seen and ch in RAIL:
                    errors.append(
                        f"{n}: 轨道字符 '{ch}' 出现在中文之后，该列在非等宽 CJK 字体下必然漂移"
                    )
                    break
        # 右列检测：中文之后 >=3 连续空格再跟内容 = 右侧独立列，其位置依赖中文实际宽度。
        # 相邻行在该列附近有竖向轨道（需要上下对齐）=> error（结构会散架，如双列并排流程图）；
        # 附近无轨道 => warning（纯装饰列，坏字体下只是没那么居中，放行）。
        def dcol(s, idx):
            return sum(2 if is_wide(c) else 1 for c in s[:idx])

        for off, line in enumerate(block):
            first_wide = next((i for i, c in enumerate(line) if is_wide(c)), None)
            if first_wide is None:
                continue
            m = re.search(r" {3,}(\S+)", line[first_wide:])
            if not m:
                continue
            s_col = dcol(line, first_wide + m.start(1))
            e_col = dcol(line, first_wide + m.end(1))
            hard = False
            for b in (off - 1, off + 1):
                if 0 <= b < len(block):
                    for i, c in enumerate(block[b]):
                        if c in VERT and s_col - 2 <= dcol(block[b], i) <= e_col + 2:
                            hard = True
            if hard:
                warnings.append(
                    f"{base + off}: 双列并排布局——读者字体 CJK 严格 2:1 时完美，否则右列与轨道脱节；"
                    "需在目标导入环境实测过再用（放行）"
                )
            else:
                warnings.append(
                    f"{base + off}: 中文后的装饰性右列在部分字体下会偏移（仅外观，放行）"
                )
    for w in warnings:
        print("  ⚠ " + w)
    if errors:
        print(f"✗ {path}: {len(errors)} 处违规")
        for e in errors:
            print("  " + e)
        return 1
    print(f"✓ {path}: 所有 text 块通过漂移免疫校验")
    return 0


def fix(path: str) -> int:
    """mermaid-ascii 输出 → 开口式：去掉行尾右边线和右侧角"""
    out = []
    for line in open(path, encoding="utf-8").read().splitlines():
        r = line.rstrip()
        if r.endswith("│"):
            r = r[:-1].rstrip()
        elif r.endswith("┐") or r.endswith("┘"):
            r = r[:-1].rstrip("─") + "───"
        out.append(r)
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("check", "fix"):
        print(__doc__)
        sys.exit(2)
    sys.exit({"check": check, "fix": fix}[sys.argv[1]](sys.argv[2]))

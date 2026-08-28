# PM Skills

给 AI 编程助手用的一套产品经理 skill：竞品拆解、开源现状调研 → 需求评估 → PRD 写作 → 埋点设计，
外加一个把全流程串起来、在关键节点停下等人确认的路由（pm-flow）。
为 Claude Code 编写（标准 SKILL.md 格式），任何能读 skill 文件夹的 agent（Codex、Gemini CLI 等）均可使用。

## 工作流关系

```text
一个功能想法（"完整过一遍"走 pm-flow；单点问题直接用对应 skill）
    │
    ▼
feature-teardown    竞品怎么做的、我们是不是已经有了
    │
    ├─ 闸门A ▶ 已经有了，是入口/认知问题 → 给改入口建议，流程终止
    ▼
prior-art           有没有开源现成实现（可跳过；产出作 Effort 依据）
    │
    ▼
requirement-eval    值不值得做（KANO 定位、RICE 打分 → 评估初稿）
    │
    ├─ 闸门B ▶ 建议「暂不做/补数据」→ 停，结论交还用户
    ▼
prd-writing         一页纸骨架 → 闸门C：骨架经用户确认才展开正文
    │
    ├─ 阶段3 调用 ▶ tracking-plan    埋点事件与成功指标（也可独立使用）
    ▼
产出落盘：产品文件夹下 prd/ eval/ tracking/
```

顺序、闸门与阶段间交接物由 [pm-flow](pm-flow/SKILL.md) 定义；五个执行 skill 保持独立可用，
pm-flow 只接"从调研到 PRD 完整走一遍"的全流程意图。

想法还没成型的发散/访谈阶段，推荐上游原版 [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) 的 `interview-me` 和 `idea-refine`，与本套件无缝衔接。

## 安装

全套（Claude Code）：

```bash
git clone https://github.com/Timi-Fish/pm-skills.git /tmp/pm-skills && cp -R /tmp/pm-skills/{prd-writing,tracking-plan,requirement-eval,feature-teardown,prior-art,pm-flow} ~/.claude/skills/
```

只要某一个（以 prd-writing 为例）：

```bash
npx degit Timi-Fish/pm-skills/prd-writing ~/.claude/skills/prd-writing
```

四个 skill 可独立使用：只装 tracking-plan 或 requirement-eval 时，它们会跳过共享上下文协议、改为会话内直接问答。装齐后自动共享产品上下文（见下）。

## 产品上下文：一次访谈，多产品复用

三个核心 skill（prd-writing / requirement-eval / tracking-plan）共享一套产品档案机制，协议见 [prd-writing/PRODUCT-CONTEXT.md](prd-writing/PRODUCT-CONTEXT.md)：

- 每个产品一个 `product.md`（覆盖端、知识库位置、输出格式、埋点体系、术语表），存放于 PM 工作区（默认 `~/Documents/PM/<产品名>/`，首次访谈可改；Windows 用户建议首访时指定路径）
- **谁先被调用谁访谈，一个产品只问一次**——先跑了需求评估，写 PRD 时不会再重复问
- 在产品 repo 里干活时，仓库根的 `.prd/product.md` 优先
- 换产品零改动：新增一个产品文件夹即可，skill 本体保持通用

## PRD 配图：ASCII 硬校准

markdown PRD 的常见导入目标（在线文档类产品）不渲染 mermaid、图片链接和 HTML 标签，等宽代码块是唯一稳定载体。prd-writing 内置一套经过校准的 ASCII 画法规格（纯 ASCII 结构字符、结构在左文本在右、漏斗四列布局），并附校验器：

```bash
python3 prd-writing/scripts/ascii_guard.py check 你的PRD.md
```

Claude Code 用户可选配 PostToolUse hook 让校验自动兜底（加入 `~/.claude/settings.json`）：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path // empty' | { read -r f; case \"$f\" in *.md) out=$(python3 \"$HOME/.claude/skills/prd-writing/scripts/ascii_guard.py\" check \"$f\" 2>&1) || { printf '%s\\n' \"$out\" 1>&2; exit 2; };; esac; }",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

其他 agent 的用户忽略此节，skill 内的 check 命令是主路径。

## 四个 skill 一览

| Skill | 做什么 | 独立可用 |
|---|---|---|
| [prd-writing](prd-writing/SKILL.md) | 一页纸骨架确认 → 分档展开（Lite/Standard/Complex 硬字数预算）→ ASCII 配图硬校准 → 调用 tracking-plan | ✅ |
| [requirement-eval](requirement-eval/SKILL.md) | KANO 定位 + RICE 打分，产出评估初稿与建议；强制暴露估算假设、压低无数据支撑的 Confidence | ✅ |
| [tracking-plan](tracking-plan/SKILL.md) | 先定北极星指标再列事件：成功指标 → 漏斗 → 事件清单 → 上报验收 | ✅ |
| [feature-teardown](feature-teardown/SKILL.md) | 功能级竞品拆解：别人家怎么做、用户路径几步、我们是不是已经有了只是用户找不到 | ✅ |
| [prior-art](prior-art/SKILL.md) | 动手写代码前查有没有开源现成的：发现分类（灵感/证据/可复用）、license 闸门；产出可作 RICE 的 Effort 依据和评审说服材料 | ✅ |
| [pm-flow](pm-flow/SKILL.md) | 全流程路由：按序驱动上面五个，三个闸门处停下等人确认；只接全流程意图，不劫持单点请求 | ✅ |

语言：全部为中文，面向中文 PM 工作流。

## License

MIT © [Timi-Fish](https://github.com/Timi-Fish)

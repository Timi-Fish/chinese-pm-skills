# Chinese PM Skills

> Product-manager skills for AI coding agents: competitor teardown → requirement evaluation → PRD writing → tracking plan, with human-in-the-loop gates. Written in Chinese.

这是一套给 AI 编程助手用的中文产品经理技能包。装上以后，你只要说"这个功能值不值得做""帮我写份 PRD""设计一下埋点"，AI 就会按对应流程干活；遇到"是否继续做"这类关键决策时，它会先停下来问你，不会擅自替你拍板。

6 个技能（5 个干活的 + 1 个总流程）可以整套装，也可以只装你需要的某一个。

适合**功能产品经理**（做功能规划、写 PRD、对接研发的工作流）。策略产品（推荐/搜索/风控这类以实验设计、指标口径、策略迭代为主的岗位）的工作物形态不同，本套件暂不适配。

## 立即试用

装好后直接用自然语言说需求，不用记技能名称：

```text
帮我评估「笔记批量导出」这个需求值不值得做
为「AI 自动打标签」写一份 PRD
给收藏功能设计一下埋点
从竞品调研到 PRD，完整分析「语音笔记自动总结」
```

第一次在一个新产品上使用时，AI 会先问你几个基本信息（产品定位、支持哪些平台、有没有资料库等），存成产品档案，之后所有技能共用，不再重复问。

## 安装

Claude Code 一键装全套：

```bash
git clone https://github.com/Timi-Fish/chinese-pm-skills.git /tmp/pm-skills && cp -R /tmp/pm-skills/{prd-writing,tracking-plan,requirement-eval,feature-teardown,prior-art,pm-flow} ~/.claude/skills/
```

只装某一个（以 prd-writing 为例）：

```bash
npx degit Timi-Fish/chinese-pm-skills/prd-writing ~/.claude/skills/prd-writing
```

每个技能都可独立使用：只装其中一个时，它会现场问你几句必要信息，不依赖共享的产品档案；装齐后自动共用档案。

其他工具（Codex、Gemini CLI 等能读 `SKILL.md` 的 agent）：理论兼容——技能就是纯 markdown 文件夹，拷到对应工具的 skills 目录即可，但各平台的安装路径我们尚未逐一验证，欢迎反馈。

## 六个技能

| 技能 | 做什么 |
|---|---|
| [prd-writing](prd-writing/SKILL.md) | 先给一页纸骨架等你确认，再按篇幅档位展开（防止一上来就是万字 PRD）；配图用字符图，粘进任何在线文档都不乱 |
| [requirement-eval](requirement-eval/SKILL.md) | 用 KANO（需求分类）和 RICE（打分排序）评估值不值得做；评分注明数据来源，没有真实数据就明确标"估算"，不制造虚假的精确感 |
| [tracking-plan](tracking-plan/SKILL.md) | 先定成功指标再列埋点：北极星指标 → 转化漏斗 → 事件清单 → 上报验收 |
| [feature-teardown](feature-teardown/SKILL.md) | 功能级竞品拆解：别人家怎么做、用户路径几步、我们是不是其实已经有了只是用户找不到 |
| [prior-art](prior-art/SKILL.md) | 写代码前查有没有能直接用或抄的开源实现（会核对 license）；结论可作需求评估里工作量估计的依据，也是评审时说服研发的材料 |
| [pm-flow](pm-flow/SKILL.md) | 总流程：把上面五个按序串起来，在三个确认点停下等你拍板；只在你要"完整走一遍"时出场，单点请求不受影响 |

## 完整工作流

说"完整分析一下 XX 功能"时，pm-flow 按下图驱动（图中 GATE = 停下来等你确认的点）：

```text
pm-flow                        # 总流程：按序驱动五个，确认点停下等你
│
├── feature-teardown           # 竞品怎么做的、我们是不是已经有了
│      └─ GATE A               #   已经有了 → 给改入口建议，不再往下做
├── prior-art                  # 有没有开源现成实现（可跳过）
├── requirement-eval           # 值不值得做：KANO 分类、RICE 打分
│      └─ GATE B               #   建议「暂不做/补数据」→ 先请你决定
└── prd-writing                # 一页纸骨架 → 分档展开 → 字符图检查
       ├─ GATE C               #   骨架和篇幅经你确认才展开正文
       └── tracking-plan       # 埋点事件与成功指标
```

上一步的结果会真的用在下一步：prior-art 查到的开源实现作为需求评估里工作量（Effort）的依据；评估结论写进 PRD 的需求背景。

想法还没成型、连"要做什么功能"都说不清的阶段，推荐上游原版 [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) 的 `interview-me` 和 `idea-refine`，与本套件无缝衔接。

## 产品档案：一次访谈，多产品复用

三个核心技能（prd-writing / requirement-eval / tracking-plan）共用一份产品档案 `product.md`，协议见 [prd-writing/PRODUCT-CONTEXT.md](prd-writing/PRODUCT-CONTEXT.md)：

- 每个产品一份档案：定位、覆盖端（支持 iOS / Android / Web 等哪些平台）、资料库位置、输出格式偏好、埋点规范、术语表
- 存放于 PM 工作区（默认 `~/Documents/PM/<产品名>/`，第一次访谈时可改；Windows 用户建议指定路径）
- 哪个技能先被使用，哪个负责建档，一个产品只问一次
- 在产品代码仓库里干活时，仓库根的 `.prd/product.md` 优先
- 换产品不用改任何技能文件，新建一个产品文件夹即可

## 可选：PRD 字符图排版检查

把 markdown 格式的 PRD 粘进在线文档（语雀 / 飞书 / Notion 一类）时，流程图（mermaid）、图片链接和 HTML 标签通常都不渲染，只有等宽代码块在哪儿都长一个样。所以 prd-writing 的配图用字符图，并附了一个排版检查器，专查"在别人的字体里会不会歪"：

```bash
python3 prd-writing/scripts/ascii_guard.py check 你的PRD.md
```

<details>
<summary>Claude Code 用户：配置保存 md 时自动检查（可选）</summary>

加入 `~/.claude/settings.json`，之后任何 md 文件保存时自动校验，违规会直接提示 AI 修正：

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

</details>

其他工具的用户忽略本节折叠部分，手动跑上面的检查命令即可。

## License

MIT © [Timi-Fish](https://github.com/Timi-Fish)

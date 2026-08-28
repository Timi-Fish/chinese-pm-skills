---
name: pm-flow
description: >-
  PM 全流程路由：把 feature-teardown → prior-art → requirement-eval → prd-writing（含 tracking-plan）
  按序串起来，在三个闸门处停下等人确认。
  触发词：完整分析这个功能、从头到尾过一遍、这个想法全流程走一下、从调研到PRD、pm-flow。
  只接全流程意图；单点问题（只要埋点/只要评估/只写PRD）直接用对应 skill，不要进本流程。
---

# PM Flow

一个功能想法进来，按序驱动五个 skill 走完"该不该做 → 值不值得做 → 怎么做"，
在闸门处停下等人。本 skill **只写顺序、闸门和交接物**，每个阶段怎么干以对应 SKILL.md 为准，
这里不复制任何阶段逻辑。

## 进入条件（不符合就一句话退出）

用户要的是**从调研到落地的完整链路**。以下情况不要进流程，直接路由到单个 skill：

- 只问竞品 → [feature-teardown](../feature-teardown/SKILL.md)
- 只问有没有开源实现 → [prior-art](../prior-art/SKILL.md)
- 只要评估结论 → [requirement-eval](../requirement-eval/SKILL.md)
- 直接要写 PRD / 埋点 → [prd-writing](../prd-writing/SKILL.md) / [tracking-plan](../tracking-plan/SKILL.md)

想法还没成型（连"要做什么功能"都说不清）→ 先推荐上游
[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) 的 interview-me / idea-refine，
成型后再进本流程。

## 流程与闸门

```text
一个功能想法
    │
    ▼
阶段0  产品上下文（PRODUCT-CONTEXT 协议：定位或建立 product.md）
    │
    ▼
阶段1  feature-teardown  竞品怎么做的、我们是不是已经有了
    │
    ├─ 闸门A ▶ 结论是「已经有了，是入口/认知问题」→ 给改入口建议，流程终止
    ▼
阶段2  prior-art  有没有开源现成实现（纯交互/文案类功能可跳过，跳过要说明）
    │
    ▼
阶段3  requirement-eval  值不值得做（prior-art 的发现表作 Effort 依据）
    │
    ├─ 闸门B ▶ 建议是「暂不做 / 补数据再定」→ 停，结论交还用户，等明确指示
    ▼
阶段4  prd-writing  一页纸骨架 → 闸门C：骨架和档位经用户确认才展开正文
    │
    ├─ 其阶段3 调用 ▶ tracking-plan  埋点与成功指标
    ▼
收尾  产物清单与一句话总结
```

**三个闸门都必须真的停**：闸门是流程的产品价值所在，不是形式。自动通关等于把 PM 的判断责任
偷偷接过来了——不许。

## 阶段间交接物

| 阶段 | 读什么 | 写什么（落产品文件夹） |
|---|---|---|
| 0 产品上下文 | product.md（无则访谈建立） | product.md |
| 1 teardown | 用户输入 + product.md 的知识库 | 拆解结论（结论四选一 + 竞品表） |
| 2 prior-art | 阶段1 的功能定义 | 发现表（类型 + license） |
| 3 eval | 阶段1 结论作需求来源，阶段2 发现表作 Effort 依据 | `eval/<需求名>.md` |
| 4 PRD | 阶段3 结论写进需求背景，product.md 全量 | `prd/<需求名>.md` 与埋点章节 |

上一阶段的产出**必须真的被下一阶段引用**（eval 的 Effort 依据栏引 prior-art 的发现、
PRD 背景引 eval 结论），不许各写各的。

## 反模式

- 劫持单点请求：用户只要个埋点方案，被拉着从竞品拆解走一遍
- 闸门自动通关：teardown 明明早退了还继续往下走
- 在本文件里给阶段逻辑打补丁——阶段逻辑归各自 SKILL.md，这里只管顺序
- 跳过阶段不声明：可以跳（如 prior-art），但要写明跳了和为什么

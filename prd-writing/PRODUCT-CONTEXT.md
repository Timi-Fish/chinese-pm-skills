# 产品上下文协议（prd-writing / requirement-eval / tracking-plan 共享）

一套 skill 服务多个产品：skill 本体通用，产品差异全部存在每个产品自己的 `product.md` 里。
换产品不改 skill，只新增一个产品文件夹。

## 定位顺序

1. `<cwd>/.prd/product.md` —— 在产品 repo 里干活时用，优先级最高
2. `<PM 工作区>/<产品名>/product.md` —— 中央管理，按用户提到的产品名匹配文件夹；
   工作区默认 `~/Documents/PM`，首次访谈可改（改了就以 product.md 实际所在位置为准）
3. 都没有 → 触发首次访谈（见下），访谈结果写入工作区的 `<产品名>/product.md`

## 首次访谈规则

- **谁先被调用谁问**：三个 skill 里第一个在新产品上运行的负责访谈并落盘
- **一个产品只访谈一次**：product.md 存在则只读；个别字段缺失只补问该字段，不重问全套
- 用 AskUserQuestion 一轮问完，不挤牙膏

## product.md 模板

```markdown
# <产品名>

- **一句话定位**：
- **覆盖端**：<自由列举，如 iOS / Android / Web / 桌面端>
- **产品知识库**：<路径或 URL；没有写"无">
- **PRD 默认输出格式**：markdown | html
- **PRD 配图方式**：ascii（默认，等宽代码块字符画，任何导入环境都稳）| mermaid fence（读者确认用 Obsidian/GitHub 等能渲染 mermaid 的环境）；html 产出一律 diagram-design inline SVG，不受此字段影响
- **双列 ASCII 实测**：未测 | OK（在目标导入环境贴过双列并排图且对齐正常——OK 才允许用双列流程图，视觉更好）
- **产品关键特性**：<如 离线优先 / 实时协作 / 单机工具——决定 PRD 异常场景章节写什么>

## 埋点体系（tracking-plan 用；未接入埋点则整节写"未接入"）
- **命名规范**：<如 模块_对象_动作，全小写下划线>
- **公共属性**：<如 user_id, platform, app_version>
- **上报通道**：<各端怎么上报>
- **看板/分析工具**：<如 Amplitude / 自建>

## 数据现状（requirement-eval 的 Confidence 依据）
- **有无真实行为数据**：<有/无；无真实数据时 Reach 靠估，Confidence ≤50%>

## 术语表
| 术语 | 含义 |
|------|------|
```

## 产出落盘

全部落在产品文件夹（product.md 所在目录）下：

- PRD → `<产品文件夹>/prd/`
- 需求评估 → `<产品文件夹>/eval/`
- 埋点方案（独立产出时）→ `<产品文件夹>/tracking/`
- repo 场景统一落 `<cwd>/.prd/` 下的同名子目录

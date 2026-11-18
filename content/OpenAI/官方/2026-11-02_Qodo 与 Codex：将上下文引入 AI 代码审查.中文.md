# Qodo 与 Codex：将上下文引入 AI 代码审查（Qodo builds context into AI code review with Codex）

> 原文：[Qodo builds context into AI code review with Codex](https://openai.com/index/qodo-codex-plugin/) · OpenAI · 2026-11-02
> 本文由 Kimi CLI 使用 Kimi K3-256k 全文翻译，并由 Agent 校对；已取得全文翻译和转载授权。
> 作者：OpenAI

2026年11月2日

初创公司

Qodo 将组织上下文与代码库标准引入 Codex，帮助开发者跨仓库捕获 P0 级问题。

[开始构建](https://openai.com/startups)

[![OpenAI_DevDay_Interview-Studio-Series-iss-06-Qodo_90s_16x9_v3_2026-10-27](../../../assets/articles/5fac02a7030911ab/vimeo-1241442369-preview.gif)](https://player.vimeo.com/video/1241442369?h=33acf4caa2&badge=0&autopause=0&player_id=0&app_id=58479)

[观看原始视频：OpenAI_DevDay_Interview-Studio-Series-iss-06-Qodo_90s_16x9_v3_2026-10-27](https://player.vimeo.com/video/1241442369?h=33acf4caa2&badge=0&autopause=0&player_id=0&app_id=58479)

公司规模：初创公司

地区：北美

行业：科技

产品：API、Codex

[Qodo⁠](https://www.qodo.ai/) 致力于构建用于代码审查和软件质量的 AI 工具，让编程智能体获得理解其所修改代码所需的组织知识。联合创始人兼首席执行官 Itamar Friedman 称之为"编程智能体的最佳拍档"。

Qodo 使用包括 GPT‑6 Astra 在内的 OpenAI 模型来汇集工程知识、审查代码并监控软件质量。其 Codex 插件将这些上下文和审查能力带入开发者的编程会话中。

> "我们喜爱 OpenAI 的模型。我们追求最前沿、推理能力最强的模型，同时也追求那些速度非常快的模型。"

——Itamar Friedman，Qodo 联合创始人兼首席执行官

## 借助 Codex 跨仓库发现 P0 级缺陷

Itamar 描述的客户环境可能横跨一万个甚至更多仓库，其中一个本地代码改动就可能导致下游服务崩溃，即便这个改动本身看起来是正确的。Qodo 在 Codex 市场中构建了一个插件来解决这个问题。

"Codex 非常擅长承接本地任务并高效地完成它，"Itamar 说。Qodo 的插件通过 Qodo 的 Agentic Toolbox，让 Codex 能够访问代码库知识、组织规则以及独立审查能力。

有了上下文，Codex 可以顾及跨仓库的依赖关系，包括由不同 Git 服务商托管的仓库，或通过 Kafka 连接的服务。"Qodo 会建立这种连接，帮助 Codex 从整体视角审视软件，从而不遗漏那些 P0 级缺陷，"Itamar 说。

## 在保留人类判断的同时实现审查自动化

在 Codex 开始编写代码之前，它可以使用 Qodo 的插件检索相关的代码库规则以及拉取请求的历史与模式。在 Codex 完成修改后，Qodo 会对这些修改进行审查，并在同一会话中将其审查结果直接返回给 Codex——这一切都发生在开发者发起拉取请求之前。

Qodo 的 AI 开发者关系负责人 Nnenna Ndukwe 看到开发者正使用这一工作流，在 Codex 中借助 GPT‑6 模型来构建功能并处理技术债务。他们正在将 Codex 的编码工作与 Qodo 独立审查之间的交接过程自动化。"这正是我所看到的开发者们在做的事情，这非常令人兴奋，因为 GPT‑6 的能力极其强大，"Nnenna 说。

Itamar 将编码智能体与审查智能体形容为"阴与阳"：一个创造代码，另一个则对代码提出挑战。每个角色都需要自己的配置和上下文，并且可能涉及多个智能体。他的愿景是让智能体讨论审查结果，并"只将它们无法接受的结论呈现出来"供人类审查。开发者将转变为规划者和审查者，能够在查看未解决问题的同时，一并查看智能体的讨论过程、上下文以及开发者以往的决策。

"这就是建立信任的方式，"Itamar 说。"我认为这能让整个流程总体上更加高效，"Nnenna 补充道。"我们得以发挥出自身专长中最有价值的部分。"

## 让 Codex 每天投入工作

在 Qodo 内部，Nnenna 一直在自己的自动化开发工作流和知识工作中使用 GPT‑6 Astra 的 Extra High 和 Ultra 推理强度设置。

> "Codex 有什么是*不*会做的？我爱 Codex 所做的一切。我喜欢把 AI 和自动化结合起来的理念。"

——Nnenna Ndukwe，Qodo AI 开发者关系负责人

Nnenna 安排 Codex 定期汇报她本周完成的工作，以及接下来可以聚焦或改进的方向。她还用它来调研社交平台上关于智能体化工程（agentic engineering）的讨论，并为开发者内容提供创意建议。至于她自己的代码改动，她会安排 Codex 分析她的工作，并建议需要创建或改进的智能体技能。

## 通过 Decisions API 选择适用哪些编码规则

Itamar 看到了一个机会：利用 OpenAI 最近推出的 Decisions API，在开发的每个阶段选择适用哪些规则和智能体技能，而不是让每一个决策都依赖语言模型来完成。

他举了一个例子：Decisions API 可以先从 200 条规则中筛选出需要检查的条目，然后再由语言模型对相关条目进行推理，这样既能让筛选过程更快、更经济，又能提升审查质量。"Decisions API 为我们为流程注入更多信任提供了巨大的机会，"Itamar 说。

## 构建客户可以拥有的软件工厂

Qodo 的方法结合了"人工智能的最佳特性与传统软件工程和脚本的最佳特性，"Nnenna 说。公司知识为编程智能体提供指引，独立审查检验它们的工作，而人类的专业判断则解决剩余的问题。

这构成了 Itamar 所描述的软件工厂的基础：一个客户可以自行组装并拥有的系统，将编程智能体与审查智能体结合在一起，并理解软件在生产环境中是如何变化的。

通过与 OpenAI 合作，Qodo 正在构建这样一个未来：编程智能体能把公司更多的经验投入实际运用，而开发者可以把自己的判断力集中在最关键的地方。

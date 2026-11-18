# CodeRabbit 如何扩展 Agent 软件开发并将交付量提升至 20 倍（CodeRabbit scales agentic software development and ships 20x more）

> 原文：[CodeRabbit scales agentic software development and ships 20x more](https://openai.com/index/coderabbit-codex-daybreak/) · OpenAI · 2026-11-09
> 本文由 Kimi CLI 使用 Kimi K3-256k 全文翻译，并由 Agent 校对；已取得全文翻译和转载授权。
> 作者：OpenAI

2026年11月9日

初创公司

CodeRabbit 使用 OpenAI 模型来治理并信任 AI 生成的代码，并借助 Codex 在同一支工程团队不变的情况下交付 20 倍数量的软件。

[![CodeRabbit-OpenAI-DevDay-Alternative-v9-4K](../../../assets/articles/51dc5b66bcc5a8ab/vimeo-1245204408-preview.gif)](https://player.vimeo.com/video/1245204408?h=e665f4c47c&badge=0&autopause=0&player_id=0&app_id=58479)

[观看原始视频：CodeRabbit-OpenAI-DevDay-Alternative-v9-4K](https://player.vimeo.com/video/1245204408?h=e665f4c47c&badge=0&autopause=0&player_id=0&app_id=58479)

公司规模：初创公司

地区：北美

行业：科技

产品：API、Codex、Daybreak

对于 [CodeRabbit⁠](https://www.coderabbit.ai/) 的联合创始人兼 CEO Harjot Gill 来说，信任并验证智能体（agentic）代码，正日益成为团队对不断增长的 AI 生成工作量施加判断力的地方。“每家公司一旦采用编程智能体，遇到的第一个瓶颈就是代码审查。”Harjot 说道。

CodeRabbit 构建了一个由 AI 驱动的治理与控制平台，旨在验证并信任 AI 生成的代码。CodeRabbit 被超过 20,000 家组织和 150,000 多个开源项目所使用，帮助团队理解、审查和保护由 AI 智能体生成的代码，并决定哪些代码已准备好发布。

据 CodeRabbit 称，OpenAI 带来的更高性价比使其能够在审查中加入更多 AI 智能体，并将这些收益传递给客户；同时 [Codex⁠](https://openai.com/codex/) 帮助它在工程团队不变的情况下交付 20 倍数量的软件。该公司还使用 [Daybreak⁠](https://openai.com/daybreak/) 来保护自身技术栈及其客户的代码。其最新产品 CodeRabbit Secure 将 Daybreak 与 Codex 模型结合使用，通过专注于安全的智能体来发现并修复漏洞。

> “随着 OpenAI 每次发布新模型，尤其是推理模型的发布，我们产品在大规模发现问题方面的能力都有了巨大提升。”

– Harjot Gill，CodeRabbit 联合创始人兼 CEO

## 借助 OpenAI 推理模型改进代码审查

CodeRabbit 的第一个产品基于 GPT‑3.5 Turbo 构建。Harjot 表示，GPT‑4 的到来使该产品能够有效地审查代码。随后，该公司较早采用了 OpenAI o1 和 OpenAI o3。由于代码审查在云端异步运行，CodeRabbit 可以使用推理时间更长、但分析能力更强的模型。

团队会基于自建的一套已知问题基准来评估新模型。采访时，Harjot 估计 [GPT‑6 Astra⁠](https://openai.com/index/gpt-6-astra/) 能捕获该数据集中 50% 的问题，在该基准中领先于其他模型。

随着智能体引入不同类型的错误，以及修复暴露早期审查遗漏的问题，这套基准也在持续演进。“bug 的性质在不断演变，随着模型变得更好，我们的基准也在不断演进。”Harjot 说道。

## 让更强大的智能体在经济上可部署

OpenAI 模型更高的性价比帮助 CodeRabbit 将各项能力从研究阶段带入产品。Harjot 指出，模型定价和缓存方面的改进使公司能够使用更多 AI、添加更多子智能体，并将收益传递给客户。

CodeRabbit 刚起步时，仅使用一到两个子智能体进行代码导航。如今，像 GPT‑6 Luna 这样成本更低的模型已能支持整个平台上的更多子智能体，而像 GPT‑6 Astra 这样的模型则负责规划与编排。

“现在我们在各种用例中到处使用智能体，而这些用例在过去是我们根本负担不起的。”Harjot 说道。这扩大了 CodeRabbit 能够执行的验证范围，也丰富了它提供给开发者的解释，帮助他们理解并信任那些并非自己亲手编写的变更。

## 借助 Codex 交付 20 倍数量的软件

Harjot 表示，通过使用 Codex，公司在过去 6 个月里交付的软件数量约为原来的 20 倍，且没有增加工程师。他本人估计，在采访前的 30 天里，他提交了 2,500 到 3,000 个拉取请求（pull request）。

实现这一点需要的不仅仅是采用 Codex。同时运行多个智能体暴露了整个开发流程中的各种约束，从笔记本内存与算力，到测试、编译和打包软件的工具，再到依赖项。

团队精简了发布流程，并重新思考了人工审批应当处于哪个环节，同时借助 CodeRabbit 自动发布那些无需人工干预的低风险变更。“我们实际上必须彻底重新思考整个软件交付流程。”Harjot 说道。

该公司还构建了一个由 Codex 驱动的 Slack 机器人，用于对生产事故、Slack 消息和支持工单进行分类处理。它可以返回一个拉取请求，供团队审查并合并。Harjot 认为，基于云的开发方式可以减少本地机器的约束，并让团队在访问控制和审计方面拥有更强的掌控力。

## 将 CodeRabbit 的更多业务作为代码来运行

CodeRabbit 将 Codex 用于工程之外的工作，包括通过代码来管理营销和运营任务。“我们尽可能地以代码的方式来运营公司。”Harjot 说道。

在营销方面，公司通过拉取请求来管理 Google Ads。团队打开并合并一个请求即可部署广告。他们还使用一个内容工作室仓库，Codex 在其中创建幻灯片演示文稿和面向客户的文档。“如果你能把营销问题转化为代码问题，你的运行速度将快 10 倍。”Harjot 说道。

## 借助 Daybreak 保护应用程序代码

自 2023 年以来，CodeRabbit 一直在沙箱环境中运行智能体，通过克隆仓库并让智能体编写代码来协助执行审查。最近，CodeRabbit 通过 Daybreak 使用 OpenAI 的 Cyber 模型来测试并保护其自身平台。

团队将该模型用于内部渗透测试，探测自身平台中可能被攻击者入侵的途径。Harjot 表示，这次早期接入帮助 CodeRabbit 保护了自身的技术栈。“我们发现了多个漏洞，一些高级的入侵手段，我们甚至无法想象它们可能发生。”Harjot 说道。

此后，该公司将这些能力推向市场，通过其最新产品 CodeRabbit Secure 帮助保护客户的代码。在过去两周里，公司开展了一项促销活动，为用户承担了价值 100 万美元的免费深度扫描费用，并在 13,000 次深度扫描中发现了超过 43,000 个安全漏洞，这一切全部由 Codex 模型驱动。其中数千个漏洞已被其客户修复，帮助他们提升了代码安全性。

## 让开发者始终掌控智能体生成的代码

随着后台智能体开始在没有人为发起每个任务的情况下响应告警和事故，Harjot 预计团队将需要更多帮助来决定哪些变更值得推进到完成。

展望未来，CodeRabbit 正在向智能体化软件开发（agentic software development）方向扩展，帮助团队大规模地验证、排序优先级、解释、保护并核实智能体生成的代码变更。

其中的机遇在于：随着智能体承担更多的构建工作，通过验证、解释和维护跟上代码产出的节奏，帮助开发者始终保持对代码的掌控。

# Awesome AI Blogs 中文 [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

面向中文读者的 AI 博客精选，收录研究进展、工程实践、产品设计和独立观点。每篇保留首发链接，有授权的中文全文可直接在仓库阅读。

[浏览文章](articles/README.md) · [订阅源清单](sources/README.md) · [推荐一篇](https://github.com/xz1220/awesome-ai-blogs-zh/issues/new/choose) · [贡献指南](CONTRIBUTING.md)

## 目录

- [按主题阅读](#按主题阅读)
- [精选文章](#精选文章)
- [近期文章](#近期文章)
- [推荐博客](#推荐博客)
- [收录标准](#收录标准)
- [贡献和许可](#贡献和许可)

<!-- catalog:start -->

## 按主题阅读

已收录 659 篇（含历史索引）、38 个推荐博客或栏目，其中 52 篇可在仓库阅读中文全文。

- [模型与研究](articles/research.md)（192 篇）— 模型架构、训练、推理方法与实验发现。
- [工程实践](articles/engineering.md)（64 篇）— Agent、软件开发、工具、工作流与生产经验。
- [基础设施](articles/infrastructure.md)（8 篇）— 推理服务、算力、部署、性能与成本。
- [评测与安全](articles/evaluation.md)（64 篇）— 评估方法、对齐、安全研究与可靠性。
- [产品与应用](articles/products.md)（75 篇）— 产品设计、重要发布和有实质经验的应用案例。
- [独立观点](articles/perspectives.md)（78 篇）— 作者对技术、产品或行业的第一手观察。
- [历史索引](articles/archive.md)（178 篇）— 早期资料、持续更新页面及其他来源。

## 精选文章

- [我们如何构建多智能体研究系统](<https://www.anthropic.com/engineering/multi-agent-research-system>) — Anthropic · 2025-06-13。
- [AlphaProof Code：深入验证复杂软件的突破](<https://deepmind.google/blog/introducing-alphaproof-code/>) — Google DeepMind · 2026-11-10 · [中文全文](content/Google%20DeepMind/%E5%AE%98%E6%96%B9/2026-11-10_AlphaProof%20Code%EF%BC%9A%E6%B7%B1%E5%85%A5%E9%AA%8C%E8%AF%81%E5%A4%8D%E6%9D%82%E8%BD%AF%E4%BB%B6%E7%9A%84%E7%AA%81%E7%A0%B4.%E4%B8%AD%E6%96%87.md)。
- [推进低资源编程语言的编码能力](<https://openai.com/index/low-resource-programming-languages/>) — OpenAI · 2026-10-19 · [中文全文](content/OpenAI/%E5%AE%98%E6%96%B9/2026-10-19_%E6%8E%A8%E8%BF%9B%E4%BD%8E%E8%B5%84%E6%BA%90%E7%BC%96%E7%A8%8B%E8%AF%AD%E8%A8%80%E7%9A%84%E7%BC%96%E7%A0%81%E8%83%BD%E5%8A%9B.%E4%B8%AD%E6%96%87.md)。 多语言SQLite实现与COBOL迁移评测，检验代码维护和行为保真。
- [LifeVal：评测个人 Agent 完成日常事务的能力](<https://openai.com/index/lifeval/>) — OpenAI · 2026-11-02 · [中文全文](content/OpenAI/%E5%AE%98%E6%96%B9/2026-11-02_LifeVal%EF%BC%9A%E8%AF%84%E6%B5%8B%E4%B8%AA%E4%BA%BA%20Agent%20%E5%AE%8C%E6%88%90%E6%97%A5%E5%B8%B8%E4%BA%8B%E5%8A%A1%E7%9A%84%E8%83%BD%E5%8A%9B.%E4%B8%AD%E6%96%87.md)。 针对个人Agent实际完成日常事务的任务评测与结果验证。
- [构建强大的安全评估体系](<https://www.anthropic.com/research/building-strong-safety-evaluations>) — Anthropic · 2026-11-13 · [中文全文](content/Anthropic/%E5%AE%98%E6%96%B9/%E5%B7%A5%E7%A8%8B%E4%B8%8E%E7%A0%94%E7%A9%B6/2026-11-13_%E6%9E%84%E5%BB%BA%E5%BC%BA%E5%A4%A7%E7%9A%84%E5%AE%89%E5%85%A8%E8%AF%84%E4%BC%B0%E4%BD%93%E7%B3%BB.%E4%B8%AD%E6%96%87.md)。 如何构建能识别危险能力、覆盖真实使用风险的安全评估。
- [Agent Substrate：推进 Kubernetes 上的大规模 Agent 运行](<https://developer.nvidia.com/blog/agent-substrate-advancing-kubernetes-for-agents-at-scale/>) — NVIDIA · 2026-11-10 · [中文全文](content/NVIDIA/%E5%AE%98%E6%96%B9/2026-11-10_Agent%20Substrate%EF%BC%9A%E6%8E%A8%E8%BF%9B%20Kubernetes%20%E4%B8%8A%E7%9A%84%E5%A4%A7%E8%A7%84%E6%A8%A1%20Agent%20%E8%BF%90%E8%A1%8C.%E4%B8%AD%E6%96%87.md)。 从调度、隔离与运行时需求看 Kubernetes 上的 Agent 基础设施。
- [设计 OpenAI 模型提供商之间的故障切换](<https://developers.openai.com/blog/designing-failover-across-openai-model-providers>) — OpenAI · 2026-10-14 · [中文全文](content/OpenAI/%E5%AE%98%E6%96%B9/2026-10-14_%E8%AE%BE%E8%AE%A1%20OpenAI%20%E6%A8%A1%E5%9E%8B%E6%8F%90%E4%BE%9B%E5%95%86%E4%B9%8B%E9%97%B4%E7%9A%84%E6%95%85%E9%9A%9C%E5%88%87%E6%8D%A2.%E4%B8%AD%E6%96%87.md)。 生产Agent工作流的多提供商路由、切换边界、状态恢复与验证。
- [A2UI 1.0：构建流畅可靠的 Agent 交互体验](<https://developers.googleblog.com/en/a2ui-10-build-delightful-fast-reliable-agentic-experiences/>) — Google · 2026-11-11 · [中文全文](content/Google/%E5%AE%98%E6%96%B9/2026-11-11_A2UI%201.0%EF%BC%9A%E6%9E%84%E5%BB%BA%E6%B5%81%E7%95%85%E5%8F%AF%E9%9D%A0%E7%9A%84%20Agent%20%E4%BA%A4%E4%BA%92%E4%BD%93%E9%AA%8C.%E4%B8%AD%E6%96%87.md)。
- [您的应用现在可以在 Claude 中打开，Claude 也能在其中工作](<https://claude.com/resources/articles/interactive-connectors-full-tool>) — Anthropic · 2026-11-10 · [中文全文](content/Anthropic/%E5%AE%98%E6%96%B9/%E5%B7%A5%E7%A8%8B%E4%B8%8E%E7%A0%94%E7%A9%B6/2026-11-10_%E6%82%A8%E7%9A%84%E5%BA%94%E7%94%A8%E7%8E%B0%E5%9C%A8%E5%8F%AF%E4%BB%A5%E5%9C%A8%20Claude%20%E4%B8%AD%E6%89%93%E5%BC%80%EF%BC%8CClaude%20%E4%B9%9F%E8%83%BD%E5%9C%A8%E5%85%B6%E4%B8%AD%E5%B7%A5%E4%BD%9C.%E4%B8%AD%E6%96%87.md)。 通过交互式连接器让 Claude 与应用界面和工具协作。
- [Curative 如何借助 Claude 上的智能体构建全国医疗服务提供者网络](<https://claude.com/resources/articles/how-curative-is-building-a-national-provider-network-with-agents-on-claude>) — Anthropic · 2026-11-10 · [中文全文](content/Anthropic/%E5%AE%98%E6%96%B9/%E5%B7%A5%E7%A8%8B%E4%B8%8E%E7%A0%94%E7%A9%B6/2026-11-10_Curative%20%E5%A6%82%E4%BD%95%E5%80%9F%E5%8A%A9%20Claude%20%E4%B8%8A%E7%9A%84%E6%99%BA%E8%83%BD%E4%BD%93%E6%9E%84%E5%BB%BA%E5%85%A8%E5%9B%BD%E5%8C%BB%E7%96%97%E6%9C%8D%E5%8A%A1%E6%8F%90%E4%BE%9B%E8%80%85%E7%BD%91%E7%BB%9C.%E4%B8%AD%E6%96%87.md)。 Curative 将 Claude Agent 应用于全国医疗服务网络建设的实践。
- [什么是评测驱动开发：如何改进 AI Agent](<https://www.langchain.com/blog/what-is-eval-driven-development>) — LangChain · 2026-11-09 · [中文全文](content/LangChain/%E5%AE%98%E6%96%B9/2026-11-09_%E4%BB%80%E4%B9%88%E6%98%AF%E8%AF%84%E6%B5%8B%E9%A9%B1%E5%8A%A8%E5%BC%80%E5%8F%91%EF%BC%9A%E5%A6%82%E4%BD%95%E6%94%B9%E8%BF%9B%20AI%20Agent.%E4%B8%AD%E6%96%87.md)。
- [由大语言模型驱动的自主智能体](<https://lilianweng.github.io/posts/2023-06-23-agent/>) — Lilian Weng · 2023-06-23。 从规划、记忆和工具使用理解早期的大模型 Agent 架构。
- [上下文工程的现状](<https://www.dbreunig.com/2026/10/24/the-state-of-context-engineering.html>) — Drew Breunig · 2026-10-24。 长上下文的常见失效方式和确定性流程的边界。

## 近期文章

- [用混沌测试循环为 Claude Docs 上线做准备](<https://claude.dev/blog/chaos-loop-claude-docs-launch/>) — Anthropic · 2026-11-17。 记录服务团队如何用持续压测、遥测和修复来验证上线容量。
- [OpenAI 发布 ChatGPT for Sales](<https://openai.com/index/introducing-chatgpt-for-sales/>) — OpenAI · 2026-11-17。 展示销售插件怎样连接 CRM 和日常工具，用于客户准备与后续沟通。
- [OpenAI 发布 GPT-6.2 Astra 和 Sol](<https://openai.com/index/introducing-gpt-6-2-astra-sol/>) — OpenAI · 2026-11-17。 发布文对比两款模型在专业工作、编程与科学任务中的表现，也列出成本和可用性。
- [Claude Code 团队如何看待验证](<https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/>) — Anthropic · 2026-11-16。 讨论如何为编码 Agent 提供可独立验证的结果和反馈。
- [OpenAI 的第一阶段嵌入式评估](<https://openai.com/index/our-first-phase-of-embedded-assessments/>) — OpenAI · 2026-11-16。 介绍独立评估者参与模型安全工作的范围、访问权限和发表协议。
- [科学前沿：研究者如何使用 ChatGPT](<https://openai.com/index/science-at-the-frontier/>) — OpenAI · 2026-11-16。 调查 1,800 多位研究者的使用方式，区分他们交给 AI 的任务和仍由自己做出的判断。
- [TokenEconomizer：用历史经验降低编码 Agent 的开销](<https://www.microsoft.com/en-us/research/blog/tokeneconomizer-learning-from-experience-to-make-ai-coding-agents-more-efficient/>) — Microsoft Research · 2026-11-16。 将已完成的工作转成给后续会话的指引，并测量真实修复任务中的效果与成本。
- [Anthropic 更新协调漏洞披露时限](<https://www.anthropic.com/research/coordinated-vulnerability-disclosure-timelines>) — Anthropic · 2026-11-16。 说明新的披露时限，以及采用较短时间窗口的依据。

## 推荐博客

### 研究机构与模型团队

- [OpenAI News](<https://openai.com/news/>) — 模型发布、研究、安全评估与产品案例。 [订阅](<https://openai.com/news/rss.xml>)
- [Anthropic Research](<https://www.anthropic.com/research>) — 大模型研究、可解释性、对齐与评测。
- [Google DeepMind Blog](<https://deepmind.google/blog/>) — 模型、强化学习与 AI for Science 的研究进展。 [订阅](<https://deepmind.google/blog/rss.xml>)
- [Qwen Blog](<https://qwenlm.github.io/blog/>) — 通义千问模型、评测及开源生态。

### 工程团队与产品博客

- [OpenAI Developers Blog](<https://developers.openai.com/blog>) — API、Codex、开发实践和真实构建案例。
- [Claude Blog](<https://claude.com/resources/articles>) — Claude 产品使用经验、性能改进和案例。
- [Cursor Blog](<https://cursor.com/blog>) — AI 编程产品、长程 Agent 和内部工程实践。

### 开源项目与社区

- [Hugging Face Blog](<https://huggingface.co/blog>) — 开源模型、工具、数据和可复现的教学实践。 [订阅](<https://huggingface.co/blog/feed.xml>)
- [LangChain Blog](<https://www.langchain.com/blog>) — Agent 搭建、评测和生产经验。

### 独立作者

- [Lilian Weng · Lil'Log](<https://lilianweng.github.io/>) — 以文献和机制为主线梳理模型、训练与 Agent。
- [Simon Willison's Weblog](<https://simonwillison.net/>) — 模型实测、工具尝试和 AI 安全观察。
- [科学空间 · 苏剑林](<https://spaces.ac.cn/>) — 中文技术长文，关注模型结构、训练与优化器。

[查看所有来源及订阅入口](sources/README.md)

<!-- catalog:end -->

## 收录标准

- 优先选择能解释方法、设计取舍、实验结果或真实使用经验的文章。首发来源包括研究机构、产品团队、开源社区和独立作者。
- 收录值得讨论的产品迭代和应用案例。简短版本流水、营销通稿和重复转述不进入精选。
- 有官方中文时优先链接官方版本。授权转载的全文保留原文出处、图表、代码和必要的上下文；引用条目始终可从原文继续阅读。

## 贡献和许可

欢迎推荐新来源、补充好文章、纠正翻译或报告缺图。条目格式和校验方法见 [贡献指南](CONTRIBUTING.md)，每日维护见 [维护手册](docs/maintenance.md)。

项目的原创索引与策展说明采用 [CC0 1.0](LICENSE)。仓库中的第三方文章、译文及媒体保留原有权利，详见 [内容权利说明](NOTICE.md)。

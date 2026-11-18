# 一次编写，跨 Agent 运行：Skills 实践指南（Build once, run on any agent: A practical guide to agent skills）

> 原文：[Build once, run on any agent: A practical guide to agent skills](https://github.blog/ai-and-ml/github-copilot/build-once-run-on-any-agent-a-practical-guide-to-agent-skills/) · GitHub · 2026-11-12
> 本文由 Kimi CLI 使用 Kimi K3-256k 全文翻译，并由 Agent 校对；已取得全文翻译和转载授权。
> 作者：Andrea Griffiths

![装饰性壁纸，Mona 穿行在像素化的路径中。](../../../assets/articles/8bc9138e516754eb/49527bc8e3a3cc642c8c2243.png)

这周你有多少次向智能体重复解释同一项任务？又有多少次，你向那位深谙组织内部知识的同事请教如何解决某个具体问题？这些上下文不应该流失在聊天记录里，也不该被锁在某一个人的脑海中。智能体技能（agent skills）让你可以把可重复的指令沉淀下来，供你和你的智能体重复使用。你今晚为自己写的技能，日后可能成为团队流水线的一部分。

智能体技能是一个以 `SKILL.md` 文件为核心的带版本目录，该文件描述了何时以及如何执行一项可重复的任务。你可以跨智能体共享这些指令，但执行这些指令所需的工具、凭证和权限仍需由运行环境提供。举例来说，一个技能可以描述如何查询数据库，但它并不会授予对该数据库的访问权限。

*在 GitHub Universe 2026 期间，我曾与 Procore 数据工程高级经理 Shishir Tewari 就这一话题进行现场分享。我们的演讲题为 [《Build once, run on any agent: a practical guide to agent skills》（构建一次，即可在任意智能体上运行：智能体技能实用指南）](https://reg.githubuniverse.com/flow/github/universe26/attendee-portal/page/sessioncatalog?search=BLD1787B)。*

## 定义一项任务及其适用时机

技能在有明确的任务、输入和输出时效果最佳。举例来说，假设你正在构建一个智能体，用于检查 AI 生成的变更是否符合原始需求。如果同一个智能体评估自己的工作，它的解释可能会影响评审结果。在 [Proof Agent](https://github.com/githubevents/build-once-run-on-any-agent/tree/main/demos/proof-agent) 中，我们使用一个独立的验证器来检查变更，并为其结论提供证据。该技能的 frontmatter 指明了任务名称并描述了其用途：

```plaintext
---
name: proof-agent
description: Adversarial verification of AI-generated work. Spawns an independent verifier to check for false claims, broken code, and security issues.
---
```

其核心是一条简单的规则：自我验证不等于验证。

Proof Agent 的 [`SKILL.md`](https://github.com/githubevents/build-once-run-on-any-agent/blob/main/demos/proof-agent/SKILL.md) 中的 `When to Verify`（何时验证）一节说明了何时调用该技能。其余指令则解释了验证器要审查什么，以及在其结论中应包含哪些证据。

## 协调多个技能以完成更大的工作流

当让数据流水线保持正确运转所需的判断力分散在四个人的头脑中，那四个人就成了路线图本身。流水线的每次变更都取决于他们是否有空、是否了解那些数据。[Data Forge](https://github.com/githubevents/build-once-run-on-any-agent/tree/main/demos/dataforge) 就是一个示例，展示了如何将这种判断力的一部分沉淀到协同工作的技能之中。

在 [support-desk 流水线示例](https://github.com/githubevents/build-once-run-on-any-agent/blob/main/demos/dataforge/examples/support-desk/DEMO.md) 中，我们从一个统计已创建和已解决事件数量的指标需求开始。在构建流水线之前，`forge-init` 技能会先探明源表、命名规范等细节，并将其写入一份已解析的清单（manifest）。其他技能则读取这份清单，以获取各自所需的项目上下文。

随后，`forge-builder` 技能协调从 issue 到拉取请求（pull request）的整个工作。它在设计和构建流水线时使用 `forge-dbx` 查询数据平台，并使用 `forge-lint` 应用团队规范。在此过程中，会有人对提出的决策进行评审，最终生成的拉取请求包含流水线代码、架构（schema）变更和测试。

每个技能都有明确的职责，它们共享项目上下文，而不是各自独立地重新探查。当某个步骤发生变化时，你只需修改一个技能，其余技能保持不变。

技能适合边界清晰、可重复、且能从可复用判断力中获益的工作，例如检查清单、发布、迁移或指标流水线。如果一个工作流需要稳定的接口、共享状态、审计追踪、长时间运行的控制，或需要在模型之外强制执行的权限，那么应用程序才是更合适的选择。

## 将项目配置排除在技能之外

我们不希望把每个项目的名称、数据库或规范硬编码到技能中。在 Data Forge 的 support-desk 示例中，一份[清单（manifest）](https://github.com/githubevents/build-once-run-on-any-agent/blob/main/demos/dataforge/examples/support-desk/dataforge.manifest.yaml)描述了项目、指标存储和平台，使技能能够使用正确的项目细节，而无需将其固化在指令中：

```
project:
  name: "support-desk"
  store_name: "support_metric_store"

platform:
  engine: "duckdb"
  pipeline_framework: "spark_python"
  duckdb_dir: "warehouse"
```

有了已解析清单中的探明细节，其他技能就不必对项目做出各自的假设。

要将探明的项目细节与团队规范分开。`forge-init` 初始化技能可以检查现有的架构和代码模式；`forge-lint` 技能则提供代码生成前需要遵循的规则。在仓库中发现的模式并不自动等于需要保留的规则，因此要让探明的细节可供评审，并在需要业务判断的地方由人来确认或修改。要检验可移植性，可以问这样一个问题：另一个团队能否使用自己的清单来复用这些技能，而无需重写它们？

## 在技能之间共享执行路径

`forge-dbx` 技能为其他 Data Forge 技能提供了一种统一访问数据平台的方式。它读取清单并选择 Databricks 或 DuckDB 适配器，因此每个技能都无需拥有自己的连接和查询逻辑。

清单可以为本地 support-desk 演示选择 DuckDB，但它无法安装 DuckDB CLI，也无法授予数据库访问权限。这些仍然是环境及其用户的设置职责。清单负责选择引擎；宿主环境负责提供访问能力。

## 在工作流中设置检查点和审批点

Data Forge 的 support-desk 工作流共有七个阶段，每个阶段都设有人工检查点。[工作流概览](https://github.com/githubevents/build-once-run-on-any-agent/blob/main/demos/dataforge/README.md#the-skills)展示了这些技能如何协同配合。在进入下一阶段之前，工作流会检查前一阶段是否已完成；在执行架构变更之前，它会请求批准。

Proof Agent 示例将同样的原则应用于代码评审。一个 GitHub Actions 工作流向验证器提供原始需求和代码变更，但不提供编码智能体自己的评估。验证器返回 `PASS`、`FAIL` 或 `PARTIAL`，且必须引用已变更文件中的证据。该 GitHub Action 对 diff 进行静态评审；它不执行代码，也不运行测试。在演示工作流中，我们设置了 `block-on-fail: false`，因此结论仅供参考。默认情况下，`FAIL` 会使检查失败，如果该检查是必需的，就会阻止合并。其目标是让测试结果和合并要求保留在你仓库的 CI 检查和规则之中。

## 为每个智能体客户端打包，然后验证其设置

支持多个客户端可能意味着要保持同一指令的多个副本同步。在 Data Forge 示例中，我们以 `skills/*/SKILL.md` 为源，使用打包脚本生成针对各客户端的文件：面向 Claude Code 的 `.claude-plugin/plugin.json`、面向 Cursor 的 `.cursor-plugin/plugin.json`，以及面向 GitHub Copilot 的 `.github/agents/*.agent.md`。该脚本还包含一个用于 CI 的检查模式：

```
node scripts/package.mjs --check
```

各客户端在可用模型、工具、凭证和权限方面可能有所不同。安装技能后，请检查客户端是否能针对预期任务识别该技能、加载其引用文件、使用所需的工具，并返回该技能要求提供的证据。

## 构建智能体技能的三条实践

1. **将业务上下文放在一个文件中。** 把项目特有的名称、架构和规范保存在一份清单中，让每个技能读取它，而不是复制这些事实。这为团队提供了一个清晰可见、可统一更新配置的位置。
2. **让相关技能以一致的方式使用平台。** 让相关技能通过同一条路径来运行查询、任务和架构变更，而不是各自定义自己的命令和连接逻辑。这使工作流的访问方式更易于理解，其行为也更容易在每个客户端中检查。
3. **用指令指导工作，用检查验证工作。** 技能可以告诉智能体应遵循哪些规范、何时请求批准。在需要上下文或判断力的决策处加入人工评审，并使用测试和 CI 检查在变更推进之前发现问题。如果某项检查必须阻止合并或部署，请在你仓库的规则中配置该要求。

从你已经解释得厌烦的那项任务开始。写下它需要什么、在哪里停止，以及评审者会看到什么。然后用另一个智能体试试它，并在实践中了解什么有效、不断改进。

[为 GitHub Copilot 添加智能体技能 >](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)

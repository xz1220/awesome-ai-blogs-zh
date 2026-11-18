# OpenAI 如何保障 OpenClaw 等持久型智能体的安全（Securing persistent agents like OpenClaw at OpenAI）

> 原文：[Securing persistent agents like OpenClaw at OpenAI](https://developers.openai.com/blog/securing-persistent-agents-like-openclaw-at-openai) · OpenAI · 2026-11-12
> 本文由 Kimi CLI 使用 Kimi K3-256k 全文翻译，并由 Agent 校对；已取得全文翻译和转载授权。
> 作者：Kevin S Lin

大约一年前 OpenClaw 发布时，它向世界展示了一种持久化智能体（persistent agent）的能力。与普通的 codex 会话不同——后者有固定的目标并需要人类引导——持久化智能体可以 7×24 小时运行，拥有广泛的任务范围，并且能够在没有用户输入的情况下主动采取行动。

虽然持久化智能体能力极强，但迄今为止它们在现实世界中的部署仍然有限。与传统软件相比，这类部署带来了许多全新的挑战。对于传统软件，我们依赖配置和代码的确定性，并且威胁（主要）来自外部攻击者。而持久化智能体可以更改自身的配置，并为完成目标编写任意代码。当智能体采取与其目标不一致（misaligned）的行动时，攻击就来自内部。

在 OpenAI，我们目前已在整个公司范围内部署了持久化智能体，其中包括数百个 OpenClaw 智能体。本文介绍了我们为在 OpenAI 部署 OpenClaw 所采用的一些控制措施。

## 分离可信与不可信的执行

为了保障持久化智能体的安全，我们需要将可信的确定性逻辑与不可信的 LLM 执行隔离开来。可信逻辑包括网络、身份和沙箱等关键组件。这些是传统的静态代码，除了软件缺陷之外，其行为应当与配置一致。智能体、智能体执行所在的环境以及智能体编写的代码都被视为不可信。在这样的环境中，智能体可以为完成目标动态生成代码，其行为没有硬性保证。

为了在 OpenClaw 中支持这一点，我们最终在开源项目中实现了[远程 harness 执行](https://docs-enterprise.openclaw.org/guides/topics/remote-harness/#gateway-and-harness)。这使得 [OpenClaw Gateway](https://github.com/openclaw/openclaw) 能够在与智能体 harness 分离的容器（在我们的案例中，是分离的集群）中运行。

通过实现这种拆分，我们可以把网关——即配置智能体的组件——视为可信的确定性代码，并专注于将智能体工作负载作为不可信代码进行沙箱隔离。

## 强制执行硬性安全边界

智能体工作负载的安全边界通过沙箱机制来强制执行，沙箱限制了智能体可以采取的行动。

对于我们的 OpenClaw 部署，我们使用了以下沙箱控制：

- 网络：控制智能体可以访问哪些端点——我们使用由组织管理的允许列表，并对受限端点显式拒绝
- 工作区：控制智能体可以访问哪些文件——我们仅允许对智能体工作目录进行写入
- 进程：控制智能体可以访问哪些进程——我们依赖 codex Linux 沙箱提供的进程隔离
- 密钥：控制智能体可以访问哪些密钥——我们通过凭据代理（credential broker）管理密钥，因此密钥对智能体不可见

对于我们的 OpenClaw 部署，我们使用了 codex harness 内置的沙箱。以下是我们采用的一些设置，分为 [`requirements.toml`](https://developers.openai.com/codex/enterprise/managed-configuration#admin-enforced-requirements-requirementstoml)（限制 codex 配置中可用的选项）和 [`config.toml`](https://developers.openai.com/codex/config-basic#codex-configuration-file)（实际的 codex 配置）两部分。请注意，我们还启用了一些额外的安全控制——移除了使用 [`danger-full-access`](https://developers.openai.com/codex/agent-approvals-security#common-sandbox-and-approval-combinations) 模式的能力，并依赖[缓存式网页搜索](https://developers.openai.com/codex/config-basic#web-search-mode)，该模式会将网页搜索请求路由到 OpenAI 自己的索引来处理搜索查询。

**`requirements.toml`**

```toml snippet=configuration reason="requirements.toml reference settings"
# Exclude unrestricted "danger-full-access" sandbox mode.
allowed_sandbox_modes = ["read-only", "workspace-write"]

# Permit cached hosted search, but not live hosted search.
allowed_web_search_modes = ["cached"]

# Require the managed network proxy.
experimental_network.enabled = true

# Prevent user-level configuration from expanding the domain allowlist.
experimental_network.managed_allowed_domains_only = true

# Allow only these destinations; replace with the workload's required hosts.
experimental_network.allowed_domains = [
  "github.com",
  "api.github.com",
  "codeload.github.com",
]

# Explicitly block these destinations, including cloud metadata endpoints.
experimental_network.denied_domains = [
  "pastebin.com",
  "*.pastebin.com",
  "webhook.site",
  "metadata.google.internal",
  "169.254.169.254",
]
```

**`config.toml`**

```toml snippet=configuration reason="config.toml reference settings"
# Select the permission profile defined below.
default_permissions = "openclaw"

# Use cached hosted search.
web_search = "cached"

[permissions.openclaw.filesystem]
# Allow reads needed by the minimal runtime environment.
":minimal" = "read"

# Allow reading and modifying the agent's workspace.
"/home/dev-user/openclaw-workspaces" = "write"

# Allow reading managed assets without modifying them.
"/home/dev-user/read-only" = "read"

# Prevent access to SSH credentials.
"/home/dev-user/.ssh" = "deny"

[permissions.openclaw.network]
# Permit network access through the administrator-required proxy.
enabled = true

# Do not inherit an upstream proxy.
allow_upstream_proxy = false

# Keep the proxy's local/private-address guard enabled.
allow_local_binding = false

# Disable the SOCKS5 listener.
enable_socks5 = false

# Disable SOCKS5 UDP support.
enable_socks5_udp = false

# Do not permit proxy listeners on non-loopback addresses.
dangerously_allow_non_loopback_proxy = false

# Do not permit unrestricted Unix-socket access.
dangerously_allow_all_unix_sockets = false

[shell_environment_policy]
# Preserve default filtering of sensitive environment variables.
ignore_default_excludes = false

# Remove GitHub credentials from agent command environments.
# This does not hide credentials stored in accessible files.
exclude = [
  "GH_TOKEN",
  "GITHUB_TOKEN",
  "OPENCLAW_GITHUB_BASIC_AUTH",
  "OPENCLAW_GITHUB_READONLY_BASIC_AUTH",
]

[apps._default]
# Disable apps unless individually enabled.
enabled = false

# Disable destructive app operations by default.
destructive_enabled = false

# Disable open-world app operations by default.
open_world_enabled = false
```

## 增加基于模型的防护措施

到目前为止我们讨论的所有控制都是静态的，也就是说，它们依赖传统的确定性代码来防止智能体采取与其目标不一致的行动。随着模型变得越来越聪明，我们同样必须拥有可随算力扩展的防御手段——也就是用其他模型来防御。

通过 [Auto-review](https://alignment.openai.com/auto-review/)（自动审查），第二个智能体可以监控并批准主智能体的行动。持续要求人工审查会造成审查疲劳，让人类被训练成盲目接受所有权限提示。通过使用基于 LLM 的审查者作为过滤器，我们将人类的注意力保留给高价值的审批。这是 OpenClaw 和 Codex 都原生支持的功能。

对于我们的 OpenClaw 部署，我们对所有智能体行动强制执行自动审查。

## 将智能体身份与用户身份分离

当智能体采取某项行动时，我们需要能够审计该行动、为智能体授予资源访问权限，并区分该行动是由智能体发起的还是由用户发起的。智能体身份为我们提供了实现这一点的手段。目前有一些新兴的规范，例如 [WAG](https://datatracker.ietf.org/doc/draft-carleton-workload-authz-grant/)，它让智能体拥有自己的资源访问权限；还有 [XAA](https://datatracker.ietf.org/doc/draft-ietf-oauth-identity-assertion-authz-grant/) 等规范，让智能体通过 OAuth 委托代表用户行事。请注意，智能体身份不同于服务账户——后者为机器人提供独立的 API 访问。两者应当结合使用——例如，你的智能体应以其自身的智能体身份行事，并通过与该身份关联的服务账户访问第三方服务。

对于我们的 OpenClaw 部署，每个智能体都有唯一的身份，并关联到一个 [ChatGPT 服务账户](https://learn.chatgpt.com/docs/enterprise/service-accounts)。这使每个智能体都拥有独立于用户的推理凭据，并允许团队将自定义插件连接到该智能体。这也让我们能够审计智能体的行动，并在必要时关闭其推理能力。

## 观察一切

全面的可观测性让运营人员能够了解智能体的完整生命周期——从它们是如何配置的，到它们采取了哪些行动。对于持久化智能体，拥有这样的覆盖能力至关重要，只有这样我们才能追踪和检测与其目标不一致的行动。

对于我们的 OpenClaw 部署，我们记录一切——控制平面上的每一次配置变更，以及智能体的所有轮次（turn）。由于智能体的轮次可能包含敏感信息，这些日志被严格锁定，仅安全团队中的少数指定人员可以访问。

## 结语

在持久化智能体的部署方面，我们仍处于采用曲线的起步阶段。由于缺乏成熟的最佳实践，如今许多企业难以采用智能体。

当我们在 OpenAI 内部推出 OpenClaw 试点时，我们见证了生产力和采用率的巨大飞跃，这来自全公司的技术和非技术团队。现在我们有超过 500 个智能体在后台主动运行，做着有意义的工作——从根据产品反馈自动提交 PR，到对新功能持续运行数据实验，不一而足。

在 OpenAI 开发者日（dev day）期间，我们[发布了 OpenClaw Enterprise（OCE）](https://openclaw.ai/blog/openclaw-enterprise)，这是一个开源的、厂商中立的智能体控制平面。如果你使用 OCE，在使用[标准 codex 预设](https://github.com/openclaw/openclaw-enterprise/blob/main/docs/guides/topics/standard-codex-preset.md)时，启动的智能体就会内置我们谈到的许多防护措施。请注意，该项目目前仍处于试点阶段，我们计划在今年年底前发布 1.0 版本。

我们相信，AI 在行业中许多最大的收益将来自持久化智能体。通过分享我们的经验并以开放的方式构建 OCE，我们希望让每个人都能更安全地部署它们。

# Greptile 与 GPT-6 Astra：超越代码审查的缺陷检测（Greptile takes bug detection beyond code review with GPT-6 Astra）

> 原文：[Greptile takes bug detection beyond code review with GPT-6 Astra](https://openai.com/index/greptile-code-review-codex-astra/) · OpenAI · 2026-10-26
> 本文由 Kimi CLI 使用 Kimi K3-256k 全文翻译，并由 Agent 校对；已取得全文翻译和转载授权。
> 作者：OpenAI

2026 年 10 月 26 日

初创公司

Greptile 如何使用 GPT‑6 Astra 测试用户工作流程，借助 Daybreak 强化安全性，并利用 Codex 减少返工。

[![Greptile takes bug detection beyond code review with GPT-6 Astra](../../../assets/articles/532d936c683b5e58/vimeo-1238949553-preview.gif)](https://player.vimeo.com/video/1238949553?h=cf3eabdf75&badge=0&autopause=0&player_id=0&app_id=58479%2Fembed)

[观看原始视频：Greptile takes bug detection beyond code review with GPT-6 Astra](https://player.vimeo.com/video/1238949553?h=cf3eabdf75&badge=0&autopause=0&player_id=0&app_id=58479%2Fembed)

公司规模：初创公司

地区：北美

行业：科技

产品：API、Codex

[Greptile⁠](https://www.greptile.com/) 构建能够在完整代码库上下文中审查和测试代码变更的 AI 智能体。联合创始人兼首席执行官 Daksh Gupta 表示：“我们的业务就是减少 bug，让全世界的软件更加可靠。”

对 Daksh 而言，这一使命不仅需要阅读代码，还需要测试应用的实际行为，而 GPT‑6 Astra 的计算机使用（computer use）能力为 Greptile 提供了一种大规模自动化测试的方法。

> “有史以来第一次，计算机使用能力达到了这样一个水平：你可以自动化模拟一个用户试图搞垮你的应用的体验，从而让大型企业能够更有信心地发布产品。”

——Daksh Gupta，Greptile 联合创始人兼首席执行官

## 借助 GPT‑6 Astra 大规模测试应用

验证一个拉取请求（pull request）需要检查代码在逻辑上是否正确、是否实现了开发者的意图、是否安全，以及是否会破坏现有功能。对于其中一些测试，你需要真正运行应用，因为仅仅阅读代码可能无法发现问题。

Daksh 举了一个例子：一个按钮在 iPhone 上查看网站时消失了。借助 GPT‑6 Astra，Greptile 可以为一个拉取请求启动开发服务器，将浏览器调整为 iPhone 尺寸的视口，并模拟用户在应用中操作。该模型的视觉理解能力使其能够检查屏幕并发现那个隐藏的按钮。

他说：“考虑到我们借助这些模型发布代码的速度，让一家 QA 公司测试你所有的变更实在慢得不切实际。”借助 GPT‑6 Astra，Greptile 能够大规模地自动化这类应用测试。

## 借助 Daybreak 强化客户防御

Daksh 表示，更强大的模型也让攻击者更容易利用应用漏洞，使公司面临风险，即使是那些以前不会成为典型攻击目标的公司也不例外。

Daksh 说：“我们希望让即使是初创公司也能非常轻松地保护自己的系统。借助 Daybreak，我们能够以一种非常安全的方式做到这一点，并且我们可以确保客户拥有比攻击者的攻击手段更先进的防御机制。”

## 借助 Codex 减少 bug 和返工

Greptile 的知识库（Knowledge Base）会对公司的代码库进行索引，并以人和智能体都能阅读的形式记录其工作原理。该公司通过模型上下文协议（Model Context Protocol，MCP）服务器将这些文档提供给 Codex。

这使得 Codex 能够编写遵循客户现有模式的代码。据 Daksh 介绍，已有数千名客户将 Codex 连接到 Greptile 的知识库。

为了衡量其影响，团队会跟踪 AI 生成的代码被回滚（revert）的频率。Daksh 说：“当我们为智能体提供上下文时，回滚的情况会减少，客户可以节省时间和推理资源。”客户可以将这些节省下来的资源投入到新工作中，而不是反复返工同样的变更。

Greptile 还使用 Codex 来构建自己的软件和智能体。Daksh 说：“我们是 Codex 的重度用户。我们在每一个职能领域都有大量的使用，尤其是工程领域。”

## 展望借助 Ultrafast 实现更快的开发

Daksh 解释说，对 Greptile 而言，唯一真正的瓶颈是团队能多快地将想法转化为可用的软件。他表示，模型的智能对许多任务来说已经足够，因此他认为 Ultrafast 是加快开发速度的一种方式。

> “我最期待的是把 Ultrafast 当作一种杠杆，让我们的行动速度完全跟上我们想出好点子的速度。”

——Daksh Gupta，Greptile 联合创始人兼首席执行官

他的长期目标是让修改和交付关键的企业级软件像交付一个业余项目一样简单，而 OpenAI 正在帮助 Greptile 构建实现这一目标所需的验证能力。

## 加入工作的新时代

全球超过 100 万家企业正在借助 OpenAI 取得切实的成果。

[联系销售](https://openai.com/contact-sales/)

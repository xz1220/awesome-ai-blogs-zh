# Microsoft Agent Framework for Go 的预配置 Agent（Preconfigured agents with Microsoft Agent Framework for Go）

> 原文：[Preconfigured agents with Microsoft Agent Framework for Go](https://devblogs.microsoft.com/go/preconfigured-agents-with-microsoft-agent-framework-for-go/) · Microsoft · 2026-11-11
> 本文由 Kimi CLI 使用 Kimi K3-256k 全文翻译，并由 Agent 校对；已取得全文翻译和转载授权。
> 作者：Michelle Clayton

Microsoft Agent Framework for Go 帮助你构建能够跟踪任务、保存和回顾笔记、加载可复用技能并调用应用程序工具的代理。
审批规则让你的应用程序可以处理需要用户决策的工具调用。
追踪功能提供计时和错误数据，用于排查模型调用和工具调用。

组合这些能力意味着要配置上下文提供程序、中间件、历史记录和会话状态。
当你希望使用相同的默认设置时，为每个代理重复这些配置会很繁琐。

我们通过代理托管框架（agent harness）解决了这一重复配置的问题，它由 `agent/harness` 包提供。
代理托管框架是负责协调工具执行并在模型调用之间提供上下文的应用程序代码。

该包自 [Microsoft Agent Framework for Go](https://github.com/microsoft/agent-framework-go) 的 v0.2.0 版本起可用。
该框架目前仍处于公开预览阶段。

## 托管框架配置的内容

`harness.AgentConfig` 返回一个已添加托管框架默认设置的 `agent.Config`。
该辅助函数将你的工具与内置工具组合，并包含你提供的中间件和上下文提供程序。
将此配置与你的提供程序构造函数一起使用即可创建代理。

代理的 `CreateSession` 方法会创建一个保存会话状态的 `agent.Session` 对象。
使用 `agent.WithSession` 将同一会话传递给后续的 `RunText` 调用，即可继续对话。

默认配置包括：

- **默认指令：** 托管框架提供 Agent Framework 的 `harness.DefaultInstructions` 文本。
  它指示模型将复杂任务分解为多个步骤、用工具验证结果，并在工具调用之间汇报进度。
- **待办事项工具：** 这些工具读取和更新会话中的结构化任务列表，使后续请求能够看到哪些工作尚未完成。
- **规划与执行模式：** 代理以规划模式启动，并配有针对讨论计划或执行计划的特定模式指令。
  请注意，这些模式不会拒绝工具使用，也不做任何沙箱隔离，仅指示代理应如何表现。
- **FileMemory：** 代理可以将计划或发现保存并更新到磁盘上，然后在后续请求中按文件名检索它们。
- **对话历史记录：** 默认情况下，历史记录提供程序将消息保存在内存中，并在每次模型调用后保存，包括中间的工具调用及其结果。
  代理在回答后续请求时可以使用这些工具结果。
- **技能：** 基于文件的技能将任务说明和 YAML 元数据保存在 `SKILL.md` 中，并附带可选的支持文件，例如参考文档或模板。
  代理可以按需加载相关说明和文件，而无需在初始提示中包含每个流程。
  默认发现机制会查找工作目录，并排除 `agent-file-memory`。
  技能还可以包含脚本（例如 Python 文件），这些脚本仅在你的应用程序提供脚本运行器时才会执行。
- **工具审批：** 中间件会记住会话期间的持续审批，并可应用你的自动审批规则，避免对匹配的调用重复提示。
  对于仍需审批的调用，你的应用程序会收到一个请求，你可以将其呈现给用户，并通过同一会话作答。
- **托管网络搜索：** 模型可以向服务请求网络搜索结果，因此你的应用程序无需自带搜索客户端。
  支持情况取决于所选的 API 和部署。
  当该工具不可用或不必要时，使用 `DisableWebSearch` 将其省略。
- **消息注入：** 你的应用程序可以在运行期间为会话排队附加输入，例如修订后的需求。
  注入器会在模型调用之间提供排队的消息。
  排队机制使你的应用程序无需丢弃当前模型调用正在执行的工作。
  如需改为取消，请使用通过 [`context.WithCancel`](https://pkg.go.dev/context#WithCancel) 创建的 Go 上下文。
- **追踪：** OpenTelemetry 分别记录代理运行、受支持的模型调用和本地工具调用。
  每条记录都包含其持续时间和任何错误。
  模型调用记录还包含提供程序报告的令牌用量。

[托管框架指南](https://learn.microsoft.com/en-us/agent-framework/concepts/harness?pivots=programming-language-go)记录了 `harness.Config` 的各项设置及其默认值。

## 使用 Foundry 运行代理

本示例针对一个 Go `net/http` 服务的规划助手运行两个请求。
第一个请求要求代理概述一个健康检查端点，将工作记录为待办事项，并将计划保存到 `healthcheck.md`。
第二个请求要求代理读取已保存的计划，并列出同一会话中未完成的任务。
该示例需要 Go 1.26 或更高版本：

```bash
go mod init example.com/harness
go get github.com/microsoft/agent-framework-go@v0.2.0
```

使用一个 Foundry 项目，并配备支持 Responses API 和函数调用的模型部署。
将 `FOUNDRY_PROJECT_ENDPOINT` 设置为[项目终结点](https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects)，例如 `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>`。
将 `FOUNDRY_MODEL` 设置为部署名称。

在本地开发时，使用 `az login` 以可调用该部署的身份登录。
[Foundry User 角色](https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry#assign-foundry-user-role-to-your-user-principal)授予所需的项目数据访问权限。
本示例使用 `DefaultAzureCredential`，它可以使用 Azure CLI 凭据进行身份验证。
该程序会向 Foundry 发送模型请求并产生使用费用。

将以下内容保存为 `main.go`：

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os"

    "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    "github.com/microsoft/agent-framework-go/agent"
    "github.com/microsoft/agent-framework-go/agent/harness"
    "github.com/microsoft/agent-framework-go/provider/foundryprovider"
)

func main() {
    endpoint := os.Getenv("FOUNDRY_PROJECT_ENDPOINT")
    deployment := os.Getenv("FOUNDRY_MODEL")
    if endpoint == "" || deployment == "" {
        log.Fatal("FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_MODEL are required")
    }

    credential, err := azidentity.NewDefaultAzureCredential(nil)
    if err != nil {
        log.Fatalf("create credential: %v", err)
    }

    cfg, err := harness.AgentConfig(
        // This example doesn't need hosted web search
        harness.Config{DisableWebSearch: true},
        agent.Config{Name: "ProjectAssistant"},
    )
    if err != nil {
        log.Fatalf("configure harness: %v", err)
    }

    a := foundryprovider.NewAgent(
        endpoint,
        credential,
        foundryprovider.ModelDeployment(deployment),
        foundryprovider.AgentConfig{
            Config:       cfg,
            Instructions: "Help with software engineering tasks. Use memory and to-do items when asked.",
            // Retain conversation history in agent.Session rather than at the service.
            DisableStoreOutput: true,
        },
    )

    ctx := context.Background()
    session, err := a.CreateSession(ctx)
    if err != nil {
        log.Fatalf("create session: %v", err)
    }

    for _, prompt := range []string{
        "Plan a health-check endpoint for a Go net/http service. Record the tasks as to-do items and save the plan in healthcheck.md.",
        "Read healthcheck.md and list the remaining to-do items. Explain what you would implement first, without editing the service.",
    } {
        fmt.Printf("User: %s\n", prompt)
        response, err := a.RunText(ctx, prompt, agent.WithSession(session)).Collect()
        if err != nil {
            log.Fatalf("run agent: %v", err)
        }
        fmt.Printf("Assistant: %s\n\n", response)
    }
}
```

运行程序：

```bash
go mod tidy
go run .
```

程序会打印每个提示，随后打印代理的响应。
代理利用第一个请求中的任务列表和已保存计划来回答第二个请求。
工具选择和回复措辞因模型而异。

本示例在其 `foundryprovider.AgentConfig` 中将 `DisableStoreOutput` 设置为 `true`，以禁用 Foundry 响应存储。
在这里，托管框架的历史记录提供程序将会话保存在本地的 `agent.Session` 中，因此程序不依赖 Foundry 来重放已存储的响应。
当你希望稍后检索响应或使用 Foundry 托管的对话历史记录时，服务端存储会很有用。

## 状态存放在哪里

`session` 变量指向 Go 进程内存中的一个 `agent.Session` 对象。
会话存储待办事项和内存文件夹路径，而 FileMemory 会将计划写入程序工作目录下的 `agent-file-memory/<session-folder>/healthcheck.md`。

再次运行程序会创建一个新会话和一个不同的文件夹。

要让你的应用程序在重启后能够继续，请保存并恢复会话状态，并使用相同的内存根目录。
[内存与持久化指南](https://learn.microsoft.com/en-us/agent-framework/get-started/memory?pivots=programming-language-go)展示了使用 `encoding/json` 进行会话序列化的方法。
恢复会话会自动还原任务列表并选择之前的内存文件夹。

如果你的代理需要来自超出提示容量的大量文档的上下文，请参阅我们的[嵌入与向量搜索文章](https://devblogs.microsoft.com/go/embeddings-and-vector-search-in-agent-framework-for-go/)，其中提供了一个按语义检索段落的示例。

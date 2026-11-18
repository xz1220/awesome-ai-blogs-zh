# Kimi Code CLI v2.6.0 发布说明（Kimi Code CLI v2.6.0）

> 原文：[Kimi Code CLI v2.6.0](https://github.com/MoonshotAI/kimi-code/releases/tag/%40moonshot-ai/kimi-code%402.6.0) · Kimi · 2026-11-12
> 本文由 Kimi CLI 使用 Kimi K3-256k 全文翻译，并由 Agent 校对；已取得全文翻译和转载授权。
> 作者：github-actions[bot]

### 次要变更

- [#4752](https://github.com/MoonshotAI/kimi-code/pull/4752) [`5aa81c5`](https://github.com/MoonshotAI/kimi-code/commit/5aa81c5e22de5a446290e33ce02ddc259b0f5c36) 感谢 [@sailist](https://github.com/sailist)! - 让 `fs:suggest` 与本地 fd 补全对齐,采用有界扫描且最多返回 20 条结果,并支持可选的流式预览;同时默认包含隐藏路径和被 gitignore 的路径,并在匹配质量相同时将普通文件排在前面。

- [#4618](https://github.com/MoonshotAI/kimi-code/pull/4618) [`e6ae8ed`](https://github.com/MoonshotAI/kimi-code/commit/e6ae8ed4bdd0a99a3f5d4c4dc1b19b0b2f9a4a9c) 感谢 [@Grapedge](https://github.com/Grapedge)! - 在全屏模式下将连续的工具调用和思考折叠为摘要行,并且不再为模型加载的技能显示"已激活技能"卡片。可在 /settings 中的"工具调用密度"和"思考折叠"下选择折叠程度,并预览每种选择的效果;也可以在 tui.toml 的 `[transcript]` 下设置 `tool_call_density = "ungrouped"` 和 `thinking = "ungrouped"` 以保留之前的布局。

### 补丁变更

- [#4751](https://github.com/MoonshotAI/kimi-code/pull/4751) [`b64a016`](https://github.com/MoonshotAI/kimi-code/commit/b64a016b16dbd8f775d87c9f6890b4c5c7b13ee5) 感谢 [@Grapedge](https://github.com/Grapedge)! - 在模型生成内容时,在活动栏中显示当前回合已运行的时长;回合完成后,显示上一个回合花费了多长时间以及何时结束。

- [#4663](https://github.com/MoonshotAI/kimi-code/pull/4663) [`1dd5578`](https://github.com/MoonshotAI/kimi-code/commit/1dd5578649e01dd8f5a2c0c7f924977f919c0b22) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 通过 WebSocket `agent` 帧上的 `compacting` 标志报告上下文压缩。

- [#4839](https://github.com/MoonshotAI/kimi-code/pull/4839) [`afadca2`](https://github.com/MoonshotAI/kimi-code/commit/afadca241660e68a9cbdb3374ef047d6cdf36750) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 服务器 API 会话现在在创建时会获取其 agent 配置文件(profile)、模型和思考级别;提示词不再接受 `profile` 参数,请改为在创建会话时传递 `agent_config.profile`。

- [#4836](https://github.com/MoonshotAI/kimi-code/pull/4836) [`5ad9aa1`](https://github.com/MoonshotAI/kimi-code/commit/5ad9aa18f140321ec257f29af0003526a5e82424) 感谢 [@sailist](https://github.com/sailist)! - 防止在恢复或撤销后出现重复的后台任务通知,并在回合收尾期间保留提示词生命周期的完成状态。

- [#4755](https://github.com/MoonshotAI/kimi-code/pull/4755) [`322d036`](https://github.com/MoonshotAI/kimi-code/commit/322d0363f4c5cf332034ff81759653bf341f165c) 感谢 [@Grapedge](https://github.com/Grapedge)! - 在 SSH 和 mosh 之外的环境中,复制操作现在只写入系统剪贴板,而不再同时经由终端(OSC 52);设置 `KIMI_CODE_CLIPBOARD_OSC52=1` 可保留旧行为。

- [#4773](https://github.com/MoonshotAI/kimi-code/pull/4773) [`881e61b`](https://github.com/MoonshotAI/kimi-code/commit/881e61b4076a40223c01668c458a0bfc458b2c27) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 在 Web UI 中,当另一项压缩正在运行时请求手动压缩,现在会报告错误,而不是静默忽略。

- [#4663](https://github.com/MoonshotAI/kimi-code/pull/4663) [`1dd5578`](https://github.com/MoonshotAI/kimi-code/commit/1dd5578649e01dd8f5a2c0c7f924977f919c0b22) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 通过服务器 WebSocket 以 `turns`、`turns.removed`、`turns.failed`、`turn.*`、`item.*` 和 `notice` 帧流式传输每个已订阅 agent 的对话,并可通过 `GET /sessions/{id}/agents/{agent_id}/turns` 分页获取更早的回合;`subscribe_v2` 现在接受 `agent_ids` 而不再是 transcript 等级;携带捆绑技能和技能激活的提示词接受客户端传入的 `prompt_id`;transcript 帧以及 `GET /sessions/{id}/transcript` 端点(包括 `/ops`、`/plan` 和 `/user-messages`)不再可用。

- [#4618](https://github.com/MoonshotAI/kimi-code/pull/4618) [`e6ae8ed`](https://github.com/MoonshotAI/kimi-code/commit/e6ae8ed4bdd0a99a3f5d4c4dc1b19b0b2f9a4a9c) 感谢 [@Grapedge](https://github.com/Grapedge)! - 修复了在模型加载多个技能后,Ctrl+O 对最新回合展开的内容过少的问题。

- [#4708](https://github.com/MoonshotAI/kimi-code/pull/4708) [`d0cd33c`](https://github.com/MoonshotAI/kimi-code/commit/d0cd33c300acdc1540f75568d77babea7b9d55c8) 感谢 [@RealKai42](https://github.com/RealKai42)! - 不再禁止对同一文件进行多次 Edit 调用,也不再要求在每次 Edit 之前重新读取文件。

- [#4777](https://github.com/MoonshotAI/kimi-code/pull/4777) [`b9c1897`](https://github.com/MoonshotAI/kimi-code/commit/b9c18978accb4da89adaed53d40483331cfaaa66) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 不再在错误响应中发送服务器堆栈跟踪,并将缺失的 provider、凭据或模型报告为设置错误,而不是内部错误。

- [#4665](https://github.com/MoonshotAI/kimi-code/pull/4665) [`8d1af37`](https://github.com/MoonshotAI/kimi-code/commit/8d1af37d5d9cdff06c17f726a83ba69ae4e02080) 感谢 [@Grapedge](https://github.com/Grapedge)! - 在使用 ctrl+o 展开大量工具输出时,保持终端 UI 响应流畅。

- [#4766](https://github.com/MoonshotAI/kimi-code/pull/4766) [`adc46cc`](https://github.com/MoonshotAI/kimi-code/commit/adc46cc072688e4ad27c53f7a5dfba245fcb2bbd) 感谢 [@pvzheroes125](https://github.com/pvzheroes125)! - 当显式选择的技能目录中的文件发生变化时,重新加载技能。

- [#4663](https://github.com/MoonshotAI/kimi-code/pull/4663) [`1dd5578`](https://github.com/MoonshotAI/kimi-code/commit/1dd5578649e01dd8f5a2c0c7f924977f919c0b22) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 对于在其回合开始之前就失败的提示词,现在以 `failed` 状态报告,而不是 `queued`。

- [#4826](https://github.com/MoonshotAI/kimi-code/pull/4826) [`13590cd`](https://github.com/MoonshotAI/kimi-code/commit/13590cdea594d3dfa86fd38f19f3ff4de22dea15) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 服务器 API 的文件历史查询不再接受 `turn_id`;请改为传递 `turn_number`。

- [#4822](https://github.com/MoonshotAI/kimi-code/pull/4822) [`4ac656c`](https://github.com/MoonshotAI/kimi-code/commit/4ac656c5028a91210d3eff135f0f2063b005332f) 感谢 [@liruifengv](https://github.com/liruifengv)! - 修复了在压缩过程中收到系统提醒时上下文压缩被取消的问题,并将这些提醒保留在压缩后的历史中。

- [#4800](https://github.com/MoonshotAI/kimi-code/pull/4800) [`4b4cf3a`](https://github.com/MoonshotAI/kimi-code/commit/4b4cf3a9dea9dfa4b30d738e2b91879ad7bc5d10) 感谢 [@kimi-agent-bot](https://github.com/kimi-agent-bot)! - 为失败的文件下载返回正确的 HTTP 错误。

- [#4719](https://github.com/MoonshotAI/kimi-code/pull/4719) [`bae3211`](https://github.com/MoonshotAI/kimi-code/commit/bae32119ca37229a301f8099e7812b07f205dbfe) 感谢 [@pvzheroes125](https://github.com/pvzheroes125)! - 修复工具更新后出现重复工具定义和空工具公告的问题。

- [#4720](https://github.com/MoonshotAI/kimi-code/pull/4720) [`df90d90`](https://github.com/MoonshotAI/kimi-code/commit/df90d90ec0714db23dcc830acd2db6232f5c7426) 感谢 [@pvzheroes125](https://github.com/pvzheroes125)! - 修复不支持动态工具加载的模型中工具定义过时的问题。

- [#4563](https://github.com/MoonshotAI/kimi-code/pull/4563) [`1eb3c53`](https://github.com/MoonshotAI/kimi-code/commit/1eb3c537eb2ae83b044e34356932edf492f83a3e) 感谢 [@kimi-agent-bot](https://github.com/kimi-agent-bot)! - 修复非 ASCII 文件名的文件预览问题。

- [#4825](https://github.com/MoonshotAI/kimi-code/pull/4825) [`41b7acc`](https://github.com/MoonshotAI/kimi-code/commit/41b7acceb3cd2e51314fd2909996fcb0213f8ff8) 感谢 [@pvzheroes125](https://github.com/pvzheroes125)! - 修复在超长 Windows 路径中启动命令以及在超长 Windows 目录中搜索文件时崩溃的问题。

- [#4832](https://github.com/MoonshotAI/kimi-code/pull/4832) [`6dd56ba`](https://github.com/MoonshotAI/kimi-code/commit/6dd56ba396a8c2ca6de73ce64d5a7728edea2430) 感谢 [@sailist](https://github.com/sailist)! - 在 agent 的可用工具发生变化后对其进行分叉(fork)时,保留提示词缓存。

- [#4867](https://github.com/MoonshotAI/kimi-code/pull/4867) [`8aacf88`](https://github.com/MoonshotAI/kimi-code/commit/8aacf888c6d2b536dc60214973e413a3646893e4) 感谢 [@sailist](https://github.com/sailist)! - 在分叉对话时保留工具结果备注,使旁支对话保持相同的模型可见历史和提示词缓存前缀。

- [#4755](https://github.com/MoonshotAI/kimi-code/pull/4755) [`322d036`](https://github.com/MoonshotAI/kimi-code/commit/322d0363f4c5cf332034ff81759653bf341f165c) 感谢 [@Grapedge](https://github.com/Grapedge)! - 修复全屏模式下的复制以及 `/copy` 在 tmux 和 Linux 上无法工作的问题。

- [#4755](https://github.com/MoonshotAI/kimi-code/pull/4755) [`322d036`](https://github.com/MoonshotAI/kimi-code/commit/322d0363f4c5cf332034ff81759653bf341f165c) 感谢 [@Grapedge](https://github.com/Grapedge)! - 为全屏模式新增"选中即复制"设置;在 `/settings` 中将其关闭后,仅在按下 `Ctrl-C` 时才进行复制。

- [#4755](https://github.com/MoonshotAI/kimi-code/pull/4755) [`322d036`](https://github.com/MoonshotAI/kimi-code/commit/322d0363f4c5cf332034ff81759653bf341f165c) 感谢 [@Grapedge](https://github.com/Grapedge)! - 在全屏模式下,现在可以使用 `Ctrl-C` 或 `Cmd-C` 复制选中的文本。

- [#4771](https://github.com/MoonshotAI/kimi-code/pull/4771) [`c01a04a`](https://github.com/MoonshotAI/kimi-code/commit/c01a04a2557fa8bae5c467a9d7bf2c13a2b3881e) 感谢 [@Grapedge](https://github.com/Grapedge)! - 当设置了 `KIMI_CODE_EXPERIMENTAL_FLAG=1` 时,TUI 默认使用全屏模式而不是常规模式。

- [#4814](https://github.com/MoonshotAI/kimi-code/pull/4814) [`f2ce60f`](https://github.com/MoonshotAI/kimi-code/commit/f2ce60f3206e1e30895219bf080542f23d04ea59) 感谢 [@Grapedge](https://github.com/Grapedge)! - 在全屏模式下,NotifyUser 更新以主色调圆点显示,而不是"更新"徽标。

- [#4827](https://github.com/MoonshotAI/kimi-code/pull/4827) [`5518d54`](https://github.com/MoonshotAI/kimi-code/commit/5518d54472315e92936cf6a1bd5d60991f9aceaf) 感谢 [@7Sageer](https://github.com/7Sageer)! - 跨回合保留 Gemini 的思考签名和原生工具上下文。

- [#4735](https://github.com/MoonshotAI/kimi-code/pull/4735) [`bc6fa89`](https://github.com/MoonshotAI/kimi-code/commit/bc6fa89a759a15fa0a92a10b9ffb2180b7545655) 感谢 [@7Sageer](https://github.com/7Sageer)! - 支持从自定义注册表导入 `google-genai` provider,包括已经以 `/v1beta` 结尾的端点。

- [#4618](https://github.com/MoonshotAI/kimi-code/pull/4618) [`e6ae8ed`](https://github.com/MoonshotAI/kimi-code/commit/e6ae8ed4bdd0a99a3f5d4c4dc1b19b0b2f9a4a9c) 感谢 [@Grapedge](https://github.com/Grapedge)! - 在工具分组或思考分组开启时，不再在全屏页脚中显示 ctrl+o 展开和折叠提示。

- [#4663](https://github.com/MoonshotAI/kimi-code/pull/4663) [`1dd5578`](https://github.com/MoonshotAI/kimi-code/commit/1dd5578649e01dd8f5a2c0c7f924977f919c0b22) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 对使用相同 `prompt_id` 重新提交的提示词及其请求，改为返回首次提交的结果，而不是冲突错误。

- [#4618](https://github.com/MoonshotAI/kimi-code/pull/4618) [`e6ae8ed`](https://github.com/MoonshotAI/kimi-code/commit/e6ae8ed4bdd0a99a3f5d4c4dc1b19b0b2f9a4a9c) 感谢 [@Grapedge](https://github.com/Grapedge)! - 实时思考过程现在以高亮的 `Thinking` 标题和已用时间计时器显示，取代原来的 `thinking…` 旋转指示器。

- [#4757](https://github.com/MoonshotAI/kimi-code/pull/4757) [`c4f81f8`](https://github.com/MoonshotAI/kimi-code/commit/c4f81f832ebcb038b264a64f16e5586fd7fee0f1) 感谢 [@7Sageer](https://github.com/7Sageer)! - 会话启动时应用 config.toml 中的 `[[permission.rules]]`，包括打印模式下的 deny、ask 和 allow 规则。

- [#4848](https://github.com/MoonshotAI/kimi-code/pull/4848) [`9ae2757`](https://github.com/MoonshotAI/kimi-code/commit/9ae2757d0385ca255ce3ca4bfd2babe6d31b0539) 感谢 [@sailist](https://github.com/sailist)! - 防止多个应用实例恢复同一会话并并发运行其待处理的任务轮次。

- [#4831](https://github.com/MoonshotAI/kimi-code/pull/4831) [`392505c`](https://github.com/MoonshotAI/kimi-code/commit/392505cf579dcb2cfa92de1ca0262bb2407ace30) 感谢 [@sailist](https://github.com/sailist)! - 修复桌面端重试状态、部分响应历史记录和后台任务调度问题。

- [#4690](https://github.com/MoonshotAI/kimi-code/pull/4690) [`27bd9ba`](https://github.com/MoonshotAI/kimi-code/commit/27bd9baba10e9f73d3db0e0fdd6f81046b4cbac9) 感谢 [@liruifengv](https://github.com/liruifengv)! - 同名工作区技能仍可在 TUI 的专属 Skills 分组中选择，并通过目录名或全局、内置标签区分其来源。

- [#4550](https://github.com/MoonshotAI/kimi-code/pull/4550) [`53d1caf`](https://github.com/MoonshotAI/kimi-code/commit/53d1caf70b2a07ed2b4d7e49716cd707a85bc2e8) 感谢 [@sailist](https://github.com/sailist)! - 持久化用户和项目权限规则，并在会话启动时应用。

- [#4644](https://github.com/MoonshotAI/kimi-code/pull/4644) [`8985b71`](https://github.com/MoonshotAI/kimi-code/commit/8985b71d7aa1afe5723af115f3459c0881186295) 感谢 [@7Sageer](https://github.com/7Sageer)! - 编辑文件时保留 UTF-8 字节顺序标记（BOM)。

- [#4800](https://github.com/MoonshotAI/kimi-code/pull/4800) [`4b4cf3a`](https://github.com/MoonshotAI/kimi-code/commit/4b4cf3a9dea9dfa4b30d738e2b91879ad7bc5d10) 感谢 [@kimi-agent-bot](https://github.com/kimi-agent-bot)! - 下载已上传文件时保留 Unicode 文件名。

- [#4842](https://github.com/MoonshotAI/kimi-code/pull/4842) [`421388b`](https://github.com/MoonshotAI/kimi-code/commit/421388b74958bf4d5060e7eb08175572d4db62ad) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 服务器 API 的会话档案端点现在与会话创建一样，忽略保留的元数据键 `cwd`、`goal`、`parent_session_id` 和 `child_session_kind`。

- [#4662](https://github.com/MoonshotAI/kimi-code/pull/4662) [`8fc5e22`](https://github.com/MoonshotAI/kimi-code/commit/8fc5e22f966187ca93ec1027153e7f6028d3661e) 感谢 [@sailist](https://github.com/sailist)! - 会话升级提示中的协议细节替换为简洁的升级消息；读取器版本仍保留在错误详情和诊断日志中。

- [#4699](https://github.com/MoonshotAI/kimi-code/pull/4699) [`2a6d1cf`](https://github.com/MoonshotAI/kimi-code/commit/2a6d1cf570d15174d6d5add04eaa8d9d6d45348b) 感谢 [@7Sageer](https://github.com/7Sageer)! - 在匿名遥测中记录会话标题生成的结果、耗时和标题长度。

- [#4698](https://github.com/MoonshotAI/kimi-code/pull/4698) [`2be062e`](https://github.com/MoonshotAI/kimi-code/commit/2be062e8ea887193db9106013c85c81eb62f2826) 感谢 [@7Sageer](https://github.com/7Sageer)! - 在 /status 和 Markdown 导出元数据中使用绑定的工作目录，并从每个会话的环境中读取会话列表的 git 详情。

- [#4427](https://github.com/MoonshotAI/kimi-code/pull/4427) [`1c259c8`](https://github.com/MoonshotAI/kimi-code/commit/1c259c8d35ff648ce8aa3f77169d9887e2a16384) 感谢 [@tpoisonooo](https://github.com/tpoisonooo)! - 允许将 `primary` 作为普通的 `[secondary_model]` 模型别名，并移除保留的 `PRIMARY_SUBAGENT_MODEL_CHOICE` SDK 导出；Tower 审查者现在使用模型池默认值而非主模型，且不再接受特殊的 `model: "primary"` 后门写法，因此要用主模型进行审查，需要显式为主模型选择一个模型池别名，或将其设为所有派生任务的 `default_model`。

- [#4855](https://github.com/MoonshotAI/kimi-code/pull/4855) [`fb8ea02`](https://github.com/MoonshotAI/kimi-code/commit/fb8ea02aaa20cb92e783e8d67e588d0968687b80) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 修复模型请求在流传输中途失败后，其部分回复仍停留在屏幕上、与自动重试的回复并列显示的问题。

- [#4767](https://github.com/MoonshotAI/kimi-code/pull/4767) [`97637e5`](https://github.com/MoonshotAI/kimi-code/commit/97637e54a079cace2ba710b38ffb4ed85b232351) 感谢 [@pvzheroes125](https://github.com/pvzheroes125)! - 避免在多次模型请求中重复上传同一张 MCP 工具图片。

- [#4617](https://github.com/MoonshotAI/kimi-code/pull/4617) [`6974ac8`](https://github.com/MoonshotAI/kimi-code/commit/6974ac880d405d5565a2189925f3bef6daea6892) 感谢 [@Grapedge](https://github.com/Grapedge)! - 展开的 Grep 和 Glob 结果中的文件列表在换行时保持缩进。

- [#4663](https://github.com/MoonshotAI/kimi-code/pull/4663) [`1dd5578`](https://github.com/MoonshotAI/kimi-code/commit/1dd5578649e01dd8f5a2c0c7f924977f919c0b22) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 从 `POST /api/v1/search` 响应中移除 `source` 字段。

- [#4778](https://github.com/MoonshotAI/kimi-code/pull/4778) [`c87878a`](https://github.com/MoonshotAI/kimi-code/commit/c87878a72ff341da26536e87ae6bc3cd5fcfc676) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 通过服务器 API 创建会话时，应用传入的智能体设置和自定义元数据；开启 Tower 模式的创建请求现在会被拒绝，请在会话创建后通过会话档案开启。

- [#4799](https://github.com/MoonshotAI/kimi-code/pull/4799) [`11d9fda`](https://github.com/MoonshotAI/kimi-code/commit/11d9fda8e39598ea13aa05fa9f69c8723861f66a) 感谢 [@liruifengv](https://github.com/liruifengv)! - 修复禁用 `Skill` 工具时技能目录从系统提示词中被遗漏的问题。

- [#4713](https://github.com/MoonshotAI/kimi-code/pull/4713) [`cd48f5e`](https://github.com/MoonshotAI/kimi-code/commit/cd48f5e84b74ddcd91c40e25d59470d43a05b6a0) 感谢 [@RealKai42](https://github.com/RealKai42)! - 引导模型通过 `Skill` 工具调用技能，而不是直接读取技能文件。

- [#4854](https://github.com/MoonshotAI/kimi-code/pull/4854) [`265783c`](https://github.com/MoonshotAI/kimi-code/commit/265783ca457191fec45b71a8532df23730a841fd) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 修复已停止的工具调用显示通用中断提示、而不是其停止前所产生输出的问题。

- [#4730](https://github.com/MoonshotAI/kimi-code/pull/4730) [`ce38ebf`](https://github.com/MoonshotAI/kimi-code/commit/ce38ebf25d19276b12eca1e1e864b0afe8cdc7d7) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 流式传输的推理和消息条目不再在所属步骤的下一个块开始时提前收到 `item.ended`；它们现在只在步骤持久化后结束一次，因此推理时长不会再事后变动。

- [#4778](https://github.com/MoonshotAI/kimi-code/pull/4778) [`c87878a`](https://github.com/MoonshotAI/kimi-code/commit/c87878a72ff341da26536e87ae6bc3cd5fcfc676) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 当服务器 API 请求要求模型不支持的思考级别时，返回校验错误而不是内部服务器错误。

- [#4862](https://github.com/MoonshotAI/kimi-code/pull/4862) [`7980593`](https://github.com/MoonshotAI/kimi-code/commit/7980593a6d7f2f75b01260e5198f1b737a48aa63) 感谢 [@sailist](https://github.com/sailist)! - 修复重新加载动态工具后出现重复工具声明错误的问题。

- [#4689](https://github.com/MoonshotAI/kimi-code/pull/4689) [`51b47db`](https://github.com/MoonshotAI/kimi-code/commit/51b47db877149a38f2f14978ff526c752569a0b0) 感谢 [@liruifengv](https://github.com/liruifengv)! - 主目录切换后，默认本地工作目录跟随当前主目录；如需保留原先固定目录的行为，请使用显式的 environmentCwd；同时保持工具、项目配置和会话索引同步。

- [#4772](https://github.com/MoonshotAI/kimi-code/pull/4772) [`aa12538`](https://github.com/MoonshotAI/kimi-code/commit/aa125382cb4d3040671a9c13ca626dbdd46e9f27) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 修复在 Web UI 中停止某个轮次后，正在运行的工具调用显示为失败的问题。

- [#4427](https://github.com/MoonshotAI/kimi-code/pull/4427) [`1c259c8`](https://github.com/MoonshotAI/kimi-code/commit/1c259c8d35ff648ce8aa3f77169d9887e2a16384) 感谢 [@tpoisonooo](https://github.com/tpoisonooo)! - 新增制品（artifact）任务，支持关键交付物审查和对整个已提交分支 tip 的人工验收；将面向 LLM 的 TowerStatus 详情列表限制为最新 20 条；并在状态和任务视图中显示任务类型。

- [#4834](https://github.com/MoonshotAI/kimi-code/pull/4834) [`bd62933`](https://github.com/MoonshotAI/kimi-code/commit/bd629337a05e0840b985fe2aee3a143f85d0f3c0) 感谢 [@sailist](https://github.com/sailist)! - 截断过大的 Skill 工具内容，并将完整内容保存在文件中。

- [#4870](https://github.com/MoonshotAI/kimi-code/pull/4870) [`bd75a36`](https://github.com/MoonshotAI/kimi-code/commit/bd75a36f436c343e4cb3023b6a6f1b83ccbf62eb) 感谢 [@Grapedge](https://github.com/Grapedge)! - 新增 `KIMI_CODE_TUI_ANIMATION_FPS` 环境变量，用于调整进行中标题的闪烁动画帧率。将其设置为 1 到 60 的整数。

- [#4663](https://github.com/MoonshotAI/kimi-code/pull/4663) [`1dd5578`](https://github.com/MoonshotAI/kimi-code/commit/1dd5578649e01dd8f5a2c0c7f924977f919c0b22) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - `POST /sessions/{id}:undo` 现在接收要撤销的轮次的 `turn_id` 和可选的 `agent_id`（而不再是一个 `count`），并返回 `removed_turn_ids`，而不再返回一页消息。

- [#4846](https://github.com/MoonshotAI/kimi-code/pull/4846) [`ac09c02`](https://github.com/MoonshotAI/kimi-code/commit/ac09c028b1bddb7c635f5f039f8e75875f85420e) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 修复了针对同一轮次的两个并发撤销请求也会移除其之前轮次的问题。

- [#4770](https://github.com/MoonshotAI/kimi-code/pull/4770) [`823c159`](https://github.com/MoonshotAI/kimi-code/commit/823c159a3825a2abaa163c1945893935c3fbab42) 感谢 [@pvzheroes125](https://github.com/pvzheroes125)! - 当额外技能目录中的文件发生变化时，重新加载技能。

- [#4871](https://github.com/MoonshotAI/kimi-code/pull/4871) [`54087b8`](https://github.com/MoonshotAI/kimi-code/commit/54087b8a73a5076b39d91ffcb824b6206d6403f5) 感谢 [@kimi-agent-bot](https://github.com/kimi-agent-bot)! - web：改进了交互并修复了已知错误。

- [#4747](https://github.com/MoonshotAI/kimi-code/pull/4747) [`79ff88b`](https://github.com/MoonshotAI/kimi-code/commit/79ff88bb2b518fc9a15a5645c7bd961447530285) 感谢 [@hunshcn](https://github.com/hunshcn)! - 修复了注册项目过多时工作区操作缓慢的问题。

- [#4823](https://github.com/MoonshotAI/kimi-code/pull/4823) [`7a0205c`](https://github.com/MoonshotAI/kimi-code/commit/7a0205c25a017b90635b285d24db513e9fb5ff99) 感谢 [@wbxl2000](https://github.com/wbxl2000)! - 修复了服务器停顿或系统时钟跳变后，服务器 WebSocket 连接因心跳超时被关闭的问题。

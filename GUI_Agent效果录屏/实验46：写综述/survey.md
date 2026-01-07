# 基础知识

## HTML、DOM、AXTree

- HTML源码：并非用户真正看到的内容。
- 无障碍树：不可进行JS注入来操作网页。
- DOM：冗余。内容比AOM多很多。

可以通过 CDP 命令（如 DOM.resolveNode）将 AXTree 的节点转回 DOM 节点，从而执行 JS吗？

这要看当前业界普遍做法，以 browser-use 为例。豆包的解释是，以DOM为主体，融合了AXTree。

总结：目前还是依赖DOM。

无障碍树（AXTree）
![[无障碍树.png]]
DOM（以HTML呈现）
![[DOM.png]]
HTML源码
![[HTML源码.png]]

---


以下是将该 Typst 文档转换为 Markdown 格式的内容：

# 主题：GUI Agent

**GUI 的定义**：图形用户界面，通过图像化的方式与用户交互。

**GUI Agent 的定义**：大模型驱动的智能体，代替人类使用图形用户界面完成任务。

# GUI Agent 的意义

*   **不能执行操作**：视力障碍人士，无法使用传统界面。
*   **不会做**：能执行操作，但是不知道如何操作。系统复杂，不会使用。
*   **不想做**：能做、会做，但是重复枯燥。
*   **做的慢**：能做、会做，但是效率低下。

# GUI Agent 的原理

# 最新 GUI Agent 发展

## WGE
*   **时间**：2018年2月。
*   **出品方**：斯坦福。
*   早在2018年的本文，就有 agent 的概念了。
*   Web tasks 的难点在于，具有很大的 action space，因为 agent 能够输入或点击任何东西。
*   前人试图让 agent 模仿专家演示，但是专家演示仅能覆盖很小的状态空间，难于泛化。
*   本文提出了不同的利用专家演示的方法（但还是用了专家演示）。
*   **本文辨析了两个概念**：
    *   **Expert demonstration (actual policy)**：具体点击哪封邮件，具体在哪个文本框中填写。
    *   **Workflow**：更高层。点击一个邮件标题 -> 点击转发按钮 -> 在文本框中输入地址 -> 点击发送按钮。
*   **强化学习设置**：在标准的强化学习设置中，一个 agent 学习一个 policy $\pi(a|s)$，将状态 $s$ 映射到动作 $a$ 上的概率分布。在每个时刻 $t$，agent 观测到环境状态 $s_t$，选择一个动作 $a_t$，前进至新的状态 $s_{t+1}$，获得一个奖赏 $r_t = r(s_t, a_t)$。目标是最大化期望 $\mathbb{E}[R]$，其中 $R = \sum_t \gamma^t r_{t+1}$。
*   网页的当前状态用 **DOM tree** 表示。
*   本文限制动作空间为两类：`Click(e)` 和 `Type(e, t)`，其中 $e$ 是 DOM Tree 的 leaf element。
*   **Neural policy $\pi$** 是一个神经网络，输入是文本（用户输入 + DOM tree），输出是文本（动作）。

## WebGPT

时间：2021年12月。出品方：OpenAI

在GPT3上进行了微调。

本文不是操作浏览器，而是记录网络进行检索以实现更好的问答。这是现在的ChatBot上的联网搜索按钮对应的论文。

## ReAct

时间：2022年10月。出品方：谷歌。

本文提出了 interactive decision making benchmarks: WebShop.

本文的本质贡献是提出可以使用 LLM 来执行 agent。（以前的agent不用LLM。如WGE2018）

agent的上下文：$c_t = (o_1, a_1, \cdots, o_{t-1}, a_{t-1}, o_t)$。大模型执行策略$\pi(a_t|c_t)$，即一个映射 $c_t \mapsto a_t$。这是 act 模式。本文在此基础上增加了额外的 reasoning，用来决定搜什么、何时买，以及哪些产品选项与指令相关。

## Mind2Web
*   **时间**：2023年6月。
*   Mind2Web是用于 web agents 的数据集：从 137 个网站收集了 2000 多个任务。本文提出的智能体为 MindAct。
*   **核心问题**：如何构建一个 web agent，给定任意网站，能够遵循自然语言执行任务？——这说明在此之前很少有人提出并解决这一问题。
*   文章列举了现有的 web agents 工作：[5][21,][22,,][35][40,,]，其中 [5, 21, 22, 39] 需要用户的 step-by-step instructions。[22] 是 WGE。
*   本文指出，利用 LLM 作为 web agents 是一种解决方案，但是目前没有相应数据集。——这说明之前的 web agents 没有使用 LLM。
* 本文指出，先前的数据集，是在模拟环境中构造虚假的网站。

数据集的每个实例由如下三部分组成：
- 任务描述
* 动作：是一个 (Target Element, Operation) 对。Target Element 指的是网页上的某个元素。Operation指的是CLICK、Type（'123'）等动作。
* 网页快照（DOM Tree）

本文指出，以前的工作着重于将 low-level instructions（Type New York in the location field, click the search button and choose the tomorrow tab）转化成具体动作的能力。本文采用的是 high-level goals: What is the weather for New York tomorrow?

MindAct：两阶段。第一阶段：精简网页元素。第二阶段：在精简的元素基础上生成动作。

问题：数据集能否下载下来实际看看？

## WebArena

- **时间**：20203年7月
- **出品方**：卡内基梅隆

配备了工具调用和用户手册。

本文使用2种提示词策略制作了三个 Web Agents。在上下文中提供两个例子。
- 第一种提示词策略：根绝当前观测、意图、历史动作，直接预测下一个动作。
- 在预测动作之间先进行 chain-of thought reasoning
- 使用包含元素ID的AXTree作为观测空间。

https://docs.google.com/spreadsheets/d/1M801lEpBbKSNwP-vDBkC_pF7LdyGU1f_ufZb_NWNBZQ/edit?gid=0#gid=0 该benchmark的榜单。能看到最新的工作。

## MemGPT

- **时间**：2023年10月
- **出品方**：加州伯克利

大模型窗口有限。本文提出 virtural context management。

在 MemGPT 中，LLM 能够决定将什么放到它的上下文中。

当上下文过长时，LLM通过调用工具，自动存储上下文中的重要信息。

## WebVoyager

### 简介
- **标题**：WebVoyager : Building an End-to-End Web Agent with Large Multimodal Models
- **时间**：2024 年 1 月
- **出品方**：腾讯
- **感知方式**：视觉+文本

## AutoWebGLM

### 简介

- **标题**：AutoWebGLM: A Large Language Model-based Web Navigating Agent
- **时间**：2024 年 4 月
- **基准测试平台**：本文提出了一个用于评估 WebAgent 的基准测试平台 AutoWebBench
	- 约一万条轨迹
- **数据收集**：本文收集了一个数据集来微调模型
	- 通过浏览器插件记录网页任务的执行过程
	- 训练的模型大小为6B，基于ChatGLM3-6B微调
## Agent S

### 要点
- **时间**：2024年10月
- 本文重点考虑了 domain-specific knowledge，提出了 experience-augmented hierarchical planning

### EXPERIENCE-AUGMENTED HIERARCHICAL PLANNING

- 用户的 Query 用于：从记忆中检索相似任务经验。检索是基于 query embedding 的相似性。
- Planner 根据经验生成 subtask
## ScribeAgent

**要点：**
- **时间**：2024年11月
- 使用生产规模的工作流数据微调模型。共60亿tokens。
- 现有的 Web Agents 基于提示词，但本文的微调策略更好。
- 仅利用网页的文本形式而非截图，因为缺乏有效的视觉处理工具

### 数据集获取
- 靠 Scribe，这是一个商业化的产品。这篇论文就是这个公司发布的
	- 类似开源工具：https://github.com/AutomaApp/automa
- 记录了页面的DOM和动作
- 有无障碍树还要对DOM进行处理，这说明无障碍树不能替代DOM
	- 我们不使用可访问性树来开发ScribeAgent，因为它可能会丢失有关HTML元素的信息，例如下拉项，并且无法在不同浏览器和设备间通用。
- 没有滚动这个动作，因为DOM就是完整的
- 收集时间：2个月
- 平均步骤：11步
- 可能涉及隐私，所以数据集不公开

### 微调
- 效果：在公开测试集上，比不微调提升了5到10个点。注意，这是对于常用应用，开源数据集上的。对于从来没有见过的业务平台，提升肯定明显。
	- 表1显示，在test split dataset上，至少有三倍提升。
- 缺点：微调需要技术、数据、算力。
- 具体怎么微调的？
- 微调时忽略了历史观测，因为上下文窗口不够
- 进行有监督微调。对于每个样本，标签是下一步动作而非后续所有动作。
- 使用LoRA进行微调。
	- epoch = 2
	- batch size = 32
	- LoRA rank = 64
	- $\alpha$ = 128
	- scheduler: cosine
	- warmup steps: 30
- learning rate: 1e-4
- 微调成本：Qwen2 7B 只需使用 8 块 H100 GPU 就能在一天内完成微调，而 Qwen2 57B 在相同的硬件配置下则需要超过一周的时间。
## PAE
* **时间**：2024年12月。
* **出品方**：亚马逊。
* **现状与问题**：如果每项技能都需要通过固定的人类标注指令手动指定，那么由于人类标注指令的数量和多样性限制，Agent的技能库必然会受到限制。
* **基于视觉**：而非DOM进行感知
* **问题**：是否涉及到模型训练？

## A Survey of WebAgents

**要点：**
- **时间**：2025 年 3 月
- **Agent S**：能够获取特定任务的经验，其中包括成功和失败路径的总结，从而生成一系列可以完成用户指令的子任务。
## UI-TARS-2
*   **时间**：2025年9月。
*   **出品方**：字节跳动。
*   **亮点**：
    1.  超越了 UI-Tars-1.5。
    2.  传统 GUI Agent 分别进行感知、规划、执行、记忆。
    3.  不仅基于 GUI-only operations（用于元素选择的点击、用于文本输入的打字、用于导航的滚动），还使用了 **SDK Functions**，如 file systems, terminal commands, APIs, MCP tool invocations, tool calling, coding 等工具。
    4.  提出了新模型。
*   **核心洞察**：数学/编程语料库很丰富，但是交互轨迹数据很少。

## Surfer 2
*   **时间**：2025年10月。
*   **出品方**：H 公司。
*   **亮点**：对于简单任务，不使用 planner。
*   **核心洞察**：先前的工作需要 environment-specific adaptations，如浏览器的 DOM parsers，手机的 accessibility trees。本文通过**纯视觉交互**统一了不同平台。

## Agent S3

设agent的操作序列是 $\tau = (s_0, a_1, s_1, \cdots, a_{T-1}, s_T)$，定义事实：$\phi_i = G(s_i, a_i, s_{i+1})$。据此可以生成行为叙事 $\tilde \tau = (s_0, \phi_0, \phi_1, \cdots, \phi_{T-1}, s_T)$，这让agent更加聚焦于轨迹之间的变化。

本文推出了两个东西：1. Agent S3，2. Agent S3 w/ bBoN（能提2~10个点）。
- Agent S3的两点改进：1. 使用tools而非单纯GUI操作。2. 使用一个agent（worker only）而非两个agent（高级规划器没有必要，有时适得其反，两者配合有过时现象）。
	- worker: 代码位于 [raw.githubusercontent.com/simular-ai/Agent-S/refs/heads/main/gui_agents/s3/agents/worker.py](https://raw.githubusercontent.com/simular-ai/Agent-S/refs/heads/main/gui_agents/s3/agents/worker.py)

## UltraCUA
*   **时间**：2025年10月。
* **Citations**: 2
*   **出品方**：苹果。
*   **亮点**：
    1.  不仅基于 GUI Operations，还结合了 tool execution。
    2.  提出了新模型。

## Prune4Web

### 简介

- **标题**：Prune4Web: DOM Tree Pruning Programming for Web Agent
- **时间**：2025年11月
- **Citations**: 0
- **发表于**: AAAI 2026
- **出品方**：北航
- **现状问题**：DOM很长，一万至十万tokens。
- **效果**：本文提出的 Purne4Web能降低 25~50 倍。
- **基于截图模式的缺点**：包含的语义信息有限，尤其是对于特殊图标，并且对分辨率变化和元素重叠非常敏感。相比之下，HTML/DOM 提供精确且稳定的语义和结构信息，使得元素选择能够准确无误，并且几乎没有歧义。
- **问题**：本文提出的 Purne4Web，是基于代码的，还是基于 LLM 的？如果是基于 LLM 的，则兴趣不大。
	- 是基于LLM的，但LLM的输入不是全量DOM。而是根据用户提出的问题生成一段修剪DOM的代码。
		- 缺点
			- 增加了调用LLM的次数
			- 生成的代码未必准确

## MAI-UI

### 简介
- **标题**：MAI-UI Technical Report: Real-World Centric Foundation GUI Agents
- **时间**：2025年12月
- **Citations**：0
- **设备**：手机。虽然提了一句可以用于电脑和网页，但是文章的各级标题都指向手机
- **感知方式**：视觉
- **Action创新点**：不再仅仅是UI动作（点击、填写），还能进行工具调用。不再仅仅强调与应用交互，还要与用户交互。
- **GUI 定位任务**：这是基于视觉的Agent衍生出来的专门任务。这说明基于视觉的agent在定位环节可能有误差。
- **训练**：进行了模型的训练。
## WebOperator

要点：
- 标题：WebOperator: Action-Aware Tree Search for Autonomous Agents in Web Environment
- 时间：2025年12月
- Citations：0
- 本文不训练模型，而是设计Agent框架。
- 使用AxTree
- 创新点：对动作进行 tree search
- 本工作是基于文本的


# GUI Agent 的分类

## 按平台分类
*   **浏览器**：Browser Use Agent
*   **手机**：Phone Use Agent
*   **桌面应用**：Computer Use Agent

## 按感知方式分类
*   **基于文本**：DOM
*   **基于图像**：视觉识别

## 按执行方式分类
*   **基于 API**：称为 API-driven agents。
*   **基于模拟键盘鼠标**：模拟人类操作。

## 按模型分类
*   **训练模型**：专门针对 GUI 任务训练的模型。
*   **通用大模型**：使用 GPT/Claude 等，重点在于 Agent 策略优化。

# Benchmark 与 结果

### OSWorld
* **Agent S**: 20.58%  
* **UI-TARS-2**: 47.5%
*   **Surfer 2**: 60.1%

### Online-Mind2Web
*   **UI-TARS-2**: 88.2

### WindowsAgentArena
*   **UI-TARS-2**: 50.6

### AndroidWorld
* **UI-TARS-2**: 73.3%
* **MAI-UI**：76.7%
* **Surfer 2 (另一测试集/版本)**: 87.1%

### MobileWorld

- **MAI-UI**：41.7%

### WebVoyage
*   **Surfer 2**: 97.1%

### WebArena
* **Surfer 2**: 69.6%
- **WebOperator**：54.6%

# 思考

## 马尔可夫决策

思考：强化学习领域，（1）告诉agent，最终目标是什么。当前状态是什么。agent输出下一步动作。（2）告诉agent，最终目标是什么。当前状态是什么。历史状态和动作是什么。agent输出下一步动作。
（1）和（2）哪个对？

在强化学习（Reinforcement Learning, RL）领域，**（1）和（2）在不同的前提条件下都是“正确”的**。它们分别对应了强化学习中两种最基本的环境模型。

简单来说：**如果环境是完全可观测的，（1）就够了；如果环境是部分可观测的，（2）才更有效。**

以下是详细的分析：

---

### 1. 情况（1）：基于马尔可夫决策过程 (MDP)
这种模式认为：**当前状态（Current State）已经包含了决策所需的所有有用信息。**

*   **理论依据：** **马尔可夫性质（Markov Property）**。即“未来只取决于现在，而与过去无关”。
*   **为什么（1）是对的：** 在标准的 MDP 中，状态 $S_t$ 被称为“充分统计量”（Sufficient Statistic）。如果你知道了现在的棋盘布局（状态），你不需要知道这盘棋是怎么下到这一步的（历史），就能做出最优决策。
*   **应用场景：** 围棋（AlphaGo）、标准的雅达利游戏（Atari）、完全已知的迷宫。
*   **结论：** 在满足马尔可夫性质的环境下，**（1）是标准做法**。加入历史信息反而会增加计算负担和噪声。

---

### 2. 情况（2）：基于部分可观测马尔可夫决策过程 (POMDP)
这种模式认为：**当前的“状态”（其实通常称为观测 Observation）并不完整，必须依靠历史来推断背后的真相。**

*   **理论依据：** **POMDP (Partially Observable MDP)**。当 Agent 无法看到环境的全貌时，单一的当前观测不足以代表真正的状态。
*   **为什么（2）是对的：** 历史信息（History）可以帮助 Agent 补全缺失的信息。
    *   *例子：* 一个避障机器人只看当前的一帧雷达图，可能不知道某个物体是在向它靠近还是远离。但如果它看了**历史三帧图**，就能通过位移计算出速度。
*   **应用场景：** 自动驾驶（需要通过历史判断行人意图）、第一人称射击游戏（你看不到身后的敌人，需要记忆）、扑克比赛（需要根据对手的历史出牌风格推断其手牌）。
*   **结论：** 在复杂或信息不透明的环境下，**（2）是更强、更实用的模型**。

---

### 3. 深度学习时代的技术实现

在实际的深度强化学习算法中，这两个思路对应了不同的架构：

*   **针对（1）：** 通常使用全连接网络（MLP）或卷积神经网络（CNN）直接处理当前帧。
*   **针对（2）：** 
    *   **Frame Stacking（帧堆叠）：** 比如把最近 4 帧游戏画面叠在一起作为“当前状态”，把（2）强行转化成（1）。
    *   **循环神经网络（RNN/LSTM/GRU）：** 让 Agent 拥有“记忆”，自动提取历史中的有用信息。
    *   **Transformer：** 现在的趋势是利用 Transformer 的注意力机制，在长历史序列中寻找对当前动作最有用的线索。

---

### 总结：到底哪个对？

*   **从严谨的学术定义看：** (1) 是强化学习的**基础定义（MDP）**。只要我们定义“状态”这个词，它本身就应该包含所有必要信息。
*   **从解决实际问题看：** (2) 是**现实世界的常态**。因为现实中我们很难获得“完美且完整”的当前状态，所以必须依赖历史。

**一句话建议：**
如果你正在处理的问题信息非常明确（如棋类、完美规则游戏），选 **（1）**；如果你处理的问题存在遮挡、噪声或需要推测动态意图（如机器人控制、金融交易），选 **（2）**。

zhbli：目前的agent都有历史信息，也就是POMDP。

## 记忆

有没有人研究agent的记忆的精简压缩？因为如果把所有历史步骤、知识库全放到上下文窗口，根本不现实

---

这是一个非常前沿且具有极高实际应用价值的研究方向。正如你所观察到的，**“无限增加上下文”不仅成本昂贵，还会导致模型出现“Lost in the Middle”（迷失在中间）现象，且推理速度会大幅下降。**

目前，学术界和工业界针对 Agent 记忆的精简与压缩，主要有以下几个核心研究方向和代表性方案：

### 1. 记忆的分层与架构化（Architecture-based）

效仿人类的大脑，将记忆分为**工作记忆（Working Memory）**和**长期记忆（Long-term Memory）**。

- **MemGPT (Memory-GPT):** 这是一个非常著名的研究。它模仿操作系统的虚拟内存管理，将上下文窗口视为“内存”，将外部数据库视为“磁盘”。当上下文快满时，Agent 会通过专门的函数调用（Function Calling）自主决定哪些信息该“写入磁盘”（存入向量数据库），哪些信息该从内存中“换出”（驱逐）。
    
- **Generative Agents (斯坦福小镇):** 该研究提出了一个“记忆流”架构。它不仅仅是存储，还引入了**“反思（Reflection）”机制**。Agent 会定期停下来，对最近发生的碎片化记忆进行归纳总结，提取出高阶的特征（例如：从“看到张三在喝咖啡”和“看到张三在看书”总结出“张三是个悠闲的人”），从而实现记忆的极大压缩。
    

### 2. 递归式总结与压缩（Summarization-based）

这种方法通过 LLM 自身的能力对历史进行“脱水”。

- **Recursive Summarization:** 当对话轮数超过阈值时，让 LLM 将前 N 轮的对话总结成一段简短的摘要，然后丢弃原始对话，只保留摘要。
    
- **Walking Memory:** 某些研究探索将记忆压缩为固定长度的“隐向量（Summary Vectors）”。通过特定的模型层（如 AutoCompressors），将数千个 token 压缩成几十个特殊的“记忆 token”，这些 token 承载了历史的关键语义，但占用的上下文窗口极小。
    

### 3. 选择性遗忘与重要性评分（Pruning & Forgetting）

并不是所有的信息都值得记录。研究者正在通过算法给记忆“打分”。

- **重要性（Poignancy）、相关性（Relevance）和时效性（Recency）:** 借鉴心理学模型，为每条记忆计算一个综合分数。低分记忆会被优先删除。
    
- **H2O (Heavy Hitter Oracle):** 在 Transformer 的 KV Cache 层级进行压缩。研究发现，Attention 机制中只有一小部分 token（Heavy Hitters）对预测起关键作用，通过动态剔除不重要的 KV 缓存，可以在不损失太多精度的情况下大幅减少显存占用。
    

### 4. 语义索引与检索增强（RAG-based Optimization）

虽然 RAG 是常规手段，但针对 Agent 的精简检索有专门的研究：

- **Hierarchical Navigation:** 将知识库构建成树状或图状结构。Agent 先检索大类，再逐步深入细节，而不是一次性扫描所有历史。
    
- **Contextual Truncation:** 根据当前任务的语义，动态决定检索回来的片段（Chunks）中哪些部分需要保留，哪些噪声可以裁剪。
    

### 5. 正在兴起的研究趋势

- **LongLoRA / StreamingLLM:** 这些研究侧重于如何在超长序列中让模型依然保持高效。例如 StreamingLLM 发现，只要保留序列开头的几个 token（Attention Sinks）和最近的滑动窗口，模型就能在无限长文本中不崩溃。
    
- **Cognitive Architectures (认知架构):** 很多团队在尝试将传统的 AI 认知架构（如 SOAR, ACT-R）与 LLM 结合。这些架构天生就有严密的记忆清理和固化机制。
    

### 总结

你提到的“精简压缩”是当前 Agent 走向实用的核心瓶颈。**目前最主流且有效的工业实践路径是：**

1. **最近对话：** 保留原始文本（保持连贯性）。
    
2. **中期历史：** 递归总结（压缩细节）。
    
3. **长期历史：** 向量化检索（丢入数据库，按需加载）。
    
4. **元记忆（Reflection）：** 定期生成关于用户或任务的高级画像（只存结论，不存过程）。
    

**如果你想深入研究，建议阅读以下论文：**

- MemGPT: Towards LLMs as Operating Systems
    
- Generative Agents: Interactive Simulacra of Human Behavior
    
- H2O: Heavy-Hitter Oracle for Efficient Generative Inference of LMMs
    
- Summarization Programs: Interpretable Language Models for Memory-Efficient Reasoning

## RAG 本质就是记忆管理

## playwright 操作网页，靠DOM还是AXTREE？

简单来说：**Playwright 两者都用，但它目前强烈推荐并倾向于让你通过 AXTREE（无障碍树/语义化）来操作网页。**

我们可以从以下几个维度来深入理解：

### 1. 传统的 DOM 操作（基础）
Playwright 最初和传统的 Selenium 一样，完全支持基于 **DOM** 的操作。
*   **选择器：** CSS 选择器（`.btn-submit`）、XPath（`//div[@id='root']`）。
*   **特点：** 这种方式是基于 HTML 的层级结构和属性。
*   **缺点：** 极其脆弱。如果前端框架（如 React/Vue）把 `<div>` 改成了 `<span>`，或者类名（class）因为混淆压缩变了，脚本就会挂掉。

### 2. 现代的 AXTREE 操作（推荐）
Playwright 现在的核心理念是 **“面向用户行为”**。它引入了基于 **无障碍树（Accessibility Tree）** 的定位器（Locators）。
*   **选择器：** `page.get_by_role("button", name="提交")`、`page.get_by_label("用户名")`、`page.get_by_placeholder("请输入密码")`。
*   **工作原理：** Playwright 会查询浏览器引擎计算出的 AXTREE。它不关心你的按钮是用 `<button>` 写的，还是用一个带有 `role="button"` 的 `<div>` 写的，只要它在 AXTREE 中被识别为“按钮”且名字叫“提交”，就能找到它。
*   **优点：** 
    *   **稳定性极高：** 即使 HTML 结构变了，只要功能没变（对用户来说还是个按钮），代码就不用改。
    *   **强制可访问性：** 如果你的自动化脚本找不到某个元素，说明残障人士的屏幕阅读器大概率也找不到，这能反向推动开发修复无障碍问题。

### 3. 底层是如何实现的？
在 Playwright 的底层架构中，它通过浏览器原生协议（如 Chromium 的 CDP 协议）同时获取 **DOM 树** 和 **计算后的无障碍属性**。

*   当你调用 `get_by_role` 时，Playwright 会在内存中匹配那些符合特定 **ARIA 角色** 和 **Accessible Name** 的 DOM 节点。
*   一旦定位到节点，Playwright 的点击、输入等动作最终还是作用于 **DOM 元素**上。

### 4. 总结对比

| 特性 | 基于 DOM (CSS/XPath) | 基于 AXTREE (Locators) |
| :--- | :--- | :--- |
| **Playwright API** | `page.locator(".my-class")` | `page.get_by_role("link")` |
| **关注点** | 代码实现细节（怎么写的） | 用户感知的功能（是什么） |
| **稳定性** | 较低（UI重构易碎） | 较高（业务逻辑不变则不碎） |
| **推荐度** | 辅助使用（用于定位无语义元素） | **首选（官方推荐标准）** |

### 建议
在编写 Playwright 脚本时，你应该**优先使用 AXTREE 相关的 Locators**（如 `get_by_role`, `get_by_text`, `get_by_label`）。只有当页面极其不规范，或者需要处理一些复杂的 CSS 伪类、特定的数据属性（如 `data-testid`）时，才回退到 DOM 选择器。

zhbli：上述内容的真实性未知。

## DOM究竟多大？我似乎发现比截图还大

截图就是涉及到靠视觉识别准不准的问题。而且DOM能精简。据说精简后的DOM能瘦身90%

能瘦身这么多（从几万个字符减少到几百个），主要是因为浏览器在渲染页面时包含的大量信息对**人类视觉**和**网页性能监测**至关重要，但对**自动化脚本**来说全是“噪音”。——这么说的话，靠DOM是没问题的。

瘦身后还能操作某个元素吗？能，靠的是ID。

## DOM 比 截图 的优势

想要全文总结，截图就不行。

## WebAgent中的经验

### 整体流程

每次任务的操作步骤（人工的/AI的）都存起来，后续再执行相似任务时，先调用这些经验。（最最开始，肯定是人工。）
- 执行的越多，积累的越多，成功率越高

### 如何保存每次任务的操作步骤

这是要做的事情
- 需要有任务prompt（用于与新任务计算余弦相似度）
- 成功完成一个任务后，根据轨迹生成SOP（新任务按照SOP进行）
	- 也就是说，对于一个新任务，它是先调取轨迹，再根据轨迹生成SOP呢？还是每一个历史轨迹完成后生成SOP呢？这是需要考量的
- 每个状态，要生成摘要（原始DOM太长）

### 如何调用这些经验

这是要做的事情
- 计算新任务 Prompt 与历史任务 Prompt 的余弦相似度

### 如何根据经验生成子任务

这是要做的事情

在web agent 领域，还有没有其他生成经验的思路？
- 首先，必要性是肯定的。大模型肯定不会操作专业性强的系统。必须要经验。
- 其次，如何生产经验
	- 现有说明书就够了
	- 编制任务的SOP（这就是我目前采用的方式）
	- 人工操作一遍，后台录制下轨迹，大模型据此生成SOP，作为后续类似任务的参考
		- nano browser: Replay Historical Tasks( experimental ): Enable storing and replaying of agent step history (experimental, may have issues) 提供了录制重播的功能，但是没法用
		- browseros自带了这个
	- 自主探索

## 点击一个动作后，要不要判断动作是否执行成功？

![[京东.png]]

当我点击添加购物车后，页面会提示添加成功，但1秒就消失了。（如果不是第一次添加该商品，右侧购物车图标数量也不会发生改变）这让agent怎么得知是否操作成功？有种策略是不执行判断。如果人没注意这个一闪而过的提示，也不知道自己有没有添加成功。这种情况很特殊。每个网站都有各自的情况，如何设计统一的流程？如果强制要求每一步都检查是否完成，则这个例子，检查结果肯定是没有完成。不过，执行一个动作后，页面没有任何变化的情况，是罕见的。
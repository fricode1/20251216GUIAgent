```mermaid
graph TD
    %% =========================================================
    %% 样式定义 (Define Styles for better visual clarity)
    %% =========================================================
    %% 核心概念、重要模型和输出节点
    classDef core fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    %% 关键技术、模块细节
    classDef technique fill:#f9fbe7,stroke:#33691e,stroke-width:1px,stroke-dasharray: 2 2;
    %% 子标题、分类
    classDef subtype fill:#eaeaea,stroke:#666,stroke-width:1px,font-style:italic;
    %% 并行/分支处理器 
    classDef processor fill:#fff3e0,stroke:#e65100,stroke-width:1px;

    %% =========================================================
    %% 第一、二、三层：输入 -> Tokenizer -> 统一序列
    %% =========================================================
    subgraph Layer1to3 [多模态输入与 Tokenizer 枢纽]
        direction TB

        %% 1. 输入层
        subgraph InputLayer [第一层：多模态输入层]
            TextIn[文本输入 Text<br/>• 自然语言文本<br/>• 问题描述、指令提示]:::core
            ImageIn[图像输入 Image<br/>• 静态图片<br/>• 视觉文档、版面图像]:::core
            VideoIn[视频输入 Video<br/>• 动态视频序列<br/>• 时序视觉数据]:::core
        end

        %% 2. Tokenizer 层
        subgraph TokenizerLayer [第二层：Tokenizer 分词编码层]
            TextToken[文本分词器]:::core
            
            subgraph ViT_Image [图像编码器 (MoonViT-3D)]:::processor
                ImageEnc[ViT 编码]
                NaViT_Tech[• NaViT Patch打包策略<br/>• 原生分辨率处理]:::technique
                ImageEnc --- NaViT_Tech
            end
            
            subgraph ViT_Video [视频编码器 (3D ViT 压缩)]:::processor
                VideoEnc[3D ViT 编码]
                Video_Tech[• 4帧分组时空压缩<br/>• 时间池化特征聚合]:::technique
                VideoEnc --- Video_Tech
            end
        end

        %% 3. 统一统一 Token 序列
        subgraph UnifiedTokenLayer [第三层：统一 Token 序列]
            UnifiedTokens["Unified Token Sequence<br/>[文本 Tokens] + [视觉 Tokens] + [模态分隔符] + [PAD 锚点]"]:::core
        end

        %% 连接关系 (L1-L3)
        TextIn --> TextToken -->|文本 Tokens| UnifiedTokens
        ImageIn --> ViT_Image:::processor -->|视觉 Tokens| UnifiedTokens
        VideoIn --> ViT_Video:::processor -->|时空 Tokens| UnifiedTokens
    end

    %% =========================================================
    %% 第三层向下分流到具体子模型
    %% =========================================================
    UnifiedTokens ---> UnderstandingModel
    UnifiedTokens ---> EmbeddingModel
    UnifiedTokens ---> GenModelBranch

    %% =========================================================
    %% 第四、五 A 层：多模态理解模型 (L)
    %% =========================================================
    subgraph UnderstandingModel [第五层 A：理解模型 (L)]
        direction TB
        %% 4. 模型标题
        L4_UnderstandingHeader["多模态理解模型 (Understanding Model)<br/>基座：Kimi K2 MoE | 输出：文本"]:::subtype

        %% 5A. 内部详细模块
        A_ViT[MoonViT-3D视觉编码器 <br/>(NaViT/3D ViT/时间池化/权重共享)]:::core
        A_MLP[MLP 投影器 <br/>(视觉-语言空间对齐)]:::core
        A_MoE["Kimi K2 MoE 语言模型 (核心)<br/>Total: 1.04T / Act: 32B / Expert: 384<br/>Act/Token: 8 / Sparsity: 48%"]:::core
        L5A_Outputs[理解与推理结果]:::core

        %% 连接关系 (5A)
        L4_UnderstandingHeader -.-> A_ViT
        A_ViT -->|视觉特征| A_MLP -->|融合特征| A_MoE --> A_L5A_T[文字推理结果]
    end

    %% =========================================================
    %% 第四、五 B 层：多模态表征模型 (M)
    %% =========================================================
    subgraph EmbeddingModel [第五层 B：表征模型 (M)]
        direction TB
        %% 4. 模型标题
        L4_EmbeddingHeader["多模态表征模型 (Embedding Model)<br/>基座：Qwen3-VL | 输出：向量"]:::subtype

        %% 5B. 内部详细模块
        B_Adapt[1. 模态适配处理<br/>- 图:保持长宽比<br/>- 视:采样+限制<br/>- 文:版面拆分拼接<br/>- 约束:32K]:::technique
        B_Input[2. 输入处理与模板解析<br/>Qwen3-VL 指令感知上下文模板]:::technique
        
        subgraph B_Support [3. 基础支撑模块]:::processor
            direction LR
            B_QwenVL_ViT[Qwen3-VL 视觉编码器]
            B_QwenLM[Qwen3 LM 稠密解码器]
            B_Mechanism[• 因果注意力<br/>• 32K 序列<br/>• 30+ 语言]:::technique
            B_QwenVL_ViT --- B_QwenLM
            B_QwenLM --- B_Mechanism
        end
        
        B_Core[4. 核心编码模块 (双编码器)<br/>- 文本:LM编码<br/>- 视觉:ViT->LM编码<br/>- 多模态:独立->轻量融合]:::core
        B_OutGen[5. 嵌入向量生成 (输出层)<br/>PAD令牌锚点提取隐藏状态]:::core

        %% 连接关系 (5B)
        L4_EmbeddingHeader -.-> B_Adapt
        B_Adapt --> B_Input -->标准化序列--> B_Support:::processor -->高维特征序列--> B_Core --> B_OutGen

        subgraph L6_EmbedOut [第六层：表征模型输出]
            L6_Out_Vec2B[2B版本：2048D 向量]:::core
            L6_Out_Vec8B[8B版本：4096D 向量]:::core
        end
        B_OutGen --> L6_Out_Vec2B
        B_OutGen --> L6_Out_Vec8B
    end

    %% =========================================================
    %% 第四、五 C 层：多模态生成模型 (R) - 根
    %% =========================================================
    subgraph GenModelBranch ["第四&五层 C：生成模型 (R)"]
        direction TB
        %% 4. 模型标题
        L4_GenHeader["多模态生成模型 (Generation Model)<br/>基座：DiT / Qwen3 | 输出：媒体"]:::subtype

        %% 分流到两个子分支
        subgraph ViewGenSub ["视图生成子分支 (MMDiT)"]:::processor
            direction TB
            V_Code[1. 文本/图像编码器]
            
            subgraph V_Parallel [2. 双分支并行处理 (MMDiT)]:::processor
                V_ViewBranch["视觉分支处理<br/>(主体/动态/镜头/过渡)"]:::processor
                V_AudioBranch["听觉分支处理<br/>(人声/音效/BGM/韵律)"]:::processor
                V_Interact["内置分支交互接口"]:::technique
                V_ViewBranch --- V_Interact
                V_AudioBranch --- V_Interact
            end
            
            V_Joint[3. 跨模态联合模块<br/>(视觉-听觉深度交互, 时间匹配)]:::core
            V_DiT[4. 音视频联合生成模块 (DiT)]:::core
            L6_Gen_Video[输出: 同步音视频内容]:::core

            V_Code --> V_Parallel:::processor -->统一跨模态特征--> V_Joint --> V_DiT -->序列+波形-->L6_Gen_Video
        end

        subgraph AudioGenSub ["语音生成子分支 (自回归)"]:::processor
            direction TB
            A_TexTok[1. 文本分词器]
            A_Speaker[2. 说话人编码器]
            
            subgraph A_ViT [3. 语音分词器 (双版本并行)]:::processor
                direction NR
                A_Code_25Hz[A. 25Hz单码本<br/>(Qwen2-Audio编码)]
                A_Code_12Hz[B. 12Hz多码本<br/>(解纠缠量化, 低延迟)]
            end

            A_ViewFuse[4. 双轨表示融合]
            A_Qwen3[5. Qwen3语言模型 (骨干)]
            A_MultiTokDiv{6. 多令牌预测<br>(12Hz专用)}:::processor
            
            subgraph A_CodeWav [7. Code2Wav 模块]:::processor
                A_CW_25Hz[A. 适配25Hz<br/>(扩散+BigVGAN)]
                A_CW_12Hz[B. 适配12Hz<br/>(因果卷积, 流式)]
            end

            subgraph A_Sliding [8. 流式解码器]:::processor
                A_Slide_25Hz[A. 25Hz 滑动窗口]
                A_Slide_12Hz[B. 12Hz 因果]
            end

            L6_Gen_Audio[9. 输出: 实时语音流]:::core

            A_TexTok --> A_ViewFuse
            A_Speaker --> A_ViewFuse
            A_Code_25Hz --> |25Hz Tokens| A_ViewFuse
            A_Code_12Hz --> |12Hz Tokens| A_ViewFuse
            A_ViewFuse --> A_Qwen3
            
            %% 12Hz 特有路径
            A_Qwen3 --> |12Hz预测| A_MultiTokDiv:::processor --> |全部残留码本| A_CodeWav:::processor
            %% 25Hz 路径直接到 CodeWav
            A_Qwen3 -.-> |25Hz预测| A_CodeWav:::processor
            
            A_CodeWav:::processor -->A_Sliding:::processor --> L6_Gen_Audio
        end
    end

    %% =========================================================
    %% 最后的输出连接关系
    %% =========================================================
    UnderstandingModel ...> |L5A| L6_U_Final[理解推理用户输出]:::core
    EmbeddingModel ...> L6_EmbedOut
    GenModelBranch ...> |L5C| L6_Gen_Video
    GenModelBranch ...> |L5C| L6_Gen_Audio
```
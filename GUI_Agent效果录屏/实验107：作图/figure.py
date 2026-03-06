
from graphviz import Digraph

# 创建有向图
graph = Digraph(
    name='Multimodal_Foundation_Model',
    format='png',
    engine='dot'
)

# 设置全局属性
graph.attr(
    rankdir='TB',  # 从上到下
    bgcolor='white',
    fontname='Times New Roman',
    fontsize='14',
    margin='0'
)

# 定义节点样式
graph.attr('node', 
    shape='box',
    style='filled,rounded',
    fontname='Times New Roman',
    fontsize='11',
    margin='0.15,0.1'
)

graph.attr('edge',
    fontname='Times New Roman',
    fontsize='10',
    arrowhead='vee'
)

# ==================== 颜色定义 ====================
color_main = '#2E5C8A'      # 主色调 - 深蓝
color_sub = '#4A90A4'       # 次色调 - 青蓝
color_module = '#6B8E9F'    # 模块色 - 灰蓝
color_detail = '#8FB8C9'    # 细节色 - 浅蓝
color_bg = '#F5F7FA'        # 背景色

# ==================== 根节点 ====================
graph.node('Root', 
    'Multimodal Foundation Model\n(Base Architecture)',
    fillcolor=color_main,
    fontcolor='white',
    shape='box',
    style='filled,rounded',
    fontsize='14',
    fontname='Times New Roman Bold'
)

# ==================== 三个主要分支 ====================
with graph.subgraph(name='cluster_understanding') as c1:
    c1.attr(
        label='Multimodal Understanding Model',
        style='filled,rounded',
        fillcolor=color_bg,
        color=color_sub,
        fontname='Times New Roman Bold',
        fontsize='12',
        labelloc='t',
        labeljust='center',
        margin='15'
    )
    
    # MoonViT-3D
    c1.node('MoonViT', 
        'MoonViT-3D\n(Native Resolution Visual Encoder)',
        fillcolor=color_module,
        fontcolor='white'
    )
    
    # MLP Projector
    c1.node('MLP', 
        'MLP Projector\n(Cross-modal Feature Alignment)',
        fillcolor=color_module,
        fontcolor='white'
    )
    
    # Kimi K2 MoE
    c1.node('KimiK2', 
        'Kimi K2 MoE LLM\n(1.04T Params, 32B Active)',
        fillcolor=color_module,
        fontcolor='white'
    )
    
    # 内部连接
    c1.edge('MoonViT', 'MLP', color=color_sub, penwidth='1.5')
    c1.edge('MLP', 'KimiK2', color=color_sub, penwidth='1.5')

with graph.subgraph(name='cluster_representation') as c2:
    c2.attr(
        label='Multimodal Representation Model',
        style='filled,rounded',
        fillcolor=color_bg,
        color=color_sub,
        fontname='Times New Roman Bold',
        fontsize='12',
        labelloc='t',
        labeljust='center',
        margin='15'
    )
    
    # 模态适配
    c2.node('ModalAdapt', 
        'Modal Adaptation Module\n(Multi-modal Preprocessing)',
        fillcolor=color_module,
        fontcolor='white'
    )
    
    # 输入处理
    c2.node('InputProc', 
        'Input Processing &\nTemplate Parsing Module',
        fillcolor=color_module,
        fontcolor='white'
    )
    
    # 基础支撑
    c2.node('BaseSupport', 
        'Base Support Module\n(Qwen3-VL Encoder + Decoder)',
        fillcolor=color_module,
        fontcolor='white'
    )
    
    # 核心编码
    c2.node('CoreEncode', 
        'Core Encoding Module\n(Dual-Encoder Architecture)',
        fillcolor=color_module,
        fontcolor='white'
    )
    
    # 嵌入生成
    c2.node('EmbedGen', 
        'Embedding Generation Module\n(2B: 2048-dim / 8B: 4096-dim)',
        fillcolor=color_module,
        fontcolor='white'
    )
    
    # 内部连接
    c2.edge('ModalAdapt', 'InputProc', color=color_sub, penwidth='1.5')
    c2.edge('InputProc', 'BaseSupport', color=color_sub, penwidth='1.5')
    c2.edge('BaseSupport', 'CoreEncode', color=color_sub, penwidth='1.5')
    c2.edge('CoreEncode', 'EmbedGen', color=color_sub, penwidth='1.5')

with graph.subgraph(name='cluster_generation') as c3:
    c3.attr(
        label='Multimodal Generation Model',
        style='filled,rounded',
        fillcolor=color_bg,
        color=color_sub,
        fontname='Times New Roman Bold',
        fontsize='12',
        labelloc='t',
        labeljust='center',
        margin='15'
    )
    
    # 子集群：视图生成
    with c3.subgraph(name='cluster_visual') as c3v:
        c3v.attr(
            label='Visual Generation (MMDiT)',
            style='filled,rounded',
            fillcolor='#E8F0F3',
            color=color_detail,
            fontname='Times New Roman',
            fontsize='11',
            labelloc='t'
        )
        
        c3v.node('TextEnc', 
            'Text Encoder\n(Semantic Encoding)',
            fillcolor=color_detail,
            fontcolor='black'
        )
        
        c3v.node('VisualBranch', 
            'Visual Branch\n(Visual Feature Processing)',
            fillcolor=color_detail,
            fontcolor='black'
        )
        
        c3v.node('AudioBranch', 
            'Audio Branch\n(Audio Feature Processing)',
            fillcolor=color_detail,
            fontcolor='black'
        )
        
        c3v.node('CrossModal', 
            'Cross-modal Joint Module\n(Feature Fusion)',
            fillcolor=color_detail,
            fontcolor='black'
        )
        
        c3v.node('AVGen', 
            'Audio-Visual Joint Generator\n(DiT Output)',
            fillcolor=color_detail,
            fontcolor='black'
        )
        
        c3v.edge('TextEnc', 'VisualBranch', color=color_detail, penwidth='1.2')
        c3v.edge('TextEnc', 'AudioBranch', color=color_detail, penwidth='1.2')
        c3v.edge('VisualBranch', 'CrossModal', color=color_detail, penwidth='1.2')
        c3v.edge('AudioBranch', 'CrossModal', color=color_detail, penwidth='1.2')
        c3v.edge('CrossModal', 'AVGen', color=color_detail, penwidth='1.2')
    
    # 子集群：语音生成
    with c3.subgraph(name='cluster_speech') as c3s:
        c3s.attr(
            label='Speech Generation (Dual-Track AR)',
            style='filled,rounded',
            fillcolor='#E8F0F3',
            color=color_detail,
            fontname='Times New Roman',
            fontsize='11',
            labelloc='t'
        )
        
        c3s.node('TextTok', 
            'Text Tokenizer',
            fillcolor=color_detail,
            fontcolor='black'
        )
        
        c3s.node('SpkEnc', 
            'Speaker Encoder\n(Voice Cloning)',
            fillcolor=color_detail,
            fontcolor='black'
        )
        
        c3s.node('SpeechTok', 
            'Speech Tokenizer\n(25Hz / 12Hz)',
            fillcolor=color_detail,
            fontcolor='black'
        )
        
        c3s.node('DualTrack', 
            'Dual-Track Fusion\n(Qwen3 Backbone)',
            fillcolor=color_detail,
            fontcolor='black'
        )
        
        c3s.node('Code2Wav', 
            'Code2Wav Module\n(Token to Waveform)',
            fillcolor=color_detail,
            fontcolor='black'
        )
        
        c3s.edge('TextTok', 'DualTrack', color=color_detail, penwidth='1.2')
        c3s.edge('SpkEnc', 'DualTrack', color=color_detail, penwidth='1.2')
        c3s.edge('SpeechTok', 'DualTrack', color=color_detail, penwidth='1.2')
        c3s.edge('DualTrack', 'Code2Wav', color=color_detail, penwidth='1.2')

# ==================== 根节点到三个分支的连接 ====================
graph.edge('Root', 'MoonViT', 
    color=color_main, 
    penwidth='2',
    style='dashed',
    ltail='cluster_root'
)

graph.edge('Root', 'ModalAdapt', 
    color=color_main, 
    penwidth='2',
    style='dashed'
)

graph.edge('Root', 'TextEnc', 
    color=color_main, 
    penwidth='2',
    style='dashed'
)

graph.edge('Root', 'TextTok', 
    color=color_main, 
    penwidth='2',
    style='dashed'
)

# 保存并渲染
graph.render('multimodal_foundation_model', cleanup=True)
print("Diagram saved to: /mnt/kimi/output/multimodal_foundation_model.png")

from graphviz import Digraph
import os

# 设置中文字体
os.environ['FONT_NAME'] = 'SimHei'

# 创建有向图
dot = Digraph('MMDiT架构框图', format='png', encoding='utf-8')
dot.attr(rankdir='TB', size='12,15', dpi='300', fontname='SimHei', fontsize='12')
dot.attr('node', shape='box', style='filled,rounded', fontname='SimHei', fontsize='11')
dot.attr('edge', fontname='SimHei', fontsize='10')

# 定义颜色方案
color_input = '#E6F3FF'
color_branch = '#FFF2E6'
color_cross = '#F0F9E8'
color_generate = '#FFE6F2'
color_output = '#F5F5F5'

# 1. 输入层
dot.node('input_text', '文本提示词\n(Text Prompt)', fillcolor=color_input)
dot.node('input_image', '参考图像\n(Reference Image)', fillcolor=color_input)
dot.node('encoder', '多模态编码器\n(Multi-Modal Encoder)', fillcolor=color_input)

# 2. 双分支处理层
dot.node('visual_branch', '视觉分支处理模块\nVisual Branch\n(Diffusion Transformer)', fillcolor=color_branch)
dot.node('audio_branch', '听觉分支处理模块\nAudio Branch\n(Diffusion Transformer)', fillcolor=color_branch)

# 3. 跨模态联合层
dot.node('cross_modal', '跨模态联合模块\nCross-Modal Fusion Module\n(跨模态注意力机制)', fillcolor=color_cross)

# 4. 生成层
dot.node('av_generator', '音视频联合生成模块\nAudio-Visual Generator\n(Diffusion Transformer)', fillcolor=color_generate)

# 5. 输出层
dot.node('output_video', '生成视频序列\nGenerated Video Sequence', fillcolor=color_output)
dot.node('output_audio', '生成音频波形\nGenerated Audio Waveform', fillcolor=color_output)

# 构建层级关系和连接
# 输入到编码器
dot.edge('input_text', 'encoder', label='文本编码')
dot.edge('input_image', 'encoder', label='视觉特征提取')

# 编码器到双分支
dot.edge('encoder', 'visual_branch', label='视觉特征向量')
dot.edge('encoder', 'audio_branch', label='音频特征向量')

# 双分支特征交互（双向）
dot.edge('visual_branch', 'audio_branch', label='特征交互', dir='both', style='dashed')

# 双分支到跨模态联合模块
dot.edge('visual_branch', 'cross_modal', label='视觉序列特征')
dot.edge('audio_branch', 'cross_modal', label='音频序列特征')

# 跨模态联合到生成模块
dot.edge('cross_modal', 'av_generator', label='统一跨模态特征表征')

# 生成模块到输出
dot.edge('av_generator', 'output_video', label='视频帧生成')
dot.edge('av_generator', 'output_audio', label='音频波形生成')

# 添加架构核心说明
dot.node('core_note', 'MMDiT = Multi-Modal Diffusion Transformer\n多模态扩散变换器（底层技术基底）', 
         shape='ellipse', fillcolor='#E8F4FD', fontsize='10', pos='0,0!')

# 保存并渲染
dot.render('MMDiT架构框图', directory='.', cleanup=True)
print("MMDiT架构框图已生成完成！")
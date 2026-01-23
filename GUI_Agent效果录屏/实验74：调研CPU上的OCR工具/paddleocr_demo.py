import os
# 跳过模型源检查
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'
os.environ['FLAGS_use_onednn'] = '0' # 关闭 oneDNN 优化
os.environ['FLAGS_enable_pir_api'] = '0' # 尝试关闭新执行器

from paddleocr import PaddleOCR

# 1. 初始化 (针对 3.0 版本参数)
ocr = PaddleOCR(
    use_textline_orientation=True,  # 替代旧版的 use_angle_cls
    lang="ch", 
    device="cpu"
)

# 2. 识别图片 (去掉 cls=True)
img_path = 'test.jpg' 

# 检查文件是否存在
if not os.path.exists(img_path):
    print(f"错误：找不到文件 {img_path}")
else:
    # 3.0 版本直接调用即可，不要传 cls 参数
    result = ocr.ocr(img_path)

    # 打印结果
    if result and result[0]:
        for line in result[0]:
            # line[1][0] 是文本内容，line[1][1] 是置信度
            print(f"检测文字: {line[1][0]}  置信度: {line[1][1]:.4f}")
    else:
        print("未检测到文字")
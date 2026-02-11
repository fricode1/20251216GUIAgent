import uiautomation as auto
import os
import datetime

# --- 配置区 ---
SAVE_DIR = "saved_images"
MAX_DEPTH = 10
# -------------

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def get_text_from_patterns(control):
    """尝试获取控件内的隐藏文本"""
    try:
        val = control.GetValuePattern().Value
        if val: return val.strip()
    except: pass
    try:
        text = control.GetTextPattern().DocumentRange.GetText()
        if text: return text.strip().replace('\r', ' ').replace('\n', ' ')[:50]
    except: pass
    return None

def save_image_control(control, index):
    """保存 ImageControl 到本地文件"""
    # 构造安全的文件名
    clean_name = "".join([c for c in (control.Name or "unnamed") if c.isalnum() or c in (' ', '_')]).strip()
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    filename = f"img_{timestamp}_{index}_{clean_name}.png"
    filepath = os.path.join(SAVE_DIR, filename)
    
    try:
        # 尝试将控件滚动到可见区域（否则截图可能是空的或失败）
        if hasattr(control, 'ScrollIntoView'):
            control.ScrollIntoView()
        
        # 捕获控件图像
        control.CaptureToImage(filepath)
        return filepath
    except Exception as e:
        return f"保存失败({e})"

def walk_and_inspect(control, depth=0, img_counter=[0]):
    """递归遍历树，获取文本并保存图片"""
    if depth > MAX_DEPTH:
        return

    indent = "  " * depth
    control_type = control.ControlTypeName
    class_name = control.ClassName or "N/A"
    name = control.Name or ""
    
    # 准备行输出内容
    display_str = f"└─ [{control_type}]"
    if name:
        display_str += f" Name: {name}"
    
    # 情况 A: 处理图片
    if control_type == "ImageControl":
        img_counter[0] += 1
        save_path = save_image_control(control, img_counter[0])
        display_str += f" | [📸 图像已保存: {save_path}]"
        
    # 情况 B: 处理文本 (如果是 Word 这里的 EditControl 会包含文字)
    else:
        extra_text = get_text_from_patterns(control)
        if extra_text and extra_text != name:
            display_str += f" | >>> Text: {extra_text} <<<"

    # 打印当前控件信息
    print(f"{indent}{display_str} (Class: {class_name})")
    
    # 递归子控件
    try:
        # 对于 Word 等大型应用，过滤掉一些已知的、产生大量冗余子控件的容器可以加速
        # 但为了完整性，这里保持全部遍历
        for child in control.GetChildren():
            walk_and_inspect(child, depth + 1, img_counter)
    except Exception:
        pass

def main():
    print("=" * 80)
    print(f"开始扫描桌面控件结构...")
    print(f"所有图片将保存至: {os.path.abspath(SAVE_DIR)}")
    print("=" * 80)
    
    # 获取桌面根控件
    desktop = auto.GetRootControl()
    
    # 开始递归
    img_count_ref = [0] # 使用列表进行引用传递计数
    walk_and_inspect(desktop, 0, img_count_ref)
    
    print("\n" + "=" * 80)
    print(f"扫描任务完成！")
    print(f"共发现并尝试保存了 {img_count_ref[0]} 张图片。")
    print("=" * 80)

if __name__ == "__main__":
    # 降低超时阈值，防止在大型应用上卡死
    auto.uiautomation.SetGlobalSearchTimeout(1)
    main()
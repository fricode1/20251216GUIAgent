import uiautomation as auto

def get_text_from_patterns(control):
    """
    尝试通过多种模式提取控件内的文本内容
    """
    # 1. 尝试 ValuePattern (适用于输入框、大部分文档区域)
    try:
        val = control.GetValuePattern().Value
        if val and len(val.strip()) > 0:
            return val.strip()
    except:
        pass

    # 2. 尝试 TextPattern (适用于 Word 文档、富文本框)
    try:
        text_pattern = control.GetTextPattern()
        if text_pattern:
            text = text_pattern.DocumentRange.GetText()
            if text and len(text.strip()) > 0:
                # 截断过长的文本，防止刷屏
                return text.strip().replace('\r', ' ').replace('\n', ' ')[:50] 
    except:
        pass

    return None

def print_integrated_tree(max_depth=10):
    """
    整合版：打印树形结构，并自动提取控件内的隐藏文本
    """
    print("\n" + "=" * 80)
    print(f"{'UI 控件与文本内容整合树':^70}")
    print("=" * 80)
    
    desktop = auto.GetRootControl()
    
    def walk_tree(control, depth=0):
        if depth > max_depth:
            return

        indent = "  " * depth
        
        # 1. 获取基础属性
        name = control.Name or ""
        control_type = control.ControlTypeName
        class_name = control.ClassName or "N/A"
        
        # 2. 获取隐藏文本内容 (针对 Word, Edit 等)
        extra_text = get_text_from_patterns(control)
        
        # 3. 格式化输出
        # 如果控件名和获取到的文本重复，就不重复打印
        content_str = f"[{control_type}]"
        if name:
            content_str += f" Name: {name}"
        
        if extra_text and extra_text != name:
            # 标记提取出的文本，用绿色或显眼方式显示逻辑（这里用符号标注）
            content_str += f" | >>> Text: {extra_text} <<<"
        
        print(f"{indent}└─ {content_str} (Class: {class_name})")
        
        # 4. 递归子节点
        try:
            # 特别注意：某些复杂控件如果尝试 GetChildren 可能会卡顿
            # 如果是文档区域且已经拿到了大量文本，可以根据需要决定是否深入
            for child in control.GetChildren():
                walk_tree(child, depth + 1)
        except Exception:
            pass

    walk_tree(desktop)

def print_quick_summary():
    """打印当前窗口的快速摘要，重点抓取有内容的文档"""
    print("\n[当前焦点窗口及其文本内容预览]")
    curr_win = auto.GetForegroundControl().GetTopLevelControl()
    if curr_win:
        print(f"窗口标题: {curr_win.Name}")
        # 深度搜索所有的 DocumentControl 和 EditControl
        for doc in curr_win.GetChildren():
            txt = get_text_from_patterns(doc)
            if txt:
                print(f"找到内容 ({doc.ControlTypeName}): {txt[:200]}...")

if __name__ == "__main__":
    # 设置全局搜索超时（可选）
    auto.uiautomation.SetGlobalSearchTimeout(1)
    
    print("提示：正在扫描全桌面的控件和文字内容，这可能需要一点时间...")
    
    # 执行整合树打印
    # 建议先运行 Word 并打一些字，然后运行此脚本
    print_integrated_tree(max_depth=8)
    
    print("\n" + "=" * 80)
    print("扫描结束")
import uiautomation as auto

def safe_get_attr(control, attr_name, default="N/A"):
    """安全获取控件属性，不存在则返回默认值"""
    try:
        return getattr(control, attr_name, default)
    except Exception as e:
        return f"获取失败: {e}"

def print_desktop_info():
    """
    打印桌面（根控件）及其子窗口信息
    """
    # 获取桌面根控件
    desktop = auto.GetRootControl()
    
    print("=" * 60)
    print("桌面信息")
    print("=" * 60)
    
    # 打印桌面控件的基本信息
    print(f"控件类型: {desktop.ControlTypeName}")
    print(f"类名: {desktop.ClassName}")
    print(f"名称: {desktop.Name}")
    print(f"句柄: {desktop.NativeWindowHandle}")
    print(f"矩形区域: {desktop.BoundingRectangle}")
    print()
    
    # 获取桌面的所有子控件（顶层窗口）
    print("-" * 60)
    print("顶层窗口列表:")
    print("-" * 60)
    
    children = desktop.GetChildren()
    
    for index, child in enumerate(children, 1):
        print(f"\n【{index}】")
        print(f"  控件类型: {child.ControlTypeName}")
        print(f"  类名: {child.ClassName}")
        print(f"  名称: {child.Name}")
        print(f"  自动化ID: {child.AutomationId}")
        print(f"  句柄: {child.NativeWindowHandle}")
        print(f"  矩形区域: {child.BoundingRectangle}")
        
        # 安全获取可能不存在的属性
        print(f"  是否启用: {safe_get_attr(child, 'IsEnabled')}")
        print(f"  是否可见: {safe_get_attr(child, 'IsVisible')}")
        print(f"  是否键盘焦点: {safe_get_attr(child, 'HasKeyboardFocus')}")
        
        # 尝试获取子控件数量
        try:
            sub_children = child.GetChildren()
            print(f"  子控件数量: {len(sub_children)}")
        except Exception as e:
            print(f"  子控件数量: 无法获取 ({e})")

def print_desktop_tree(max_depth=8):
    """
    以树形结构打印桌面控件层次结构
    """
    print("\n" + "=" * 60)
    print(f"桌面控件树 (最大深度: {max_depth})")
    print("=" * 60)
    
    desktop = auto.GetRootControl()
    
    def print_control_tree(control, depth=0):
        # 缩进
        indent = "  " * depth
        
        # 获取控件信息
        name = control.Name or "无名称"
        class_name = control.ClassName or "无类名"
        control_type = control.ControlTypeName
        
        # 打印当前控件
        if name != '无名称':
            print(f"{indent}└─ [{control_type}] {name} (Class: {class_name})")
        
        # 递归打印子控件
        if depth < max_depth:
            try:
                children = control.GetChildren()
                for child in children:
                    print_control_tree(child, depth + 1)
            except Exception as e:
                print(f"{indent}   获取子控件失败: {e}")
    
    print_control_tree(desktop)

def print_mouse_point_control():
    """
    打印当前鼠标位置下的控件信息
    """
    print("\n" + "=" * 60)
    print("鼠标位置控件信息")
    print("=" * 60)
    
    # 获取鼠标当前位置的控件
    control = auto.ControlFromCursor()
    
    if control:
        print(f"控件类型: {control.ControlTypeName}")
        print(f"  类名: {control.ClassName}")
        print(f"  名称: {control.Name}")
        print(f"  自动化ID: {control.AutomationId}")
        print(f"  句柄: {control.NativeWindowHandle}")
        print(f"  矩形区域: {control.BoundingRectangle}")
        print(f"  是否启用: {safe_get_attr(control, 'IsEnabled')}")
        print(f"  是否可见: {safe_get_attr(control, 'IsVisible')}")
        
        # 获取顶层窗口
        try:
            top_window = control.GetTopLevelControl()
            if top_window:
                print(f"\n所属顶层窗口:")
                print(f"  名称: {top_window.Name}")
                print(f"  类名: {top_window.ClassName}")
        except Exception as e:
            print(f"\n获取顶层窗口失败: {e}")
    else:
        print("未找到鼠标位置的控件")

def main():
    """
    主函数：执行所有打印功能
    """
    # 1. 打印桌面基本信息和顶层窗口
    print_desktop_info()
    
    # 2. 打印控件树结构
    print_desktop_tree()
    
    # 3. 打印鼠标位置控件信息
    print_mouse_point_control()
    
    print("\n" + "=" * 60)
    print("桌面信息打印完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
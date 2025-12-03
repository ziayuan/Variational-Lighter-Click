import json
import math
import os
import time
import pyautogui

# ========== 可配置参数 ==========
order_count = 40        # 下单次数（每边下多少笔）
interval = 5.0          # 两次下单之间的间隔（秒）
use_double_click = True  # 是否使用双击
click_delay = 0.1       # 点击间隔（秒）
# ===============================

# 全局中断标志
interrupted = False

# 鼠标晃动检测配置
last_mouse_pos = None
last_mouse_time = None
mouse_check_interval = 0.1  # 每0.1秒检查一次
movement_threshold = 800  # 像素/秒的速度阈值
check_in_waiting_only = True  # 只在等待间隔检查，避免干扰程序点击

def check_interrupt():
    """检查是否被中断"""
    return interrupted

def check_mouse_movement():
    """检测鼠标快速晃动"""
    global last_mouse_pos, last_mouse_time, interrupted
    
    try:
        current_pos = pyautogui.position()
        current_time = time.time()
        
        # 首次记录位置
        if last_mouse_pos is None or last_mouse_time is None:
            last_mouse_pos = current_pos
            last_mouse_time = current_time
            return False
        
        # 计算距离和时间差
        distance = math.sqrt(
            (current_pos.x - last_mouse_pos.x) ** 2 + 
            (current_pos.y - last_mouse_pos.y) ** 2
        )
        time_delta = current_time - last_mouse_time
        
        # 如果时间差太小，跳过
        if time_delta < 0.01:
            return False
        
        # 计算速度（像素/秒）
        speed = distance / time_delta
        
        # 如果速度超过阈值，触发中断
        if speed > movement_threshold:
            print(f"\n⚠️ 检测到快速鼠标移动（速度: {speed:.0f} 像素/秒）")
            interrupted = True
            return True
        
        # 更新记录
        last_mouse_pos = current_pos
        last_mouse_time = current_time
        
        return False
        
    except Exception as e:
        # 如果检测失败，不中断程序
        return False




# 运行时询问是否使用保存的坐标
print("\n" + "="*50)
print("🎯 欢迎使用套利下单工具！")
print("="*50)
print("\n请选择坐标模式：")
print("  1. 使用之前保存的坐标（快速开始）")
print("  2. 重新记录坐标（第一次使用或坐标变化）")
print()

while True:
    choice = input("请输入选择 (1/2): ").strip()
    if choice == '1':
        use_saved_coords = True
        break
    elif choice == '2':
        use_saved_coords = False
        break
    else:
        print("❌ 无效选择，请输入 1 或 2")

print(f"\n✅ 已选择: {'使用保存的坐标' if use_saved_coords else '重新记录坐标'}\n")

def save_coordinates(var_pos, lig_pos):
    """保存坐标到文件"""
    coords = {
        'var_pos': {'x': var_pos.x, 'y': var_pos.y},
        'lig_pos': {'x': lig_pos.x, 'y': lig_pos.y}
    }
    with open('coordinates.json', 'w') as f:
        json.dump(coords, f)
    print("💾 坐标已保存到 coordinates.json")

def load_coordinates():
    """从文件加载坐标"""
    try:
        with open('coordinates.json', 'r') as f:
            coords = json.load(f)
        var_pos = pyautogui.Point(coords['var_pos']['x'], coords['var_pos']['y'])
        lig_pos = pyautogui.Point(coords['lig_pos']['x'], coords['lig_pos']['y'])
        print("📂 已加载保存的坐标:")
        print(f"   - Variational: Point(x={var_pos.x}, y={var_pos.y})")
        print(f"   - Lighter: Point(x={lig_pos.x}, y={lig_pos.y})")
        return var_pos, lig_pos
    except FileNotFoundError:
        print("❌ 未找到保存的坐标文件 coordinates.json")
        return None, None
    except Exception as e:
        print(f"❌ 加载坐标时出错: {e}")
        return None, None

# 根据配置决定是使用保存的坐标还是记录新坐标
if use_saved_coords:
    var_pos, lig_pos = load_coordinates()
    if var_pos is None or lig_pos is None:
        print("⚠️  无法加载保存的坐标，将重新记录坐标...")
        use_saved_coords = False

if not use_saved_coords:
    print("请把鼠标移动到Variational or Lighter的下单按钮上，3秒后自动记录坐标...")
    time.sleep(3)
    var_pos = pyautogui.position()
    print("✅ 按钮坐标记录为:", var_pos)

    print("请把鼠标移动到Variational or Lighter的下单按钮上，3秒后自动记录坐标...")
    time.sleep(3)
    lig_pos = pyautogui.position()
    print("✅ 按钮坐标记录为:", lig_pos)
    
    # 保存坐标供下次使用
    save_coordinates(var_pos, lig_pos)

print("\n📋 下单配置:")
print(f"   - 下单次数: {order_count}")
print(f"   - 使用双击: {'是' if use_double_click else '否'}")
print(f"   - 点击间隔: {click_delay}秒")
print(f"   - 下单间隔: {interval}秒")
print(f"   - 使用保存坐标: {'是' if use_saved_coords else '否'}")

print("\n💡 提示: 按Ctrl+C可随时中断程序")
print("💡 快速晃动鼠标也可中断程序")

input("\n👉 确认好页面（数量输入框、交易对等），按回车开始执行下单...")

try:
    for i in range(order_count):
        # 检查中断
        if check_interrupt():
            print(f"\n⏹️ 用户中断，已执行 {i}/{order_count} 次下单")
            break
            
        print(f"第 {i+1}/{order_count} 次下单...")
        
        # 这里不检测鼠标，避免误触发
        if check_interrupt():
            break
        if use_double_click:
            pyautogui.doubleClick(var_pos.x, var_pos.y)
        else:
            pyautogui.click(var_pos.x, var_pos.y)
        time.sleep(click_delay)
        
        # 再点击（这里也不检测鼠标）
        if check_interrupt():
            break
        if use_double_click:
            pyautogui.doubleClick(lig_pos.x, lig_pos.y)
        else:
            pyautogui.click(lig_pos.x, lig_pos.y)
        
        print(f"⏱️  等待 {interval} 秒...")
        
        # 在等待期间检测鼠标晃动（这里才检测）
        start_time = time.time()
        check_count = 0
        while time.time() - start_time < interval:
            if check_interrupt():
                break
            # 在等待期间才检测鼠标晃动
            if check_in_waiting_only:
                check_mouse_movement()
            if check_interrupt():
                break
            time.sleep(0.1)
    
    if not check_interrupt():
        print("✅ 所有下单完成。")
        # 发出滴声提醒
        os.system('afplay /System/Library/Sounds/Glass.aiff')  # macOS系统提示音
    else:
        print("⚠️ 程序被中断。")
        
except KeyboardInterrupt:
    print("\n\n⚠️ 收到中断信号...")
    print("正在安全退出...")

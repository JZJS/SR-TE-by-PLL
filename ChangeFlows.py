import os
import re
import sys

BASE_PATH = "E:/project/PLL/ChinaTelecom"
NEW_VALUE = 1000  # 您希望设置的新值

def modify_script(script_name):
    full_script_path = os.path.join(BASE_PATH, script_name)
    
    # 读取原始脚本内容
    with open(full_script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式替换内容
    content = re.sub(r'for _ in range\(\d+\):', f'for _ in range({NEW_VALUE}):', content)
    
    # 写回到脚本中
    with open(full_script_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    scripts = [
        "V30dijkstra_ChinaTelecom_ECMP_hop.py",
        "V30dijkstra_ChinaTelecom_hop.py",
        "V30dijkstra_ChinaTelecom_kshortest_hop.py",
        "V30pll_heuristic2_ChinaTelecom_ECMP1_hop.py",
        "V30pll_heuristic2_ChinaTelecom_ECMP2_hop.py",
        "V30pll_heuristic2_ChinaTelecom_hop.py",
        "V30pll_heuristic3_ChinaTelecom_ECMP1_hop.py",
        "V30pll_heuristic3_ChinaTelecom_ECMP2_hop.py",
        "V30pll_heuristic3_ChinaTelecom_hop.py",
        "V30pll_heuristic_ChinaTelecom_ECMP1_hop.py",
        "V30pll_heuristic_ChinaTelecom_ECMP2_hop.py",
        "V30pll_heuristic_ChinaTelecom_ECMP3_hop.py",
        "V30pll_heuristic_ChinaTelecom_hop.py"
    ]

    for script in scripts:
        modify_script(script)
        print(f"Modified {script}")

if __name__ == "__main__":
    NEW_VALUE = int(sys.argv[1])  # 从命令行参数获取新的K值
    main()

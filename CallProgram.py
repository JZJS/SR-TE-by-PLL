import subprocess
import os
import sys

BASE_PATH = "E:/project/PLL/ChinaTelecom"

def change_k_landmark(new_value):
    script_path = os.path.join(BASE_PATH, 'ChangeKLandmark.py')
    os.system(f'python {script_path} {new_value}')

def change_flows(new_value):
    script_path = os.path.join(BASE_PATH, 'ChangeFlows.py')
    os.system(f'python {script_path} {new_value}')

def run_hundred_times(output_file):
    script_path = os.path.join(BASE_PATH, 'Runhundredtimes.py')
    with open(output_file, 'w') as f:
        result = subprocess.run(['python', script_path], stdout=f, stderr=subprocess.PIPE)
        if result.stderr:
            print(f"Error while running {script_path}: {result.stderr.decode('utf-8')}")



def main():
    # 设置K的值从3到10
    for k in range(3, 11):
        print(f"Current k value: {k}")
        # 使用ChangeKLandmark.py将K值设置为k
        change_k_landmark(k)
        
        # 使用ChangeFlows.py将Flows设置为500
        change_flows(500)
        
        # 运行Runhundredtimes.py并将输出写入到CallK=k.txt
        output_file = os.path.join(BASE_PATH, "CallK=" + str(k) + ".txt")
        print(f"Output file path: {output_file}")
        run_hundred_times(output_file)
        
        # 使用ChangeFlows.py将Flows设置为1000
        change_flows(1000)
        
        # 运行Runhundredtimes.py并将输出写入到CallK=k_1000.txt
        output_file = os.path.join(BASE_PATH, "CallK=" + str(k) + "_1000.txt")

        print(f"Output file path: {output_file}")
        run_hundred_times(output_file)
        
if __name__ == "__main__":
    main()

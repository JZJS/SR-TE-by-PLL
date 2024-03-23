import os

def rename_files(folder_path):
    # 获取指定文件夹下的所有文件名
    file_list = os.listdir(folder_path)

    # 遍历文件名并进行修改
    for filename in file_list:
        new_filename = filename.replace("synth50", "ChinaTelecom")  # 将5替换为20
        #new_filename = new_filename + ""  # 文件名后面加上x100

        # 构建旧文件路径和新文件路径
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_filename)

        # 重命名文件
        os.rename(old_path, new_path)

# 指定文件夹路径，替换为你需要的文件夹路径
folder_path = "E:\project\PLL\ChinaTelecom"

# 调用函数进行文件名修改
rename_files(folder_path)

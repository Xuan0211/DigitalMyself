import csv
import re
from pathlib import Path
LOCAL_PATH = str(Path(__file__).parent)

def filter_csv(input_file, output_file):
    filtered_rows = []

    with open(input_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for i, row in enumerate(reader):
            if i >= 3:  # 从第四行开始读取数据表
                if len(row) > 1:
                    items = re.findall(r'([^,]*?)\s(https?://\S+)', row[1])  # 使用正则表达式找出每行中的文字和链接
                    if items:
                        for text, link in items:
                            filtered_rows.append(['"'+ text.strip() + link.strip() + '"'])

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in filtered_rows:
            writer.writerow(row)

    print("过滤完成，结果已写入新的CSV文件。")

# 使用示例
input_file = LOCAL_PATH + '\\input\\校园集市.csv'  # 输入的CSV文件名
output_file = LOCAL_PATH + '\\output\\校园集市.csv'  # 输出的CSV文件名

filter_csv(input_file, output_file)
# -*- coding: utf-8 -*-
# @Time    : 2023.12.2
# @Author  : Xuan
# @Email   : 2022134346@qq.com
# @File    : md2csv.py
# @Software: Vscode

import re
import csv
from pathlib import Path
LOCAL_PATH = str(Path(__file__).parent)
INPUT_FOLDER = LOCAL_PATH + '\\store\\databank\\input\\'
OUTPUT_FOLDER = LOCAL_PATH + '\\store\\databank\\output\\'

def extract_blocks(markdown_text: str) -> list[(int, str)]:
    """分割Markdown文件，规则为获取两个''#'*n' "''#'*n' 之间的文本块，并记录'#'的数量到level，便于分析块的层级关系

    Args:
        markdown_text (string):markdown文字串

    Returns:
        list[(int, str)]: 返回一个表示字符块层级的数字和字符块
    """
    pattern = r'(#+)\s*(.*?)\s*(?=(?:#+\s*|$))'
    matches = re.findall(pattern, markdown_text, re.DOTALL)
    blocks = []
    for match in matches:
        level = len(match[0])
        title = match[1].strip()
        blocks.append((level, title))
    return blocks

def process_markdown_file(file_path: str) -> list[str]:
    """读取字符块并和上级标题拼合，并去掉纯标题的字符块。


    Args:
        file_path (str): 文件路径

    Returns:
        list[str]: 拼合后的字符串数组
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        markdown_text = file.read()
        markdown_text = markdown_text.replace("&#x20;", "")
        blocks = extract_blocks(markdown_text)
        blocks_withTitle = []
        
        # 拼合上级标题
        for i in range(len(blocks)):
            level, content = blocks[i]
            level_t = level
            title = '#' * blocks[i][0]
            for j in range(i-1, -1, -1):
                if blocks[j][0] <= level_t - 1:
                    title = '#' * blocks[j][0] + ' ' + blocks[j][1] + ' - ' + title
                    level_t = blocks[j][0]
            blocks_withTitle.append((level, title + content))
        result = []
        level_now = blocks_withTitle[len(blocks_withTitle) - 1][0]
        
        # 对比level，如果标号比当前低，则跳过，如果相等，说明是相同层级的块，加入，如果更高，那说明是上一个块中的低级块，更新level并加入
        for i in range(len(blocks_withTitle) - 1, -1, -1):
            if (blocks_withTitle[i][0] == level_now):
                result.append(blocks_withTitle[i][1])
            else:
                if blocks_withTitle[i][0] < level_now:
                    level_now = blocks_withTitle[i][0]
                else:
                    result.append(blocks_withTitle[i][1])
                    level_now = blocks_withTitle[i][0]
        result.reverse()
        return result


def save_to_csv(blocks: list[str], output_file: str) -> None:
    """将字符块写入csv中

    Args:
        blocks (list[str]): 字符块数组
        output_file (str): 写入的文件名
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in blocks:
            writer.writerow(['"'+ row +'"'])
            
def single_file_to_csv(file_path: str, id: int) -> None:
    """处理单个文件，并将结果保存到csv文件中

    Args:
        file_path (str): 文件路径
    """
    blocks = process_markdown_file(file_path)
    output_file = OUTPUT_FOLDER + str(id) + '.csv'
    save_to_csv(blocks, output_file)
    print(f"File {file_path} processed and saved to {output_file}")

if __name__ == '__main__':
    # 获取指定文件夹中的所有md文件
    md_files = Path(INPUT_FOLDER).rglob('*.md')

    for file in md_files:
        output_file = str(file).replace(INPUT_FOLDER, OUTPUT_FOLDER).replace('.md', '.csv')
        blocks = process_markdown_file(str(file))
        save_to_csv(blocks, output_file)

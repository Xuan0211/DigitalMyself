import re
import csv
from pathlib import Path
LOCAL_PATH = str(Path(__file__).parent)
def extract_blocks(markdown_text):
    pattern = r'(#+)\s*(.*?)\s*(?=(?:#+\s*|$))'
    matches = re.findall(pattern, markdown_text, re.DOTALL)
    blocks = []
    for match in matches:
        level = len(match[0])
        title = match[1].strip()
        blocks.append((level, title))
    return blocks

def process_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        markdown_text = file.read()
        markdown_text = markdown_text.replace("&#x20;", "")
        blocks = extract_blocks(markdown_text)
        blocks_withTitle = []
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

def save_to_csv(blocks, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in blocks:
            writer.writerow(['"'+ row +'"'])

# 获取指定文件夹中的所有md文件
input_folder = LOCAL_PATH + '\store\databank\input'
output_folder = LOCAL_PATH + '\store\databank\output'

md_files = Path(input_folder).rglob('*.md')

for file in md_files:
    output_file = str(file).replace(input_folder, output_folder).replace('.md', '.csv')
    blocks = process_markdown_file(str(file))
    save_to_csv(blocks, output_file)

import re
import os

def split_text_by_chapter(file_path, output_folder):
    chapter_pattern = re.compile(r'## 第(\d+)章\s?.+ ##')
    chapter_content = []
    chapter_title = None  # 用于保存章节标题
    chapter_number = None  # 用于保存章节编号

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = chapter_pattern.match(line.strip())
            if match:
                if chapter_content and chapter_number:  # 有内容且章节编号存在时才保存
                    # 在内容开头加上章节标题
                    chapter_content.insert(0, chapter_title + "\n")
                    with open(os.path.join(output_folder, f'{chapter_number}.txt'), 'w', encoding='utf-8') as chapter_file:
                        chapter_file.write(''.join(chapter_content))
                    chapter_content = []  # 清空内容以用于下一章节
                chapter_title = line.strip()  # 更新章节标题
                chapter_number = match.group(1)  # 更新章节编号

            else:
                chapter_content.append(line)

        # 保存最后一章的内容
        if chapter_content and chapter_number:
            chapter_content.insert(0, chapter_title + "\n")
            with open(os.path.join(output_folder, f'{chapter_number}.txt'), 'w', encoding='utf-8') as chapter_file:
                chapter_file.write(''.join(chapter_content))


# 使用示例
split_text_by_chapter('9518.txt', 'Novel_24')

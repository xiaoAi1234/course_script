import re
import json
import os

def read_file_content(file_path):
    """
    通过文件路径读取文件内容
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 '{file_path}'，请检查路径是否正确")
        return None

    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return None

def write_file_content(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def process_document(file_content):
    # 1. 解析文本，转换为字典数组
    # 使用正则表达式按照 "第 X 页" 切分文本
    raw_pages = re.split(r'第\s*\d+\s*页\s*\n', file_content.strip())

    dict_array = []

    # 将每页ppt内容转换为字典对象
    for page in raw_pages:
        page = page.strip()
        if not page:
            continue

        # 按行切分，第一行是 type，剩下的是 content
        lines = page.split('\n', 1)
        if len(lines) >= 1:
            page_type = lines[0].strip()
            # 如果有内容则保留，否则为空字符串
            content = lines[1].strip() if len(lines) > 1 else ""

            dict_array.append({
                "type": page_type,
                "content": content
            })

    return dict_array

def interact_with_user(dict_array, start_num):
    # 2. 输出每页ppt的卡片生成提示词
    print("====== 开始 ======")
    for i, item in enumerate(dict_array[start_num - 1:]):
        # 根据页面类型输出不同提示词
        page_type = item.get("type")

        if page_type not in PAGE_TYPES:
            print("非合法页面类型")
            continue

        prompt_path = PROMPT_MAP.get(page_type)

        file_text = read_file_content(prompt_path)

        if file_text:
            write_file_content(PATH_DICT["output"], file_text + f"{item.get('content')}")

        print(f"第 {x + i} 页    {item.get('type')}")

        # 询问用户是否继续
        while True:
            user_input = input("是否继续？(按下回车继续，输入 n 退出): ").strip().lower()

            if user_input == '':
                break
            elif user_input == 'n':
                print("结束操作")
                return
            else:
                print("输入无效，请重新输入！")

if __name__ == "__main__":

    # 文件路径字典
    PATH_DICT = {
        "input": "./file/input.txt",
        "output": "./file/output.txt",

        "cover_page_prompt": "./file/prompt/cover_page.txt",
        "toc_page_prompt": "./file/prompt/toc_page.txt",
        "section_page_prompt": "./file/prompt/section_page.txt",
        "text_content_page_prompt": "./file/prompt/text_content_page.txt",
        "visual_content_page_prompt": "./file/prompt/visual_content_page.txt",
        "exercise_page_prompt": "./file/prompt/exercise_page.txt",
    }

    # 页面类型列表
    PAGE_TYPES = [
        "封面页",
        "目录页",
        "分隔页",
        "文字内容页",
        "可视化内容页",
        "习题页"
    ]

    # 页面类型对应的 prompt 文件
    PROMPT_MAP = {
        "封面页": PATH_DICT["cover_page_prompt"],
        "目录页": PATH_DICT["toc_page_prompt"],
        "分隔页": PATH_DICT["section_page_prompt"],
        "文字内容页": PATH_DICT["text_content_page_prompt"],
        "可视化内容页": PATH_DICT["visual_content_page_prompt"],
        "习题页": PATH_DICT["exercise_page_prompt"],
    }

    # 2. 读取文件内容
    file_text = read_file_content(PATH_DICT["input"])

    # 3. 输出每页ppt的卡片生成提示词
    if file_text is not None:
        parsed_array = process_document(file_text)
        # 从第 x 页开始输出
        x = 1
        interact_with_user(parsed_array,x)
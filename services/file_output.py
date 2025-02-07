from datetime import datetime
import os
import json

def save_to_json(data: dict, field_name: str, book_title: str):
    """
    将数据保存到JSON文件
    
    Args:
        data: 要保存的数据
        field_name: 字段名称（用作文件名前缀）
        book_title: 书籍标题（用作文件名的一部分）
    """
    # 创建输出目录（如果不存在）
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 格式化当前日期
    current_date = datetime.now().strftime("%Y%m%d")
    
    # 处理书籍标题（移除特殊字符）
    book_title = book_title.replace("《", "").replace("》", "")
    
    # 构建文件名
    filename = f"{output_dir}/{field_name}_{current_date}_{book_title}.json"
    
    # 保存数据到文件
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"数据已保存到文件: {filename}")
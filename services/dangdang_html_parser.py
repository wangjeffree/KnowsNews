import requests
from bs4 import BeautifulSoup
import time

def get_hot_book_list():
    # 设置请求头模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    titles = []

    # 目标URL
    for i in range(1, 10):
        url = f'http://bang.dangdang.com/books/newhotsales/01.00.00.00.00.00-recent7-0-0-1-{i}'
        # http://bang.dangdang.com/books/newhotsales/01.00.00.00.00.00-recent7-0-0-1-1
        # http://bang.dangdang.com/books/newhotsales/01.00.00.00.00.00-recent7-0-0-1-25

        try:
            # 发送HTTP请求
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # 检查状态码
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 定位书名所在元素(根据实际页面结构调整选择器)
            book_list = soup.select('ul.bang_list li')  # 每个li标签包含一本书的信息
            
            # 提取书名
            for book in book_list:
                title_tag = book.select_one('div.name a')
                if title_tag:
                    title = title_tag.get('title') or title_tag.text.strip()
                    titles.append(title)
            
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
        except Exception as e:
            print(f"解析错误: {e}")

    # 打印结果
    print(f"共抓取到{len(titles)}本书:")
    for idx, title in enumerate(titles, 1):
        print(f"{idx}. {title}")

    return titles

if __name__ == '__main__':
    get_hot_book_list()

import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import json
from services.config import *
import time
def get_news():

    # 从聚合数据API获取新闻列表
    juhe_news_list = get_news_from_juhe()
    print("聚合数据新闻列表:", juhe_news_list)
    # 将聚合数据新闻列表保存为json文件，文件名中包含当前日期
    date_str = time.strftime("%Y-%m-%d", time.localtime())
    filename = f"output/news_list_{date_str}.json"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(juhe_news_list, f, ensure_ascii=False, indent=4)
        print(f"聚合新闻已成功保存到文件: {filename}")
    except Exception as e:
        print(f"保存聚合新闻到文件失败: {e}")
    
    # 爬取百度热搜新闻
    baidu_news_list = crawl_baidu_hotnews() 
    print("百度热搜新闻:", baidu_news_list)
    
    # 计算新闻标题相似度,找出最相关的新闻
    max_similarity = 0
    most_similar_title = ""
    most_similar_uniquekey = ""
    
    for juhe_news in juhe_news_list:
        for baidu_news in baidu_news_list:
            similarity = calculate_similarity(juhe_news["title"], baidu_news["title"])
            if similarity >= max_similarity:
                max_similarity = similarity
                most_similar_title = juhe_news["title"]
                most_similar_uniquekey = juhe_news["uniquekey"]

    print("最相关新闻标题:", most_similar_title)
    print("最相关新闻uniquekey:", most_similar_uniquekey)
    return most_similar_uniquekey

def get_news_content(news_uniquekey):
    # 测试模式：读取测试新闻详情数据
    if DEBUG_MODE:
        try:
            with open(TEST_NEWS_CONTENT_PATH, 'r', encoding='utf-8') as f:
                content_data = json.load(f)
                return content_data["result"]["detail"]["title"], content_data["result"]["content"]
        except Exception as e:
            print(f"读取测试新闻详情数据失败: {e}")
            return f"{news_uniquekey} 的详细内容：这是测试环境下的模拟新闻详情。"
    
    # 正常模式：调用聚合数据API获取新闻详情
    url = f"{JUHE_NEWS_CONTENT_API}?uniquekey={news_uniquekey}&key={JUHE_API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["error_code"] == 0:
                # 保存新闻详情到json文件
                # date = time.strftime("%Y-%m-%d", time.localtime())
                # filename = f"data/news_content_{date}_{data['result']['title']}.json"

                # try:
                #     with open(filename, 'w', encoding='utf-8') as f:
                #         json.dump(data, f, ensure_ascii=False, indent=4)
                #     print(f"新闻详情已保存到文件: {filename}")
                # except Exception as e:
                #     print(f"保存新闻详情到文件失败: {e}")
                return data["result"]["detail"]["title"], data["result"]["content"]
            
        print(f"获取新闻详情失败: {data}")
        return f"{news_uniquekey} 的详细内容：API调用失败时的默认新闻详情。"
            
    except Exception as e:
        print(f"获取新闻详情API调用异常: {e}")
        return f"{news_uniquekey} 的详细内容：发生异常时的默认新闻详情。"
    return f"{news_title} 的详细内容：这是一条模拟新闻的详细描述。"

def get_news_from_juhe():
    if DEBUG_MODE:
        try:
            with open(TEST_NEWS_LIST_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)["result"]["data"]
        except Exception as e:
            print(f"读取测试数据失败: {e}")
            return [
                {"title": "测试新闻标题1", "url": "http://example.com/1"},
                {"title": "测试新闻标题2", "url": "http://example.com/2"},
            ]
    
    # 正常模式：调用聚合数据API
    url = f"{JUHE_NEWS_LIST_API}?type=top&key={JUHE_API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["error_code"] == 0:
                return data["result"]["data"]
            
        print(data)
            
        # 如果API调用失败，返回模拟数据
        return [
            {"title": "新闻标题1", "url": "http://example.com/1"},
            {"title": "新闻标题2", "url": "http://example.com/2"},
        ]
    except Exception as e:
        print(f"API调用失败: {e}")
        return [
            {"title": "新闻标题1", "url": "http://example.com/1"},
            {"title": "新闻标题2", "url": "http://example.com/2"},
        ]

def crawl_baidu_hotnews():
    url = "https://www.baidu.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            hot_news = []
            # 实际实现中需要根据百度首页的具体HTML结构来定位热搜新闻
            # 这里返回模拟数据
            titles = soup.find_all(class_="title-content-title")
            for title in titles:
                hot_news.append({
                    "title": title.text.strip()
                })
            return hot_news
    except:
        return [
            {"title": "百度热搜1"},
            {"title": "百度热搜2"},
        ]

def calculate_similarity(text1, text2):
    # 使用SequenceMatcher计算两个文本的相似度
    return SequenceMatcher(None, text1, text2).ratio() 

if __name__ == "__main__":
    get_news()

import requests

def deepseek_recommend_books(news_detail):
    # 模拟 deepseek 模型推荐书籍的逻辑
    # 假设返回一本书名
    try:
        # 假设 deepseek r1 接口的URL地址
        url = "http://api.deepseek.com/r1"
        # 构造请求数据，将新闻内容传递给接口进行分析
        payload = {"news_content": news_detail}
        # 发送POST请求调用 deepseek r1 接口
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            result = response.json()
            # 假定接口返回格式为 { "recommended_book": "书籍名称" }
            book_title = result.get("recommended_book")
            if book_title:
                return book_title
    except Exception as e:
        # 这里可以添加错误日志记录逻辑，目前直接忽略异常
        pass
    return "《Python编程入门》"


def query_douban(book_title):
    # 模拟豆瓣API查询书籍相关介绍
    return f"{book_title} 是一本面向初学者的入门书籍，包含丰富案例和实战技巧。"


def generate_narration(news_detail, book_intro):
    # 模拟生成旁白
    return f"新闻内容：{news_detail}。推荐书籍介绍：{book_intro}。"


def generate_video_and_audio():
    
    # 模拟生成视频和音频
    return "video_generated.mp4", "audio_generated.mp3"


def generate_ad_copy(narration):
    # 模拟生成带货文案
    # 调用 OpenRouter 服务生成带货文案
    try:
        from services.ai_openrouter import OpenRouterService
        from services.config import OPENROUTER_API_KEY
        
        openrouter = OpenRouterService(OPENROUTER_API_KEY)
        ad_copy = openrouter.generate_ad_copy(narration, "对短视频感兴趣的年轻用户")
        return ad_copy
    except Exception as e:
        print(f"生成带货文案失败: {str(e)}")
    return "带货短视频精彩呈现，点击了解更多！" 
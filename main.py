from services.ai_openrouter import OpenRouterService
from services.config import *
from services.dangdang_html_parser import get_hot_book_list
from services.news import get_news, get_news_detail
from services.ai import deepseek_recommend_books, query_douban, generate_narration, generate_video_and_audio, generate_ad_copy


def main():
    
    services = {
            # "deepseek": DeepseekService(DEEPSEEK_API_KEY),
            # "siliconflow": SiliconflowService(SILICONFLOW_API_KEY),
            # "openrouter": OpenRouterService(OPENROUTER_API_KEY)
    }
    ai_service = OpenRouterService(OPENROUTER_API_KEY)
    
    # 热点新闻获取
    most_similar_uniquekey = get_news()
    news_content = get_news_detail(most_similar_uniquekey)
    print("获取的新闻详情:", news_content)

    # AI模型分析，推荐书籍
    # book_title = deepseek_recommend_books(news_content)

    # 用当当网获取热门书籍
    hot_book_list = get_hot_book_list()
    book_title = ai_service.analyze_news_and_recommend_book(news_content, hot_book_list)
    print("推荐书籍:", book_title)

    # 查询豆瓣，获取书籍介绍
    # book_intro = query_douban(book_title)
    # print("豆瓣书籍介绍:", book_intro)

    # 生成旁白
    narration = ai_service.generate_narration(news_content, book_title)
    print("生成的旁白:", narration)

    # 生成视频和音频
    video, audio = generate_video_and_audio()
    print("生成的视频:", video)
    print("生成的音频:", audio)

    # 生成带货文案
    ad_copy = generate_ad_copy(narration)
    print("生成的带货文案:", ad_copy)


if __name__ == '__main__':
    main()




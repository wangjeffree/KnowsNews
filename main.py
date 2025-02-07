from services.ai_client.ai_deepseek import DeepseekService
from services.ai_client.ai_openrouter import OpenRouterService
from services.ai_client.ai_siliconflow import SiliconflowService
from services.config import *
from services.dangdang_html_parser import get_hot_book_list
from services.file_output import save_to_json
from services.news import get_news, get_news_content
from services.ai_generator import deepseek_recommend_books, query_douban, generate_narration, generate_video_and_audio, generate_ad_copy

def main():
    

    services = {
            "deepseek": DeepseekService(DEEPSEEK_API_KEY),
            "siliconflow": SiliconflowService(SILICONFLOW_API_KEY),
            "openrouter": OpenRouterService(OPENROUTER_API_KEY)
    }
    ai_service = services["openrouter"]
    
    # 热点新闻获取
    most_similar_uniquekey = get_news()
    news_title, news_content = get_news_content(most_similar_uniquekey)
    print("获取的新闻详情:", news_content)
    # 保存新闻内容
    save_to_json({"content": news_content}, "news", news_title)


    # AI模型分析，推荐书籍
    # book_title = deepseek_recommend_books(news_content)

    # 用当当网获取热门书籍
    hot_book_list = get_hot_book_list()
    save_to_json({"hot_book_list": hot_book_list}, "hot_book_list", "周畅销书榜")
    book_title = ai_service.analyze_news_and_recommend_book(news_content, hot_book_list)
    print("推荐书籍:", book_title)

    # 查询豆瓣，获取书籍介绍
    # book_intro = query_douban(book_title)
    # print("豆瓣书籍介绍:", book_intro)

    # 生成旁白解说词
    narration = ai_service.generate_narration(news_content, book_title)
    print("生成的旁白:", narration)
    
    # 生成带货文案
    ad_copy = ai_service.generate_ad_copy(news_content, book_title, "对短视频感兴趣的年轻读者")
    print("生成的带货文案:", ad_copy)
    # 保存旁白和带货文案
    save_to_json({"book_title": book_title, "narration": narration, "ad_copy": ad_copy}, 
                 "book_ad", book_title)


    # 生成视频分镜脚本和AI视频prompt
    # video_script, ai_video_prompt = ai_service.generate_video_script(narration)
    # print("生成的视频分镜脚本:", video_script)
    # print("生成的AI视频prompt:", ai_video_prompt)
    # # 保存视频相关信息
    # save_to_json({
    #     "video_script": video_script,
    #     "ai_video_prompt": ai_video_prompt
    # }, "video", book_title)

    # # 生成视频和音频
    # video, audio = generate_video_and_audio()
    # print("生成的视频:", video)
    # print("生成的音频:", audio)



if __name__ == '__main__':
    main()




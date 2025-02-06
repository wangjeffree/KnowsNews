from services.news import get_news, get_news_detail
from services.ai import deepseek_recommend_books, query_douban, generate_narration, generate_video_and_audio, generate_ad_copy


def main():
    # 热点新闻获取
    most_similar_uniquekey = get_news()
    news_content = get_news_detail(most_similar_uniquekey)
    print("获取的新闻详情:", news_content)

    # AI模型分析，推荐书籍
    book_title = deepseek_recommend_books(news_content)
    print("推荐书籍:", book_title)


    # 查询豆瓣，获取书籍介绍
    book_intro = query_douban(book_title)
    print("豆瓣书籍介绍:", book_intro)

    # 生成旁白
    narration = generate_narration(news_content, book_intro)
    print("生成的旁白:", narration)


    # 生成视频和音频
    video, audio = generate_video_and_audio()
    print("生成的视频:", video)
    print("生成的音频:", audio)

    # 生成带货文案
    ad_copy = generate_ad_copy()
    print("生成的带货文案:", ad_copy)


if __name__ == '__main__':
    main()




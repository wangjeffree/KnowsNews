from abc import ABC, abstractmethod

class AIServiceBase(ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    @abstractmethod
    def analyze_news_and_recommend_book(self, news_content: str) -> str:
        """分析新闻内容并推荐相关书籍"""
        pass
    
    @abstractmethod
    def generate_narration(self, news_content: str, book_intro: str) -> str:
        """生成视频旁白"""
        pass
    
    @abstractmethod
    def generate_video_script(self, narration: str) -> tuple[str, str]:
        """生成视频和音频脚本"""
        pass
    
    @abstractmethod
    def generate_ad_copy(self, news_content: str, book_info: str, target_audience: str) -> str:
        """生成带货文案"""
        pass 
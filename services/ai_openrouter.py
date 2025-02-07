import requests
from services.ai_base import AIServiceBase
from services.config import OPENROUTER_HTTP_REFERER

class OpenRouterService(AIServiceBase):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.api_base = "https://openrouter.ai/api/v1"
        
    def _call_api(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": OPENROUTER_HTTP_REFERER,
                    "Content-Type": "application/json"
                },
                json={
                    # "model": "deepseek/deepseek-r1", 
                    # "model": "deepseek/deepseek-chat",
                    "model": "deepseek/deepseek-r1-distill-llama-70b:free",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                }
            )
            response.raise_for_status()  # 检查HTTP错误
            result = response.json()
            if "choices" not in result or len(result["choices"]) == 0:
                raise ValueError("API返回结果格式错误")
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API请求失败: {str(e)}")
        except (KeyError, ValueError, TypeError) as e:
            raise RuntimeError(f"解析API响应失败: {str(e)}")
    def analyze_news_and_recommend_book(self, news_content: str, hot_book_list: list) -> str:
        prompt = f"""你是一位作为专业的小视频带货高手。请分析以下新闻，推荐一本书籍：


新闻内容：
{news_content}

基于新闻内容，请推荐一本最合适的书籍：
1. 与新闻主题高度相关
2. 内容要有深度，能扩展新闻话题
3. 优先选择近期出版的畅销书
4. 通过带货尽量能够获得佣金
5. 从这个列表中获取对应图书：
{hot_book_list}
6. 只需返回书名，格式：《书名》"""
        
        return self._call_api(prompt)
        
    def generate_narration(self, news_content: str, book_intro: str) -> str:
        prompt = f"""作为专业的短视频编剧，请为以下内容创作旁白：

新闻内容：
{news_content}

推荐书籍：
{book_intro}

创作要求：
1. 以新闻热点开场，吸引观众注意
2. 巧妙过渡到书籍推荐环节
3. 重点突出新闻与书籍的关联性
4. 语言要简洁生动，适合短视频
5. 是旁白解说词,不是展示文本,不需要段落格式,而是需要搭配短视频.流畅的解说词
6. 总字数控制在300字左右"""
        

        return self._call_api(prompt)
        
    def generate_video_script(self, narration: str) -> tuple[str, str]:
        prompt = f"""作为专业的视频导演，请为以下旁白设计完整的视频方案：

旁白内容：
{narration}

请提供两个部分：
1. 视频分镜脚本：包含画面设计、镜头调度、转场特效等
2. 音频设计方案：包含背景音乐风格、音效设计、氛围营造等

输出格式：
视频脚本：
[分镜脚本内容]

音频建议：
[音频方案内容]"""
        
        result = self._call_api(prompt)
        video_script, audio_script = result.split("音频建议：")
        return video_script.replace("视频脚本：", "").strip(), audio_script.strip()
        
    def generate_ad_copy(self, book_info: str, target_audience: str) -> str:
        prompt = f"""作为专业的文案策划，请为图书创作带货文案：

图书信息：
{book_info}

目标受众：
{target_audience}

文案要求：
1. 开场要有吸引力，抓住用户痛点
2. 提炼3个最有说服力的卖点
3. 语言要符合目标受众的表达习惯
4. 结尾要有强有力的行动召唤
5. 总字数控制在150字以内"""
        
        return self._call_api(prompt) 
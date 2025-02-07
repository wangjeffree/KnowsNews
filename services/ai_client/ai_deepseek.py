import requests
from services.ai_client.ai_base import AIServiceBase

class DeepseekService(AIServiceBase):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.api_base = "https://api.deepseek.com/v1"
        
    # 调用DeepSeek大模型API
    # prompt: 请求参数
    # model: 模型名称，默认deepseek-chat（即v3），可选deepseek-reasoner（即r1）
    def _call_api(self, prompt: str, model: str = "deepseek-chat") -> str:
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 2000
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
    def analyze_news_and_recommend_book(self, news_content: str) -> str:
        prompt = f"""分析以下新闻内容，推荐一本最相关的书籍：
        
新闻内容：{news_content}

请推荐一本与新闻主题最相关的书籍，要求：
1. 书籍内容与新闻主题高度相关
2. 优先选择近期出版的畅销书
3. 只返回书名，格式：《书名》"""
        
        return self._call_api(prompt, "deepseek-reasoner")
        
    def generate_narration(self, news_content: str, book_intro: str) -> str:
        prompt = f"""基于以下新闻内容和推荐书籍，生成视频旁白：

新闻内容：{news_content}

推荐书籍：{book_intro}

要求：
1. 先介绍新闻背景
2. 然后自然引出推荐书籍
3. 突出书籍与新闻的关联性
4. 语言要生动活泼，适合视频配音
5. 控制在300字以内"""
        
        return self._call_api(prompt)
        
    def generate_video_script(self, narration: str) -> tuple[str, str]:
        prompt = f"""基于以下旁白生成视频脚本和音频建议：

旁白内容：{narration}

请分别生成：
1. 视频画面脚本：包括场景、镜头、转场等
2. 音频设计建议：包括背景音乐风格、音效等

格式：
视频脚本：
[具体内容]

音频建议：
[具体内容]"""
        
        result = self._call_api(prompt)
        video_script, audio_script = result.split("音频建议：")
        return video_script.replace("视频脚本：", "").strip(), audio_script.strip()
        
    def generate_ad_copy(self, book_info: str, target_audience: str) -> str:
        prompt = f"""为以下图书生成带货文案：

图书信息：{book_info}
目标受众：{target_audience}

要求：
1. 突出书籍价值和受众痛点
2. 包含2-3个吸引人的卖点
3. 结尾加入号召性用语
4. 控制在150字以内"""
        
        return self._call_api(prompt) 
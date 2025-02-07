import requests
from services.ai_base import AIServiceBase

class SiliconflowService(AIServiceBase):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.api_base = "https://api.siliconflow.com/v1"
        
    def _call_api(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-ai/DeepSeek-R1", 
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
        prompt = f"""作为专业的小视频带货高手，请分析以下新闻并推荐相关书籍：

新闻内容：
{news_content}

请根据新闻主题和内容，推荐一本最相关的书籍。要求：
1. 书籍主题与新闻高度相关
2. 内容具有深度和广度
3. 优先推荐近期出版的畅销书
4. 只返回书名，格式：《书名》"""
        
        return self._call_api(prompt)
        
    def generate_narration(self, news_content: str, book_intro: str) -> str:
        prompt = f"""请为短视频生成旁白稿件：

新闻内容：
{news_content}

推荐书籍：
{book_intro}

要求：
1. 开头要吸引人，引出新闻热点
2. 中间自然过渡到书籍推荐
3. 突出新闻与书籍的关联性
4. 语言生动有趣，适合视频配音
5. 字数控制在300字左右"""
        
        return self._call_api(prompt)
        
    def generate_video_script(self, narration: str) -> tuple[str, str]:
        prompt = f"""请为以下旁白内容设计视频脚本：

旁白内容：
{narration}

请分别提供：
1. 视频画面脚本：详细说明画面、镜头语言、转场效果
2. 音频设计方案：包括背景音乐风格、音效设计等

输出格式：
视频脚本：
[详细脚本内容]

音频建议：
[详细音频方案]"""
        
        result = self._call_api(prompt)
        video_script, audio_script = result.split("音频建议：")
        return video_script.replace("视频脚本：", "").strip(), audio_script.strip()
        
    def generate_ad_copy(self, book_info: str, target_audience: str) -> str:
        prompt = f"""请为图书生成带货文案：

图书信息：
{book_info}

目标受众：
{target_audience}

要求：
1. 开头要吸引眼球
2. 突出2-3个核心卖点
3. 描述要精准打动目标受众
4. 结尾加强购买理由
5. 字数控制在150字以内"""
        
        return self._call_api(prompt) 
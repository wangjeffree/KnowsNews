from services.ai_client.ai_openrouter import OpenRouterService
from services.config import OPENROUTER_API_KEY

def generate_video_copy(video_content: str) -> str:
    ai_service = OpenRouterService(api_key=OPENROUTER_API_KEY)
    return ai_service.generate_video_copy(video_content)

if __name__ == "__main__":
    video_content = "[第一视角] 用废旧电脑机箱改造赛博风桌面鱼缸,电钻打孔+LED灯光接线过程特写,快剪配合机械音效,最后鱼群游过散热孔慢镜头"
    print(generate_video_copy(video_content))



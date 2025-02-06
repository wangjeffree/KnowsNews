import unittest
from services.config import *
from services.ai_deepseek import DeepseekService
from services.ai_siliconflow import SiliconflowService
from services.ai_openrouter import OpenRouterService

class TestAIServices(unittest.TestCase):
    def setUp(self):
        """初始化测试环境"""
        self.test_news = """
        《哪吒之魔童闹海》的现象级"魔力"：电影以突破57.76亿元票房成为中国内地影史票房冠军。
        影片通过现代化改编，将传统神话角色重塑为具有当代特质的形象，在保持传统文化精髓的同时，
        赋予了故事新的时代内涵。
        """
        self.test_book_info = "《中国神话》，作者：袁珂，这是一本系统介绍中国神话的经典著作。"
        self.test_target_audience = "对中国传统文化感兴趣的年轻读者"
        
        # 初始化三个服务
        self.services = {
            "deepseek": DeepseekService(DEEPSEEK_API_KEY),
            "siliconflow": SiliconflowService(SILICONFLOW_API_KEY),
            "openrouter": OpenRouterService(OPENROUTER_API_KEY)
        }
        
    def test_all_services(self):
        """测试所有服务的完整流程"""
        for service_name, service in self.services.items():
            print(f"\n测试 {service_name} 服务:")
            try:
                # 1. 测试图书推荐
                book_title = service.analyze_news_and_recommend_book(self.test_news)
                print(f"推荐书籍: {book_title}")
                self.assertIsInstance(book_title, str)
                self.assertIn("《", book_title)
                self.assertIn("》", book_title)
                
                # 2. 测试旁白生成
                narration = service.generate_narration(self.test_news, book_title)
                print(f"生成旁白: {narration[:100]}...")
                self.assertIsInstance(narration, str)
                self.assertTrue(len(narration) > 0)
                
                # 3. 测试视频脚本生成
                video_script, audio_script = service.generate_video_script(narration)
                print(f"视频脚本: {video_script[:100]}...")
                print(f"音频脚本: {audio_script[:100]}...")
                self.assertIsInstance(video_script, str)
                self.assertIsInstance(audio_script, str)
                
                # 4. 测试文案生成
                ad_copy = service.generate_ad_copy(self.test_book_info, self.test_target_audience)
                print(f"广告文案: {ad_copy}")
                self.assertIsInstance(ad_copy, str)
                self.assertTrue(len(ad_copy) > 0)
                
            except Exception as e:
                self.fail(f"{service_name} 服务测试失败: {str(e)}")

def run_tests():
    """运行测试"""
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == "__main__":
    run_tests() 
"""
测试点提取 Skill
从需求描述中提取测试点
"""
from typing import Dict, Any
from langchain.chains.llm import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from skills.base_skill import BaseSkill
from utils import load_prompt_template


class TestPointExtractionSkill(BaseSkill):
    """测试点提取 Skill"""
    
    def __init__(self):
        super().__init__(
            name="test_point_extraction",
            description="从需求描述中提取测试点"
        )
        self.prompt_path = "prompts/generate_test_points.md"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行测试点提取
        
        Args:
            **kwargs: 必须包含 'requirement' 参数
            
        Returns:
            dict: 包含 'test_points' 的结果字典
            
        Raises:
            ValueError: 缺少必要参数
            Exception: 执行过程中的错误
        """
        # 获取需求描述
        requirement = kwargs.get('requirement')
        if not requirement:
            raise ValueError("缺少必要参数: requirement")
        
        try:
            # 加载 Prompt 模板
            prompt_text = load_prompt_template(self.prompt_path)
            
            # 创建 Prompt Template
            prompt_template = PromptTemplate(
                input_variables=["requirement"],
                template=prompt_text,
            )
            
            # 创建 LLM
            llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
            
            # 创建 Chain
            chain = LLMChain(llm=llm, prompt=prompt_template)
            
            # 执行
            test_points = chain.run(requirement=requirement)
            
            print(f"📋 提取的测试点:\n{test_points}\n")
            
            return {
                "test_points": test_points,
                "success": True
            }
            
        except Exception as e:
            raise Exception(f"测试点提取失败: {str(e)}")

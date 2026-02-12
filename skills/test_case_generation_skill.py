"""
测试用例生成 Skill
根据测试点生成结构化测试用例
"""
from typing import Dict, Any
from langchain.chains.llm import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from skills.base_skill import BaseSkill
from utils import load_prompt_template


class TestCaseGenerationSkill(BaseSkill):
    """测试用例生成 Skill"""
    
    def __init__(self):
        super().__init__(
            name="test_case_generation",
            description="根据测试点生成结构化测试用例"
        )
        self.prompt_path = "prompts/generate_test_cases.md"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行测试用例生成
        
        Args:
            **kwargs: 必须包含 'requirement' 和 'test_points' 参数
            
        Returns:
            dict: 包含 'test_cases_json' 的结果字典
            
        Raises:
            ValueError: 缺少必要参数
            Exception: 执行过程中的错误
        """
        # 获取参数
        requirement = kwargs.get('requirement')
        test_points = kwargs.get('test_points')
        
        if not requirement:
            raise ValueError("缺少必要参数: requirement")
        if not test_points:
            raise ValueError("缺少必要参数: test_points")
        
        try:
            # 加载 Prompt 模板
            prompt_text = load_prompt_template(self.prompt_path)
            
            # 创建 Prompt Template
            prompt_template = PromptTemplate(
                input_variables=["requirement", "test_points"],
                template=prompt_text,
            )
            
            # 创建 LLM
            llm = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo")
            
            # 创建 Chain
            chain = LLMChain(llm=llm, prompt=prompt_template)
            
            # 执行
            test_cases_json = chain.run({
                "requirement": requirement,
                "test_points": test_points
            })
            
            print(f"📄 生成的测试用例 JSON:\n{test_cases_json[:500]}...\n")
            
            # 如果配置了 MCP 客户端，可以进行验证
            if self.mcp_client:
                try:
                    validation_result = self.mcp_client.call_tool(
                        "testcase_validator",
                        {"test_case_json": test_cases_json}
                    )
                    if validation_result.get("valid"):
                        print(f"✅ 测试用例验证通过: {validation_result.get('message')}")
                    else:
                        print(f"⚠️  测试用例验证警告: {validation_result.get('errors')}")
                except Exception as e:
                    print(f"⚠️  验证失败: {str(e)}")
            
            return {
                "test_cases_json": test_cases_json,
                "success": True
            }
            
        except Exception as e:
            raise Exception(f"测试用例生成失败: {str(e)}")

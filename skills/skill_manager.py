"""
Skill 管理器
负责管理和编排所有 Skills
"""
from typing import Dict, List, Any
from skills.base_skill import BaseSkill


class SkillManager:
    """管理和编排所有 Skills"""
    
    def __init__(self, mcp_client=None):
        """
        初始化 Skill Manager
        
        Args:
            mcp_client: MCP 客户端实例（可选）
        """
        self.skills: Dict[str, BaseSkill] = {}
        self.mcp_client = mcp_client
    
    def register_skill(self, skill: BaseSkill):
        """
        注册 Skill
        
        Args:
            skill: BaseSkill 实例
        """
        # 设置 MCP 客户端
        if self.mcp_client:
            skill.set_mcp_client(self.mcp_client)
        
        # 注册到管理器
        self.skills[skill.name] = skill
        print(f"✅ 注册 Skill: {skill.name}")
    
    def get_skill(self, name: str) -> BaseSkill:
        """
        获取 Skill
        
        Args:
            name: Skill 名称
            
        Returns:
            BaseSkill: Skill 实例
            
        Raises:
            KeyError: Skill 不存在
        """
        if name not in self.skills:
            raise KeyError(f"Skill '{name}' 未注册")
        return self.skills[name]
    
    def execute_workflow(self, workflow: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行 Skill 工作流
        
        Args:
            workflow: Skill 名称列表，定义执行顺序
            context: 初始上下文字典，包含执行所需的参数
            
        Returns:
            dict: 包含所有 Skill 执行结果的字典
            
        Raises:
            KeyError: Skill 不存在
            Exception: Skill 执行失败
        """
        results = {}
        
        print(f"\n🚀 开始执行工作流，共 {len(workflow)} 个步骤")
        print(f"工作流: {' -> '.join(workflow)}\n")
        
        for idx, skill_name in enumerate(workflow, 1):
            print(f"[{idx}/{len(workflow)}] 执行 Skill: {skill_name}")
            
            skill = self.get_skill(skill_name)
            
            try:
                # 执行 Skill
                result = skill.execute(**context)
                
                # 更新上下文（下一个 Skill 可以使用前一个的结果）
                context.update(result)
                
                # 保存结果
                results[skill_name] = result
                
                print(f"✅ {skill_name} 执行成功\n")
                
            except Exception as e:
                error_msg = f"❌ {skill_name} 执行失败: {str(e)}"
                print(error_msg)
                results[skill_name] = {"success": False, "error": str(e)}
                raise Exception(error_msg)
        
        print("🎉 工作流执行完成！\n")
        return results
    
    def list_skills(self) -> List[str]:
        """
        列出所有已注册的 Skills
        
        Returns:
            list: Skill 名称列表
        """
        return list(self.skills.keys())
    
    def __str__(self) -> str:
        return f"SkillManager(skills={self.list_skills()})"
    
    def __repr__(self) -> str:
        return self.__str__()

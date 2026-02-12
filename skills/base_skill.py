"""
Skills 基类
所有 Skill 的抽象基类
"""
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseSkill(ABC):
    """Skills 基类"""
    
    def __init__(self, name: str, description: str):
        """
        初始化 Skill
        
        Args:
            name: Skill 名称
            description: Skill 描述
        """
        self.name = name
        self.description = description
        self.mcp_client = None
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行 Skill 的核心逻辑
        
        Args:
            **kwargs: 执行所需的参数
            
        Returns:
            dict: 执行结果
        """
        pass
    
    def set_mcp_client(self, client):
        """
        设置 MCP 客户端
        
        Args:
            client: MCP 客户端实例
        """
        self.mcp_client = client
    
    def __str__(self) -> str:
        return f"Skill({self.name}): {self.description}"
    
    def __repr__(self) -> str:
        return self.__str__()

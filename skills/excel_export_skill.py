"""
Excel 导出 Skill
将测试用例导出为 Excel 文件
"""
from typing import Dict, Any

from skills.base_skill import BaseSkill


class ExcelExportSkill(BaseSkill):
    """Excel 导出 Skill"""
    
    def __init__(self):
        super().__init__(
            name="excel_export",
            description="将测试用例导出为 Excel 文件"
        )
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行 Excel 导出
        
        Args:
            **kwargs: 必须包含 'test_cases_json' 和 'filename' 参数
            
        Returns:
            dict: 包含导出结果的字典
            
        Raises:
            ValueError: 缺少必要参数或 MCP 客户端未配置
            Exception: 执行过程中的错误
        """
        # 获取参数
        test_cases_json = kwargs.get('test_cases_json')
        filename = kwargs.get('filename', 'test_cases.xlsx')
        
        if not test_cases_json:
            raise ValueError("缺少必要参数: test_cases_json")
        
        # 检查 MCP 客户端
        if not self.mcp_client:
            raise ValueError("MCP 客户端未配置，无法导出 Excel")
        
        try:
            # 调用 MCP 的 Excel 导出工具
            result = self.mcp_client.call_tool(
                "excel_exporter",
                {
                    "data": test_cases_json,
                    "filename": filename
                }
            )
            
            if result.get("success"):
                print(f"✅ {result.get('message')}")
                print(f"📊 文件路径: {result.get('filename')}")
            else:
                raise Exception(result.get("error", "导出失败"))
            
            return {
                "export_result": result,
                "filename": filename,
                "success": True
            }
            
        except Exception as e:
            raise Exception(f"Excel 导出失败: {str(e)}")

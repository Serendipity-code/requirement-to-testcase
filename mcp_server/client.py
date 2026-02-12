"""
MCP 客户端实现
用于连接和调用 MCP 服务器工具
"""
import json
import subprocess
import os
from typing import Dict, Any, Optional


class MCPClient:
    """MCP 客户端类"""
    
    def __init__(self, config_path: str = "mcp_config.json"):
        """
        初始化 MCP 客户端
        
        Args:
            config_path: MCP 配置文件路径
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.server_process = None
    
    def _load_config(self) -> Dict[str, Any]:
        """加载 MCP 配置"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"MCP 配置文件不存在: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用 MCP 工具
        
        Args:
            tool_name: 工具名称
            arguments: 工具参数
            
        Returns:
            dict: 工具执行结果
            
        Raises:
            Exception: 调用失败时抛出异常
        """
        try:
            # 直接导入工具模块并调用（简化实现）
            # 在实际 MCP 协议中，这会通过 stdio 与服务器通信
            from mcp_server.tools.file_operations import FileOperations
            from mcp_server.tools.excel_exporter import ExcelExporter
            from mcp_server.tools.testcase_validator import TestCaseValidator
            
            if tool_name == "file_operations":
                file_ops = FileOperations()
                operation = arguments.get("operation")
                path = arguments.get("path")
                
                if operation == "read":
                    content = file_ops.read_file(path)
                    return {"success": True, "content": content}
                elif operation == "write":
                    content = arguments.get("content", "")
                    success = file_ops.write_file(path, content)
                    return {"success": success, "message": "文件写入成功"}
                else:
                    return {"success": False, "error": f"未知操作: {operation}"}
            
            elif tool_name == "excel_exporter":
                exporter = ExcelExporter()
                data = arguments.get("data")
                filename = arguments.get("filename")
                columns = arguments.get("columns")
                
                return exporter.export_to_excel(data, filename, columns)
            
            elif tool_name == "testcase_validator":
                validator = TestCaseValidator()
                test_case_json = arguments.get("test_case_json")
                
                return validator.validate_test_case(test_case_json)
            
            else:
                return {"success": False, "error": f"未知工具: {tool_name}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def close(self):
        """关闭客户端连接"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None

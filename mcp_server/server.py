"""
MCP 服务器实现
提供文件操作、Excel 导出和测试用例验证工具
"""
import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from tools.file_operations import FileOperations
from tools.excel_exporter import ExcelExporter
from tools.testcase_validator import TestCaseValidator


# 创建服务器实例
server = Server("testcase-tools")

# 工具实例
file_ops = FileOperations()
excel_exporter = ExcelExporter()
validator = TestCaseValidator()


@server.list_tools()
async def list_tools() -> list[Tool]:
    """列出所有可用的工具"""
    return [
        Tool(
            name="file_operations",
            description="文件读写操作工具，支持读取和写入文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["read", "write"],
                        "description": "操作类型：read（读取）或 write（写入）"
                    },
                    "path": {
                        "type": "string",
                        "description": "文件路径"
                    },
                    "content": {
                        "type": "string",
                        "description": "写入的内容（仅 write 操作需要）"
                    }
                },
                "required": ["operation", "path"]
            }
        ),
        Tool(
            name="excel_exporter",
            description="将 JSON 格式的测试用例导出为格式化的 Excel 文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "JSON 格式的测试用例数据"
                    },
                    "filename": {
                        "type": "string",
                        "description": "输出的 Excel 文件名"
                    },
                    "columns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "列名列表（可选）"
                    }
                },
                "required": ["data", "filename"]
            }
        ),
        Tool(
            name="testcase_validator",
            description="验证测试用例的格式和完整性，检查必填字段和数据类型",
            inputSchema={
                "type": "object",
                "properties": {
                    "test_case_json": {
                        "type": "string",
                        "description": "JSON 格式的测试用例字符串"
                    }
                },
                "required": ["test_case_json"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """处理工具调用"""
    try:
        if name == "file_operations":
            operation = arguments.get("operation")
            path = arguments.get("path")
            
            if operation == "read":
                content = file_ops.read_file(path)
                result = {"success": True, "content": content}
            elif operation == "write":
                content = arguments.get("content", "")
                success = file_ops.write_file(path, content)
                result = {"success": success, "message": "文件写入成功"}
            else:
                result = {"success": False, "error": f"未知操作: {operation}"}
            
        elif name == "excel_exporter":
            data = arguments.get("data")
            filename = arguments.get("filename")
            columns = arguments.get("columns")
            
            result = excel_exporter.export_to_excel(data, filename, columns)
            
        elif name == "testcase_validator":
            test_case_json = arguments.get("test_case_json")
            result = validator.validate_test_case(test_case_json)
            
        else:
            result = {"success": False, "error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
    except Exception as e:
        error_result = {"success": False, "error": str(e)}
        return [TextContent(type="text", text=json.dumps(error_result, ensure_ascii=False, indent=2))]


async def main():
    """启动 MCP 服务器"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

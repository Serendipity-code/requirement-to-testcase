"""
基于 MCP 和 Skills 架构的智能测试用例生成器
"""
from dotenv import load_dotenv
from skills.skill_manager import SkillManager
from skills.test_point_extraction_skill import TestPointExtractionSkill
from skills.test_case_generation_skill import TestCaseGenerationSkill
from skills.excel_export_skill import ExcelExportSkill
from mcp_server.client import MCPClient

# 加载环境变量
load_dotenv()


def main():
    """主程序入口"""
    print("=" * 60)
    print("🚀 基于 MCP 和 Skills 架构的智能测试用例生成器")
    print("=" * 60)
    
    # 初始化 MCP 客户端
    print("\n📡 初始化 MCP 客户端...")
    mcp_client = MCPClient(config_path="mcp_config.json")
    print("✅ MCP 客户端初始化成功")
    
    # 创建 Skill Manager
    print("\n🎯 创建 Skill Manager...")
    skill_manager = SkillManager(mcp_client)
    
    # 注册 Skills
    print("\n📦 注册 Skills...")
    skill_manager.register_skill(TestPointExtractionSkill())
    skill_manager.register_skill(TestCaseGenerationSkill())
    skill_manager.register_skill(ExcelExportSkill())
    
    # 定义工作流
    workflow = [
        "test_point_extraction",
        "test_case_generation",
        "excel_export"
    ]
    
    # 准备初始上下文
    requirement = "用户可以使用邮箱和密码登录系统，成功后跳转到首页。若邮箱或密码错误，应显示错误信息。"
    context = {
        "requirement": requirement,
        "filename": "test_cases.xlsx"
    }
    
    print(f"\n📝 需求描述:\n{requirement}\n")
    
    try:
        # 执行工作流
        results = skill_manager.execute_workflow(workflow, context)
        
        # 输出结果摘要
        print("=" * 60)
        print("✅ 工作流执行成功！")
        print("=" * 60)
        print(f"\n📊 结果摘要:")
        for skill_name, result in results.items():
            if result.get("success"):
                print(f"  ✅ {skill_name}: 成功")
            else:
                print(f"  ❌ {skill_name}: 失败")
        
        if results.get("excel_export", {}).get("filename"):
            print(f"\n📁 生成的 Excel 文件: {results['excel_export']['filename']}")
        
    except Exception as e:
        print(f"\n❌ 工作流执行失败: {str(e)}")
        raise
    finally:
        # 关闭 MCP 客户端
        mcp_client.close()


if __name__ == "__main__":
    main()

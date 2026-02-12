# 架构设计文档

## 1. 系统概述

本项目基于 **MCP (Model Context Protocol)** 和 **Skills** 架构设计，将测试用例生成流程模块化，提升系统的可扩展性和可维护性。

## 2. 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                         Main Program                        │
│                         (main.py)                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      Skill Manager                          │
│                 (skills/skill_manager.py)                   │
│                                                             │
│  - 注册和管理 Skills                                         │
│  - 编排执行工作流                                            │
│  - 依赖注入（MCP Client）                                    │
└────┬────────────────────┬────────────────────┬──────────────┘
     │                    │                    │
     ▼                    ▼                    ▼
┌─────────────┐  ┌──────────────────┐  ┌────────────────┐
│  Test Point │  │  Test Case       │  │  Excel Export  │
│  Extraction │  │  Generation      │  │  Skill         │
│  Skill      │  │  Skill           │  │                │
└──────┬──────┘  └────────┬─────────┘  └────────┬───────┘
       │                  │                     │
       │ LLM Call         │ LLM Call            │ MCP Call
       ▼                  ▼                     ▼
┌─────────────┐  ┌──────────────────┐  ┌────────────────┐
│   OpenAI    │  │    OpenAI        │  │   MCP Client   │
│   GPT-3.5   │  │    GPT-3.5       │  │                │
└─────────────┘  └──────────────────┘  └────────┬───────┘
                                                 │
                                                 ▼
                                        ┌────────────────┐
                                        │   MCP Server   │
                                        │   (Tools)      │
                                        └────────┬───────┘
                                                 │
                    ┌────────────────────────────┼────────────────────────┐
                    ▼                            ▼                        ▼
            ┌───────────────┐          ┌─────────────────┐      ┌──────────────┐
            │ File          │          │ Excel           │      │ TestCase     │
            │ Operations    │          │ Exporter        │      │ Validator    │
            └───────────────┘          └─────────────────┘      └──────────────┘
```

## 3. 核心组件

### 3.1 MCP (Model Context Protocol)

MCP 是一个标准化的工具调用协议，用于在 AI 应用中封装和调用工具。

#### 3.1.1 MCP Server (`mcp_server/server.py`)

MCP 服务器提供三个核心工具：

**1. file_operations**
- 功能：文件读写操作
- 方法：
  - `read(path)`: 读取文件内容
  - `write(path, content)`: 写入文件内容
- 用途：处理配置文件、Prompt 模板等

**2. excel_exporter**
- 功能：JSON 到 Excel 的转换
- 特性：
  - 自动解析 JSON 格式的测试用例
  - 支持列宽自动调整
  - 美化表格样式（标题加粗、颜色、边框）
  - 自动处理 steps 列表字段
- 输入：测试用例 JSON 字符串
- 输出：格式化的 Excel 文件

**3. testcase_validator**
- 功能：验证测试用例格式
- 检查项：
  - 必填字段：title, steps, expected_result
  - 可选字段：description, precondition, actual_result, pass_fail
  - 数据类型验证
  - 字段完整性检查
- 输出：验证报告（valid, errors, warnings）

#### 3.1.2 MCP Client (`mcp_server/client.py`)

MCP 客户端负责：
- 加载 MCP 配置文件 (`mcp_config.json`)
- 调用 MCP 工具
- 错误处理和重试逻辑
- 连接生命周期管理

#### 3.1.3 MCP Tools (`mcp_server/tools/`)

工具模块采用独立的 Python 类实现：
- `file_operations.py`: FileOperations 类
- `excel_exporter.py`: ExcelExporter 类
- `testcase_validator.py`: TestCaseValidator 类

每个工具都可以独立测试和复用。

### 3.2 Skills 架构

Skills 是业务逻辑的封装单元，每个 Skill 负责一个特定的任务。

#### 3.2.1 BaseSkill (`skills/base_skill.py`)

所有 Skill 的抽象基类，定义了：
- 基本属性：name, description
- MCP 客户端引用
- 抽象方法 `execute(**kwargs)` - 子类必须实现

#### 3.2.2 TestPointExtractionSkill

**功能**: 从需求描述中提取测试点

**实现**:
- 使用 LangChain LLMChain
- 加载 `prompts/generate_test_points.md` 作为 Prompt
- 调用 OpenAI GPT-3.5 模型
- Temperature: 0（确定性输出）

**输入**:
- `requirement`: 需求描述文本

**输出**:
- `test_points`: 测试点列表（字符串格式）

#### 3.2.3 TestCaseGenerationSkill

**功能**: 根据测试点生成结构化测试用例

**实现**:
- 使用 LangChain LLMChain
- 加载 `prompts/generate_test_cases.md` 作为 Prompt
- 调用 OpenAI GPT-3.5 模型
- Temperature: 0.2（允许一定创造性）
- 可选：使用 MCP 的 testcase_validator 验证输出

**输入**:
- `requirement`: 需求描述
- `test_points`: 测试点列表

**输出**:
- `test_cases_json`: JSON 格式的测试用例

#### 3.2.4 ExcelExportSkill

**功能**: 将测试用例导出为 Excel 文件

**实现**:
- 调用 MCP Client 的 excel_exporter 工具
- 完全移除对 PythonREPLTool 的依赖
- 直接使用 MCP 工具进行导出

**输入**:
- `test_cases_json`: JSON 格式的测试用例
- `filename`: 输出文件名（默认: test_cases.xlsx）

**输出**:
- `export_result`: 导出结果信息
- `filename`: 实际输出的文件路径

#### 3.2.5 SkillManager (`skills/skill_manager.py`)

**功能**: 管理和编排 Skills

**核心方法**:
- `register_skill(skill)`: 注册 Skill，并注入 MCP 客户端
- `execute_workflow(workflow, context)`: 按顺序执行 Skill 列表
- `get_skill(name)`: 获取已注册的 Skill
- `list_skills()`: 列出所有 Skill

**工作流执行**:
1. 接收工作流定义（Skill 名称列表）
2. 接收初始上下文（输入参数）
3. 按顺序执行每个 Skill
4. 将前一个 Skill 的输出合并到上下文中
5. 返回所有 Skill 的执行结果

## 4. 工作流引擎

### 4.1 标准工作流

```python
workflow = [
    "test_point_extraction",   # Step 1: 提取测试点
    "test_case_generation",    # Step 2: 生成测试用例
    "excel_export"             # Step 3: 导出 Excel
]
```

### 4.2 上下文传递

```python
# 初始上下文
context = {
    "requirement": "需求描述",
    "filename": "test_cases.xlsx"
}

# Step 1 执行后，context 包含:
# {
#     "requirement": "需求描述",
#     "filename": "test_cases.xlsx",
#     "test_points": "测试点列表",
#     "success": True
# }

# Step 2 执行后，context 包含:
# {
#     "requirement": "需求描述",
#     "filename": "test_cases.xlsx",
#     "test_points": "测试点列表",
#     "test_cases_json": "JSON 测试用例",
#     "success": True
# }

# Step 3 执行后，context 包含所有结果
```

### 4.3 自定义工作流

可以通过修改工作流定义来自定义执行流程：

```python
# 只提取测试点
workflow = ["test_point_extraction"]

# 跳过导出
workflow = ["test_point_extraction", "test_case_generation"]

# 添加验证步骤（未来扩展）
workflow = [
    "test_point_extraction",
    "test_case_generation",
    "test_case_validation",  # 新增
    "excel_export"
]
```

## 5. 数据流

```
需求描述 (requirement)
    │
    ▼
TestPointExtractionSkill
    │
    ├─► Prompt: prompts/generate_test_points.md
    ├─► LLM: OpenAI GPT-3.5 (temperature=0)
    │
    ▼
测试点列表 (test_points)
    │
    ▼
TestCaseGenerationSkill
    │
    ├─► Prompt: prompts/generate_test_cases.md
    ├─► LLM: OpenAI GPT-3.5 (temperature=0.2)
    │
    ▼
测试用例 JSON (test_cases_json)
    │
    ▼
ExcelExportSkill
    │
    ├─► MCP Tool: excel_exporter
    ├─► 解析 JSON
    ├─► 创建 DataFrame
    ├─► 美化格式
    │
    ▼
Excel 文件 (test_cases.xlsx)
```

## 6. 扩展指南

### 6.1 添加新的 MCP 工具

1. 在 `mcp_server/tools/` 创建新的工具类：
```python
# mcp_server/tools/my_tool.py
class MyTool:
    @staticmethod
    def my_method(param: str) -> dict:
        # 实现逻辑
        return {"result": "..."}
```

2. 在 `mcp_server/server.py` 注册工具：
```python
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # ... 现有工具
        Tool(
            name="my_tool",
            description="我的工具描述",
            inputSchema={...}
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Any):
    if name == "my_tool":
        # 调用工具
        from tools.my_tool import MyTool
        result = MyTool.my_method(arguments["param"])
```

3. 在 `mcp_config.json` 添加工具配置：
```json
{
  "mcpServers": {
    "testcase-tools": {
      "tools": ["file_operations", "excel_exporter", "testcase_validator", "my_tool"]
    }
  }
}
```

### 6.2 添加新的 Skill

1. 创建 Skill 类：
```python
# skills/my_skill.py
from skills.base_skill import BaseSkill

class MySkill(BaseSkill):
    def __init__(self):
        super().__init__(
            name="my_skill",
            description="我的 Skill 描述"
        )
    
    def execute(self, **kwargs):
        # 获取输入
        input_data = kwargs.get("input_key")
        
        # 执行逻辑
        result = self._process(input_data)
        
        # 返回结果
        return {
            "output_key": result,
            "success": True
        }
```

2. 在主程序中注册：
```python
from skills.my_skill import MySkill

skill_manager.register_skill(MySkill())
```

3. 添加到工作流：
```python
workflow = [
    "test_point_extraction",
    "test_case_generation",
    "my_skill",  # 新增
    "excel_export"
]
```

### 6.3 自定义 Prompt

修改 `prompts/` 目录下的 Markdown 文件即可：

- `generate_test_points.md`: 控制测试点提取
- `generate_test_cases.md`: 控制测试用例生成
- `export_to_excel.md`: 控制 Excel 导出（已废弃，现由 MCP 工具处理）

## 7. 设计原则

### 7.1 单一职责原则
- 每个 Skill 只负责一个明确的任务
- 每个 MCP 工具只提供一类功能

### 7.2 依赖注入
- SkillManager 将 MCP Client 注入到 Skills
- Skills 不直接创建依赖，而是接收注入

### 7.3 可测试性
- MCP 工具可以独立测试
- Skills 可以通过 Mock MCP Client 测试
- 工作流可以通过 Mock Skills 测试

### 7.4 可扩展性
- 通过添加 MCP 工具扩展系统能力
- 通过添加 Skills 扩展业务流程
- 通过组合工作流实现不同场景

## 8. 与原架构的对比

| 维度 | 原架构 | 新架构 (MCP + Skills) |
|------|--------|---------------------|
| **Excel 导出** | PythonREPLTool + Agent | MCP Excel Exporter 工具 |
| **模块化** | 函数式 | 面向对象 (Skills) |
| **可测试性** | 较低 | 高（独立工具和 Skills） |
| **扩展性** | 需修改主程序 | 注册新 Skill/Tool 即可 |
| **工作流编排** | 硬编码 | SkillManager 动态编排 |
| **错误处理** | 分散 | 集中在 SkillManager |
| **依赖管理** | 全局依赖 | 依赖注入 |

## 9. 性能考虑

- **缓存**: 可在 SkillManager 中添加结果缓存
- **并行**: 未来可支持无依赖的 Skills 并行执行
- **流式**: 可扩展支持流式 LLM 输出

## 10. 安全考虑

- **环境变量**: API Key 从 .env 加载，不硬编码
- **输入验证**: MCP 工具进行参数验证
- **错误处理**: 避免泄露敏感信息
- **文件操作**: 限制文件路径范围（未来可添加）

## 11. 总结

新架构通过 MCP 和 Skills 实现了：
- ✅ 更好的模块化和封装
- ✅ 更高的可测试性和可维护性
- ✅ 更灵活的工作流编排
- ✅ 更容易的功能扩展
- ✅ 移除了对 PythonREPLTool 的依赖，提升了安全性

同时保持了：
- ✅ 与原项目相同的功能
- ✅ 相同的输出格式
- ✅ Prompt 工程的最佳实践

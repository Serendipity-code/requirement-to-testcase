# 基于 MCP 和 Skills 架构的智能测试用例生成器

## 📖 项目简介

本项目是一个基于大语言模型（LLM）、**MCP (Model Context Protocol)** 和 **Skills** 架构的智能测试用例生成系统。它能够自动完成从需求分析到测试用例生成，再到 Excel 文件导出的全流程自动化，极大地提升测试工程师的工作效率。

### 🎯 核心功能

随着 AI 和大模型（LLM）技术的成熟和普及，测试工程师可以利用 AI 生成和优化测试用例，提高测试覆盖率，减少测试设计的重复性工作。本项目实现了以下三个核心流程：

1. **需求分析 → 测试点提取**  
   通过 TestPointExtractionSkill 调用大语言模型（如 GPT-3.5）解析需求语义，自动提取出可测试的功能点、边界条件、异常路径等。

2. **测试点 → 结构化测试用例**  
   结合原始需求与提取的测试点，TestCaseGenerationSkill 生成完整的结构化测试用例，包含标题、前置条件、测试步骤、预期结果等字段。

3. **测试用例 → Excel 文件导出**  
   ExcelExportSkill 通过 MCP 的 ExcelExporter 工具，将 JSON 格式的测试用例导出为格式化的 Excel 文件，便于后续导入测试管理平台。

### ⚡ 新架构优势

- ✅ **模块化设计**：基于 Skills 架构，每个功能独立封装
- ✅ **标准化工具**：MCP 协议统一工具调用接口
- ✅ **灵活编排**：通过 SkillManager 动态编排工作流
- ✅ **易于扩展**：添加新 Skill 或 MCP 工具即可扩展功能
- ✅ **安全可靠**：移除 PythonREPLTool，使用专用的 MCP 工具
- ✅ **可测试性**：各组件可独立测试和验证

## 🏗️ 项目结构

```
requirement-to-testcase/
│
├── main.py                          # 主程序入口（基于 Skills 工作流）
├── mcp_server/                      # MCP 服务器和工具
│   ├── __init__.py
│   ├── server.py                    # MCP 服务器实现
│   ├── client.py                    # MCP 客户端
│   └── tools/                       # MCP 工具实现
│       ├── __init__.py
│       ├── file_operations.py       # 文件读写工具
│       ├── excel_exporter.py        # Excel 导出工具
│       └── testcase_validator.py   # 测试用例验证工具
├── skills/                          # Skills 模块
│   ├── __init__.py
│   ├── base_skill.py                # Skills 基类
│   ├── skill_manager.py             # Skill 管理器
│   ├── test_point_extraction_skill.py      # 测试点提取
│   ├── test_case_generation_skill.py       # 测试用例生成
│   └── excel_export_skill.py               # Excel 导出
├── prompts/                         # Prompt 模板
│   ├── generate_test_points.md      # 测试点提取 Prompt
│   ├── generate_test_cases.md       # 测试用例生成 Prompt
│   └── export_to_excel.md           # Excel 导出 Prompt（已废弃）
├── docs/
│   └── ARCHITECTURE.md              # 架构设计文档
├── utils.py                         # 工具函数
├── requirements.txt                 # 项目依赖
├── mcp_config.json                  # MCP 配置文件
├── .env                             # 环境变量配置（需自行创建）
└── README.md                        # 项目说明文档
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.10 或更高版本
- OpenAI API Key（或其他兼容的 LLM API）

### 2. 安装步骤

#### 2.1 克隆项目

```bash
git clone https://github.com/bridgeshi85/requirement-to-testcase.git
cd requirement-to-testcase
```

#### 2.2 创建虚拟环境

```bash
# Mac/Linux
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

#### 2.3 安装依赖

```bash
pip install -r requirements.txt
```

依赖包括：
- `langchain==0.3.25` - LLM 应用框架
- `openai==1.10.0` - OpenAI API 客户端
- `pandas==2.2.2` - 数据处理和表格操作
- `openpyxl==3.1.2` - Excel 文件支持
- `python-dotenv==1.0.1` - 环境变量管理
- `langchain-experimental==0.3.4` - LangChain 实验性功能
- `mcp>=1.0.0` - MCP 协议支持

#### 2.4 配置 API Key

在项目根目录创建 `.env` 文件，添加以下内容：

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> **注意**：本示例使用 GPT-3.5-turbo 模型，你也可以修改代码切换到其他 LLM 模型。

### 3. 运行项目

```bash
python main.py
```

运行后，程序将：
1. 分析示例需求，提取测试点
2. 基于测试点生成结构化测试用例
3. 自动将测试用例导出为 `test_cases.xlsx` 文件

## 💡 使用说明

### 自定义需求

修改 `main.py` 中的 `requirement` 变量，替换为你自己的需求描述：

```python
requirement = "你的需求描述..."
```

例如：

```python
requirement = """
用户可以在商城中浏览商品列表，选择商品加入购物车。
购物车支持修改商品数量、删除商品。
用户点击结算后跳转到订单确认页面。
"""
```

### 工作流程详解

#### Step 1: 提取测试点

程序会调用 `generate_test_points.md` Prompt，从需求中提取测试点。

**示例输入：**
```
用户可以使用邮箱和密码登录系统，成功后跳转到首页。若邮箱或密码错误，应显示错误信息。
```

**示例输出：**
```
- 使用正确的邮箱和密码登录系统，验证是否成功跳转到首页
- 使用错误的邮箱登录系统，验证是否显示错误信息
- 使用错误的密码登录系统，验证是否显示错误信息
- 使用错误的邮箱和密码登录系统，验证是否显示错误信息
- 使用空邮箱登录系统，验证是否显示错误信息
- 使用空密码登录系统，验证是否显示错误信息
```

#### Step 2: 生成测试用例

基于测试点和原始需求，调用 `generate_test_cases.md` Prompt 生成结构化的 JSON 测试用例。

**测试用例格式：**
```json
[
  {
    "title": "邮箱密码正确时登录成功",
    "description": "验证邮箱和密码输入正确后可登录系统",
    "precondition": "已打开登录页面",
    "steps": [
      "输入正确邮箱地址",
      "输入正确密码",
      "点击登录按钮"
    ],
    "expected_result": "成功跳转到系统首页",
    "actual_result": "待测试",
    "pass_fail": "待测试"
  }
]
```

#### Step 3: 导出 Excel

ExcelExportSkill 通过 MCP 的 ExcelExporter 工具将 JSON 转换为 Excel 文件。

工具会自动：
1. 解析 JSON 格式的测试用例
2. 转换为 pandas DataFrame
3. 美化表格样式（标题加粗、颜色、边框）
4. 自动调整列宽
5. 生成 `test_cases.xlsx` 文件

## 🔧 MCP 架构说明

### 什么是 MCP？

MCP (Model Context Protocol) 是一个标准化的工具调用协议，用于在 AI 应用中封装和调用各种工具。

### MCP 工具

本项目实现了三个 MCP 工具：

#### 1. FileOperations
- **功能**：文件读写操作
- **方法**：
  - `read_file(path)`: 读取文件内容
  - `write_file(path, content)`: 写入文件内容

#### 2. ExcelExporter
- **功能**：将 JSON 数据导出为格式化的 Excel 文件
- **特性**：
  - 自动解析 JSON 格式
  - 支持列宽自动调整
  - 美化表格样式（标题颜色、边框、对齐）
  - 处理复杂字段（如 steps 列表）

#### 3. TestCaseValidator
- **功能**：验证测试用例格式和完整性
- **检查项**：
  - 必填字段：title, steps, expected_result
  - 可选字段：description, precondition, actual_result, pass_fail
  - 数据类型验证

### MCP 配置

MCP 配置文件 `mcp_config.json` 定义了服务器和工具：

```json
{
  "mcpServers": {
    "testcase-tools": {
      "command": "python",
      "args": ["mcp_server/server.py"],
      "tools": [
        "file_operations",
        "excel_exporter",
        "testcase_validator"
      ]
    }
  }
}
```

## 🎯 Skills 架构说明

### 什么是 Skills？

Skills 是业务逻辑的封装单元，每个 Skill 负责一个特定的任务。所有 Skills 继承自 `BaseSkill` 抽象基类。

### 核心 Skills

#### 1. TestPointExtractionSkill
- **功能**：从需求描述中提取测试点
- **输入**：需求描述文本
- **输出**：测试点列表
- **实现**：使用 LangChain + GPT-3.5 + Prompt 模板

#### 2. TestCaseGenerationSkill
- **功能**：根据测试点生成结构化测试用例
- **输入**：需求描述 + 测试点列表
- **输出**：JSON 格式的测试用例
- **实现**：使用 LangChain + GPT-3.5 + Prompt 模板
- **可选**：自动调用 TestCaseValidator 验证输出

#### 3. ExcelExportSkill
- **功能**：将测试用例导出为 Excel
- **输入**：测试用例 JSON
- **输出**：Excel 文件路径
- **实现**：调用 MCP 的 ExcelExporter 工具

### SkillManager

SkillManager 负责管理和编排 Skills：

```python
# 创建 Skill Manager
skill_manager = SkillManager(mcp_client)

# 注册 Skills
skill_manager.register_skill(TestPointExtractionSkill())
skill_manager.register_skill(TestCaseGenerationSkill())
skill_manager.register_skill(ExcelExportSkill())

# 定义工作流
workflow = [
    "test_point_extraction",
    "test_case_generation",
    "excel_export"
]

# 执行工作流
results = skill_manager.execute_workflow(workflow, context)
```

## 🔄 工作流编排

### 标准工作流

```
需求描述
    ↓
TestPointExtractionSkill → 测试点列表
    ↓
TestCaseGenerationSkill → 测试用例 JSON
    ↓
ExcelExportSkill → Excel 文件
```

### 自定义工作流

可以通过修改 `workflow` 列表来自定义执行流程：

```python
# 只提取测试点
workflow = ["test_point_extraction"]

# 跳过 Excel 导出
workflow = ["test_point_extraction", "test_case_generation"]

# 添加自定义 Skill
workflow = [
    "test_point_extraction",
    "test_case_generation",
    "my_custom_skill",  # 自定义
    "excel_export"
]
```

### 上下文传递

工作流中的 Skills 通过 `context` 字典共享数据：

- 初始上下文包含输入参数（如 requirement, filename）
- 每个 Skill 的输出会自动合并到上下文
- 后续 Skill 可以使用前面 Skill 的输出

## 🔧 扩展指南

### 添加新的 MCP 工具

1. 在 `mcp_server/tools/` 创建新的工具类
2. 在 `mcp_server/server.py` 注册工具
3. 更新 `mcp_config.json` 配置

详见 [架构文档](docs/ARCHITECTURE.md#61-添加新的-mcp-工具)

### 添加新的 Skill

1. 创建继承自 `BaseSkill` 的新类
2. 实现 `execute(**kwargs)` 方法
3. 在主程序中注册 Skill
4. 添加到工作流

详见 [架构文档](docs/ARCHITECTURE.md#62-添加新的-skill)

## 🔧 自定义 Prompt

项目中的 Prompt 模板可以根据需要自定义：

1. **`prompts/generate_test_points.md`**  
   控制如何从需求中提取测试点

2. **`prompts/generate_test_cases.md`**  
   控制测试用例的生成格式和质量

修改这些文件可以调整生成结果的风格和结构。

## 📊 输出示例

运行成功后，控制台会显示类似以下内容：

```
============================================================
🚀 基于 MCP 和 Skills 架构的智能测试用例生成器
============================================================

📡 初始化 MCP 客户端...
✅ MCP 客户端初始化成功

🎯 创建 Skill Manager...

📦 注册 Skills...
✅ 注册 Skill: test_point_extraction
✅ 注册 Skill: test_case_generation
✅ 注册 Skill: excel_export

📝 需求描述:
用户可以使用邮箱和密码登录系统，成功后跳转到首页。若邮箱或密码错误，应显示错误信息。

🚀 开始执行工作流，共 3 个步骤
工作流: test_point_extraction -> test_case_generation -> excel_export

[1/3] 执行 Skill: test_point_extraction
📋 提取的测试点:
- 使用正确的邮箱和密码登录系统，验证是否成功跳转到首页
- 使用错误的邮箱登录系统，验证是否显示错误信息
...
✅ test_point_extraction 执行成功

[2/3] 执行 Skill: test_case_generation
📄 生成的测试用例 JSON:
[{"title": "邮箱密码正确时登录成功", ...}]
✅ test_case_generation 执行成功

[3/3] 执行 Skill: excel_export
✅ 成功导出 5 条测试用例到 test_cases.xlsx
📊 文件路径: test_cases.xlsx
✅ excel_export 执行成功

🎉 工作流执行完成！

============================================================
✅ 工作流执行成功！
============================================================

📊 结果摘要:
  ✅ test_point_extraction: 成功
  ✅ test_case_generation: 成功
  ✅ excel_export: 成功

📁 生成的 Excel 文件: test_cases.xlsx
```

生成的 `test_cases.xlsx` 文件可直接用于：
- 测试管理工具（如 Jira、TestRail）导入
- 团队协作和评审
- 测试执行跟踪

## ⚠️ 注意事项

1. **API 调用费用**  
   本项目会调用 OpenAI API，产生一定费用。建议在测试时使用较小的需求文本。

2. **模型选择**  
   默认使用 `gpt-3.5-turbo` 模型。如需更好的效果，可以修改为 `gpt-4` 或其他模型：
   ```python
   llm = ChatOpenAI(temperature=0, model="gpt-4")
   ```

3. **中文支持**  
   所有 Prompt 和示例均使用简体中文，确保生成的测试用例符合中文场景需求。

4. **安全性**  
   不要将 `.env` 文件提交到版本控制系统。已在 `.gitignore` 中排除。

## 🔍 技术栈

- **MCP (Model Context Protocol)**: 标准化的工具调用协议
- **Skills 架构**: 模块化的业务逻辑封装
- **LangChain**: 用于构建 LLM 应用和 Chain
- **OpenAI GPT-3.5**: 核心语言模型
- **Pandas + OpenPyXL**: Excel 文件生成和格式化
- **Python 异步编程**: MCP 服务器的异步实现

## 🎓 适用场景

- 快速需求分析和测试点提取
- 批量测试用例生成
- 测试用例标准化和规范化
- 提升测试团队效率
- 减少重复性测试设计工作

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

本项目遵循 MIT License。

## 📞 联系方式

项目地址：[https://github.com/bridgeshi85/requirement-to-testcase](https://github.com/bridgeshi85/requirement-to-testcase)

---

**让 AI 赋能测试，让测试更智能！** 🚀

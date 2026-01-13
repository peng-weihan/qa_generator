# 调用链选择题生成器

基于函数调用链（推理链）自动生成选择题的工具。

## 目录结构

```
question_generator/
├── README.md                    # 本文件
├── generate_questions_from_chain.py  # 主程序：生成选择题
├── setup_api_config.py          # API配置工具
├── api_config.json              # API密钥配置文件
├── requests_call_chains.json    # 调用链数据（示例）
└── call_chains.txt              # 调用链文本格式（示例）
```

## 快速开始

### 1. 配置 API Key

#### 方法 A：使用交互式配置脚本（推荐）

```bash
cd question_generator
python3 setup_api_config.py
```

#### 方法 B：直接编辑配置文件

编辑 `api_config.json` 文件：

```json
{
  "openai": {
    "api_key": "sk-your-actual-openai-api-key-here",
    "model": "gpt-4"
  },
  "anthropic": {
    "api_key": "sk-ant-your-actual-anthropic-api-key-here",
    "model": "claude-3-opus-20240229"
  }
}
```

### 2. 安装依赖

```bash
# 如果使用 OpenAI
pip install openai

# 如果使用 Anthropic
pip install anthropic
```

### 3. 生成选择题

```bash
# 使用默认设置（调用链ID=1，API类型=openai）
python3 generate_questions_from_chain.py

# 指定调用链ID
python3 generate_questions_from_chain.py 3

# 指定调用链ID和API类型
python3 generate_questions_from_chain.py 1 anthropic
```

## 功能说明

### generate_questions_from_chain.py

主程序，功能包括：
- 从 JSON 文件读取调用链信息
- 提取调用链中所有函数的完整代码和注释
- 调用 LLM API 生成选择题
- 生成包含题目和完整调用链信息的输出文件

**参数：**
- 第1个参数：调用链ID（默认：1）
- 第2个参数：API类型，`openai` 或 `anthropic`（默认：openai）

**输出：**
- 生成的文件：`chain_{chain_id}_question.txt`
- 包含：选择题、正确答案、解析、完整调用链代码

### setup_api_config.py

交互式配置工具，用于设置 API keys。

**使用方法：**
```bash
python3 setup_api_config.py
```

## 配置文件说明

### api_config.json

API 密钥配置文件，格式：

```json
{
  "openai": {
    "api_key": "your-api-key",
    "model": "gpt-4"
  },
  "anthropic": {
    "api_key": "your-api-key",
    "model": "claude-3-opus-20240229"
  }
}
```

**优先级：**
1. 配置文件 (`api_config.json`)
2. 环境变量 (`OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY`)
3. 示例题目（如果都未配置）

## 数据文件格式

### requests_call_chains.json

调用链数据文件，包含：
- `call_chains`: 调用链列表
- `functions`: 函数信息（代码、注释、位置等）

**生成方法：**
使用 `extract_call_chains.py` 脚本从代码库中提取。

## 安全提示

⚠️ **重要**：
- `api_config.json` 包含敏感信息，不要提交到 Git 仓库
- 建议将 `api_config.json` 添加到 `.gitignore`

## 示例输出

生成的文件包含：
1. **选择题**：题目、选项、正确答案、解析
2. **调用链详细信息**：每个函数的完整代码、文档字符串、文件位置

## 故障排除

### 问题：提示"未配置 API Key"

**解决方案：**
1. 运行 `python3 setup_api_config.py` 配置
2. 或直接编辑 `api_config.json` 文件
3. 或设置环境变量：`export OPENAI_API_KEY="your-key"`

### 问题：提示"未安装 openai 库"

**解决方案：**
```bash
pip install openai
# 或
pip install anthropic
```

### 问题：API 调用失败

**检查：**
1. API key 是否正确
2. 网络连接是否正常
3. API 配额是否充足

## 扩展使用

### 使用自己的调用链数据

1. 使用 `extract_call_chains.py` 从代码库提取调用链
2. 将生成的 JSON 文件放到本目录
3. 修改 `generate_questions_from_chain.py` 中的 `json_file` 路径

## 许可证

请参考项目主目录的许可证文件。


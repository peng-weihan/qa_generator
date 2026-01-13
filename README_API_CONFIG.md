# API Key 配置说明

## 配置文件位置

API keys 配置文件位于：`/home/ugproj/raymone/api_config.json`

## 配置方法

### 1. 编辑配置文件

打开 `api_config.json` 文件，将你的 API key 填入：

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

### 2. 使用编辑器直接编辑

```bash
# 使用 nano
nano /home/ugproj/raymone/api_config.json

# 或使用 vim
vim /home/ugproj/raymone/api_config.json
```

### 3. 使用 Python 脚本配置（推荐）

创建一个简单的配置脚本：

```python
import json

config = {
    "openai": {
        "api_key": input("请输入 OpenAI API Key: "),
        "model": "gpt-4"
    },
    "anthropic": {
        "api_key": input("请输入 Anthropic API Key: "),
        "model": "claude-3-opus-20240229"
    }
}

with open("api_config.json", "w") as f:
    json.dump(config, f, indent=2)

print("配置已保存！")
```

## 安全提示

⚠️ **重要**: 
- 不要将 `api_config.json` 提交到 Git 仓库
- 建议将 `api_config.json` 添加到 `.gitignore`
- 配置文件包含敏感信息，请妥善保管

## 优先级

脚本会按以下优先级查找 API key：

1. **配置文件** (`api_config.json`) - 最高优先级
2. **环境变量** (`OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY`)
3. **示例题目** - 如果都未配置，使用示例题目

## 验证配置

运行脚本测试配置是否成功：

```bash
python3 generate_questions_from_chain.py 1 openai
```

如果配置正确，会调用真实的 API 生成题目；如果未配置或配置错误，会使用示例题目并显示警告信息。


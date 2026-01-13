#!/usr/bin/env python3
"""交互式配置 API Keys"""

import json
import os

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, 'api_config.json')

def setup_config():
    """设置 API 配置"""
    print("=" * 60)
    print("API Key 配置工具")
    print("=" * 60)
    print()
    
    # 读取现有配置
    config = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("已找到现有配置文件")
        except:
            print("配置文件格式错误，将创建新配置")
    
    # OpenAI 配置
    print("\n1. OpenAI 配置")
    print("-" * 60)
    openai_key = input("请输入 OpenAI API Key (留空跳过): ").strip()
    if openai_key:
        config["openai"] = {
            "api_key": openai_key,
            "model": input("请输入模型名称 (默认: gpt-4): ").strip() or "gpt-4"
        }
        print("✓ OpenAI 配置已保存")
    elif config.get("openai"):
        print(f"保留现有 OpenAI 配置 (模型: {config['openai'].get('model', 'gpt-4')})")
    
    # Anthropic 配置
    print("\n2. Anthropic 配置")
    print("-" * 60)
    anthropic_key = input("请输入 Anthropic API Key (留空跳过): ").strip()
    if anthropic_key:
        config["anthropic"] = {
            "api_key": anthropic_key,
            "model": input("请输入模型名称 (默认: claude-3-opus-20240229): ").strip() or "claude-3-opus-20240229"
        }
        print("✓ Anthropic 配置已保存")
    elif config.get("anthropic"):
        print(f"保留现有 Anthropic 配置 (模型: {config['anthropic'].get('model', 'claude-3-opus-20240229')})")
    
    # 保存配置
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"\n✓ 配置已保存到: {CONFIG_FILE}")
        print("\n提示: 配置文件包含敏感信息，请不要提交到 Git 仓库")
    except Exception as e:
        print(f"\n✗ 保存配置失败: {e}")

if __name__ == '__main__':
    setup_config()


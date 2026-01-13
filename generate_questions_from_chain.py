#!/usr/bin/env python3
"""基于调用链生成选择题"""

import json
import os
from typing import Dict, List, Optional

# 配置文件路径
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'api_config.json')

# 如果需要使用OpenAI API，取消下面的注释并设置API key
# import openai
# openai.api_key = os.getenv("OPENAI_API_KEY")

def format_chain_with_code(chain: Dict, functions: Dict) -> str:
    """格式化调用链，包含完整代码"""
    lines = []
    lines.append("=" * 80)
    lines.append(f"调用链 ID: {chain['id']}, 长度: {chain['length']}")
    lines.append("=" * 80)
    lines.append("")
    
    for i, link in enumerate(chain['chain'], 1):
        func_name = link['function']
        func_info = functions.get(func_name, {})
        
        lines.append(f"步骤 {i}: {func_name}")
        lines.append(f"文件: {func_info.get('file', link['file'])}")
        lines.append(f"行号: {func_info.get('line', link['line'])}")
        lines.append("-" * 80)
        
        # 添加文档字符串
        if func_info.get('docstring'):
            lines.append("文档说明:")
            lines.append(func_info['docstring'])
            lines.append("")
        
        # 添加完整源代码
        if func_info.get('source'):
            lines.append("完整代码:")
            lines.append(func_info['source'])
        else:
            lines.append("(代码未找到)")
        
        lines.append("")
        lines.append("=" * 80)
        lines.append("")
    
    return "\n".join(lines)


def generate_question_prompt(chain_text: str) -> str:
    """生成用于LLM的提示词"""
    prompt = f"""你是一位经验丰富的编程教育专家。请基于以下函数调用链（推理链）设计一道高质量的多项选择题。

要求：
1. 题目应该考察对调用链执行流程的理解
2. 选项应该具有迷惑性，但只有一个正确答案
3. 题目应该测试对代码逻辑、函数调用顺序、数据流转的理解
4. 题目难度适中，适合有一定编程基础的开发者

函数调用链信息：
{chain_text}

请生成一道选择题，格式如下：

题目：[题目内容]

A. [选项A]
B. [选项B]
C. [选项C]
D. [选项D]

正确答案：[选项字母]
解析：[详细解析为什么这个答案是正确的，以及其他选项为什么错误]
"""
    return prompt


def get_example_question() -> str:
    """返回示例题目"""
    return """题目：在以下调用链中，当 SessionRedirectMixin.rebuild_proxies() 被调用时，代理配置的解析流程是什么？

A. resolve_proxies -> get_environ_proxies -> should_bypass_proxies -> proxy_bypass -> proxy_bypass_registry
B. get_environ_proxies -> resolve_proxies -> proxy_bypass -> should_bypass_proxies -> proxy_bypass_registry
C. resolve_proxies -> proxy_bypass -> get_environ_proxies -> should_bypass_proxies -> proxy_bypass_registry
D. should_bypass_proxies -> resolve_proxies -> get_environ_proxies -> proxy_bypass -> proxy_bypass_registry

正确答案：A
解析：根据调用链的执行顺序，rebuild_proxies() 首先调用 resolve_proxies() 来解析代理配置，然后 resolve_proxies() 调用 get_environ_proxies() 从环境变量获取代理信息，接着 get_environ_proxies() 调用 should_bypass_proxies() 判断是否应该绕过代理，如果需要绕过，则调用 proxy_bypass()，最后 proxy_bypass() 调用 proxy_bypass_registry() 来检查代理绕过注册表。选项B、C、D的顺序都不正确，不符合实际的函数调用顺序。"""


def call_llm_api(prompt: str, api_type: str = "openai") -> str:
    """调用LLM API生成题目"""
    # 这里可以使用OpenAI API或其他LLM API
    # 示例使用OpenAI（需要安装openai库并设置API key）
    
    try:
        # 如果使用OpenAI
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=[
        #         {"role": "system", "content": "你是一位经验丰富的编程教育专家。"},
        #         {"role": "user", "content": prompt}
        #     ],
        #     temperature=0.7
        # )
        # return response.choices[0].message.content
        
        # 临时返回示例（实际使用时需要替换为真实的API调用）
        return """题目：在以下调用链中，当 Session.send() 被调用时，代理配置的解析流程是什么？

A. resolve_proxies -> get_environ_proxies -> should_bypass_proxies -> proxy_bypass -> proxy_bypass_registry
B. get_environ_proxies -> resolve_proxies -> proxy_bypass -> should_bypass_proxies -> proxy_bypass_registry
C. resolve_proxies -> proxy_bypass -> get_environ_proxies -> should_bypass_proxies -> proxy_bypass_registry
D. should_bypass_proxies -> resolve_proxies -> get_environ_proxies -> proxy_bypass -> proxy_bypass_registry

正确答案：A
解析：根据调用链的执行顺序，Session.send() 首先调用 resolve_proxies() 来解析代理配置，然后 resolve_proxies() 调用 get_environ_proxies() 从环境变量获取代理信息，接着 get_environ_proxies() 调用 should_bypass_proxies() 判断是否应该绕过代理，如果需要绕过，则调用 proxy_bypass()，最后 proxy_bypass() 调用 proxy_bypass_registry() 来检查代理绕过注册表。选项B、C、D的顺序都不正确，不符合实际的函数调用顺序。"""
    except Exception as e:
        return f"调用LLM API时出错: {e}\n\n提示：请配置LLM API（如OpenAI）或使用其他LLM服务。"


def generate_question_from_chain(json_file: str, chain_id: int = 1, output_file: Optional[str] = None, api_type: str = "openai"):
    """从指定调用链生成选择题"""
    
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 找到指定的调用链
    chain = None
    for c in data['call_chains']:
        if c['id'] == chain_id:
            chain = c
            break
    
    if not chain:
        print(f"未找到ID为 {chain_id} 的调用链")
        return
    
    print(f"正在处理调用链 ID: {chain_id}, 长度: {chain['length']}")
    
    # 格式化调用链（包含完整代码）
    chain_text = format_chain_with_code(chain, data['functions'])
    
    # 生成提示词
    prompt = generate_question_prompt(chain_text)
    
    # 调用LLM生成题目
    print(f"正在调用LLM生成题目 (API类型: {api_type})...")
    question = call_llm_api(prompt, api_type=api_type)
    
    # 输出结果
    output = []
    output.append("=" * 80)
    output.append("基于调用链生成的选择题")
    output.append("=" * 80)
    output.append("")
    output.append(question)
    output.append("")
    output.append("=" * 80)
    output.append("")
    output.append("调用链详细信息:")
    output.append("")
    output.append(chain_text)
    
    result = "\n".join(output)
    
    # 保存到文件
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"结果已保存到: {output_file}")
    else:
        print(result)
    
    return result


if __name__ == '__main__':
    import sys
    
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, 'requests_call_chains.json')
    chain_id = 1  # 默认使用第一条调用链
    api_type = "openai"  # 默认使用OpenAI API
    
    if len(sys.argv) > 1:
        chain_id = int(sys.argv[1])
    if len(sys.argv) > 2:
        api_type = sys.argv[2]  # openai 或 anthropic
    
    output_file = os.path.join(script_dir, f'chain_{chain_id}_question.txt')
    
    print(f"使用调用链 ID: {chain_id}")
    print(f"API 类型: {api_type}")
    print()
    
    generate_question_from_chain(json_file, chain_id, output_file, api_type=api_type)


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/3/7 14:06
# @Author  : Tang
# @Software: PyCharm
# @Desc    :
import pandas as pd

def parse_excel_to_prompt(file_path):
    # 读取 Excel 文件
    df = pd.read_excel(file_path)

    # 假设 Excel 有两列："问题" 和 "答案"
    if not {"ID", "标题"}.issubset(df.columns):
        raise ValueError("Excel 文件必须包含 'ID' 和 '标题' 列")

    # 生成 Prompt 格式
    prompt_parts = [f"Q: {row['ID']}\nA: {row['标题']}" for _, row in df.iterrows()]
    prompt = "\n\n".join(prompt_parts)

    return prompt

# 示例调用
file_path = "D:\python\example.xlsx"  # 替换为你的 Excel 文件路径
formatted_prompt = parse_excel_to_prompt(file_path)
print(formatted_prompt)

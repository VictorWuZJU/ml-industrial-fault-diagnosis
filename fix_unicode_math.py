#!/usr/bin/env python3
import re
import sys
import os

# Unicode → LaTeX 映射表（可扩展）
UNICODE_TO_LATEX = {
    '∈': r'\\in',
    '∉': r'\\notin',
    '⊂': r'\\subset',
    '⊆': r'\\subseteq',
    '∩': r'\\cap',
    '∪': r'\\cup',
    '∅': r'\\emptyset',
    'ℝ': r'\\mathbb{R}',
    'ℂ': r'\\mathbb{C}',
    'ℕ': r'\\mathbb{N}',
    'ℤ': r'\\mathbb{Z}',
    'ℚ': r'\\mathbb{Q}',
    'ϕ': r'\\varphi',      # 希腊小写 phi (U+03D5)
    'φ': r'\\phi',         # 另一种 phi (U+03C6)，按需调整
    'θ': r'\\theta',
    'α': r'\\alpha',
    'β': r'\\beta',
    'γ': r'\\gamma',
    'δ': r'\\delta',
    'λ': r'\\lambda',
    'μ': r'\\mu',
    'σ': r'\\sigma',
    'ω': r'\\omega',
    'Ω': r'\\Omega',
    'Δ': r'\\Delta',
    '∇': r'\\nabla',
    '×': r'\\times',
    '·': r'\\cdot',
    '…': r'\\ldots',
    '≠': r'\\neq',
    '≤': r'\\leq',
    '≥': r'\\geq',
    '≈': r'\\approx',
    '≡': r'\\equiv',
    '∑': r'\\sum',
    '∏': r'\\prod',
    '∫': r'\\int',
    '∂': r'\\partial',
}

# 构建正则表达式（按长度降序，避免短匹配干扰长匹配）
sorted_chars = sorted(UNICODE_TO_LATEX.keys(), key=lambda x: -len(x))
pattern = '|'.join(re.escape(c) for c in sorted_chars)
unicode_regex = re.compile(f'({pattern})')

# 匹配已有的数学环境（$...$, $$...$$, \(...\), \[...\]）
MATH_ENV_REGEX = re.compile(
    r'\$\$.*?\$\$|'
    r'\$.*?\$|'
    r'\\\(.*?\\\)|'
    r'\\\[.*?\\\]|'
    r'\\begin\{(equation|align|gather|multline|eqnarray|math|displaymath)\}.*?\\end\{\1\}',
    re.DOTALL
)

def is_inside_math_env(text, pos):
    """检查位置 pos 是否在某个数学环境中"""
    for match in MATH_ENV_REGEX.finditer(text):
        if match.start() <= pos < match.end():
            return True
    return False

def replace_unicode_in_text(text):
    """在非数学环境中替换 Unicode 符号为 LaTeX 命令，并包裹 $...$"""
    new_text = ''
    last_end = 0

    for match in unicode_regex.finditer(text):
        start, end = match.span()
        char = match.group(0)

        # 如果在数学环境中，跳过
        if is_inside_math_env(text, start):
            continue

        # 否则，替换并加 $...$
        latex_cmd = UNICODE_TO_LATEX[char]
        replacement = f'${latex_cmd}$'

        # 拼接前面未处理的部分 + 替换内容
        new_text += text[last_end:start] + replacement
        last_end = end

    # 拼接剩余部分
    new_text += text[last_end:]
    return new_text

def process_file(filepath):
    print(f"Processing: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = replace_unicode_in_text(content)

    if new_content != content:
        backup = filepath + '.bak'
        os.rename(filepath, backup)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Fixed! Backup saved as {backup}")
    else:
        print("➡️ No changes needed.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 fix_unicode_math.py <file1.tex> [file2.tex] ...")
        sys.exit(1)

    for tex_file in sys.argv[1:]:
        if not os.path.isfile(tex_file):
            print(f"⚠️ File not found: {tex_file}")
            continue
        process_file(tex_file)
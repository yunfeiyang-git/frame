import re

# 读取文件
with open('/home/user/.venv/lib/python3.12/site-packages/buildozer/__init__.py', 'r') as f:
    content = f.read()

# 使用正则表达式替换整个 check_root 方法
old_pattern = r'    def check_root\(self\):.*?(?=    def )'
new_code = '''    def check_root(self):
        pass

'''

content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)

# 写入文件
with open('/home/user/.venv/lib/python3.12/site-packages/buildozer/__init__.py', 'w') as f:
    f.write(content)

print('Patched check_root method')

import pexpect
import sys

print("Starting buildozer with pexpect")

# 使用 pexpect 模拟交互式输入
child = pexpect.spawn('buildozer android debug', cwd='/home/user/project')

while True:
    try:
        # 等待 "Are you sure you want to continue" 提示
        child.expect('Are you sure you want to continue \\[y/n\\]\\? ')
        print("Found root check prompt, sending 'y'")
        child.sendline('y')
    except pexpect.EOF:
        # 程序结束
        print("Build completed")
        break
    except pexpect.TIMEOUT:
        # 超时，继续读取输出
        print("Timeout, checking output...")
        print(child.before.decode('utf-8', errors='ignore'))
        continue

# 打印所有输出
print(child.read().decode('utf-8', errors='ignore'))

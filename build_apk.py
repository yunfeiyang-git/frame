import subprocess
import os
import sys

# Monkey patch input function to auto-answer 'y'
original_input = __builtins__.input

def patched_input(prompt=''):
    if 'Are you sure you want to continue' in prompt:
        print(f"AUTO-ANSWERING: {prompt}y")
        return 'y'
    return original_input(prompt)

__builtins__.input = patched_input

print("Monkey patched input function")

# Run buildozer
subprocess.run(['buildozer', 'android', 'debug'], cwd='/home/user/project')

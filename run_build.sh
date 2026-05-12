#!/bin/bash

echo "=== Patching buildozer ==="
python3 /home/user/project/patch_buildozer.py

echo "=== Running buildozer ==="
buildozer android debug

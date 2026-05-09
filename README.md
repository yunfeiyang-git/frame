# 幻灯片播放器 - Android应用

适用于华为平板的幻灯片播放应用，支持多种切换效果和定时功能。

## 功能特性

- 从相册文件夹加载图片进行幻灯片播放
- 自定义播放间隔时间（1-60秒）
- 多种切换效果：淡入淡出、滑动、缩放、随机
- 定时启动和关闭功能
- 支持横屏和竖屏

## 项目结构

```
幻灯片播放器/
├── main.py           # 主程序代码
├── buildozer.spec    # APK打包配置
├── requirements.txt  # Python依赖
└── README.md         # 使用说明
```

## 开发环境搭建

### 方法一：Windows桌面测试

1. **安装Python 3.8+**
   - 下载：https://www.python.org/downloads/
   - 安装时勾选 "Add Python to PATH"

2. **安装Kivy**
   ```bash
   pip install kivy
   ```

3. **运行测试**
   ```bash
   cd 幻灯片播放器
   python main.py
   ```

### 方法二：打包APK（需要Linux环境）

由于Buildozer只支持Linux，推荐使用以下方式：

#### 选项1：使用WSL (Windows Subsystem for Linux)

1. **启用WSL**
   ```powershell
   # 在PowerShell管理员模式下运行
   wsl --install -d Ubuntu
   ```

2. **安装依赖**
   ```bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev automake
   ```

3. **安装Buildozer**
   ```bash
   pip3 install buildozer
   ```

4. **打包APK**
   ```bash
   cd 幻灯片播放器
   buildozer init  # 如果没有buildozer.spec
   buildozer -v android debug
   ```

#### 选项2：使用GitHub Actions（推荐，最简单）

1. **创建GitHub仓库**
   - 在GitHub上创建新仓库
   - 上传项目文件

2. **创建 `.github/workflows/build.yml`**
   ```yaml
   name: Build APK
   
   on:
     push:
       branches: [ main ]
   
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.9'
         
         - name: Install Buildozer
           run: pip install buildozer
         
         - name: Build APK
           run: |
             cd 幻灯片播放器
             buildozer -v android debug
         
         - name: Upload APK
           uses: actions/upload-artifact@v3
           with:
             name: app-debug
             path: 幻灯片播放器/bin/*.apk
   ```

3. **推送代码后自动构建**
   - GitHub Actions会自动构建APK
   - 在Actions页面下载构建好的APK

#### 选项3：使用在线服务

- **Google Colab**：可以在Colab中运行Buildozer
- **Docker**：使用kivy/buildozer Docker镜像

## 使用说明

### 基本操作

1. **选择图片文件夹**
   - 点击"设置"按钮
   - 点击"选择图片文件夹"
   - 输入或选择包含图片的文件夹路径

2. **设置播放间隔**
   - 在设置界面拖动滑块调整间隔时间
   - 支持1-60秒

3. **选择切换效果**
   - 淡入淡出：图片逐渐切换
   - 向左滑动：图片从右向左滑入
   - 向右滑动：图片从左向右滑入
   - 缩放：图片缩小消失后新图片放大出现
   - 随机：随机使用以上效果

4. **定时功能**
   - 点击"设置启动时间"设置自动开始播放的时间
   - 点击"设置关闭时间"设置自动停止播放的时间

### 播放控制

- **上一张**：显示上一张图片
- **播放/暂停**：开始或暂停自动播放
- **下一张**：显示下一张图片
- **设置**：打开设置界面

## Android权限

应用需要以下权限：
- `READ_EXTERNAL_STORAGE`：读取图片文件
- `WRITE_EXTERNAL_STORAGE`：保存配置

## 支持的图片格式

- JPG/JPEG
- PNG
- BMP
- GIF
- WebP

## 常见问题

### Q: 在Windows上运行报错？
A: 确保已正确安装Kivy：`pip install kivy`

### Q: APK打包失败？
A: 确保在Linux环境下运行Buildozer，或使用GitHub Actions

### Q: 华为平板无法安装？
A: 在设置中允许安装未知来源应用

### Q: 找不到图片？
A: 确保图片文件夹路径正确，Android上通常是 `/storage/emulated/0/DCIM/`

## 技术栈

- **Python 3**：主要编程语言
- **Kivy**：跨平台GUI框架
- **Buildozer**：Android打包工具

## 许可证

MIT License

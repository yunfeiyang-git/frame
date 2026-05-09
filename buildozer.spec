[app]

# 应用名称
title = 幻灯片播放器

# 包名
package.name = slideshowplayer

# 包域名
package.domain = org.example

# 源代码目录
source.dir = .

# 源代码包含的文件类型
source.include_exts = py,png,jpg,kv,atlas,json

# 版本号
version = 1.0.0

# 应用描述
requirements = python3,kivy

# 支持的Android版本
android.minapi = 21

# 支持的Android架构
android.archs = arm64-v8a,armeabi-v7a

# 权限
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# 屏幕方向 (landscape横向, portrait纵向, all自动)
orientation = all

# 全屏模式
fullscreen = 0

# 应用类别
android.api = 31

# Android NDK版本
android.ndk = 25b

# 是否允许备份
android.allow_backup = True

# 主题
android.theme = "@android:style/Theme.Translucent.NoTitleBar"

[buildozer]

# 日志级别 (0-2)
log_level = 2

# 显示警告
show_warnings = True

# 构建目录
build_dir = ./build

# 输出目录
bin_dir = ./bin

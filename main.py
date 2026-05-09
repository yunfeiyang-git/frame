#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
幻灯片播放器 - Android应用
适用于华为平板

功能:
1. 从相册选择图片进行幻灯片播放
2. 设置播放间隔时间
3. 多种切换效果(淡入淡出、滑动、缩放、随机)
4. 定时启动和关闭

使用方法:
1. 安装依赖: pip install kivy
2. 运行: python main.py
3. 打包APK: 使用buildozer
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition, SwapTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle

import os
import random
from datetime import datetime, timedelta
import json

# 导入TextInput用于桌面版
from kivy.uix.textinput import TextInput

# 尝试导入Android特定模块
try:
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
    ANDROID_MODE = True
except ImportError:
    ANDROID_MODE = False
    print("非Android模式运行")


class SlideshowScreen(Screen):
    """幻灯片播放界面"""
    
    current_index = NumericProperty(0)
    is_playing = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.images = []
        self.interval = 5.0
        self.transition_type = 'fade'
        self.schedule_event = None
        self.build_ui()
    
    def build_ui(self):
        """构建用户界面"""
        # 主布局
        self.layout = BoxLayout(orientation='vertical')
        
        # 图片显示区域
        self.image_widget = Image(
            source='',
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 0.9)
        )
        self.layout.add_widget(self.image_widget)
        
        # 控制按钮区域
        controls = BoxLayout(size_hint=(1, 0.1), spacing=dp(5), padding=dp(5))
        
        self.btn_prev = Button(text='上一张', font_size='18sp')
        self.btn_prev.bind(on_press=self.prev_image)
        controls.add_widget(self.btn_prev)
        
        self.btn_play = Button(text='播放', font_size='18sp')
        self.btn_play.bind(on_press=self.toggle_play)
        controls.add_widget(self.btn_play)
        
        self.btn_next = Button(text='下一张', font_size='18sp')
        self.btn_next.bind(on_press=self.next_image)
        controls.add_widget(self.btn_next)
        
        self.btn_settings = Button(text='设置', font_size='18sp')
        self.btn_settings.bind(on_press=self.open_settings)
        controls.add_widget(self.btn_settings)
        
        self.layout.add_widget(controls)
        self.add_widget(self.layout)
    
    def load_images(self, folder_path):
        """从文件夹加载图片"""
        self.images = []
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')
        
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(supported_formats):
                    self.images.append(os.path.join(folder_path, filename))
        
        self.images.sort()
        
        if self.images:
            self.current_index = 0
            self.show_image()
        
        return len(self.images)
    
    def show_image(self, *args):
        """显示当前图片"""
        if self.images and 0 <= self.current_index < len(self.images):
            self.image_widget.source = self.images[self.current_index]
    
    def next_image(self, *args):
        """显示下一张图片"""
        if self.images:
            self.current_index = (self.current_index + 1) % len(self.images)
            self.apply_transition()
    
    def prev_image(self, *args):
        """显示上一张图片"""
        if self.images:
            self.current_index = (self.current_index - 1) % len(self.images)
            self.apply_transition()
    
    def apply_transition(self):
        """应用切换效果"""
        if self.transition_type == 'random':
            transition_type = random.choice(['fade', 'slide_left', 'slide_right', 'zoom'])
        else:
            transition_type = self.transition_type
        
        if transition_type == 'fade':
            self.fade_transition()
        elif transition_type == 'slide_left':
            self.slide_transition('left')
        elif transition_type == 'slide_right':
            self.slide_transition('right')
        elif transition_type == 'zoom':
            self.zoom_transition()
        else:
            self.show_image()
    
    def fade_transition(self):
        """淡入淡出效果"""
        anim = Animation(opacity=0, duration=0.3)
        anim.bind(on_complete=lambda *args: self._fade_in())
        anim.start(self.image_widget)
    
    def _fade_in(self):
        """淡入"""
        self.show_image()
        anim = Animation(opacity=1, duration=0.3)
        anim.start(self.image_widget)
    
    def slide_transition(self, direction='left'):
        """滑动切换效果"""
        width = self.image_widget.width
        if direction == 'left':
            anim = Animation(x=-width, duration=0.3)
            anim.bind(on_complete=lambda *args: self._slide_in(width))
        else:
            anim = Animation(x=width * 2, duration=0.3)
            anim.bind(on_complete=lambda *args: self._slide_in(-width))
        anim.start(self.image_widget)
    
    def _slide_in(self, offset):
        """滑入"""
        self.show_image()
        self.image_widget.x = self.x - offset
        anim = Animation(x=self.x, duration=0.3)
        anim.start(self.image_widget)
    
    def zoom_transition(self):
        """缩放切换效果"""
        anim = Animation(size=(0, 0), opacity=0, duration=0.3)
        anim.bind(on_complete=lambda *args: self._zoom_in())
        anim.start(self.image_widget)
    
    def _zoom_in(self):
        """放大显示"""
        self.show_image()
        self.image_widget.size = (0, 0)
        self.image_widget.opacity = 0
        anim = Animation(size=self.layout.size, opacity=1, duration=0.3)
        anim.start(self.image_widget)
    
    def toggle_play(self, *args):
        """切换播放/暂停"""
        if self.is_playing:
            self.stop_slideshow()
        else:
            self.start_slideshow()
    
    def start_slideshow(self):
        """开始幻灯片播放"""
        if self.images:
            self.is_playing = True
            self.btn_play.text = '暂停'
            self.schedule_event = Clock.schedule_interval(self.next_image, self.interval)
    
    def stop_slideshow(self):
        """停止幻灯片播放"""
        self.is_playing = False
        self.btn_play.text = '播放'
        if self.schedule_event:
            self.schedule_event.cancel()
            self.schedule_event = None
    
    def set_interval(self, seconds):
        """设置播放间隔"""
        self.interval = seconds
        if self.is_playing:
            self.stop_slideshow()
            self.start_slideshow()
    
    def set_transition(self, transition_type):
        """设置切换效果"""
        self.transition_type = transition_type
    
    def open_settings(self, *args):
        """打开设置界面"""
        app = App.get_running_app()
        app.sm.current = 'settings'


class SettingsScreen(Screen):
    """设置界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """构建设置界面"""
        # 主布局
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # 标题
        title = Label(
            text='幻灯片设置',
            font_size='28sp',
            size_hint=(1, 0.1),
            bold=True
        )
        self.layout.add_widget(title)
        
        # 播放间隔设置
        interval_layout = BoxLayout(size_hint=(1, 0.1), spacing=dp(10))
        interval_layout.add_widget(Label(text='播放间隔(秒):', font_size='18sp', size_hint=(0.4, 1)))
        
        self.interval_slider = Slider(
            min=1, max=60, value=5,
            step=1,
            size_hint=(0.5, 1)
        )
        self.interval_slider.bind(value=self.on_interval_change)
        interval_layout.add_widget(self.interval_slider)
        
        self.interval_label = Label(text='5', font_size='18sp', size_hint=(0.1, 1))
        interval_layout.add_widget(self.interval_label)
        self.layout.add_widget(interval_layout)
        
        # 切换效果设置
        transition_layout = BoxLayout(size_hint=(1, 0.1), spacing=dp(10))
        transition_layout.add_widget(Label(text='切换效果:', font_size='18sp', size_hint=(0.4, 1)))
        
        self.transition_spinner = Spinner(
            text='淡入淡出',
            values=['淡入淡出', '向左滑动', '向右滑动', '缩放', '随机'],
            size_hint=(0.6, 1),
            font_size='18sp'
        )
        self.transition_spinner.bind(text=self.on_transition_change)
        transition_layout.add_widget(self.transition_spinner)
        self.layout.add_widget(transition_layout)
        
        # 定时启动设置
        schedule_layout = BoxLayout(size_hint=(1, 0.15), spacing=dp(10))
        schedule_layout.add_widget(Label(text='定时启动:', font_size='18sp', size_hint=(0.4, 1)))
        
        self.start_time_input = Button(
            text='设置启动时间',
            size_hint=(0.6, 1),
            font_size='16sp'
        )
        self.start_time_input.bind(on_press=self.show_time_picker_start)
        schedule_layout.add_widget(self.start_time_input)
        self.layout.add_widget(schedule_layout)
        
        # 定时关闭设置
        end_layout = BoxLayout(size_hint=(1, 0.15), spacing=dp(10))
        end_layout.add_widget(Label(text='定时关闭:', font_size='18sp', size_hint=(0.4, 1)))
        
        self.end_time_input = Button(
            text='设置关闭时间',
            size_hint=(0.6, 1),
            font_size='16sp'
        )
        self.end_time_input.bind(on_press=self.show_time_picker_end)
        end_layout.add_widget(self.end_time_input)
        self.layout.add_widget(end_layout)
        
        # 选择图片文件夹
        folder_layout = BoxLayout(size_hint=(1, 0.15), spacing=dp(10))
        self.folder_btn = Button(
            text='选择图片文件夹',
            size_hint=(1, 1),
            font_size='18sp'
        )
        self.folder_btn.bind(on_press=self.select_folder)
        folder_layout.add_widget(self.folder_btn)
        self.layout.add_widget(folder_layout)
        
        # 图片数量显示
        self.image_count_label = Label(
            text='已加载: 0 张图片',
            font_size='16sp',
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.image_count_label)
        
        # 返回按钮
        back_btn = Button(
            text='返回播放',
            size_hint=(1, 0.1),
            font_size='20sp',
            background_color=(0.2, 0.6, 1, 1)
        )
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)
        
        self.add_widget(self.layout)
        
        # 定时相关变量
        self.start_time = None
        self.end_time = None
        self.schedule_start_event = None
        self.schedule_end_event = None
    
    def on_interval_change(self, instance, value):
        """间隔时间改变"""
        self.interval_label.text = str(int(value))
        app = App.get_running_app()
        if hasattr(app, 'slideshow_screen'):
            app.slideshow_screen.set_interval(value)
    
    def on_transition_change(self, instance, value):
        """切换效果改变"""
        transition_map = {
            '淡入淡出': 'fade',
            '向左滑动': 'slide_left',
            '向右滑动': 'slide_right',
            '缩放': 'zoom',
            '随机': 'random'
        }
        app = App.get_running_app()
        if hasattr(app, 'slideshow_screen'):
            app.slideshow_screen.set_transition(transition_map.get(value, 'fade'))
    
    def show_time_picker_start(self, *args):
        """显示启动时间选择器"""
        self._show_time_picker('start')
    
    def show_time_picker_end(self, *args):
        """显示关闭时间选择器"""
        self._show_time_picker('end')
    
    def _show_time_picker(self, time_type):
        """显示时间选择弹出框"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # 小时选择
        hour_layout = BoxLayout(size_hint=(1, 0.3))
        hour_layout.add_widget(Label(text='时:', font_size='18sp'))
        hour_spinner = Spinner(
            text='12',
            values=[str(i).zfill(2) for i in range(24)],
            size_hint=(0.5, 1),
            font_size='18sp'
        )
        hour_layout.add_widget(hour_spinner)
        content.add_widget(hour_layout)
        
        # 分钟选择
        minute_layout = BoxLayout(size_hint=(1, 0.3))
        minute_layout.add_widget(Label(text='分:', font_size='18sp'))
        minute_spinner = Spinner(
            text='00',
            values=[str(i).zfill(2) for i in range(60)],
            size_hint=(0.5, 1),
            font_size='18sp'
        )
        minute_layout.add_widget(minute_spinner)
        content.add_widget(minute_layout)
        
        # 确定按钮
        btn_confirm = Button(text='确定', size_hint=(1, 0.4), font_size='18sp')
        content.add_widget(btn_confirm)
        
        popup = Popup(
            title='选择时间',
            content=content,
            size_hint=(0.8, 0.5)
        )
        
        def on_confirm(*args):
            hour = int(hour_spinner.text)
            minute = int(minute_spinner.text)
            time_str = f'{hour:02d}:{minute:02d}'
            
            if time_type == 'start':
                self.start_time = (hour, minute)
                self.start_time_input.text = f'启动时间: {time_str}'
                self.setup_schedule_start()
            else:
                self.end_time = (hour, minute)
                self.end_time_input.text = f'关闭时间: {time_str}'
                self.setup_schedule_end()
            
            popup.dismiss()
        
        btn_confirm.bind(on_press=on_confirm)
        popup.open()
    
    def setup_schedule_start(self):
        """设置定时启动"""
        if self.schedule_start_event:
            Clock.unschedule(self.schedule_start_event)
        
        if self.start_time:
            self.schedule_start_event = Clock.schedule_interval(
                self.check_start_time, 60
            )
    
    def setup_schedule_end(self):
        """设置定时关闭"""
        if self.schedule_end_event:
            Clock.unschedule(self.schedule_end_event)
        
        if self.end_time:
            self.schedule_end_event = Clock.schedule_interval(
                self.check_end_time, 60
            )
    
    def check_start_time(self, *args):
        """检查是否到达启动时间"""
        if self.start_time:
            now = datetime.now()
            if now.hour == self.start_time[0] and now.minute == self.start_time[1]:
                app = App.get_running_app()
                if hasattr(app, 'slideshow_screen'):
                    app.slideshow_screen.start_slideshow()
                    app.sm.current = 'slideshow'
    
    def check_end_time(self, *args):
        """检查是否到达关闭时间"""
        if self.end_time:
            now = datetime.now()
            if now.hour == self.end_time[0] and now.minute == self.end_time[1]:
                app = App.get_running_app()
                if hasattr(app, 'slideshow_screen'):
                    app.slideshow_screen.stop_slideshow()
    
    def select_folder(self, *args):
        """选择图片文件夹"""
        if ANDROID_MODE:
            self.select_folder_android()
        else:
            self.select_folder_desktop()
    
    def select_folder_android(self):
        """Android平台选择文件夹"""
        try:
            storage_path = primary_external_storage_path()
            dcim_path = os.path.join(storage_path, 'DCIM')
            
            if os.path.exists(dcim_path):
                self.load_folder(dcim_path)
            else:
                self.load_folder(storage_path)
        except Exception as e:
            self.show_message(f'错误: {str(e)}')
    
    def select_folder_desktop(self):
        """桌面平台选择文件夹"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # 默认路径输入
        path_input = TextInput(
            text=os.path.expanduser('~/Pictures'),
            multiline=False,
            size_hint=(1, 0.3),
            font_size='16sp'
        )
        content.add_widget(Label(text='输入图片文件夹路径:', font_size='16sp', size_hint=(1, 0.2)))
        content.add_widget(path_input)
        
        # 按钮
        btn_layout = BoxLayout(size_hint=(1, 0.3), spacing=dp(10))
        btn_cancel = Button(text='取消', font_size='16sp')
        btn_confirm = Button(text='确定', font_size='16sp')
        btn_layout.add_widget(btn_cancel)
        btn_layout.add_widget(btn_confirm)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='选择文件夹',
            content=content,
            size_hint=(0.9, 0.4)
        )
        
        def on_confirm(*args):
            path = path_input.text.strip()
            if os.path.exists(path):
                self.load_folder(path)
                popup.dismiss()
            else:
                self.show_message('路径不存在!')
        
        btn_confirm.bind(on_press=on_confirm)
        btn_cancel.bind(on_press=popup.dismiss)
        popup.open()
    
    def load_folder(self, folder_path):
        """加载文件夹中的图片"""
        app = App.get_running_app()
        if hasattr(app, 'slideshow_screen'):
            count = app.slideshow_screen.load_images(folder_path)
            self.image_count_label.text = f'已加载: {count} 张图片'
            self.show_message(f'成功加载 {count} 张图片')
    
    def show_message(self, message):
        """显示消息"""
        popup = Popup(
            title='提示',
            content=Label(text=message, font_size='18sp'),
            size_hint=(0.6, 0.3)
        )
        popup.open()
    
    def go_back(self, *args):
        """返回播放界面"""
        app = App.get_running_app()
        app.sm.current = 'slideshow'


class SlideshowApp(App):
    """主应用"""
    
    def build(self):
        """构建应用"""
        # 设置窗口大小(桌面版)
        if not ANDROID_MODE:
            Window.size = (1024, 768)
        
        # 创建屏幕管理器
        self.sm = ScreenManager(transition=FadeTransition())
        
        # 创建屏幕
        self.slideshow_screen = SlideshowScreen(name='slideshow')
        self.settings_screen = SettingsScreen(name='settings')
        
        # 添加屏幕
        self.sm.add_widget(self.slideshow_screen)
        self.sm.add_widget(self.settings_screen)
        
        return self.sm
    
    def on_start(self):
        """应用启动时"""
        # Android权限请求
        if ANDROID_MODE:
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])


if __name__ == '__main__':
    SlideshowApp().run()

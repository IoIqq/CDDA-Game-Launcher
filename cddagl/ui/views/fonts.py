# SPDX-FileCopyrightText: 2015-2021 Rémy Roy
#
# SPDX-License-Identifier: MIT
import logging
import os
import json

from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QTabWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox, QRadioButton, QGroupBox, QPlainTextEdit, QListView

logger = logging.getLogger('cddagl')

class FontsTab(QTabWidget):
    def __init__(self):
        super(FontsTab, self).__init__()

        # 创建主布局
        main_layout = QGridLayout()

        # 创建QListView来实现字体选择
        font_list_view = QListView()
        font_list_view.setEditTriggers(QListView.NoEditTriggers)
        font_families = self.load_fonts()
        font_model = QStringListModel(font_families)
        font_list_view.setModel(font_model)
        
        # 创建字体设置的GroupBox并添加按钮
        font_settings_groupbox = QGroupBox("字体设置")
        font_buttons_layout = QVBoxLayout()
        set_ui_font_button = QPushButton("设为UI字体")
        set_map_font_button = QPushButton("设为地图字体")
        set_large_map_font_button = QPushButton("设为大地图字体")
        set_all_button = QPushButton("设为全部")
        reset_all_font_button = QPushButton("重置全部字体")
        
        font_buttons_layout.addWidget(font_list_view)
        font_buttons_layout.addWidget(set_ui_font_button)
        font_buttons_layout.addWidget(set_map_font_button)
        font_buttons_layout.addWidget(set_large_map_font_button)
        font_buttons_layout.addWidget(set_all_button)
        font_buttons_layout.addWidget(reset_all_font_button)
        font_settings_groupbox.setLayout(font_buttons_layout)

        # 创建四个标签
        ui_font_label = QLabel("UI字体大小:")
        map_font_label = QLabel("地图字体大小:")
        large_map_font_label = QLabel("大地图字体大小:")
        font_mixture_label = QLabel("字体混合:")

        # 创建三个调节字体大小的SpinBox
        self.ui_font_size_spinbox = QSpinBox()
        self.map_font_size_spinbox = QSpinBox()
        self.large_map_font_size_spinbox = QSpinBox()

        # 初始化字体大小为14
        self.ui_font_size_spinbox.setValue(14)
        self.map_font_size_spinbox.setValue(14)
        self.large_map_font_size_spinbox.setValue(14)

        # 创建RadioButton
        self.font_mixture_radio = QRadioButton("启用")

        # 创建保存按钮
        save_button = QPushButton("保存")

        # 创建预览的GroupBox，并将QPlainTextEdit添加到其中
        preview_groupbox = QGroupBox("预览")
        preview_layout = QVBoxLayout()
        test_text_edit = QPlainTextEdit()
        test_text = """这是一些常见的测试文本。
Hello, World!
1234567890
!@#$%^&*()_+
Это пример текста на кириллице."""
        test_text_edit.setPlainText(test_text)
        test_text_edit.setReadOnly(True)
        test_text_edit.setStyleSheet("background-color: black; color: white;")
        self.test_text_edit = test_text_edit
        preview_layout.addWidget(test_text_edit)
        preview_groupbox.setLayout(preview_layout)

        # 创建目前字体和备用字体的GroupBox，并添加QPlainTextEdit
        current_font_groupbox = QGroupBox("目前字体和备用字体")
        current_font_layout = QVBoxLayout()
        current_font_text_edit = QPlainTextEdit()
        
        current_font_text_edit.setReadOnly(True)
        current_font_layout.addWidget(current_font_text_edit)
        current_font_groupbox.setLayout(current_font_layout)
        self.current_font_text_edit = current_font_text_edit

        # 使用QGridLayout将标签和SpinBox布局在一行
        label_spinbox_layout = QGridLayout()
        label_spinbox_layout.addWidget(ui_font_label, 0, 0)
        label_spinbox_layout.addWidget(self.ui_font_size_spinbox, 0, 1)
        label_spinbox_layout.addWidget(map_font_label, 1, 0)
        label_spinbox_layout.addWidget(self.map_font_size_spinbox, 1, 1)
        label_spinbox_layout.addWidget(large_map_font_label, 2, 0)
        label_spinbox_layout.addWidget(self.large_map_font_size_spinbox, 2, 1)
        label_spinbox_layout.addWidget(font_mixture_label, 3, 0)
        label_spinbox_layout.addWidget(self.font_mixture_radio, 3, 1)

        # 创建其他设置的GroupBox并添加标签和SpinBox的布局
        other_settings_groupbox = QGroupBox("其他设置")
        other_settings_groupbox.setLayout(label_spinbox_layout)

        # 将字体设置的GroupBox添加到主布局
        main_layout.addWidget(font_settings_groupbox, 0, 0)  # 字体设置
        main_layout.addWidget(preview_groupbox, 0, 1)  # 预览
        main_layout.addWidget(other_settings_groupbox, 1, 1)  # 其他设置
        main_layout.addWidget(current_font_groupbox, 1, 0)  # 目前字体和备用字体

        self.setLayout(main_layout)

        # 绑定事件（预留函数）
        set_ui_font_button.clicked.connect(self.set_ui_font)
        set_map_font_button.clicked.connect(self.set_map_font)
        set_large_map_font_button.clicked.connect(self.set_large_map_font)
        set_all_button.clicked.connect(self.set_all_font)
        reset_all_font_button.clicked.connect(self.reset_all_font)
        save_button.clicked.connect(self.save_settings)
        font_list_view.selectionModel().currentChanged.connect(self.font_selected)


        # 初始化字体大小和是否启用的变量
        self.ui_font_size = None
        self.map_font_size = None
        self.large_map_font_size = None
        self.font_mixture_enabled = False
        self.selected_font = None
        self.game_dir = None
        self.load_font_settings()

    def load_font_settings(self):
        # 从fontsjson中加载字体设置
        self.fontsjson = {
            "typeface": ["userdata/font/Terminus.ttf", "userdata/font/unifont.ttf"],
            "map_typeface": ["userdata/font/Terminus.ttf", "userdata/font/unifont.ttf"],
            "over_map_typeface": ["userdata/font/Terminus.ttf", "userdata/font/unifont.ttf"]
        }

        # 更新current_font_text_edit的文本
        self.update_current_font_text_edit()

    def update_current_font_text_edit(self):
        typeface = self.fontsjson.get("typeface", [])
        map_typeface = self.fontsjson.get("map_typeface", [])
        over_map_typeface = self.fontsjson.get("over_map_typeface", [])

        current_font_text = f"""UI： {typeface[0]} => {typeface[1] if len(typeface) > 1 else ''}
地图： {map_typeface[0]} => {map_typeface[1] if len(map_typeface) > 1 else ''}
大地图： {over_map_typeface[0]} => {over_map_typeface[1] if len(over_map_typeface) > 1 else ''}
"""
        self.current_font_text_edit.setPlainText(current_font_text)
        
    def load_fonts(self):
        # 加载可用字体并返回字体列表
        font_database = QFontDatabase()
        font_families = font_database.families(QFontDatabase.Latin)
        return font_families

    def set_ui_font(self):
        logger.debug("触发设为UI字体事件")
        print(self.game_dir)
        if self.selected_font is not None:
            # 更新fontsjson的UI字体部分
            self.fontsjson["typeface"][0] = self.selected_font
            write_fontsjson_to_path(self.fontsjson)
            copy_font_to_directory_by_name(self.selected_font)
            self.update_current_font_text_edit()

    def set_map_font(self):
        logger.debug("触发设为地图字体事件")
        if self.selected_font is not None:
            # 更新fontsjson的地图字体部分
            self.fontsjson["map_typeface"][0] = self.selected_font
            write_fontsjson_to_path(self.fontsjson)
            copy_font_to_directory_by_name(self.selected_font)
            self.update_current_font_text_edit()

    def set_large_map_font(self):
        logger.debug("触发设为大地图字体事件")
        if self.selected_font is not None:
            # 更新fontsjson的大地图字体部分
            self.fontsjson["over_map_typeface"][0] = self.selected_font
            write_fontsjson_to_path(self.fontsjson)
            copy_font_to_directory_by_name(self.selected_font)
            self.update_current_font_text_edit()

    def set_all_font(self):
        logger.debug("触发设为全部字体事件")
        if self.selected_font is not None:
            selected_font = self.selected_font

            # 更新字体设置字典中的所有字体
            self.fontsjson["typeface"] = [selected_font, selected_font]
            self.fontsjson["map_typeface"] = [selected_font, selected_font]
            self.fontsjson["over_map_typeface"] = [selected_font, selected_font]
            write_fontsjson_to_path(self.fontsjson)
            copy_font_to_directory_by_name(self.selected_font)
            # 更新UI界面
            self.update_current_font_text_edit()

    def reset_all_font(self):
        logger.debug("触发重置全部字体事件")
        # 实现重置全部字体的操作
        self.load_font_settings()

    def save_settings(self):
        logger.debug("触发保存设置事件")
        # 将字体大小和是否启用的变量存储在这里
        self.ui_font_size = self.ui_font_size_spinbox.value()
        self.map_font_size = self.map_font_size_spinbox.value()
        self.large_map_font_size = self.large_map_font_size_spinbox.value()
        self.font_mixture_enabled = self.font_mixture_radio.isChecked()

    def font_selected(self, index):
        # 处理字体选择变化事件
        self.selected_font = index.data()
        logger.debug(f"选择了字体：{self.selected_font}")

        # 设置test_text_edit的字体
        font = QFont(self.selected_font, 14)
        font_style = f'font-family: "{self.selected_font}"; font-size: 14px;background-color: black; color: white;'
        self.test_text_edit.setStyleSheet(font_style)
        self.test_text_edit.setFont(font)
        pass

    def game_dir_changed(self, new_dir):
        # todo
        # 设置游戏目录为新的目录
        self.game_dir = new_dir
        # 清空现有的模组列表

        # 构建游戏的模组目录和用户模组目录的路径
        fonts_dir = os.path.join(new_dir, 'data', 'font')
        user_fonts_dir = os.path.join(new_dir, 'font')

        self.load_fonts()
        
    def get_main_window(self):
        return self.parentWidget().parentWidget().parentWidget()

    def get_main_tab(self):
        return self.parentWidget().parentWidget().main_tab
    



def write_fontsjson_to_path(data, subpath='userdata\config'):
    try:
        # 检查路径是否存在，如果不存在则创建它
        if not os.path.exists(subpath):
            os.makedirs(subpath)

        # 构建JSON文件的完整路径
        json_path = os.path.join(os.getcwd(), subpath, 'fonts.json')

        # 写入JSON数据到文件
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"JSON数据已成功写入到路径: {json_path}")
    except Exception as e:
        print(f"写入JSON数据时出错: {str(e)}")

def copy_font_to_directory_by_name(font_name, subpath='data/fonts', font_size=14):
    target_directory = os.path.join(os.getcwd(), subpath)
    
    # 使用 QFontDatabase 来获取字体文件路径
    font_database = QFontDatabase()
    font_id = font_database.addApplicationFont(QFont(font_name, font_size).toString())
    
    if font_id == -1:
        print(f"无法找到字体文件: {font_name}")
        return

    font_file_paths = font_database.applicationFontPaths(font_id)
    font_file_name = os.path.basename(font_file_paths[0])

    # 检查目标目录是否存在字体文件
    target_font_path = os.path.join(target_directory, font_file_name)
    if os.path.exists(target_font_path):
        print(f"字体 '{font_name}' 已存在于目标目录中.")
        return

    try:
        # 复制字体文件到目标目录
        shutil.copy(font_file_paths[0], target_directory)
        print(f"字体 '{font_name}' 已成功复制到目标目录.")
    except Exception as e:
        print(f"复制字体 '{font_name}' 到目标目录时发生错误: {str(e)}")

def get_windows_fonts_directory():
    # 获取系统文件夹路径
    windir = os.environ.get('WINDIR', 'C:\\Windows')

    # 检查系统位数（32位或64位）
    is_64bit = ctypes.windll.kernel32.IsWow64Process()

    if is_64bit:
        # 64位系统
        fonts_directory = os.path.join(windir, 'SysNative', 'fonts')
    else:
        # 32位系统
        fonts_directory = os.path.join(windir, 'fonts')

    return fonts_directory



# class CataWindow(QWidget):
#     def __init__(self, terminalwidth, terminalheight, font, fontsize, fontwidth,
#             fontheight, fontblending):
#         super(CataWindow, self).__init__()
# 
    #     self.terminalwidth = terminalwidth
    #     self.terminalheight = terminalheight

    #     self.cfont = font
    #     self.fontsize = fontsize
    #     self.cfont.setPixelSize(fontsize)
    #     self.cfont.setStyle(QFont.StyleNormal)
    #     self.fontwidth = fontwidth
    #     self.fontheight = fontheight
    #     self.fontblending = fontblending

    #     #self.text = '@@@\nBBB\n@@@\nCCC'
    #     self.text = '####\n####\n####\n####\n'

    # def sizeHint(self):
    #     return QSize(self.terminalwidth * self.fontwidth,
    #         self.terminalheight * self.fontheight)

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.fillRect(0, 0, self.width(), self.height(), QColor(0, 0, 0))
    #     painter.setPen(QColor(99, 99, 99));
    #     painter.setFont(self.cfont)

    #     term_x = 0
    #     term_y = 0
    #     for char in self.text:
    #         if char == '\n':
    #             term_y += 1
    #             term_x = 0
    #             continue
    #         x = self.fontwidth * term_x
    #         y = self.fontheight * term_y

    #         rect = QRect(x, y, self.fontwidth, self.fontheight)
    #         painter.drawText(rect, 0, char)

    #         term_x += 1

    #     x = self.fontwidth * term_x
    #     y = self.fontheight * term_y

    #     rect = QRect(x, y, self.fontwidth, self.fontheight)

    #     painter.fillRect(rect, Qt.green)


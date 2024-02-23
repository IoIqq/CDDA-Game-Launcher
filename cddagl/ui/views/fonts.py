# SPDX-FileCopyrightText: 2015-2021 Rémy Roy
#
# SPDX-License-Identifier: MIT
import logging
import os
import re
import json
import ctypes
import shutil

from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QTabWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox, QRadioButton, QGroupBox, QPlainTextEdit, QListView
from cddagl.sql.functions import (
    get_config_value, set_config_value)
logger = logging.getLogger('cddagl')

class FontsTab(QTabWidget):
    def __init__(self):
        super(FontsTab, self).__init__()

        self.initialize_variables()
        # 创建主布局
        main_layout = QGridLayout()
        params = get_config_value('command.params', '').strip()
        logger.debug(params)
        # 创建QListView来实现字体选择
        self.font_list_view = QListView()
        self.font_list_view.setEditTriggers(QListView.NoEditTriggers)
        self.font_families = self.load_fonts()
        
        
        # 创建字体设置的GroupBox并添加按钮
        font_settings_groupbox = QGroupBox("字体设置")
        font_buttons_layout = QVBoxLayout()
        set_ui_font_button = QPushButton("设为UI字体")
        set_map_font_button = QPushButton("设为地图字体")
        set_large_map_font_button = QPushButton("设为大地图字体")
        set_all_button = QPushButton("设为全部")
        reset_all_font_button = QPushButton("重置全部字体")
        
        font_buttons_layout.addWidget(self.font_list_view)
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
        test_text = """这就是一些常见的测试文本。
AB汉字1234测试cd。
Hello, World!
World, Hello!
1234567890
0987654321
!@#$%^&*()_+
+_)(*&^%$#@!
Это пример текста на кириллице.
"""
        ascii_art_edit = QPlainTextEdit()
        ascii_art = """   █████████             █████                       ████                                         █████     █████          
  ███░░░░░███           ░░███                       ░░███                                        ░░███     ░░███           
 ███     ░░░   ██████   ███████    ██████    ██████  ░███  █████ ████  █████  █████████████    ███████   ███████   ██████  
░███          ░░░░░███ ░░░███░    ░░░░░███  ███░░███ ░███ ░░███ ░███  ███░░  ░░███░░███░░███  ███░░███  ███░░███  ░░░░░███ 
░███           ███████   ░███      ███████ ░███ ░░░  ░███  ░███ ░███ ░░█████  ░███ ░███ ░███ ░███ ░███ ░███ ░███   ███████ 
░░███     ███ ███░░███   ░███ ███ ███░░███ ░███  ███ ░███  ░███ ░███  ░░░░███ ░███ ░███ ░███ ░███ ░███ ░███ ░███  ███░░███ 
 ░░█████████ ░░████████  ░░█████ ░░████████░░██████  █████ ░░███████  ██████  █████░███ █████░░████████░░████████░░████████
  ░░░░░░░░░   ░░░░░░░░    ░░░░░   ░░░░░░░░  ░░░░░░  ░░░░░   ░░░░░███ ░░░░░░  ░░░░░ ░░░ ░░░░░  ░░░░░░░░  ░░░░░░░░  ░░░░░░░░ 
                                                            ███ ░███                                                       
                                                           ░░██████                                                        
                                                            ░░░░░░                                                         
"""

        ascii_art+="""
▓█████▄  ▒█████   ██▓     ██▓    ▄▄▄       ██▀███    ██████ 
▒██▀ ██▌▒██▒  ██▒▓██▒    ▓██▒   ▒████▄    ▓██ ▒ ██▒▒██    ▒ 
░██   █▌▒██░  ██▒▒██░    ▒██░   ▒██  ▀█▄  ▓██ ░▄█ ▒░ ▓██▄   
░▓█▄   ▌▒██   ██░▒██░    ▒██░   ░██▄▄▄▄██ ▒██▀▀█▄    ▒   ██▒
░▒████▓ ░ ████▓▒░░██████▒░██████▒▓█   ▓██▒░██▓ ▒██▒▒██████▒▒
 ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒░▓  ░░ ▒░▓  ░▒▒   ▓▒█░░ ▒▓ ░▒▓░▒ ▒▓▒ ▒ ░
 ░ ▒  ▒   ░ ▒ ▒░ ░ ░ ▒  ░░ ░ ▒  ░ ▒   ▒▒ ░  ░▒ ░ ▒░░ ░▒  ░ ░
 ░ ░  ░ ░ ░ ░ ▒    ░ ░     ░ ░    ░   ▒     ░░   ░ ░  ░  ░  
   ░        ░ ░      ░  ░    ░  ░     ░  ░   ░           ░  
 ░                                                          
"""
        test_text_edit.setPlainText(test_text)
        test_text_edit.setReadOnly(True)
        test_text_edit.setStyleSheet("background-color: black; color: white;")
        self.test_text_edit = test_text_edit
        
        ascii_art_edit.setPlainText(ascii_art)
        ascii_art_edit.setReadOnly(True)
        ascii_art_edit.setStyleSheet("font-size: 5px;background-color: black; color: white;")
        self.ascii_art_edit = ascii_art_edit
        
        preview_layout.addWidget(test_text_edit)
        preview_layout.addWidget(ascii_art_edit)
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
        self.font_list_view.selectionModel().currentChanged.connect(self.font_selected)

        self.load_font_settings()
        
    def initialize_variables(self):
        # 初始化字体大小和是否启用的变量
        self.ui_font_size = None
        self.map_font_size = None
        self.large_map_font_size = None
        self.font_mixture_enabled = False
        self.selected_font = None
        self.game_dir = None
        

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
        # 自定义字体目录
        font_filenames_custom = []
        if self.game_dir:
            CUSTOM_FONT_DIRECTORY = os.path.join(self.game_dir, "data", "font")
            font_filenames_custom = load_font_filenames(CUSTOM_FONT_DIRECTORY)
            logger.debug(f'CUSTOM_FONT_DIRECTORY: {CUSTOM_FONT_DIRECTORY}')
        # 获取系统字体目录
        system_fonts_directory = get_windows_fonts_directory()

        font_filenames_system = load_font_filenames(system_fonts_directory)

        fontnamemaps = []
        for filename in font_filenames_custom + font_filenames_system:
            font_id = QFontDatabase.addApplicationFont(filename)
            font_name = QFontDatabase.applicationFontFamilies(font_id)[0]
            if font_name:
                fontnamemaps.append([filename,font_name])
        
        font_model = QStringListModel([fontnamemap[1] for fontnamemap in fontnamemaps])
        self.font_list_view.setModel(font_model)
        self.font_list_view.selectionModel().currentChanged.connect(self.font_selected)
        
        return fontnamemaps

    def set_ui_font(self):
        logger.debug("触发设为UI字体事件")
        if self.selected_font is not None:
            filepath = self.selected_fontmaps[0]
            target_subdirectory = 'data/fonts'
            font_name = os.path.basename(filepath)
            target_filepath = os.path.normpath(os.path.join(os.getcwd(), target_subdirectory, font_name))
            # 更新fontsjson的UI字体部分
            self.fontsjson["typeface"][0] = target_filepath
            
            params = get_config_value('command.params', '').strip()
            userdatadir = os.path.join(os.getcwd(), 'userdata')
            params = update_userdir_param(params, userdatadir)
            set_config_value('command.params', params)
            self.get_main_window().central_widget.settings_tab.launcher_settings_group_box.command_line_parameters_edit.setText(get_config_value('command.params',
            ''))
            
            write_fontsjson_to_path(self.fontsjson)
            copy_font_to_directory_by_name(filepath)
            self.update_current_font_text_edit()

    def set_map_font(self):
        logger.debug("触发设为地图字体事件")
        if self.selected_font is not None:
            filepath = self.selected_fontmaps[0]
            target_subdirectory = 'data/fonts'
            font_name = os.path.basename(filepath)
            target_filepath = os.path.normpath(os.path.join(os.getcwd(), target_subdirectory, font_name))
            # 更新fontsjson的地图字体部分
            self.fontsjson["map_typeface"][0] = target_filepath
            
            params = get_config_value('command.params', '').strip()
            userdatadir = os.path.join(os.getcwd(), 'userdata')
            params = update_userdir_param(params, userdatadir)
            set_config_value('command.params', params)
            self.get_main_window().central_widget.settings_tab.launcher_settings_group_box.command_line_parameters_edit.setText(get_config_value('command.params',
            ''))
            
            write_fontsjson_to_path(self.fontsjson)
            
            copy_font_to_directory_by_name(filepath)
            self.update_current_font_text_edit()

    def set_large_map_font(self):
        logger.debug("触发设为大地图字体事件")
        if self.selected_font is not None:
            filepath = self.selected_fontmaps[0]
            target_subdirectory = 'data/fonts'
            font_name = os.path.basename(filepath)
            target_filepath = os.path.normpath(os.path.join(os.getcwd(), target_subdirectory, font_name))

            # 更新fontsjson的大地图字体部分
            self.fontsjson["over_map_typeface"][0] = target_filepath
            
            params = get_config_value('command.params', '').strip()
            userdatadir = os.path.join(os.getcwd(), 'userdata')
            params = update_userdir_param(params, userdatadir)
            set_config_value('command.params', params)
            self.get_main_window().central_widget.settings_tab.launcher_settings_group_box.command_line_parameters_edit.setText(get_config_value('command.params',
            ''))
            
            write_fontsjson_to_path(self.fontsjson)
            
            
            copy_font_to_directory_by_name(filepath)
            self.update_current_font_text_edit()

    def set_all_font(self):
        logger.debug("触发设为全部字体事件")
        if self.selected_font is not None:
            selected_font = self.selected_font
            filepath = self.selected_fontmaps[0]
            target_subdirectory = 'data/fonts'
            font_name = os.path.basename(filepath)
            target_filepath = os.path.normpath(os.path.join(os.getcwd(), target_subdirectory, font_name))
            
            # 更新字体设置字典中的所有字体
            self.fontsjson["typeface"] = [target_filepath, target_filepath]
            self.fontsjson["map_typeface"] = [target_filepath, target_filepath]
            self.fontsjson["over_map_typeface"] = [target_filepath, target_filepath]
            
            params = get_config_value('command.params', '').strip()
            userdatadir = os.path.join(os.getcwd(), 'userdata')
            params = update_userdir_param(params, userdatadir)
            set_config_value('command.params', params)
            self.get_main_window().central_widget.settings_tab.launcher_settings_group_box.command_line_parameters_edit.setText(get_config_value('command.params',
            ''))
            
            write_fontsjson_to_path(self.fontsjson)
            copy_font_to_directory_by_name(filepath)
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
        logger.debug("触发字体选择变化事件")
        # 处理字体选择变化事件
        self.selected_fontmaps = self.font_families[index.row()]
        self.selected_font = self.selected_fontmaps[1]
        logger.debug(f"选择了字体：{self.selected_font}")

        # 设置test_text_edit的字体
        font_style = f'font-family: "{self.selected_font}"; font-size: 32px; background-color: black; color: white; '
        ascii_font_style = f'font-family: "{self.selected_font}"; font-size: 6px; background-color: black; color: white; '
        logger.debug(f"font_style: {font_style}")

        self.test_text_edit.setStyleSheet(font_style)
        self.ascii_art_edit.setStyleSheet(ascii_font_style)
        
        # todo

    def game_dir_changed(self, new_dir):
        logger.debug("触发游戏目录改变事件")
        # todo
        # 设置游戏目录为新的目录
        self.game_dir = new_dir
        # 清空现有的模组列表

        # 构建游戏的模组目录和用户模组目录的路径
        fonts_dir = os.path.join(new_dir, 'data', 'font')
        user_fonts_dir = os.path.join(new_dir, 'font')

        self.font_families = self.load_fonts()
        
    def get_main_window(self):
        return self.parentWidget().parentWidget().parentWidget()

    def get_main_tab(self):
        return self.parentWidget().parentWidget().main_tab
    

def load_font_filenames(directory):
    try:
        # 获取目录中所有文件的文件名
        filenames = os.listdir(directory)
        
        # 只选择特定类型的字体文件（比如.ttf或.otf），并且兼顾大小写
        font_filenames = [os.path.join(directory, filename) for filename in filenames if filename.lower().endswith(('.ttf', '.otf', '.ttc'))]
        
        return font_filenames
    except Exception as e:
        logger.error(f"加载字体文件失败: {e}")
        return []


# 加载字体
def load_font(font_path):
    try:
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            return QFont(font_families[0])
    except Exception as e:
        logger.error(f"加载字体失败 '{font_path}': {e}")
    return None

def write_fontsjson_to_path(data, subpath='userdata\\config'):
    try:
        # 检查路径是否存在，如果不存在则创建它
        if not os.path.exists(subpath):
            os.makedirs(subpath)

        # 构建JSON文件的完整路径
        json_path = os.path.join(os.getcwd(), subpath, 'fonts.json')

        # 手动构造带有换行的JSON字符串
        formatted_json = json.dumps(data, indent=4)
        formatted_json = formatted_json.replace('],', '],\n').replace('[', '[\n    ').replace(']', '\n  ]')

        # 写入JSON数据到文件
        with open(json_path, 'w') as json_file:
            json_file.write(formatted_json)

        print(f"JSON数据已成功写入到路径: {json_path}")
    except Exception as e:
        print(f"写入JSON数据时出错: {str(e)}")

def copy_font_to_directory_by_name(font_path, target_subdirectory='userdata/font'):
    # 目标目录
    target_directory = os.path.join(os.getcwd(), target_subdirectory)

    # 从font_path中提取文件名
    font_name = os.path.basename(font_path)

    # 使用文件名构建目标字体路径
    target_font_path = os.path.join(target_directory, font_name)

    # 检查目标目录是否已存在字体文件
    if os.path.exists(target_font_path):
        print(f"字体 '{font_name}' 已存在于目标目录中.")
        return

    # 确保目标目录存在
    os.makedirs(target_directory, exist_ok=True)

    try:
        # 复制字体文件到目标目录
        shutil.copy(font_path, target_font_path)
        print(f"字体 '{font_name}' 已成功复制到目标目录.")
    except Exception as e:
        print(f"复制字体 '{font_name}' 到目标目录时发生错误: {str(e)}")

def get_windows_fonts_directory():
    # 获取系统文件夹路径
    windir = os.environ.get('WINDIR', 'C:\\Windows')
    
    fonts_directory = os.path.join(windir, 'Fonts')

    return fonts_directory

def update_userdir_param(params, userdir_path):
    """
    替换或添加`--userdir`参数到给定的命令行参数字符串中。
    
    如果`params`字符串中已存在`--userdir`参数，则替换其路径；
    否则，向`params`添加`--userdir`参数和指定的路径。
    
    参数:
    - params: 原始的命令行参数字符串。
    - userdir_path: 要设置的`--userdir`参数的路径。
    
    返回:
    - 更新后的命令行参数字符串。
    """
    # 将路径中的反斜杠转义，以避免正则表达式解析错误
    safe_userdir_path = userdir_path.replace('\\', '\\\\')
    
    # 构建正则表达式以匹配--userdir参数
    userdir_pattern = re.compile(r'--userdir\s+"[^"]*"')
    
    # 检查params中是否已存在--userdir参数
    match = userdir_pattern.search(params)
    if match:
        # 如果已存在，替换其路径
        params = userdir_pattern.sub(f'--userdir "{safe_userdir_path}"', params)
    else:
        # 如果不存在，添加参数
        if params:
            params += ' '
        params += f'--userdir "{safe_userdir_path}"'
    return params
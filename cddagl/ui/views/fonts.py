# SPDX-FileCopyrightText: 2015-2021 Rémy Roy
#
# SPDX-License-Identifier: MIT
import logging

from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QWidget, QGridLayout, QTabWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox, QRadioButton, QGroupBox, QPlainTextEdit, QListView

logger = logging.getLogger('cddagl')

class FontsTab(QTabWidget):
    def __init__(self):
        super(FontsTab, self).__init__()

        # 创建主布局
        main_layout = QGridLayout()

        # 创建QListView来实现字体选择
        font_list_view = QListView()
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
        font_list_view.clicked.connect(self.font_selected)

        # 初始化字体大小和是否启用的变量
        self.ui_font_size = None
        self.map_font_size = None
        self.large_map_font_size = None
        self.font_mixture_enabled = False
        self.selected_font = None
        
        self.load_font_settings()

    def load_font_settings(self):
        # 从fontjson中加载字体设置
        self.fontjson = {
            "typeface": ["data/font/Terminus.ttf", "data/font/unifont.ttf"],
            "map_typeface": ["data/font/Terminus.ttf", "data/font/unifont.ttf"],
            "over_map_typeface": ["data/font/Terminus.ttf", "data/font/unifont.ttf"]
        }

        # 更新current_font_text_edit的文本
        self.update_current_font_text_edit()

    def update_current_font_text_edit(self):
        typeface = self.fontjson.get("typeface", [])
        map_typeface = self.fontjson.get("map_typeface", [])
        over_map_typeface = self.fontjson.get("over_map_typeface", [])

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
        if self.selected_font is not None:
            # 更新fontjson的UI字体部分
            self.fontjson["typeface"][0] = self.selected_font
            self.update_current_font_text_edit()

    def set_map_font(self):
        logger.debug("触发设为地图字体事件")
        if self.selected_font is not None:
            # 更新fontjson的地图字体部分
            self.fontjson["map_typeface"][0] = self.selected_font
            self.update_current_font_text_edit()

    def set_large_map_font(self):
        logger.debug("触发设为大地图字体事件")
        if self.selected_font is not None:
            # 更新fontjson的大地图字体部分
            self.fontjson["over_map_typeface"][0] = self.selected_font
            self.update_current_font_text_edit()

    def set_all_font(self):
        logger.debug("触发设为全部字体事件")
        if self.selected_font is not None:
            selected_font = self.selected_font

            # 更新字体设置字典中的所有字体
            self.fontjson["typeface"] = [selected_font, selected_font]
            self.fontjson["map_typeface"] = [selected_font, selected_font]
            self.fontjson["over_map_typeface"] = [selected_font, selected_font]

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
        # 在这里处理选择的字体
        pass

    def get_main_window(self):
        return self.parentWidget().parentWidget().parentWidget()

    def get_main_tab(self):
        return self.parentWidget().parentWidget().main_tab











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


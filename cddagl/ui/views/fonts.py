# SPDX-FileCopyrightText: 2015-2021 Rémy Roy
#
# SPDX-License-Identifier: MIT

import logging

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QPainter, QColor, QFont, QFontDatabase
from PyQt5.QtWidgets import QWidget, QGridLayout, QTabWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox, QRadioButton, QGroupBox, QPlainTextEdit, QListView, QFontComboBox

logger = logging.getLogger('cddagl')

class FontsTab(QTabWidget):
    def __init__(self):
        super(FontsTab, self).__init__()

        layout = QGridLayout()

        # 创建垂直布局和按钮
        v_layout = QVBoxLayout()

        # 创建GroupBox并将按钮添加到GroupBox内
        font_settings_groupbox = QGroupBox("字体设置")
        buttons_layout = QVBoxLayout()
        set_ui_font_button = QPushButton("设为UI字体")
        set_map_font_button = QPushButton("设为地图字体")
        set_large_map_font_button = QPushButton("设为大地图自提")
        set_all_button = QPushButton("设为全部")
        reset_all_font_button = QPushButton("重置全部字体")
        buttons_layout.addWidget(set_ui_font_button)
        buttons_layout.addWidget(set_map_font_button)
        buttons_layout.addWidget(set_large_map_font_button)
        buttons_layout.addWidget(set_all_button)
        buttons_layout.addWidget(reset_all_font_button)
        font_settings_groupbox.setLayout(buttons_layout)

        # 创建四个QLabel
        ui_font_label = QLabel("UI字体大小:")
        map_font_label = QLabel("地图字体大小:")
        large_map_font_label = QLabel("大地图字体大小:")
        font_mixture_label = QLabel("字体混合:")

        # 创建三个调节字体大小的框
        ui_font_size_spinbox = QSpinBox()
        map_font_size_spinbox = QSpinBox()
        large_map_font_size_spinbox = QSpinBox()

        # 创建RadioButton
        font_mixture_radio = QRadioButton("启用")

        # 创建保存按钮
        save_button = QPushButton("保存")

        # 添加QPlainTextEdit来显示测试文本
        test_text_edit = QPlainTextEdit()
        test_text = """这是一些常见的测试文本。
Hello, World!
1234567890
!@#$%^&*()_+
Это пример текста на кириллице."""
        test_text_edit.setPlainText(test_text)

        # 设置QPlainTextEdit为不可编辑
        test_text_edit.setReadOnly(True)

        # 设置背景颜色为黑色 设置文字颜色为白色
        test_text_edit.setStyleSheet("background-color: black; color: white;")

        # 创建QListView和QFontComboBox
        font_list_view = QListView()
        font_combobox = QFontComboBox()

        # 初始化字体列表
        self.load_fonts(font_combobox)

        # 使用QGridLayout将标签和SpinBox布局在一行
        label_spinbox_layout = QGridLayout()
        label_spinbox_layout.addWidget(ui_font_label, 0, 0)
        label_spinbox_layout.addWidget(ui_font_size_spinbox, 0, 1)
        label_spinbox_layout.addWidget(map_font_label, 1, 0)
        label_spinbox_layout.addWidget(map_font_size_spinbox, 1, 1)
        label_spinbox_layout.addWidget(large_map_font_label, 2, 0)
        label_spinbox_layout.addWidget(large_map_font_size_spinbox, 2, 1)
        label_spinbox_layout.addWidget(font_mixture_label, 3, 0)
        label_spinbox_layout.addWidget(font_mixture_radio, 3, 1)

        # 创建GroupBox并将标签和SpinBox的布局添加到GroupBox内
        other_settings_groupbox = QGroupBox("其他设置")
        other_settings_groupbox.setLayout(label_spinbox_layout)

        # 将GroupBox添加到垂直布局
        v_layout.addWidget(other_settings_groupbox)
        v_layout.addWidget(test_text_edit)
        v_layout.addWidget(font_combobox)  # 添加字体选择框
        v_layout.addWidget(font_list_view)  # 添加字体列表
        v_layout.addWidget(save_button)

        # 将按钮GroupBox添加到垂直布局
        v_layout.addWidget(font_settings_groupbox)

        # 添加垂直布局到主布局
        layout.addLayout(v_layout, 0, 1)

        self.setLayout(layout)

        # 绑定事件（预留函数）
        set_ui_font_button.clicked.connect(self.set_ui_font)
        set_map_font_button.clicked.connect(self.set_map_font)
        set_large_map_font_button.clicked.connect(self.set_large_map_font)
        set_all_button.clicked.connect(self.set_all_font)
        reset_all_font_button.clicked.connect(self.reset_all_font)
        save_button.clicked.connect(self.save_settings)

        # 绑定字体选择框的信号
        font_combobox.currentFontChanged.connect(self.font_selected)

        # 初始化字体大小和是否启用的变量
        self.ui_font_size = None
        self.map_font_size = None
        self.large_map_font_size = None
        self.font_mixture_enabled = False

    def load_fonts(self, font_combobox):
        # 加载可用字体并更新字体列表
        font_database = QFontDatabase()
        font_families = font_database.families(QFontDatabase.Latin)
        font_combobox.clear()
        font_combobox.addItems(font_families)

    def set_ui_font(self):
        logger.info("触发设为UI字体事件")
        # 实现设为UI字体的操作
        pass

    def set_map_font(self):
        logger.debug("触发设为地图字体事件")
        # 实现设为地图字体的操作
        pass

    def set_large_map_font(self):
        logger.debug("触发设为大地图自提事件")
        # 实现设为大地图自提的操作
        pass

    def set_all_font(self):
        logger.debug("触发设为全部字体事件")
        # 实现设为全部字体的操作
        pass

    def reset_all_font(self):
        logger.debug("触发重置全部字体事件")
        # 实现重置全部字体的操作
        pass

    def save_settings(self):
        logger.debug("触发保存设置事件")
        # 将字体大小和是否启用的变量存储在这里
        self.ui_font_size = ui_font_size_spinbox.value()
        self.map_font_size = map_font_size_spinbox.value()
        self.large_map_font_size = large_map_font_size_spinbox.value()
        self.font_mixture_enabled = font_mixture_radio.isChecked()
        pass

    def font_selected(self, font):
        # 处理字体选择变化事件
        logger.debug(f"选择了字体：{font.family()}")
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


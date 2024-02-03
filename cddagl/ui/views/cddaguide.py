# SPDX-FileCopyrightText: 2015-2021 Rémy Roy
#
# SPDX-License-Identifier: MIT

import logging
from PyQt5.QtCore import QSize
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebEngineCore import QWebEngineHttpRequest
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

logger = logging.getLogger('cddagl')

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super(CustomWebEnginePage, self).__init__(parent)

    def createRequest(self, _type, request):
        # 修改请求头
        request.setHeader("Referer", "cddagl")
        return super().createRequest(_type, request)

class CDDAGuideTab(QTabWidget):
    def __init__(self):
        super(CDDAGuideTab, self).__init__()

        # 创建浏览器视图
        self.browser = QWebEngineView(self)
        self.browser.setPage(CustomWebEnginePage(self.browser))

        # 设置初始页面
        self.browser.setUrl(QUrl("https://cdda.doiiars.com/?lang=zh_CN"))

        # 设置用户代理
        user_agent = "cddagl"  # 你可以设置自己的用户代理字符串
        self.browser.page().profile().setHttpUserAgent(user_agent)

        # 设置本地存储路径
        local_storage_path = "./"  # 设置本地存储数据库的路径
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)  # 启用本地存储
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)  # 启用JavaScript
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)  # 启用插件
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)  # JavaScript可以打开新窗口
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)  # JavaScript可以访问剪贴板
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)  # 启用本地存储

        # 创建布局并将浏览器视图添加到布局中
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        self.setLayout(layout)

    def set_text(self):
        pass

    def get_main_window(self):
        return self.parentWidget().parentWidget().parentWidget()

    def get_main_tab(self):
        return self.parentWidget().parentWidget().main_tab


# 测试代码
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = QMainWindow()
    tab = CDDAGuideTab()
    mainWin.setCentralWidget(tab)
    mainWin.show()
    sys.exit(app.exec_())

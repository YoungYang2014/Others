# -*- coding: utf-8 -*-

"""
主界面逻辑处理
"""
import sip
import os

sip.setapi('QString',2)
sip.setapi('QVariant',2)
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import csv

# 自定义模块
from UI_Main import Ui_MainWindow

import Login_Start
from iclock import GetAbnormal


class MainWindow(QtGui.QMainWindow):
    """主界面"""
    signalStatusBar=QtCore.pyqtSignal()

    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        # 初始化考勤爬虫
        self.get_abnormal=GetAbnormal()
        # 初始化登录窗口
        self.LoginUI=Login_Start.MainWindow(self.get_abnormal)
        self.LoginUI.show()
        self.connect(self.LoginUI,QtCore.SIGNAL("transfer_login"),self.setLoginStatus)
        # 设置界面样式
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口拉动按钮
        sizeGrip=QSizeGrip(self)
        sizeGrip.setStyleSheet("image: url(:/Imag/Imag/sizegrip.png);")
        self.ui.sizeGrip_layout.addWidget(sizeGrip)
        self.ui.sizeGrip_layout.setAlignment(sizeGrip,Qt.AlignRight)
        # 初始化表格
        self.initToolBox()
        self.tmp_dataList=[]
        self.LoginStatus=False

    @pyqtSignature("bool")
    def on_QToolButton_Login_clicked(self):
        self.LoginUI.show()

    @pyqtSignature("bool")
    def on_QToolButton_abnormite_clicked(self):
        if self.LoginStatus:
            self.headerList=[u"考勤号码",u"姓名",u"时间",u"星期",u"迟到",u"早退",u"旷工",u"请假"]
            self.dataList=self.get_abnormal.get_error()
            self.addReportData()
        else:
            self.LoginUI.show()

    @pyqtSignature("bool")
    def on_QToolButton_attshifts_clicked(self):
        if self.LoginStatus:
            self.headerList=[u"考勤号码",u"姓名",u"日期",u"上班打卡",u"下班打卡",u"加班时长(分)"]
            self.dataList=self.get_abnormal.get_history()
            self.addReportData()
        else:
            self.LoginUI.show()

    # 系统函数----------------------------------------------------------------------
    def show_message(self,log):
        """消息提示框"""
        QtGui.QMessageBox.information(self,u"提示",log)

    def mousePressEvent(self,event):
        """鼠标点击事件"""
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition=event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self,event):
        """鼠标移动事件"""
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    # 登陆状态----------------------------------------------------------------
    def setLoginStatus(self):
        self.LoginStatus=True
        self.ui.QToolButton_Login.setText(u"已登录")

    # 表格函数-----------------------------------------------------------------
    def initToolBox(self):
        """初始化表格"""
        self.layout=QVBoxLayout()
        self.MyTable=QTableWidget()
        self.layout.addWidget(self.MyTable)
        self.ui.tab1.setLayout(self.layout)
        # 设为行交替颜色
        self.MyTable.setAlternatingRowColors(True)
        # 初始化右键菜单
        self.initMenu()
        # 隐藏表头
        self.MyTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.MyTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def initMyToolBox(self):
        """设置表头"""
        self.MyTable.setRowCount(len(self.dataList))
        self.MyTable.setColumnCount(len(self.headerList))
        self.MyTable.setHorizontalHeaderLabels(self.headerList)

    def addReportData(self):
        """向表格中填写数据"""
        self.MyTable.clear()  # 清空表头及表数据
        self.initMyToolBox()  # 二维表格初始化行列、设置表头
        for i in range(len(self.dataList)):
            for j in range(len(self.dataList[i])):
                Info=unicode(self.dataList[i][j])
                newItem=QTableWidgetItem(Info)
                # 添加提示气泡
                newItem.setToolTip(Info)
                self.MyTable.setItem(i,j,newItem)
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.MyTable.setColumnWidth(2,150)
        self.MyTable.show()

    def initMenu(self):
        """初始化右键菜单"""
        self.menu=QtGui.QMenu(self)
        saveAction=QtGui.QAction(u'保存为CSV',self)
        saveAction.triggered.connect(self.saveToCsv)
        self.menu.addAction(saveAction)

    def saveToCsv(self):
        """保存表格内容到CSV文件"""
        # 先关闭右键菜单
        self.menu.close()
        # 获取想要保存的文件名
        path=QtGui.QFileDialog.getSaveFileName(self,u'保存数据','','CSV(*.csv)')
        try:
            if not os.path.exists(path):
                with open(unicode(path),'wb') as f:
                    writer=csv.writer(f)
                    # 保存标签
                    headers=[header.encode('gbk') for header in self.headerList]
                    writer.writerow(headers)
                    # 保存每行内容
                    for row in range(self.MyTable.rowCount()):
                        rowdata=[]
                        for column in range(self.MyTable.columnCount()):
                            item=self.MyTable.item(row,column)
                            if item is not None:
                                rowdata.append(
                                    unicode(item.text()).encode('gbk'))
                            else:
                                rowdata.append('')
                        writer.writerow(rowdata)
        except IOError:
            pass

    def contextMenuEvent(self,event):
        """右键点击事件"""
        self.menu.popup(QtGui.QCursor.pos())

    def close(self):
        sys.exit(0)


if __name__ == '__main__':
    app=QtGui.QApplication(sys.argv)
    import qdarkstyle

    app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    main=MainWindow()
    main.show()
    sys.exit(app.exec_())

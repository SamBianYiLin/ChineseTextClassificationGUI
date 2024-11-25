#2024-10-31 20:14
#应物222 边奕霖 2206020201
#Chinese Text Classification
# -*- coding: utf-8 -*-
# 导入所需的库
import os
import sys
import torch
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, \
    QCheckBox, qApp, QMenu, QAction, QApplication, QMessageBox
from Classify import MyClassifier
from utils import build_vocab, MAX_VOCAB_SIZE, DatasetIterater

# 设置插件路径
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(os.path.dirname(QtCore.__file__), 'plugins')

# 加个小彩蛋
class EasterEgg(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # 设置窗口标题和大小
        self.setWindowTitle("Easter Egg")
        self.setGeometry(100, 100, 400, 200)
        # 设置窗口图标
        self.setWindowIcon(QtGui.QIcon('CTCico.ico'))
        # 窗口内容
        label = QLabel("This windows is for my own.\n"
                       "I am Sam iLiant.\n"
                       "I am the developer of this app.\n"
                       "I am the student of Applied Physics 222.\n"
                       "My Chinese name is 边奕霖.\n"
                       "I started to develop this app on 2024-10-29.\n"
                       "Today is 2024-11-02,I code this Easter Egg for my own.\n"
                       "Now there are still some bugs in this app.\n"
                       "I will fix them in the future.\n"
                       "I hope this will be fixed soon.\n"
                       "This windows is like a log for this app.\n")
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label) # 添加标签到布局
        self.setLayout(layout) # 设置布局
        self.center()

    def center(self):
        # 获取屏幕尺寸
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class TextClassificationApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("Chinese Text Classification")
        self.setGeometry(100, 100, 1200, 330)

        # 创建布局
        main_layout = QtWidgets.QVBoxLayout()

        # 设置窗口图标
        self.setWindowIcon(QtGui.QIcon('CTCico.ico'))

        # 创建标题
        title_layout = QtWidgets.QHBoxLayout()
        title_label = QtWidgets.QLabel("Chinese Text Classification")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # 添加标题到布局并居中
        title_layout.addWidget(title_label, alignment=QtCore.Qt.AlignCenter)
        main_layout.addLayout(title_layout)

        # 添加空白区域
        main_layout.addStretch(1)
        main_layout.addSpacing(20)

        # 创建输入行
        input_layout = QtWidgets.QHBoxLayout()
        input_label = QtWidgets.QLabel("Chinese Title：")
        input_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        input_label.setFixedHeight(60)
        self.text_edit = QtWidgets.QTextEdit()
        # 设置固定高度
        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setFixedHeight(60)  # 设置固定高度
        self.text_edit.setMinimumWidth(200)
        # 将输入行添加到布局中
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.text_edit)
        # 将输入行添加到主布局中
        main_layout.addLayout(input_layout)

        # 添加一个横向的空白区域
        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        main_layout.addItem(spacer)  # 添加可扩展的横向空白区域

        #创建复选框布局
        checkbox_layout = QtWidgets.QHBoxLayout()
        #定义“模型”标签
        self.model_label = QtWidgets.QLabel("Model：")
        self.model_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        #定义“全选”按钮
        self.SelectALL = QtWidgets.QRadioButton("Select All")
        #self.SelectALL.setFixedWidth(120)
        #定义各个模型的复选框
        self.CNN = QtWidgets.QCheckBox("CNN")
        # self.CNN.setFixedWidth(75)
        self.RNN= QtWidgets.QCheckBox("RNN")
        # self.RNN.setFixedWidth(80)
        self.Transformer= QtWidgets.QCheckBox("Transformer")
        # self.Transformer.setFixedWidth(145)
        self.RNN_Att= QtWidgets.QCheckBox("RNN_Att")
        #self.RNN_Att.setFixedWidth(115)
        self.RCNN= QtWidgets.QCheckBox("RCNN")
        #self.RCNN.setFixedWidth(100)
        self.FastText= QtWidgets.QCheckBox("FastText")
        #self.FastText.setFixedWidth(125)
        self.DPCNN= QtWidgets.QCheckBox("DPCNN")
        #self.DPCNN.setFixedWidth(120)

        #将各个复选框添加到布局中
        checkbox_layout.addWidget(self.model_label)
        checkbox_layout.addWidget(self.SelectALL,alignment=QtCore.Qt.AlignLeft)
        self.SelectALL.toggled.connect(self.select_all_models)
        checkbox_layout.addWidget(self.CNN)
        checkbox_layout.addWidget(self.RNN)
        checkbox_layout.addWidget(self.Transformer)
        checkbox_layout.addWidget(self.RNN_Att)
        checkbox_layout.addWidget(self.RCNN)
        checkbox_layout.addWidget(self.FastText)
        checkbox_layout.addWidget(self.DPCNN)

        #将复选框布局添加到主布局中
        main_layout.addLayout(checkbox_layout)

        # 添加一个横向的空白区域
        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        main_layout.addItem(spacer)  # 添加可扩展的横向空白区域

        #创建结果行
        output_layout = QtWidgets.QHBoxLayout()
        output_label = QtWidgets.QLabel("Result：")
        output_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        #output_label.setFixedHeight(60)
        self.result_label = QtWidgets.QLabel("Please press Classify button to get the result")
        self.result_label.setMargin(0)
        self.result_label.setStyleSheet("font-size: 20px; font-weight: bold;border: 1px solid black;")
        self.result_label.setMinimumHeight(180)
        self.result_label.setFixedWidth(1010)
        self.result_label.setContentsMargins(10,10,10,10)

        #将结果行添加到布局中
        output_layout.addWidget(output_label,alignment=QtCore.Qt.AlignLeft)
        output_layout.addWidget(self.result_label,alignment=QtCore.Qt.AlignLeft)

        #将结果行添加到主布局中
        main_layout.addLayout(output_layout)

        # 创建按钮
        button_layout = QtWidgets.QHBoxLayout()
        self.classify_button = QtWidgets.QPushButton("Classify")
        self.classify_button.clicked.connect(self.classify) #实现预测功能
        self.classify_button.setFixedHeight(50)
        self.classify_button.setFixedWidth(200)
        self.classify_button.setStyleSheet("font-size: 20px; font-weight: bold;")
        #self.classify_button.clicked.connect(self.classify)
        self.Clear_button = QtWidgets.QPushButton("Clear")
        self.Clear_button.setFixedHeight(50)
        self.Clear_button.setFixedWidth(200)
        self.Clear_button.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.Clear_button.clicked.connect(self.clear)
        self.quit_button = QtWidgets.QPushButton("Quit")
        self.quit_button.setFixedHeight(50)
        self.quit_button.setFixedWidth(200)
        self.quit_button.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.quit_button.clicked.connect(qApp.quit)

        button_layout.addWidget(self.classify_button)
        button_layout.addWidget(self.Clear_button)
        button_layout.addWidget(self.quit_button)

        main_layout.addLayout(button_layout)

        # 输入框和模型选择改变，自动清空输出框内容
        self.text_edit.textChanged.connect(self.clear_output)
        self.CNN.stateChanged.connect(self.clear_output)
        self.RNN.stateChanged.connect(self.clear_output)
        self.Transformer.stateChanged.connect(self.clear_output)
        self.RNN_Att.stateChanged.connect(self.clear_output)
        self.RCNN.stateChanged.connect(self.clear_output)
        self.FastText.stateChanged.connect(self.clear_output)
        self.DPCNN.stateChanged.connect(self.clear_output)
        self.SelectALL.toggled.connect(self.clear_output)

        # 添加空白区域
        main_layout.addStretch(10)
        # 设置主布局
        self.setLayout(main_layout)

        #彩蛋默认不显示
        self.EasterEgg= None

        #监听输入框的回车事件
        self.text_edit.installEventFilter(self)

        # 中心显示窗体
        self.center()

    # 选择所有模型(连接到全选按钮)
    def select_all_models(self):
        if self.SelectALL.isChecked():
            self.CNN.setChecked(True)
            self.RNN.setChecked(True)
            self.Transformer.setChecked(True)
            self.RNN_Att.setChecked(True)
            self.RCNN.setChecked(True)
            self.FastText.setChecked(True)
            self.DPCNN.setChecked(True)
        else:
            self.CNN.setChecked(False)
            self.RNN.setChecked(False)
            self.Transformer.setChecked(False)
            self.RNN_Att.setChecked(False)
            self.RCNN.setChecked(False)
            self.FastText.setChecked(False)
            self.DPCNN.setChecked(False)

    # 窗口居中
    def center(self):
        # 获取屏幕尺寸
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 清空输入框和结果
    def clear(self):
        self.text_edit.clear()
        self.result_label.setText("Please press Classify button to get the result")
        self.CNN.setChecked(False)
        self.RNN.setChecked(False)
        self.Transformer.setChecked(False)
        self.RNN_Att.setChecked(False)
        self.RCNN.setChecked(False)
        self.FastText.setChecked(False)
        self.DPCNN.setChecked(False)
        self.SelectALL.setChecked(False)

    # 关于(连接右键——关于)
    def about(self):
        QtWidgets.QMessageBox.about(self, "About Chinese Text Classification",
                                    "This is a Chinese Text Classification App,\n using CNN,RNN,Transformer,etc models to classify news.\n"
                                    "\n"
                                    "It is developed by PyQt5\n"
                                    "Author: Yilin Bian(边奕霖)\n"
                                    "Student ID: 2206020201\n"
                                    "Class: Applied Physics 222\n"
                                    "Version: 1.0\n"
                                    "Begin Date: 2024-10-29\n"
                                    "End Date: 2024-11-06")

    # 右键菜单
    def contextMenuEvent(self,event):
        cmenu = QMenu(self)
        clear = cmenu.addAction("Clear")
        clear.setIcon(QtGui.QIcon('clear.png'))
        quit = cmenu.addAction("Quit")
        quit.setIcon(QtGui.QIcon('quit.png'))
        about = cmenu.addAction("About")
        about.setIcon(QtGui.QIcon('about.png'))
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        if action == clear:
            self.clear()
        if action == quit:
            qApp.quit()
        if action == about:
            self.about()

    # 回车事件
    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress and source is self.text_edit:
            if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
                self.classify_button.click()
                return True
        return super().eventFilter(source, event)

    def clear_output(self):
        self.result_label.setText("Please press Classify button to get the result")

    # 预测功能逻辑的实现
    def classify(self):
        self.result_label.setText("Please wait for a moment...")
        QtWidgets.QApplication.processEvents()  # 强制界面刷新
        text = self.text_edit.toPlainText()
        print(text)
        results = []

        #Check if any model is selected
        if not (self.CNN.isChecked() or
                self.RNN.isChecked() or
                self.Transformer.isChecked() or
                self.RNN_Att.isChecked() or
                self.RCNN.isChecked() or
                self.FastText.isChecked()
                or self.DPCNN.isChecked()):
            QMessageBox.warning(self, "Warning", "Please select at least one model to classify!", QMessageBox.Ok)
            return

        if text=="":
            QMessageBox.warning(self, "Warning", "Please input Chinese text to classify!", QMessageBox.Ok)
            return
        if text=="Sam iLiant":
            if not self.EasterEgg:
                self.EasterEgg = EasterEgg()
            self.EasterEgg.show()
            return


        try:
            if self.CNN.isChecked():
                classifier = MyClassifier(model_name='TextCNN', dataset='saved_dict', embedding='random', word=False)
                cnn_result = classifier.classify(text)
                results.append(f"CNN: {cnn_result}")
            #完成功能实现，2024-11-02 00:06

            if self.RNN.isChecked():
                classifier = MyClassifier(model_name='TextRNN', dataset='saved_dict', embedding='random', word=False)
                rnn_result = classifier.classify(text)
                results.append(f"RNN: {rnn_result}")
            #完成功能实现，2024-11-02 00:14

            if self.Transformer.isChecked():
                classifier = MyClassifier(model_name='Transformer', dataset='saved_dict', embedding='random', word=False)
                trans_result = classifier.classify(text)
                results.append(f"Transformer: {trans_result}")
            #完成功能实现，2024-11-02 00:17

            if self.RNN_Att.isChecked():
                classifier = MyClassifier(model_name='TextRNN_Att', dataset='saved_dict', embedding='random',
                                          word=False)
                rnn_att_result = classifier.classify(text)
                results.append(f"RNN_Att: {rnn_att_result}")
            #完成功能实现，2024-11-02 00:24

            if self.RCNN.isChecked():
                classifier = MyClassifier(model_name='TextRCNN', dataset='saved_dict', embedding='random',
                                          word=False)
                rcnn_result = classifier.classify(text)
                results.append(f"RCNN: {rcnn_result}")
                #results.append("RCNN:Sorry,RCNN is Not Ready for Use.")
            #出现些许问题，2024-11-02 00:32
            #完成功能实现，2024-11-06 19:35

            if self.FastText.isChecked():
                classifier = MyClassifier(model_name='FastText', dataset='saved_dict', embedding='random',
                                          word=False)
                fast_text_result = classifier.classify(text)
                results.append(f"FastText: {fast_text_result}")
            #完成功能实现，2024-11-02 00:38

            if self.DPCNN.isChecked():
                classifier = MyClassifier(model_name='DPCNN', dataset='saved_dict', embedding='random',
                                           word=False)
                dpcnn_result = classifier.classify(text)
                # class_list = [x.strip() for x in open('./saved_dict/class.txt', encoding='utf-8').readlines()]
                # if dpcnn_result not in class_list or dcpnn_result is None:
                #     dpcnn_result = "ERROR! 分类错误"
                results.append(f"DPCNN: {dpcnn_result}")
                #results.append("DCPNN:Sorry,DPCNN is Not Ready for Use.")
            #出现些许问题，2024-11-02 00:49
            #完成功能实现，2024-11-06 19:35
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")
            print(f"Error: {str(e)}")

        # 显示结果
        self.result_label.setText("\n".join(results))

    #加载模型
    def load_model(self, model_path):
        model = torch.load(model_path,weights_only=True)
        model.eval()
        return model

# 主函数
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # 创建应用
    window = TextClassificationApp()    # 创建窗口
    window.show()
    sys.exit(app.exec_())

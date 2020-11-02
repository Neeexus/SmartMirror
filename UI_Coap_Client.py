# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'embedded.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from coapthon.client.helperclient import HelperClient

class Coap_Client_with_UI(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(821, 539)

        #Coap 셋업
        self.coap_setup(host="192.168.137.209", port= 5683)

        #UI 메인 윈도위 셋업
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
 
        #버튼 셋업
        self.get_btn = QtWidgets.QPushButton(self.centralwidget)
        self.get_btn.setGeometry(QtCore.QRect(530, 180, 101, 31))
        self.get_btn.setObjectName("get_btn")
        self.put_bnt = QtWidgets.QPushButton(self.centralwidget)
        self.put_bnt.setGeometry(QtCore.QRect(530, 230, 101, 31))
        self.put_bnt.setObjectName("put_bnt")
        self.post_bnt = QtWidgets.QPushButton(self.centralwidget)
        self.post_bnt.setGeometry(QtCore.QRect(530, 280, 101, 31))
        self.post_bnt.setObjectName("post_bnt")
        self.observe_bnt = QtWidgets.QPushButton(self.centralwidget)
        self.observe_bnt.setGeometry(QtCore.QRect(660, 180, 101, 31))
        self.observe_bnt.setObjectName("observe_bnt")
        self.delete_bnt = QtWidgets.QPushButton(self.centralwidget)
        self.delete_bnt.setGeometry(QtCore.QRect(660, 230, 101, 31))
        self.delete_bnt.setObjectName("delete_bnt")

        #버튼-함수 연결
        self.get_btn.clicked.connect(self.push_get)
        self.put_bnt.clicked.connect(self.push_put)
        self.post_bnt.clicked.connect(self.push_post)
        self.observe_bnt.clicked.connect(self.push_observe)
        self.delete_bnt.clicked.connect(self.push_delete)

        #Input Text 셋업
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(540, 50, 231, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(540, 110, 231, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")

        #Text board (display) 셋업
        self.text_board = QtWidgets.QTextBrowser(self.centralwidget)
        self.text_board.setGeometry(QtCore.QRect(10, 40, 491, 421))
        self.text_board.setObjectName("text_board")

        # 그 외 UI 구성요소 셋업
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(540, 30, 56, 12))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(540, 90, 56, 12))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 821, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow) # UI 구성요소 이름, 텍스트 등을 재조정
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        # UI 구성요소 재조정을 위한 함수
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CoAP Client"))
        self.get_btn.setText(_translate("MainWindow", "GET"))
        self.lineEdit.setText(_translate("MainWindow", "observe"))
        self.lineEdit_2.setText(_translate("MainWindow", "22.0"))
        self.put_bnt.setText(_translate("MainWindow", "PUT"))
        self.post_bnt.setText(_translate("MainWindow", "POST"))
        self.observe_bnt.setText(_translate("MainWindow", "Observe"))
        self.delete_bnt.setText(_translate("MainWindow", "Delete"))
        self.label.setText(_translate("MainWindow", "path"))
        self.label_2.setText(_translate("MainWindow", "SetTemp"))

    def coap_setup(self, host, port):
        #Coap 서버와 연결, setupUi 함수 맨 앞에서 실행 됨
        self.client = HelperClient(server=(host, port)) # 클래스 변수로 Client 객체 저장

    def when_listen_observe(self, response):
        #observe 메세지를 수신했을 때 실행되는 함수
        self.text_board.append("-----------------Observing-----------------")
        self.text_board.append(response.pretty_print()) # Text board에 수신한 Observe 메세지 출력

    def push_get(self):
        # Push 버튼이 눌리면 실행되는 함수
        path = self.lineEdit.text() # Path 텍스트 input에서 문자열 읽어오기
        payload = self.lineEdit_2.text() # Payload 텍스트 input에서 문자열 읽어오기
        response = self.client.get(path=path, payload=payload, timeout=3) # GET 메세지 전송
        self.text_board.append("-----------------Get Response from %s-----------------" % (path))
        self.text_board.append(response.pretty_print())  # Text board에 수신한 response 출력

    def push_put(self):
        # Put 버튼이 눌리면 실행되는 함수
        path = self.lineEdit.text()
        payload = self.lineEdit_2.text()
        response = self.client.put(path=path, payload=payload, timeout=3) # Put 메세지 전송
        self.text_board.append("-----------------Put Response from %s-----------------" % (path))
        self.text_board.append(response.pretty_print())
        
        

    def push_observe(self):
        # Observe 버튼이 눌리면 실행되는 함수
        path = self.lineEdit.text()
        payload = self.lineEdit_2.text()
        observe = self.client.observe(path=path, callback=self.when_listen_observe) # observe 메세지 수신하면 self.when_listen_observe 실행
      
    def push_post(self):
        # Post 버튼이 눌리면 실행되는 함수
        path = self.lineEdit.text()
        payload = self.lineEdit_2.text()
        response = self.client.post(path=path, payload=payload, timeout=3)
        self.text_board.append("-----------------Post Response from %s-----------------" % (path))
        self.text_board.append(response.pretty_print())

    def push_delete(self):
        # Delete 버튼이 눌리면 실행되는 함수
        path = self.lineEdit.text()
        payload = self.lineEdit_2.text()
        response = self.client.delete(path=path, payload=payload, timeout=3)
        self.text_board.append("-----------------Delete Response from %s-----------------" % (path))
        self.text_board.append(response.pretty_print())

    def connection_test(self):
        res = self.client.get(path="", timeout=3)
        if res == None:
            self.text_board.append("서버와 Test 통신 실패")
        else:
            self.text_board.append("서버와 Test 통신 성공")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Coap_Client_with_UI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.connection_test() # Coap 서버 연결 확인
    sys.exit(app.exec_())


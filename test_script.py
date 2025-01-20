# -*- coding: utf-8 -*-
import datetime
import getpass
import inspect
import io
import os.path
import shutil
import time
from logging import exception
from operator import index

import can.interfaces.ixxat.exceptions
from click import prompt
from reportlab.pdfbase.pdfmetrics import parseAFMFile
from screeninfo import get_monitors
import CommandSetDcLoadUsb
import CommandSetSmrBatteryCan
import PFC_control_done
import test_order_done
from ModbusServer import MODBUS_CHECK
from report_gui import *
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
import xml_generator
from prompts import *
import M1KLC
from PyQt5.QtCore import QThread, pyqtSignal, QObject


class Worker(QObject):
    # Define signals for starting, stopping, and logging
    started_signal = pyqtSignal()
    finished_signal = pyqtSignal()
    log_signal = pyqtSignal(str)
    result_signal = pyqtSignal(str)

    def __init__(self, start_function):
        super().__init__()
        self.running = False
        self.start_function = start_function

    def run(self):
        self.start_function()  # Execute the start_function logic in the background

    def stop_function(self):
        self.running = False
        self.log_signal.emit("Test Stopped")
        self.finished_signal.emit()
# import application_detection

global w, h, m, factor

"""MULTIPLYING FACTOR"""
if os.path.exists(gui_global.directory_location):
    try:
        factor = abs(eval(SettingRead('MULTIPLY')['factor']))
        # if factor <= 0 or factor >= 2:
        #     factor = 1
    except TypeError:
        with open(f'{gui_global.files_directory_location}setting.txt', 'a') as file:
            file.write("\n[MULTIPLY]\nfactor=0.8\n")
        factor = round(abs(eval(SettingRead('MULTIPLY')['factor'])))
        if factor <= 0 or factor >= 2:
            factor = 1
    print(factor)
w = get_monitors()[0].width
h = get_monitors()[0].height

from config_done import *
import M1000Telnet
import M2000
from prompts import Prompt

try:
    if os.path.exists(os.path.join(gui_global.files_directory_location), 'setting.txt'):
        if SettingRead("SETTING")['ate load comm type'] == "RS232C":
            from CommandDCLoad import *
        if SettingRead("SETTING")['ate load comm type'] == "USB" or \
                SettingRead("SETTING")['ate load comm type'] == "GPIB":
            from CommandDCLoad import *

        ATE_LOAD_COUNT = int(SettingRead("SETTING")['ate load count'])
except:
    pass


def get_date_time(date=0, time=0):
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = "0" + day
    date_only = day + "-" + month + "-" + year
    hour = str(now.hour)
    if len(hour) == 1:
        hour = "0" + hour
    minute = str(now.minute)
    if len(minute) == 1:
        minute = "0" + minute
    second = str(now.second)
    if len(second) == 1:
        second = "0" + second
    time_only = hour + ":" + minute + ":" + second
    if time == 1 and date == 1:
        return date_only + " " + time_only
    elif date == 1:
        return date_only
    elif time == 1:
        return time_only


class WindowSignalHandler(QObject):
    openWindow = pyqtSignal()


class Ui_Test(object):
    global w, h

    def setupUi(self, MainWindow):
        super().__init__()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1402, 778)
        font = QtGui.QFont()
        font.setPointSize(8)
        MainWindow.setFont(font)
        MainWindow.setWindowIcon(QtGui.QIcon(f"{gui_global.image_directory_location}logo_1.png"))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # self.heading_box = QtWidgets.QGroupBox(self.centralwidget)
        # self.heading_box.setGeometry(
        #     QtCore.QRect(int(w * 0.28505), int(h * 0.052083), int(w * 0.3806), int(h * 0.0651)))
        # self.heading_box.setTitle("")
        # self.heading_box.setObjectName("heading_box")
        self.heading = QtWidgets.QLabel(self.centralwidget)
        self.heading.setGeometry(QtCore.QRect(width(410), int(h * 0.039), int(w * 0.3806), int(h * 0.0651)))
        font = QtGui.QFont()
        font.setPointSize(width(22))
        font.setBold(True)
        font.setWeight(width(75))
        self.heading.setStyleSheet("QLabel{\n\nborder-top: 5px solid black;\nborder-bottom: 5px solid black;\n\n}")
        self.heading.setFont(font)
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setObjectName("heading")
        self.test_detail_box = QtWidgets.QGroupBox(self.centralwidget)
        self.test_detail_box.setEnabled(True)
        self.test_detail_box.setGeometry(QtCore.QRect(width(30), height(150), width(330), height(461)))
        self.font8_BF_UF_50 = QtGui.QFont()
        self.font8_BF_UF_50.setPointSize(width(8))
        self.font8_BF_UF_50.setBold(False)
        self.font8_BF_UF_50.setUnderline(False)
        self.font8_BF_UF_50.setWeight(width(50))
        self.test_detail_box.setStyleSheet(
            "QGroupBox{background-color:rgba(42,58,86,255);color:rgba(255,255,255,255); border-top-right-radius:50px; border-bottom-left-radius:50px; padding-top:10px}")
        self.test_detail_box.setFont(self.font8_BF_UF_50)
        self.test_detail_box.setObjectName("test_detail_box")
        self.test_id = QtWidgets.QLabel(self.test_detail_box)
        self.test_id.setGeometry(QtCore.QRect(width(20), height(60), width(71), height(16)))
        self.font11_BF_UF_50 = QtGui.QFont()
        self.font11_BF_UF_50.setPointSize(width(11))
        self.font11_BF_UF_50.setBold(False)
        self.font11_BF_UF_50.setUnderline(False)
        self.font11_BF_UF_50.setWeight(width(50))
        self.test_id.setStyleSheet("color:rgba(255,255,255,255)")
        self.test_id.setFont(self.font11_BF_UF_50)
        self.test_id.setObjectName("test_id")
        self.system_part_no = QtWidgets.QLabel(self.test_detail_box)
        self.system_part_no.setGeometry(QtCore.QRect(width(20), height(90), width(141), height(16)))
        self.system_part_no.setStyleSheet("color:rgba(255,255,255,255)")
        self.system_part_no.setFont(self.font11_BF_UF_50)
        self.system_part_no.setObjectName("system_part_no")
        self.dut_serial_number = QtWidgets.QLabel(self.test_detail_box)
        self.dut_serial_number.setGeometry(QtCore.QRect(width(20), height(120), width(101), height(16)))
        self.dut_serial_number.setStyleSheet("color:rgba(255,255,255,255)")
        self.dut_serial_number.setFont(self.font11_BF_UF_50)
        self.dut_serial_number.setObjectName("dut_serial_number")
        self.test_id_edit = QtWidgets.QLineEdit(self.test_detail_box)
        self.test_id_edit.setGeometry(QtCore.QRect(width(150), height(60), width(151), height(20)))
        self.test_id_edit.setStyleSheet(
            "QLineEdit\n{\nbackground-color:rgba(0,0,0,0);\nborder:none;\nborder-bottom:2px solid rgba(42,226,230,255);\ncolor:rgba(255,255,255,255);\npadding-bottom:7px;\n}")
        self.test_id_edit.setObjectName("test_id_edit")
        self.test_id_edit.setReadOnly(True)
        self.test_id_edit.setPlaceholderText("Test ID will be shown here")
        self.test_id_edit.setStyleSheet(
            "QLineEdit\n{\nbackground-color:rgba(0,0,0,0);\nborder:none;\nborder-bottom:2px solid rgba(42,226,230,255);\ncolor:rgba(255,255,255,255);\npadding-bottom:7px;\n}")
        self.test_id_edit.setFont(self.font8_BF_UF_50)

        self.system_part_no_edit = QtWidgets.QLineEdit(self.test_detail_box)
        self.system_part_no_edit.setGeometry(QtCore.QRect(width(150), height(90), width(151), height(20)))
        self.system_part_no_edit.setObjectName("system_part_no_edit")
        self.system_part_no_edit.setStyleSheet(
            "QLineEdit\n{\nbackground-color:rgba(0,0,0,0);\nborder:none;\nborder-bottom:2px solid rgba(42,226,230,255);\ncolor:rgba(255,255,255,255);\npadding-bottom:7px;\n}")
        self.system_part_no_edit.setPlaceholderText("System Part Code")
        self.system_part_no_edit.setFont(self.font8_BF_UF_50)
        self.dut_serial_number_edit = QtWidgets.QLineEdit(self.test_detail_box)
        self.dut_serial_number_edit.setGeometry(QtCore.QRect(width(150), height(120), width(151), height(20)))
        self.dut_serial_number_edit.setObjectName("dut_serial_number_edit")
        self.dut_serial_number_edit.setStyleSheet(
            "QLineEdit\n{\nbackground-color:rgba(0,0,0,0);\nborder:none;\nborder-bottom:2px solid rgba(42,226,230,255);\ncolor:rgba(255,255,255,255);\npadding-bottom:7px;\n}")
        self.dut_serial_number_edit.setPlaceholderText("System Serial Number")
        self.dut_serial_number_edit.setFont(self.font8_BF_UF_50)
        self.customer_name = QtWidgets.QLabel(self.test_detail_box)
        self.customer_name.setGeometry(QtCore.QRect(width(20), height(150), width(131), height(16)))
        self.customer_name.setStyleSheet("color:rgba(255,255,255,255)")
        self.customer_name.setFont(self.font11_BF_UF_50)
        self.customer_name.setObjectName("customer_name")
        self.associate_name = QtWidgets.QLabel(self.test_detail_box)
        self.associate_name.setGeometry(QtCore.QRect(width(20), height(180), width(131), height(16)))
        self.associate_name.setStyleSheet("color:rgba(255,255,255,255)")
        self.associate_name.setFont(self.font11_BF_UF_50)
        self.associate_name.setObjectName("associate_name")
        self.associate_name_edit = QtWidgets.QLineEdit(self.test_detail_box)
        self.associate_name_edit.setGeometry(QtCore.QRect(width(150), height(180), width(151), height(20)))
        self.associate_name_edit.setObjectName("associate_name_edit")
        self.associate_name_edit.setStyleSheet(
            "QLineEdit\n{\nbackground-color:rgba(0,0,0,0);\nborder:none;\nborder-bottom:2px solid rgba(42,226,230,255);\ncolor:rgba(255,255,255,255);\npadding-bottom:7px;\n}")
        self.associate_name_edit.setPlaceholderText("Enter Associate Name")
        self.associate_name_edit.setFont(self.font8_BF_UF_50)
        self.customer_name_edit = QtWidgets.QLineEdit(self.test_detail_box)
        self.customer_name_edit.setGeometry(QtCore.QRect(width(150), height(150), width(151), height(20)))
        self.customer_name_edit.setObjectName("customer_name_edit")
        self.customer_name_edit.setReadOnly(True)

        self.customer_name_edit.setStyleSheet(
            "QLineEdit\n{\nbackground-color:rgba(0,0,0,0);\nborder:none;\nborder-bottom:2px solid rgba(42,226,230,255);\ncolor:rgba(255,255,255,255);\npadding-bottom:7px;\n}")
        self.customer_name_edit.setPlaceholderText("Cust. Name will be shown here")

        self.customer_name_edit.setFont(self.font8_BF_UF_50)

        self.start_time_edit = QtWidgets.QLineEdit(self.test_detail_box)
        self.start_time_edit.setGeometry(QtCore.QRect(width(150), height(220), width(151), height(20)))
        self.start_time_edit.setObjectName("start_time_edit")
        self.start_time_edit.setReadOnly(True)

        self.start_time_edit.setStyleSheet(
            "QLineEdit\n{\nbackground-color:rgba(0,0,0,0);\nborder:none;\nborder-bottom:2px solid rgba(42,226,230,255);\ncolor:rgba(255,255,255,255);\npadding-bottom:7px;\n}")
        self.start_time_edit.setPlaceholderText("Start time of test")
        self.start_time_edit.setFont(self.font8_BF_UF_50)

        self.end_time_edit = QtWidgets.QLineEdit(self.test_detail_box)
        self.end_time_edit.setGeometry(QtCore.QRect(width(150), height(250), width(151), height(20)))
        self.end_time_edit.setObjectName("end_time_edit")
        self.end_time_edit.setReadOnly(True)

        self.end_time_edit.setStyleSheet(
            "QLineEdit\n{\nbackground-color:rgba(0,0,0,0);\nborder:none;\nborder-bottom:2px solid rgba(42,226,230,255);\ncolor:rgba(255,255,255,255);\npadding-bottom:7px;\n}")
        self.end_time_edit.setPlaceholderText("End time of test")
        self.end_time_edit.setFont(self.font8_BF_UF_50)

        self.end_time = QtWidgets.QLabel(self.test_detail_box)
        self.end_time.setGeometry(QtCore.QRect(width(20), height(250), width(141), height(16)))
        self.end_time.setStyleSheet("color:rgba(255,255,255,255)")
        self.end_time.setFont(self.font11_BF_UF_50)
        self.end_time.setObjectName("end_time")
        self.start_time = QtWidgets.QLabel(self.test_detail_box)
        self.start_time.setGeometry(QtCore.QRect(width(20), height(220), width(161), height(16)))
        self.start_time.setFont(self.font11_BF_UF_50)
        self.start_time.setObjectName("start_time")
        self.start_time.setStyleSheet("color:rgba(255,255,255,255)")

        self.barcode_check = QtWidgets.QCheckBox(self.test_detail_box)
        self.barcode_check.setGeometry(QtCore.QRect(width(20), height(30), width(91), height(17)))
        self.barcode_check.setObjectName("barcode_check")
        self.barcode_check.setFont(self.font11_BF_UF_50)
        self.barcode_check.setStyleSheet("color:rgba(255,255,255,255)")

        self.previous_output = QtWidgets.QLabel(self.test_detail_box)
        self.previous_output.setGeometry(QtCore.QRect(width(120), height(15), width(120), height(17)))
        self.previous_output.setObjectName("daily_output")
        self.previous_output.setFont(self.font11_BF_UF_50)
        self.previous_output.setStyleSheet("color:rgba(255,255,255,255)")

        self.daily_output = QtWidgets.QLabel(self.test_detail_box)
        self.daily_output.setGeometry(QtCore.QRect(width(230), height(15), width(120), height(17)))
        self.daily_output.setObjectName("daily_output")
        self.daily_output.setFont(self.font11_BF_UF_50)
        self.daily_output.setStyleSheet("color:rgba(255,255,255,255)")

        self.custom_check = QtWidgets.QCheckBox(self.test_detail_box)
        self.custom_check.setGeometry(QtCore.QRect(width(20), height(300), width(141), height(21)))
        self.custom_check.setFont(self.font11_BF_UF_50)
        self.custom_check.setStyleSheet("color:rgba(255,255,255,255)")
        self.custom_check.setObjectName("custom_check")
        # self.custom_check.setCheckState(True)
        self.custom_check.setChecked(True)
        self.manual_checkbox = QtWidgets.QCheckBox(self.test_detail_box)
        self.manual_checkbox.setGeometry(QtCore.QRect(width(165), height(300), width(151), height(21)))
        # self.manual_checkbox.setStyleSheet("QCheckBox::indicator { width: 50px; height: 50px;}")
        self.manual_checkbox.setFont(self.font11_BF_UF_50)
        self.manual_checkbox.setStyleSheet("color:rgba(255,255,255,255)")
        self.manual_checkbox.setObjectName("manual_checkbox")
        self.start = QtWidgets.QPushButton(self.test_detail_box)
        self.start.setGeometry(QtCore.QRect(width(0), height(335), width(330), height(41)))
        font = QtGui.QFont()
        font.setPointSize(width(15))
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(width(75))
        self.start.setStyleSheet(
            "QPushButton{\nbackground-color:rgba(42,226,230,255);\nfont: 75 25pt 'MS Shell Dlg 2';\nborder-bottom-left-radius:0px;\n}\nQPushButton::hover{\nfont: 75 35pt 'MS Shell Dlg 2';\nbackground-color:rgba(42,226,230,255);\n}\nQPushButton::pressed{\nfont: 75 35pt 'MS Shell Dlg 2';\nbackground-color:rgba(42,226,230,255);\npadding-top:10px;\n}")
        self.start.setFont(font)
        # self.start.setToolTip("Starts the test")
        self.start.setObjectName("start")
        self.stop = QtWidgets.QPushButton(self.test_detail_box)
        self.stop.setGeometry(QtCore.QRect(width(0), height(390), width(330), height(41)))
        font = QtGui.QFont()
        font.setPointSize(width(15))
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(width(75))
        self.stop.setFont(font)
        self.stop.setObjectName("stop")
        self.stop.setStyleSheet(
            "QPushButton{\nbackground-color:rgba(42,226,230,255);\nfont: 75 25pt 'MS Shell Dlg 2';\nborder-bottom-left-radius:5fpx;\n}\nQPushButton::hover{\nfont: 75 35pt 'MS Shell Dlg 2';\nbackground-color:rgba(42,226,230,255);\n}\nQPushButton::pressed{\nfont: 75 35pt 'MS Shell Dlg 2';\nbackground-color:rgba(42,226,230,255);\npadding-top:10px;\n}")

        """
        FONT FOR TEST ITEM GROUP BOX
        """

        self.font11_UF = QtGui.QFont()
        self.font11_UF.setPointSize(width(9))
        self.font11_UF.setUnderline(False)

        self.test_item_box = QtWidgets.QGroupBox(self.centralwidget)
        self.test_item_box.setGeometry(QtCore.QRect(width(410), height(105), width(521), height(566)))
        self.test_item_box.setFont(self.font11_BF_UF_50)
        self.test_item_box.setStyleSheet(
            "QGroupBox{border:5px solid black; border-top-left-radius:80px; border-bottom-right-radius:80px; border-top-right-radius:8px; border-bottom-left-radius:8px;}")
        self.test_item_box.setObjectName("test_item_box")
        self.test_item_label = QtWidgets.QLabel(self.test_item_box)
        self.test_item_label.setGeometry(QtCore.QRect(width(70), height(50), width(101), height(16)))
        self.test_item_label.setFont(self.font11_UF)
        self.test_item_label.setObjectName("test_item_label")
        self.status_label = QtWidgets.QLabel(self.test_item_box)
        self.status_label.setGeometry(QtCore.QRect(width(430), height(50), width(61), height(21)))
        self.status_label.setFont(self.font11_UF)
        self.status_label.setObjectName("status_label")
        self.serial_label = QtWidgets.QLabel(self.test_item_box)
        self.serial_label.setGeometry(QtCore.QRect(width(10), height(50), width(41), height(16)))
        self.serial_label.setFont(self.font11_UF)
        self.serial_label.setObjectName("serial_label")
        self.serial1 = QtWidgets.QLabel(self.test_item_box)
        self.serial1.setGeometry(QtCore.QRect(width(20), height(80), width(21), height(31)))
        self.serial1.setFont(self.font11_UF)
        self.serial1.setObjectName("serial1")
        self.controller_health_label = QtWidgets.QLabel(self.test_item_box)
        self.controller_health_label.setGeometry(QtCore.QRect(width(70), height(85), width(121), height(21)))
        self.controller_health_label.setFont(self.font11_UF)
        self.controller_health_label.setObjectName("controller_health_label")
        self.controller_health_status = QtWidgets.QLabel(self.test_item_box)
        self.controller_health_status.setGeometry(QtCore.QRect(width(430), height(80), width(61), height(31)))
        self.controller_health_status.setFont(self.font11_UF)
        self.controller_health_status.setObjectName("controller_health_status")
        self.serial2 = QtWidgets.QLabel(self.test_item_box)
        self.serial2.setGeometry(QtCore.QRect(width(20), height(110), width(21), height(31)))
        self.serial2.setObjectName("serial2")
        self.serial2.setFont(self.font11_UF)
        self.serial3 = QtWidgets.QLabel(self.test_item_box)
        self.serial3.setGeometry(QtCore.QRect(width(20), height(140), width(21), height(31)))
        self.serial3.setObjectName("serial3")
        self.serial3.setFont(self.font11_UF)
        self.serial4 = QtWidgets.QLabel(self.test_item_box)
        self.serial4.setGeometry(QtCore.QRect(width(20), height(170), width(21), height(31)))
        self.serial4.setObjectName("serial4")
        self.serial4.setFont(self.font11_UF)
        self.serial5 = QtWidgets.QLabel(self.test_item_box)
        self.serial5.setGeometry(QtCore.QRect(width(20), height(200), width(21), height(31)))
        self.serial5.setObjectName("serial5")
        self.serial5.setFont(self.font11_UF)
        self.serial6 = QtWidgets.QLabel(self.test_item_box)
        self.serial6.setGeometry(QtCore.QRect(width(20), height(230), width(21), height(31)))
        self.serial6.setObjectName("serial6")
        self.serial6.setFont(self.font11_UF)
        self.serial7 = QtWidgets.QLabel(self.test_item_box)
        self.serial7.setGeometry(QtCore.QRect(width(20), height(260), width(21), height(31)))
        self.serial7.setObjectName("serial7")
        self.serial7.setFont(self.font11_UF)
        self.serial8 = QtWidgets.QLabel(self.test_item_box)
        self.serial8.setGeometry(QtCore.QRect(width(20), height(290), width(21), height(31)))
        self.serial8.setObjectName("serial8")
        self.serial8.setFont(self.font11_UF)
        self.serial9 = QtWidgets.QLabel(self.test_item_box)
        self.serial9.setGeometry(QtCore.QRect(width(20), height(320), width(21), height(31)))
        self.serial9.setObjectName("serial9")
        self.serial9.setFont(self.font11_UF)
        self.serial10 = QtWidgets.QLabel(self.test_item_box)
        self.serial10.setGeometry(QtCore.QRect(width(20), height(350), width(21), height(31)))
        self.serial10.setObjectName("serial10")
        self.serial10.setFont(self.font11_UF)
        self.serial11 = QtWidgets.QLabel(self.test_item_box)
        self.serial11.setGeometry(QtCore.QRect(width(20), height(380), width(21), height(31)))
        self.serial11.setObjectName("serial11")
        self.serial11.setFont(self.font11_UF)
        self.unit_comm_label = QtWidgets.QLabel(self.test_item_box)
        self.unit_comm_label.setGeometry(QtCore.QRect(width(70), height(110), width(141), height(31)))
        self.unit_comm_label.setFont(self.font11_UF)
        self.unit_comm_label.setObjectName("unit_comm_label")
        self.temp_label = QtWidgets.QLabel(self.test_item_box)
        self.temp_label.setGeometry(QtCore.QRect(width(70), height(140), width(191), height(31)))
        self.temp_label.setFont(self.font11_UF)
        self.temp_label.setObjectName("temp_label")
        self.output_pfc_label = QtWidgets.QLabel(self.test_item_box)
        self.output_pfc_label.setGeometry(QtCore.QRect(width(70), height(170), width(121), height(31)))
        self.output_pfc_label.setFont(self.font11_UF)
        self.output_pfc_label.setObjectName("output_pfc_label")
        self.input_pfc_label = QtWidgets.QLabel(self.test_item_box)
        self.input_pfc_label.setGeometry(QtCore.QRect(width(70), height(200), width(121), height(31)))
        self.input_pfc_label.setFont(self.font11_UF)
        self.input_pfc_label.setObjectName("input_pfc_label")
        self.dc_voltage_check_label = QtWidgets.QLabel(self.test_item_box)
        self.dc_voltage_check_label.setGeometry(QtCore.QRect(width(70), height(230), width(171), height(31)))
        self.dc_voltage_check_label.setFont(self.font11_UF)
        self.dc_voltage_check_label.setObjectName("dc_voltage_check_label")
        self.dc_voltage_calib_label = QtWidgets.QLabel(self.test_item_box)
        self.dc_voltage_calib_label.setGeometry(QtCore.QRect(width(70), height(260), width(241), height(31)))
        self.dc_voltage_calib_label.setFont(self.font11_UF)
        self.dc_voltage_calib_label.setObjectName("dc_voltage_calib_label")
        self.dc_current_check_discharge_label = QtWidgets.QLabel(self.test_item_box)
        self.dc_current_check_discharge_label.setGeometry(QtCore.QRect(width(70), height(290), height(251), height(31)))
        self.dc_current_check_discharge_label.setFont(self.font11_UF)
        self.dc_current_check_discharge_label.setObjectName("dc_current_check_discharge_label")
        self.smr_register_label = QtWidgets.QLabel(self.test_item_box)
        self.smr_register_label.setGeometry(QtCore.QRect(width(70), height(320), width(121), height(31)))
        self.smr_register_label.setFont(self.font11_UF)
        self.smr_register_label.setObjectName("smr_register_label")
        self.dc_current_check_charge_label = QtWidgets.QLabel(self.test_item_box)
        self.dc_current_check_charge_label.setGeometry(QtCore.QRect(width(70), height(350), width(241), height(31)))
        self.dc_current_check_charge_label.setFont(self.font11_UF)
        self.dc_current_check_charge_label.setObjectName("dc_current_check_charge_label")
        self.dc_current_calib_label = QtWidgets.QLabel(self.test_item_box)
        self.dc_current_calib_label.setGeometry(QtCore.QRect((width(70)), height(380), width(241), height(31)))
        self.dc_current_calib_label.setFont(self.font11_UF)
        self.dc_current_calib_label.setObjectName("dc_current_calib_label")
        self.lvd_label = QtWidgets.QLabel(self.test_item_box)
        self.lvd_label.setGeometry(QtCore.QRect(width(70), height(410), width(111), height(31)))
        self.lvd_label.setFont(self.font11_UF)
        self.lvd_label.setObjectName("lvd_label")
        self.ac_phase_label = QtWidgets.QLabel(self.test_item_box)
        self.ac_phase_label.setGeometry(QtCore.QRect(width(70), height(440), width(131), height(31)))
        self.ac_phase_label.setFont(self.font11_UF)
        self.ac_phase_label.setObjectName("ac_phase_label")
        self.current_sharing_label = QtWidgets.QLabel(self.test_item_box)
        self.current_sharing_label.setGeometry(QtCore.QRect(width(70), height(470), width(181), height(31)))
        self.current_sharing_label.setFont(self.font11_UF)
        self.current_sharing_label.setObjectName("current_sharing_label")
        self.rs485_label = QtWidgets.QLabel(self.test_item_box)
        self.rs485_label.setGeometry(QtCore.QRect(width(70), height(500), width(71), height(31)))
        self.rs485_label.setFont(self.font11_UF)
        self.rs485_label.setObjectName("rs485_label")
        self.default_label = QtWidgets.QLabel(self.test_item_box)
        self.default_label.setGeometry(QtCore.QRect(width(70), height(530), width(61), height(31)))
        self.default_label.setFont(self.font11_UF)
        self.default_label.setObjectName("default_label")
        self.serial12 = QtWidgets.QLabel(self.test_item_box)
        self.serial12.setGeometry(QtCore.QRect(width(20), height(410), width(21), height(31)))
        self.serial12.setObjectName("serial12")
        self.serial12.setFont(self.font11_UF)
        self.serial13 = QtWidgets.QLabel(self.test_item_box)
        self.serial13.setGeometry(QtCore.QRect(width(20), height(440), width(21), height(31)))
        self.serial13.setObjectName("serial13")
        self.serial13.setFont(self.font11_UF)
        self.serial14 = QtWidgets.QLabel(self.test_item_box)
        self.serial14.setGeometry(QtCore.QRect(width(20), height(470), width(21), height(31)))
        self.serial14.setObjectName("serial14")
        self.serial14.setFont(self.font11_UF)
        self.serial15 = QtWidgets.QLabel(self.test_item_box)
        self.serial15.setGeometry(QtCore.QRect(width(20), height(500), width(21), height(31)))
        self.serial15.setObjectName("serial15")
        self.serial15.setFont(self.font11_UF)
        self.serial16 = QtWidgets.QLabel(self.test_item_box)
        self.serial16.setGeometry(QtCore.QRect(width(20), height(530), width(21), height(31)))
        self.serial16.setObjectName("serial16")
        self.serial16.setFont(self.font11_UF)
        self.unit_comm_status = QtWidgets.QLabel(self.test_item_box)
        self.unit_comm_status.setGeometry(QtCore.QRect(width(430), height(110), width(61), height(31)))
        self.unit_comm_status.setFont(self.font11_UF)
        self.unit_comm_status.setObjectName("unit_comm_status")
        self.temp_status = QtWidgets.QLabel(self.test_item_box)
        self.temp_status.setGeometry(QtCore.QRect(width(430), height(140), width(61), height(31)))
        self.temp_status.setFont(self.font11_UF)
        self.temp_status.setObjectName("temp_status")
        self.output_pfc_status = QtWidgets.QLabel(self.test_item_box)
        self.output_pfc_status.setGeometry(QtCore.QRect(width(430), height(170), width(61), height(31)))
        self.output_pfc_status.setFont(self.font11_UF)
        self.output_pfc_status.setObjectName("output_pfc_status")
        self.input_pfc_status = QtWidgets.QLabel(self.test_item_box)
        self.input_pfc_status.setGeometry(QtCore.QRect(width(430), height(200), width(61), height(31)))
        self.input_pfc_status.setFont(self.font11_UF)
        self.input_pfc_status.setObjectName("input_pfc_status")
        self.dc_voltage_check_status = QtWidgets.QLabel(self.test_item_box)
        self.dc_voltage_check_status.setGeometry(QtCore.QRect(width(430), height(230), width(61), height(31)))
        self.dc_voltage_check_status.setFont(self.font11_UF)
        self.dc_voltage_check_status.setObjectName("dc_voltage_check_status")
        self.dc_voltage_calib_status = QtWidgets.QLabel(self.test_item_box)
        self.dc_voltage_calib_status.setGeometry(QtCore.QRect(width(430), height(260), width(61), height(31)))
        self.dc_voltage_calib_status.setFont(self.font11_UF)
        self.dc_voltage_calib_status.setObjectName("dc_voltage_calib_status")
        self.dc_current_check_discharge_status = QtWidgets.QLabel(self.test_item_box)
        self.dc_current_check_discharge_status.setGeometry(QtCore.QRect(width(430), height(290), width(61), height(31)))
        self.dc_current_check_discharge_status.setFont(self.font11_UF)
        self.dc_current_check_discharge_status.setObjectName("dc_current_check_discharge_status")
        self.smr_register_status = QtWidgets.QLabel(self.test_item_box)
        self.smr_register_status.setGeometry(QtCore.QRect(width(430), height(320), width(61), height(31)))
        self.smr_register_status.setFont(self.font11_UF)
        self.smr_register_status.setObjectName("smr_register_status")
        self.dc_current_check_charge_status = QtWidgets.QLabel(self.test_item_box)
        self.dc_current_check_charge_status.setGeometry(QtCore.QRect(width(430), height(350), width(61), height(31)))
        self.dc_current_check_charge_status.setFont(self.font11_UF)
        self.dc_current_check_charge_status.setObjectName("dc_current_check_charge_status")
        self.dc_current_calib_status = QtWidgets.QLabel(self.test_item_box)
        self.dc_current_calib_status.setGeometry(QtCore.QRect(width(430), height(380), width(61), height(31)))
        self.dc_current_calib_status.setFont(self.font11_UF)
        self.dc_current_calib_status.setObjectName("dc_current_calib_status")
        self.lvd_status = QtWidgets.QLabel(self.test_item_box)
        self.lvd_status.setGeometry(QtCore.QRect(width(430), height(410), width(61), height(31)))
        self.lvd_status.setFont(self.font11_UF)
        self.lvd_status.setObjectName("lvd_status")
        self.ac_phase_status = QtWidgets.QLabel(self.test_item_box)
        self.ac_phase_status.setGeometry(QtCore.QRect(width(430), height(440), width(61), height(31)))
        self.ac_phase_status.setFont(self.font11_UF)
        self.ac_phase_status.setObjectName("ac_phase_status")
        self.current_sharing_status = QtWidgets.QLabel(self.test_item_box)
        self.current_sharing_status.setGeometry(QtCore.QRect(width(430), height(470), width(61), height(31)))
        self.current_sharing_status.setFont(self.font11_UF)
        self.current_sharing_status.setObjectName("current_sharing_status")
        self.default_status = QtWidgets.QLabel(self.test_item_box)
        self.default_status.setGeometry(QtCore.QRect(width(430), height(530), width(61), height(31)))
        self.default_status.setFont(self.font11_UF)
        self.default_status.setObjectName("default_status")
        self.rs485_status = QtWidgets.QLabel(self.test_item_box)
        self.rs485_status.setGeometry(QtCore.QRect(width(430), height(500), width(61), height(31)))
        self.rs485_status.setFont(self.font11_UF)
        self.rs485_status.setObjectName("rs485_status")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(width(980), height(80), width(341), height(481)))
        self.frame.setObjectName("frame_window")
        self.frame.setStyleSheet(
            "QFrame {\nborder-top-right-radius: 50px;\nbackground-color:rgba(240,240,240,255);\nborder-bottom-right-radius: 50px;\n}\n")

        self.log_window = QtWidgets.QTextBrowser(self.frame)
        self.log_window.setGeometry(QtCore.QRect(width(0), height(0), width(341), height(481)))
        self.log_window.setObjectName("log_window")
        self.log_window.setFont(self.font8_BF_UF_50)
        self.log_window.setStyleSheet(
            "QTextBrowser{\nborder:2px solid black;\nborder-top-left-radius:20px;\nborder-top-right-radius:20px;\nborder-bottom-left-radius:20px;\nborder-bottom-right-radius:20px;\n}")
        self.test_log = QtWidgets.QLabel(self.centralwidget)
        self.test_log.setGeometry(QtCore.QRect(width(985), height(42), width(101), height(41)))
        self.test_log.setFont(self.font11_BF_UF_50)
        self.test_log.setOpenExternalLinks(True)
        self.test_log.setObjectName("test_log")

        self.report = QtWidgets.QLabel(self.centralwidget)
        self.report.setGeometry(QtCore.QRect(width(1120), height(40), width(130), height(41)))
        self.report.setFont(self.font11_BF_UF_50)
        self.report.setStyleSheet("QLabel{color:Blue;}")
        self.report.mousePressEvent = self.report_function
        self.report.setObjectName("test_log")

        self.log_clear = QtWidgets.QPushButton(self.centralwidget)
        self.log_clear.setGeometry(QtCore.QRect(width(1240), height(50), width(75), height(23)))
        self.log_clear.setFont(self.font8_BF_UF_50)
        self.log_clear.setStyleSheet(
            "QPushButton{\nbackground-color:rgba(42,226,230,255);\nborder-bottom-left-radius:0px;border:2px solid black;\n"
            "border-top-left-radius:15px;border-bottom-right-radius:15px;}QPushButton::pressed{padding-top:5px;}")

        self.log_clear.setObjectName("log_clear")
        # self.final_status_box = QtWidgets.QGroupBox(self.centralwidget)
        # self.final_status_box.setGeometry(QtCore.QRect(width(980), height(580), width(341), height(71)))
        # self.final_status_box.setTitle("")
        # self.final_status_box.setObjectName("final_status_box")
        self.final_status = QtWidgets.QLabel(self.centralwidget)
        self.final_status.setGeometry(QtCore.QRect(width(980), height(580), width(341), height(71)))
        font = QtGui.QFont()
        font.setPointSize(width(28))
        font.setBold(True)
        font.setWeight(width(75))
        self.final_status.setFont(font)
        self.final_status.setStyleSheet("QLabel{border:5px solid black; border-radius:40px;}")
        self.final_status.setScaledContents(True)
        self.final_status.setAlignment(QtCore.Qt.AlignCenter)
        self.final_status.setObjectName("final_status")
        self.ate_logo = QtWidgets.QLabel(self.centralwidget)
        self.ate_logo.setGeometry(QtCore.QRect(width(70), height(50), width(251), height(71)))
        self.ate_logo.setText("")
        self.ate_logo.setPixmap(QtGui.QPixmap(f"{gui_global.image_directory_location}exicome logo.png"))
        self.ate_logo.setScaledContents(True)
        # self.ate_logo.setStyleSheet("QLabel{border:2px solid black; border-bottom-right-radius:50px; border-top-left-radius:50px}")
        self.ate_logo.setAlignment(QtCore.Qt.AlignCenter)
        self.ate_logo.setObjectName("ate_logo")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        try:
            test_mode = SettingRead('TEST MODE')['test_mode']
            if test_mode == "test":
                self.system_part_no_edit.setText("HE518800")
                self.dut_serial_number_edit.setText("123456789012345")
                self.associate_name_edit.setText("paras")
        except Exception:
            pass

        self.prompt = Prompt()
        self.M2000 = M2000.M2000CommandSet()
        self.M1KLC = M1KLC.M1KLC()
        self.pfc = PFC_control_done.pfc_control()
        self.contact = PFC_control_done.pfc_control()

        self.dcload = CommandSetDcLoadUsb
        self.smrcan = CommandSetSmrBatteryCan

        # CanModule.CAN.CAN_WRITE_SOLO(CanModule.CAN, 0, 0x208, [0x60B, 0, 0, 43, 00, 32, 00, 00, 20, 00, 00])

        self.start.clicked.connect(self.start_thread)
        self.stop.clicked.connect(self.stop_thread)

        self.thread1 = QThread()
        self.worker = Worker(self.start_function)

        # Move the worker to the thread
        self.worker.moveToThread(self.thread1)

        # Connect signals
        self.worker.started_signal.connect(self.start_function)
        self.worker.finished_signal.connect(self.stop_function)
        self.worker.log_signal.connect(self.update_log)
        self.worker.result_signal.connect(self.update_result)

        self.test_executed = False
        self.retranslateUi(MainWindow)
        date = OutputRead('TEST ID')['pre_date']
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        if datetime.date.today() > date:
            print("welcome to new day")
            config.read(f"{gui_global.files_directory_location}output.txt")
            SectionCall = config['TEST ID']
            print(datetime.date.today())
            SectionCall['previous_count'] = str(OutputRead('TEST ID')['today_count'])
            SectionCall['today_count'] = '0'
            SectionCall['pre_date'] = str(datetime.date.today())
            with open(f"{gui_global.files_directory_location}output.txt", 'w') as configfile:
                config.write(configfile)
        else:
            print("welcome")
        self.previous_output.setText(f"Previous: {OutputRead('TEST ID')['previous_count']}")
        self.pass_count_today = int(OutputRead('TEST ID')['today_count']) if OutputRead('TEST ID')[
                                                                                 'today_count'] != '0' else 0
        self.daily_output.setText(f"Today: {self.pass_count_today}")
        QtWidgets.qApp.processEvents()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        global ate_name
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", ""))
        self.heading.setText(_translate("MainWindow", "Production ATS"))
        self.test_detail_box.setTitle(_translate("MainWindow", ""))
        self.previous_output.setText(_translate("MainWindow", "Previous Day:"))
        self.daily_output.setText(_translate("MainWindow", "Today:"))
        self.test_id.setText(_translate("MainWindow", "Test ID"))
        self.system_part_no.setText(_translate("MainWindow", "System Part No."))
        self.dut_serial_number.setText(_translate("MainWindow", "DUT Serial No."))
        self.customer_name.setText(_translate("MainWindow", "Customer Name"))
        self.associate_name.setText(_translate("MainWindow", "Associate Name"))
        self.end_time.setText(_translate("MainWindow", "End Time"))
        self.start_time.setText(_translate("MainWindow", "Start Time"))
        self.barcode_check.setText(_translate("MainWindow", "Bar Code"))
        self.custom_check.setText(_translate("MainWindow", "Custom Settings"))
        self.manual_checkbox.setText(_translate("MainWindow", "Manual Resources"))
        self.start.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.start.setText(_translate("MainWindow", "START"))
        self.stop.setText(_translate("MainWindow", "STOP"))
        self.test_item_box.setTitle(_translate("MainWindow", "Test Program"))
        self.test_item_label.setText(_translate("MainWindow", "Test Item"))
        self.status_label.setText(_translate("MainWindow", "Status"))
        self.serial_label.setText(_translate("MainWindow", "S No."))
        self.serial1.setText(_translate("MainWindow", "1"))
        self.controller_health_label.setText(_translate("MainWindow", "ATE Initialization"))
        self.controller_health_status.setText(_translate("MainWindow", "Pending"))
        self.serial2.setText(_translate("MainWindow", "2"))
        self.serial3.setText(_translate("MainWindow", "3"))
        self.serial4.setText(_translate("MainWindow", "4"))
        self.serial5.setText(_translate("MainWindow", "5"))
        self.serial6.setText(_translate("MainWindow", "6"))
        self.serial7.setText(_translate("MainWindow", "7"))
        self.serial8.setText(_translate("MainWindow", "8"))
        self.serial9.setText(_translate("MainWindow", "9"))
        self.serial10.setText(_translate("MainWindow", "10"))
        self.serial11.setText(_translate("MainWindow", "11"))
        self.unit_comm_label.setText(_translate("MainWindow", "DUT Communication"))
        self.temp_label.setText(_translate("MainWindow", "Temperature Measurement"))
        self.output_pfc_label.setText(_translate("MainWindow", "Output PFC"))
        self.input_pfc_label.setText(_translate("MainWindow", "Input PFC"))
        self.dc_voltage_check_label.setText(_translate("MainWindow", "DC Voltage Measurement"))
        self.dc_voltage_calib_label.setText(_translate("MainWindow", "DC Voltage Calibration/Verification"))
        self.dc_current_check_discharge_label.setText(_translate("MainWindow", "DC Current Measurement (Discharge)"))
        self.smr_register_label.setText(_translate("MainWindow", "SMR Registration"))
        self.dc_current_check_charge_label.setText(_translate("MainWindow", "DC Current Measurement (Charge)"))
        self.dc_current_calib_label.setText(_translate("MainWindow", "DC Current Calibration/Verification"))
        self.lvd_label.setText(_translate("MainWindow", "LVD Contactor"))
        self.ac_phase_label.setText(_translate("MainWindow", "AC Phase Allocation"))
        self.current_sharing_label.setText(_translate("MainWindow", "Current Sharing / Bus Drop"))
        self.rs485_label.setText(_translate("MainWindow", "RS485"))
        self.default_label.setText(_translate("MainWindow", "Default"))
        self.serial12.setText(_translate("MainWindow", "12"))
        self.serial13.setText(_translate("MainWindow", "13"))
        self.serial14.setText(_translate("MainWindow", "14"))
        self.serial15.setText(_translate("MainWindow", "15"))
        self.serial16.setText(_translate("MainWindow", "16"))
        self.unit_comm_status.setText(_translate("MainWindow", "Pending"))
        self.temp_status.setText(_translate("MainWindow", "Pending"))
        self.output_pfc_status.setText(_translate("MainWindow", "Pending"))
        self.input_pfc_status.setText(_translate("MainWindow", "Pending"))
        self.dc_voltage_check_status.setText(_translate("MainWindow", "Pending"))
        self.dc_voltage_calib_status.setText(_translate("MainWindow", "Pending"))
        self.dc_current_check_discharge_status.setText(_translate("MainWindow", "Pending"))
        self.smr_register_status.setText(_translate("MainWindow", "Pending"))
        self.dc_current_check_charge_status.setText(_translate("MainWindow", "Pending"))
        self.dc_current_calib_status.setText(_translate("MainWindow", "Pending"))
        self.lvd_status.setText(_translate("MainWindow", "Pending"))
        self.ac_phase_status.setText(_translate("MainWindow", "Pending"))
        self.current_sharing_status.setText(_translate("MainWindow", "Pending"))
        self.default_status.setText(_translate("MainWindow", "Pending"))
        self.rs485_status.setText(_translate("MainWindow", "Pending"))
        self.test_log.setText(
            _translate("MainWindow", f"<a href='file:D:\\ATE-{SettingRead('STATION')['id']}\\logs'>Log Folder</a>"))
        self.report.setText(_translate("MainWindow", "Reports"))
        self.log_clear.setText(_translate("MainWindow", "Log Clear"))
        self.final_status.setText(_translate("MainWindow", ""))
        self.start.setToolTip(_translate("MainWindow", "Starts the test"))

        # self.dcload.DC_LOAD.OPEN_DC_LOAD(self.dcload.DC_LOAD)
        # self.dcload.DC_LOAD_SET_CURRENT_CC(5)

    def dut_serial_check(self):
        global customer_name
        self.associate_name_edit.setText(self.associate_name_edit.text().upper())
        self.system_part_no_edit.setText(self.system_part_no_edit.text().upper())
        self.dut_serial_number_edit.setText(self.dut_serial_number_edit.text().upper())
        self.associate_name = self.associate_name_edit.text()
        self.part_number = self.system_part_no_edit.text()
        self.serial_number = self.dut_serial_number_edit.text()
        name_check = False
        part_check = False
        serial_check = False
        if self.associate_name == "":
            self.prompt.Message("Error!", "Kindly enter NAME to proceed!", 0)
        else:
            name_check = True
            if self.part_number == "":
                self.prompt.Message("Error!", "Kindly enter HE-Part Code", 0)
            else:
                if len(self.part_number) == 8:
                    with open(f"{gui_global.files_directory_location}customer_detail.csv", 'r') as file:
                        lines = file.readlines()
                    not_found = True
                    self.config_version_list = []
                    for i in lines:
                        if self.part_number == i.split(",")[0]:
                            not_found = False
                            self.customer_name = i.split(",")[2]
                            self.config_version_list.append(float(i.split(",")[1]))
                            self.mcm_type = i.split(",")[3].split("\n")[0]
                            if self.mcm_type == "M1000":
                                self.mcm_type = 1
                            elif self.mcm_type == "M2000":
                                self.mcm_type = 2
                            elif self.mcm_type == "M1000_LC":
                                self.mcm_type = 3
                                break
                            print(f"Type of MCM is: {self.mcm_type}")
                    if not_found:
                        self.prompt.Message("Warning!", "HE Part Code not found in Database!")
                    else:
                        self.customer_name_edit.setText(str(self.customer_name))
                        part_check = True
                        if self.serial_number == "":
                            self.prompt.Message("Error!", "Kindly enter/ scan system serial number", 0)
                        else:
                            if len(self.serial_number) == 15:
                                serial_check = True
                            else:
                                self.prompt.Message("Warning!", "Kindly enter correct length of Serial Number", 0)
                else:
                    self.prompt.Message("Warning!", "Kindly enter correct length of Part Code", 0)

        if name_check and serial_check and part_check:
            self.test_id_edit.setText(SettingRead("TEST ID")['count'])
            self.configversion = max(self.config_version_list)
            count = int(float(self.test_id_edit.text())) + 1
            config.read(f"{gui_global.files_directory_location}setting.txt")
            SectionCall = config['TEST ID']
            for option in SectionCall:
                SectionCall[option] = str(count)

            with open(f"{gui_global.files_directory_location}setting.txt", 'w') as configfile:
                config.write(configfile)

            self.start_time_edit.setText(str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            return True
        else:
            return False


    def initials(self):
        self.final_status.setText("")
        self.final_status.setStyleSheet("QLabel{border:5px solid black; border-radius:40px;}")
        self.controller_health_status.setText("Pending")
        self.controller_health_status.setStyleSheet("")
        self.unit_comm_status.setText("Pending")
        self.unit_comm_status.setStyleSheet("")
        self.temp_status.setText("Pending")
        self.temp_status.setStyleSheet("")
        self.output_pfc_status.setText("Pending")
        self.output_pfc_status.setStyleSheet("")
        self.input_pfc_status.setText("Pending")
        self.input_pfc_status.setStyleSheet("")
        self.dc_voltage_check_status.setText("Pending")
        self.dc_voltage_calib_status.setText("Pending")
        self.dc_voltage_check_status.setStyleSheet("")
        self.dc_voltage_calib_status.setStyleSheet("")
        self.dc_current_check_discharge_status.setText("Pending")
        self.dc_current_check_discharge_status.setStyleSheet("")
        self.smr_register_status.setText("Pending")
        self.smr_register_status.setStyleSheet("")
        self.dc_current_check_charge_status.setText("Pending")
        self.dc_current_check_charge_status.setStyleSheet("")
        self.dc_current_calib_status.setText("Pending")
        self.dc_current_calib_status.setStyleSheet("")
        self.lvd_status.setText("Pending")
        self.lvd_status.setStyleSheet("")
        self.ac_phase_status.setText("Pending")
        self.ac_phase_status.setStyleSheet("")
        self.current_sharing_status.setText("Pending")
        self.current_sharing_status.setStyleSheet("")
        self.rs485_status.setText("Pending")
        self.rs485_status.setStyleSheet("")
        self.default_status.setText("Pending")
        self.default_status.setStyleSheet("")
        self.end_time_edit.clear()
        self.log_window.clear()
        gui_global.communication_lost = False
        gui_global.telnet_connection_not_restablished = False

    def test_detail_clear(self):
        self.test_id_edit.clear()
        self.system_part_no_edit.clear()
        self.dut_serial_number_edit.clear()
        self.customer_name_edit.clear()
        self.associate_name_edit.clear()

    def start_thread(self):
        """Start the thread and execute the function"""
        self.thread1.started.connect(self.worker.run)
        self.thread1.start()
        self.start.setDisabled(True)  # Disable the start button

    def stop_thread(self):
        """Stop the thread"""
        self.worker.stop_function()  # Stop the worker
        self.thread1.quit()  # Quit the thread
        self.start.setEnabled(True)  # Enable the start button

    def start_function(self):
        try:
            """
            This function starts and handles the test script with final result status, Log and Report Creation

            final_output: list ==> shows test cases result, initially BLANK
            test_detail_flag: bool ==> Result of details in Test Details Box are correctly filled
            testing_flag: bool ==> signifies the status of IS TESTING ACTIVE, initially TRUE
            """
            self.start.setDisabled(True)
            global final_output
            testing_flag = True
            # CanModule.CAN.CAN_WRITE_SOLO(CanModule.CAN, 0, 0x208, [0x60B, 0, 0, 43, 00, 32, 00, 1, 18, 00, 00])

            # CanModule.CAN.CAN_WRITE_SOLO(CanModule.CAN, 0, 0x208, [0x60B, 0, 0, 43, 00, 32, 00, 1, 48, 00, 00])
            test_detail_flag = self.dut_serial_check()

            if test_detail_flag:
                '''Set the initials to default before starting the testing'''
                self.initials()
                if getpass.getuser() == "paras.mittal":
                    pass
                else:
                    blue_off()
                    green_on()
                    red_off()
                    relay_on()
                    self.serial_number_filled()
                    self.pfc.pfc_set(0, 'pfc 2', 1)
                self.test_order = test_order_done.Ui_Form.get_values(test_order_done.Ui_Form)
                # self.physical_check(BYPASS=True)
                self.prompt.Message(prompt="Switch OFF Load MCBs/ Battery MCBs/ Remove Fuses/ SMR MCBs")

                self.print_console(f'DUT PART NUMBER: {self.part_number}')
                self.print_console(f'DUT SERIAL NUMBER: {self.serial_number}')
                self.print_console(f'CUSTOMER NAME: {self.customer_name_edit.text()}')
                if self.part_number == "HE517553" or self.part_number == "HE517610":
                    self.print_console(f"SOFTWARE VERSION: {self.configversion}")
                else:
                    self.print_console(f"CONFIGURATION FILE VERSION: {self.configversion}")
                self.print_console(f"TEST START DATE TIME: {get_date_time(date=1, time=1)}")
                self.print_console(f"ASSOCIATE NAME: {self.associate_name_edit.text()}")

                '''Starting testing'''
                self.excel_handler = CSVHandler(os.path.join(gui_global.directory_location + "/records/", "active_" + str(SettingRead("STATION")['id']) + ".csv"))
                value = self.excel_handler.get_last_row_first_column_value() or "0"
                value = value if value != "SR NO" else "0"
                last_cell = int(value) + 1
                bulk_upload = [str(last_cell)] + ["FAIL"] * (len(self.excel_handler.get_headers()) - 1)
                self.config_load = None
                self.file_present = False
                self.excel_handler.append_row(bulk_upload)
                self.excel_handler.update_cell("TEST DATE", str(get_date_time(1, 0)))
                self.excel_handler.update_cell("CUSTOMER NAME", self.customer_name_edit.text())
                self.excel_handler.update_cell("PART NUMBER", self.part_number)
                self.excel_handler.update_cell("SERIAL NUMBER", self.serial_number)
                self.excel_handler.update_cell("CONFIG VERSION", self.configversion)
                self.excel_handler.update_cell("OPERATOR", self.associate_name_edit.text())
                self.excel_handler.update_cell("START TEST TIME", str(get_date_time(1, 1)))
                self.all_stop = False
                blue_off()

                while testing_flag:
                    final_output = []
                    self.block_test = set()
                    for i in range(1, 17):
                        function_status = ''
                        green_on()
                        self.test_retryCount = 0
                        for j in range(1, 5):
                            self.test_retryCount += 1
                            if self.all_stop:
                                testing_flag = False
                                break
                            function_status = self.run_test1(i)  # Running test sequences
                            if function_status == "NA":
                                break
                            elif function_status == True:
                                break
                            else:
                                if self.all_stop:
                                    testing_flag = False
                                    break
                                user_response = self.prompt.User_prompt("Do you want to retry this test?", 1, 100)
                                if user_response:
                                    pass
                                else:
                                    function_status = False
                                    break
                        if function_status:
                            final_output.append(function_status)
                        else:
                            if self.all_stop:
                                testing_flag = False
                                final_output.append(function_status)
                                break
                            user_response = self.prompt.User_prompt("Do you want to skip\nthis test and continue?", 1, 100)
                            if user_response:
                                testing_flag = True
                                final_output.append(function_status)
                            else:
                                final_output.append(function_status)
                                testing_flag = False
                                break
                    if self.all_stop:
                        break
                    if i == 16:
                        testing_flag = False
                        break
                # Handle final status and reporting
                console_output_flag = True
                for results in final_output:
                    if results == False:
                        console_output_flag = False
                if all(final_output):
                    self.final_status.setText("PASS")
                    self.excel_handler.update_cell("RESULT", "PASS")
                else:
                    self.final_status.setText("FAIL")
                    self.excel_handler.update_cell("RESULT", "FAIL")

                self.end_time_edit.setText(str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
                self.upload_log_on_server(self.filename)
                self.pfc.pfc_set(0, 'pfc 2', 0)
            else:
                self.prompt.Message("Error!", "Kindly complete Test Details", 0)
            try:
                self.excel_handler.update_cell("END TEST TIME", str(get_date_time(1, 1)))  # add here
            except Exception as e:
                print((e))
            CanModule.CAN.CAN_WRITE_SOLO(CanModule.CAN, 0, 0x208, [0x60B, 0, 0, 43, 00, 32, 00, 00, 20, 00, 00])
        except Exception as e:
            print(str(e))
        finally:
            self.start.setDisabled(False)
            self.stop_function()

    def stop_function(self):
        """This function runs when the test stops"""
        self.final_status.setText("Test Aborted")
        self.log_console.append("Test stopped.")
        self.end_time_edit.setText(str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

    def update_log(self, message):
        self.log_console.append(message)  # Update the log in the UI

    def update_result(self, result):
        self.final_status.setText(result)  # Update the result in the UI

    def serial_number_filled(self):
        serial_number = self.dut_serial_number_edit.text()
        if len(serial_number) == 15:
            pass
        elif len(serial_number) == 24:
            self.dut_serial_number_edit.setText(serial_number.split("#")[1])
            self.system_part_no_edit.setText(serial_number.split("#")[0])
        time.sleep(0.1)
        QtWidgets.qApp.processEvents()

    def start_function(self):
        try:
            """
            This function starts and handles the test script with final result status, Log and Report Creation
    
            final_output: list ==> shows test cases result, initially BLANK
            test_detail_flag: bool ==> Result of details in Test Details Box are correctly filled
            testing_flag: bool ==> signifies the status of IS TESTING ACTIVE, initially TRUE
            """
            self.start.setDisabled(True)
            global final_output
            testing_flag = True
            # CanModule.CAN.CAN_WRITE_SOLO(CanModule.CAN, 0, 0x208, [0x60B, 0, 0, 43, 00, 32, 00, 1, 18, 00, 00])

            # CanModule.CAN.CAN_WRITE_SOLO(CanModule.CAN, 0, 0x208, [0x60B, 0, 0, 43, 00, 32, 00, 1, 48, 00, 00])
            test_detail_flag = self.dut_serial_check()

            if test_detail_flag:
                '''Set the initials to default before starting the testing'''
                self.initials()
                if getpass.getuser() == "paras.mittal":
                    pass
                else:
                    blue_off()
                    green_on()
                    red_off()
                    relay_on()
                    self.serial_number_filled()
                    self.pfc.pfc_set(0, 'pfc 2', 1)
                self.test_order = test_order_done.Ui_Form.get_values(test_order_done.Ui_Form)
                # self.physical_check(BYPASS=True)
                self.prompt.Message(prompt="Switch OFF Load MCBs/ Battery MCBs/ Remove Fuses/ SMR MCBs")

                self.print_console(f'DUT PART NUMBER: {self.part_number}')
                self.print_console(f'DUT SERIAL NUMBER: {self.serial_number}')
                self.print_console(f'CUSTOMER NAME: {self.customer_name_edit.text()}')
                if self.part_number == "HE517553" or self.part_number == "HE517610":
                    self.print_console(f"SOFTWARE VERSION: {self.configversion}")
                else:
                    self.print_console(f"CONFIGURATION FILE VERSION: {self.configversion}")
                self.print_console(f"TEST START DATE TIME: {get_date_time(date=1, time=1)}")
                self.print_console(f"ASSOCIATE NAME: {self.associate_name_edit.text()}")

                print(f"Test detail flag: {test_detail_flag}")  # Shows Boolean expression of test_detail_flag

                '''Starting testing'''
                self.excel_handler = CSVHandler(os.path.join(gui_global.directory_location + "/records/",
                                                             "active_" + str(SettingRead("STATION")['id']) + ".csv"))
                value = self.excel_handler.get_last_row_first_column_value() or "0"
                value = value if value != "SR NO" else "0"
                # Incrementing the value by 1
                last_cell = int(value) + 1

                # Generating bulk upload data
                bulk_upload = [str(last_cell)] + ["FAIL"] * (len(self.excel_handler.get_headers()) - 1)
                self.config_load = None
                self.file_present = False
                self.excel_handler.append_row(bulk_upload)
                # self.excel_handler.update_cell("SR NO", str(value))
                self.excel_handler.update_cell("TEST DATE", str(get_date_time(1, 0)))
                self.excel_handler.update_cell("CUSTOMER NAME", self.customer_name_edit.text())
                self.excel_handler.update_cell("PART NUMBER", self.part_number)
                self.excel_handler.update_cell("SERIAL NUMBER", self.serial_number)
                self.excel_handler.update_cell("CONFIG VERSION", self.configversion)
                self.excel_handler.update_cell("OPERATOR", self.associate_name_edit.text())
                self.excel_handler.update_cell("START TEST TIME", str(get_date_time(1, 1)))
                self.all_stop = False
                blue_off()
                while testing_flag:
                    final_output = []
                    self.block_test = set()
                    for i in range(1, 17):
                        function_status = ''
                        """
                        Buffer command for Tower Light
                        """
                        # CanModule.CAN.CAN_WRITE_SOLO(CanModule.CAN, 0, 0x208, [0x60B, 0, 0, 43, 00, 32, 00, 1, 18, 00, 00])
                        green_on()
                        self.test_retryCount = 0
                        for j in range(1, 5):
                            self.test_retryCount += 1
                            if self.all_stop:
                                testing_flag = False
                                break
                            function_status = self.run_test1(i)  # Running test sequences

                            print(
                                f"Test Number {i} : {function_status}")  # Display the status of the last function block tested
                            if function_status == "NA":
                                break
                            elif function_status == True:
                                break
                            else:
                                if self.all_stop:
                                    testing_flag = False
                                    break
                                user_response = self.prompt.User_prompt("Do you want to retry this test?", 1, 100)
                                if user_response:
                                    pass
                                else:
                                    function_status = False
                                    break

                        '''Keeping/ Storing the status of last function block tested'''

                        if function_status:
                            final_output.append(function_status)

                        else:
                            if self.all_stop:
                                testing_flag = False
                                final_output.append(function_status)
                                break
                            user_response = self.prompt.User_prompt("Do you want to skip\nthis test and continue?", 1, 100)
                            if user_response:
                                testing_flag = True
                                final_output.append(function_status)
                            else:
                                final_output.append(function_status)
                                testing_flag = False
                                break  # terminating test loop if USER wishes not to continue the test

                        if self.all_stop:
                            break
                        '''Terminating test loop when all tests are performed'''
                        if i == 16:
                            testing_flag = False
                            print(final_output)
                            break

                console_output_flag = True
                for results in final_output:
                    if results == False:
                        console_output_flag = False

                if all(final_output):
                    self.final_status.setText("PASS")
                    # self.final_status.setStyleSheet("QLabel{border:5px solid black; border-radius:40px;}")
                    self.final_status.setFont(QtGui.QFont("Calibri", 60))
                    self.final_status.setStyleSheet("QLabel{border:5px solid black; border-radius:40px;color:DARKGREEN;}")
                    self.excel_handler.update_cell("RESULT", "PASS")
                    self.dut_serial_number_edit.setText("")
                    self.system_part_no_edit.setText("")
                    self.pass_count_today += 1
                    config.read(f"{gui_global.files_directory_location}output.txt")
                    SectionCall = config['TEST ID']
                    # for option in SectionCall:
                    SectionCall['today_count'] = str(self.pass_count_today)
                    SectionCall['pre_date'] = str(datetime.date.today())

                    with open(f"{gui_global.files_directory_location}output.txt", 'w') as configfile:
                        config.write(configfile)
                    self.daily_output.setText(f"Today: {self.pass_count_today}")

                    self.report_generate()

                else:
                    if len(final_output) != 16:
                        self.final_status.setText("ABORTED")
                    else:
                        self.final_status.setText("FAIL")
                    # self.final_status.setStyleSheet("QLabel{border:5px solid black; border-radius:40px;}")
                    self.final_status.setFont(QtGui.QFont("Calibri", 60))
                    self.final_status.setStyleSheet("QLabel{border:5px solid black; border-radius:40px;color:RED;}")
                    self.excel_handler.update_cell("RESULT", "FAIL")
                self.shadowFunction(self.final_status, (0, 0, 0, 255), 35, (10, 10))

                self.end_time_edit.setText(str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

                self.upload_log_on_server(self.filename)
                # self.thread1.terminate()
                self.pfc.pfc_set(0, 'pfc 2', 0)
            else:
                self.prompt.Message("Error!", "Kindly complete Test Details", 0)
            try:
                self.excel_handler.update_cell("END TEST TIME", str(get_date_time(1, 1)))  # add here
            except Exception as e:
                print((e))
            CanModule.CAN.CAN_WRITE_SOLO(CanModule.CAN, 0, 0x208, [0x60B, 0, 0, 43, 00, 32, 00, 00, 20, 00, 00])
        except RuntimeError as err:
            print(err, type(err))
            self.print_console("CAN ERROR ERROR OCCURRED...")
        except TypeError as e:
            print(str(e))
        except AttributeError as e:
            print(str(e))
        except FileNotFoundError as e:
            print(str(e))
        except ZeroDivisionError as e:
            print(str(e))
            self.print_console("MCM COMM ERROR")
        except can.interfaces.ixxat.exceptions as err:
            print(err)
        except Exception as err:
            print(err)
            print(f'Type of error is : {type(err)}')
        finally:
            self.start.setDisabled(False)
            print("test done")
            self.stop_function()
            print('im exiting')
            if gui_global.test_stop:
                self.pfc.pfc_set(0, 'pfc 2', 0)


    def report_generate(self):
        '''
                        GENERATING REPORT AFTER RACK BEING PASSED ONLY
                        '''

        from reportlab.pdfgen import canvas
        from pdfCreation import generateReport

        fileName = str(self.part_number.upper()) + "#" + str(
            self.serial_number.upper()) + "_" + "PASS" + ".pdf"
        if os.path.exists(rf'D:\ATE-{str(SettingRead("STATION")["id"])}\reports'):
            pass
        else:
            os.chdir("D:")
            if os.path.exists(rf'D:\ATE-{str(SettingRead("STATION")["id"])}'):
                pass
            else:
                os.makedirs(f'ATE-{str(SettingRead("STATION")["id"])}\\reports')

        fileName = os.path.join(rf'D:\ATE-{str(SettingRead("STATION")["id"])}\reports', fileName)
        ARR = os.listdir(rf'D:\ATE-{str(SettingRead("STATION")["id"])}\reports')
        if fileName[11:] in ARR:
            pass
        else:
            c = canvas.Canvas(fileName)
            par = [self.customer_name_edit.text().upper(),
                   self.part_number.upper(),
                   self.serial_number.upper(),
                   str(self.configversion), self.mac_id.upper(),
                   self.associate_name_edit.text().upper(), "",
                   self.start_time_edit.text(),
                   "PASS", "PASS", "PASS", "PASS", "PASS",
                   "PASS", "PASS", "PASS", "PASS", "PASS",
                   "PASS", "PASS", "PASS", "PASS", "PASS", "PASS"] + self.left_over_list + ['PASS']
            generateReport(c, parameters=par)
            c.showPage()
            c.save()

        '''
        PORTION ENDS HERE
        '''

    def shadowFunction(self, element, colors_alpha=(0, 0, 0, 0), blurRadius=0, offset=(0, 0)):
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(blurRadius)
        effect.setColor(QColor(colors_alpha[0], colors_alpha[1], colors_alpha[2], colors_alpha[3]))
        effect.setOffset(offset[0], offset[1])
        element.setGraphicsEffect(effect)

    def run_test1(self, test_number):
        list_of_test = ['ATE INITIALIZATION', 'UNIT COMMUNICATION', 'TEMPERATURE MEASUREMENT',
                        'OUTPUT PFC', 'INPUT PFC',
                        'DC VOLTAGE MEASUREMENT', 'DC VOLTAGE CALIBRATION/VERIFICATION',
                        'DC CURRENT MEASUREMENT (DISCHARGE)', 'SMR REGISTRATION',
                        'DC CURRENT MEASUREMENT (CHARGE)', 'DC CURRENT CALIBRATION/VERIFICATION',
                        'LVD CONTACTOR', 'AC PHASE ALLOCATION', 'CURRENT SHARING / BUS DROP',
                        'RS485', 'DEFAULT']
        status_variables = [self.controller_health_status, self.unit_comm_status, self.temp_status,
                            self.output_pfc_status, self.input_pfc_status, self.dc_voltage_check_status,
                            self.dc_voltage_calib_status, self.dc_current_check_discharge_status,
                            self.smr_register_status, self.dc_current_check_charge_status, self.dc_current_calib_status,
                            self.lvd_status, self.ac_phase_status, self.current_sharing_status, self.rs485_status,
                            self.default_status]
        test_functions = [self.physical_check, self.CARD_COMMUNICATION, self.TEMPERATURE_MEASUREMENT, self.OP_PFC_CHECK,
                          self.IP_PFC_CHECK, self.DC_VOLTAGE_MEASUREMENT, self.CALIBRATE_DC_VOLTAGE,
                          self.DC_CURRENT_MEASUREMENT_BATT_DISCHARGE, self.SMR_REGISTRATION,
                          self.DC_CURRENT_MEASUREMENT_BATT_CHARGE, self.CALIBRATE_DC_CURRENT, self.LVD_CONTACTOR_CHECK,
                          self.PHASE_ALLOCATION, self.CURRENT_SHARING, self.RS_485_CHECK, self.DEFAULT_SETTING]
        Excel_values = ['ATE INITIALIZATION', 'UNIT COMMUNICATION', 'TEMPERATURE', "OUTPUT/INPUT PFC",
                        "OUTPUT/INPUT PFC", 'DC VOLTAGE', 'DC VOLTAGE CALIBRATION', 'DC CURRENT',
                        'SMR REGISTRATION', 'DC CURRENT CALIBRATION', 'DC CURRENT CALIBRATION', 'LVD',
                        'AC PHASE ALLOCATION', 'DC CURRENT SHARING/ BUS DROP', 'RS-485',
                        'DEFAULT SETTING']

        NEW_BLOCK = [' TEST BLOCK COUNT', ' TEST BLOCK START TIME', ' TEST BLOCK END TIME']

        self.test_order = TestOrder('TEST ORDER')
        self.test_order = list(self.test_order.values())
        for i in range(16):
            file_present = None
            if self.file_present:
                pass
            else:
                for config_create_count in range(1, 3):
                    for filename in os.listdir(f'{gui_global.files_directory_location}test_config'):
                        print(os.path.splitext(os.path.basename(filename))[0], self.part_number)
                        if os.path.splitext(os.path.basename(filename))[0].upper() == str(self.part_number).upper():
                            file_present = True
                            break
                        else:
                            file_present = False

                    if file_present:
                        self.config_load = xml_generator.xml_reader(self.part_number)
                        if self.config_load:
                            print("length of list is ", len(self.config_load))
                            if len(self.config_load) == 39:
                                file_present = True
                            else:
                                self.prompt.Message(prompt="Recipe has been updated, kindly make new file")
                                self.print_console("Test Configuration for this Product is not updated!", "RED")
                                config_create_count += 1
                                Dialog = QtWidgets.QDialog()
                                ui = xml_generator.Ui_Recipe()
                                ui.setupUi(Dialog)
                                Dialog.exec_()
                                self.print_console("Test Configuration Creation attempted!")
                        break
                    else:
                        self.prompt.Message(prompt="NO Test Configuration Available, Contact Support Person!", buzzer=0)
                        # self.all_stop = True
                        self.print_console("Test Configuration for this Product is not available!", "RED")
                        config_create_count += 1
                        Dialog = QtWidgets.QDialog()
                        ui = xml_generator.Ui_Dialog()
                        ui.setupUi(Dialog)
                        Dialog.exec_()
                        self.print_console("Test Configuration Creation attempted!")

                if not self.config_load:
                    self.print_console("Test Configuration Creation attempt FAILED!", "RED")
                    return

            test_name = list_of_test[int(self.test_order[i]) - 1].upper()
            print(int(test_number), int(TestOrder('TEST ORDER')[test_name.lower()]), test_name)
            if int(test_number) == int(TestOrder('TEST ORDER')[test_name.lower()]):
                if TestOrder('TEST STATE')[test_name.lower()] == "YES":
                    current_time = str(datetime.datetime.now())
                    if test_name not in self.block_test:
                        self.block_test.add(test_name)
                        self.excel_handler.update_cell(test_name + str(NEW_BLOCK[1]), current_time)
                    else:
                        pass
                    self.print_console('Start Time for test: ' + str(test_name) + " :: " + current_time)
                    self.excel_handler.update_cell(test_name + str(NEW_BLOCK[0]), self.test_retryCount)
                    self.setStatus(status_variables[list_of_test.index(test_name)], 2)
                    result_variable = test_functions[list_of_test.index(test_name)]()
                    self.setStatus(status_variables[list_of_test.index(test_name)],
                                   header=Excel_values[list_of_test.index(test_name)])
                    if result_variable:
                        self.setStatus(status_variables[list_of_test.index(test_name)], 1,
                                       Excel_values[list_of_test.index(test_name)])

                    self.print_console('End Time for test: ' + str(test_name) + " :: " + str(datetime.datetime.now()))
                    self.excel_handler.update_cell(test_name + str(NEW_BLOCK[2]), str(datetime.datetime.now()))
                    return result_variable
                else:
                    self.print_console(test_name + "Test has been By-PASSED")
                    self.setStatus(status_variables[list_of_test.index(test_name)], 3,
                                   Excel_values[list_of_test.index(test_name)])
                    return "NA"
            else:
                pass

        return False

    def run_test(self, test_number):

        list_of_test = [self.controller_health_label.text(), self.unit_comm_label.text(), self.temp_label.text(),
                        self.output_pfc_label.text(), self.input_pfc_label.text(),
                        self.dc_voltage_check_label.text(), self.dc_voltage_calib_label.text(),
                        self.dc_current_check_discharge_label.text(), self.smr_register_label.text(),
                        self.dc_current_calib_label.text(), self.dc_current_check_charge_label.text(),
                        self.lvd_label.text(), self.ac_phase_label.text(), self.current_sharing_label.text(),
                        self.default_label.text()]

        test_name = list_of_test[int(test_number) - 1].upper()

        if test_number == int(self.test_order[0]):
            if TestOrder('TEST STATE')[test_name.lower()] == "YES":
                self.setStatus(self.controller_health_status, 2)
                # controller_health_check_variable = self.prompt.User_prompt("Do you want to pass this test and continue?")
                controller_health_check_variable = self.physical_check(BYPASS=False)
                self.setStatus(self.controller_health_status, header="ATE INITIALIZATION")
                if controller_health_check_variable:
                    self.setStatus(self.controller_health_status, 1, "ATE INITIALIZATION")
                return controller_health_check_variable
            else:
                self.print_console(test_name + "Test has been By-PASSED")
                self.setStatus(self.controller_health_status, 3, "ATE INITIALIZATION")
                return "NA"
        elif test_number == int(self.test_order[1]):
            if TestOrder('TEST STATE')[test_name.lower()] == "YES":
                self.setStatus(self.unit_comm_status, 2)
                # unit_comm_variable = self.prompt.User_prompt("Do you want to pass this test and continue?")
                unit_comm_variable = self.CARD_COMMUNICATION()
                self.setStatus(self.unit_comm_status, header="COMMUNICATION TEST")
                if unit_comm_variable:
                    self.setStatus(self.unit_comm_status, 1, "COMMUNICATION TEST")
                return unit_comm_variable
            else:
                self.print_console(test_name + " Test has not been assigned for testing!")
                self.setStatus(self.unit_comm_status, 3, "COMMUNICATION TEST")
                return "NA"
        elif test_number == int(self.test_order[2]):
            if TestOrder('TEST STATE')[test_name.lower()] == "YES":
                self.setStatus(self.temp_status, 2)
                # temp_variable = self.prompt.User_prompt("Do you want to pass this test and continue?")
                temp_variable = self.TEMPERATURE_MEASUREMENT()
                self.setStatus(self.temp_status, header="TEMPERATURE TEST")
                if temp_variable:
                    self.setStatus(self.temp_status, 1, "TEMPERATURE TEST")
                return temp_variable
            else:
                self.print_console(test_name + " Test has not been assigned for testing!")
                self.setStatus(self.unit_comm_status, 3, "TEMPERATURE TEST")
                return "NA"
        elif test_number == int(self.test_order[3]):
            self.setStatus(self.output_pfc_status, 2)
            # out_pfc_variable = self.prompt.User_prompt("Do you want to pass this test and continue?")
            out_pfc_variable = self.OP_PFC_CHECK()
            self.excel_handler.update_cell("OUTPUT/INPUT PFC", "FAIL")
            self.setStatus(self.output_pfc_status)
            if out_pfc_variable:
                self.setStatus(self.output_pfc_status, 1)
                self.excel_handler.update_cell("OUTPUT/INPUT PFC", "PASS")
            return out_pfc_variable
        elif test_number == int(self.test_order[4]):
            self.setStatus(self.input_pfc_status, 2)
            # input_pfc_variable = self.prompt.User_prompt("Do you want to pass this test and continue?")
            input_pfc_variable = self.IP_PFC_CHECK()
            self.setStatus(self.input_pfc_status)
            self.excel_handler.update_cell("OUTPUT/INPUT PFC", "FAIL")
            if input_pfc_variable:
                self.setStatus(self.input_pfc_status, 1)
                self.excel_handler.update_cell("OUTPUT/INPUT PFC", "PASS")
            return input_pfc_variable
        elif test_number == int(self.test_order[5]):
            self.setStatus(self.dc_voltage_check_status, 2)
            # dc_voltage_check = self.prompt.User_prompt("Do you want to pass this test and continue?")
            dc_voltage_check = self.DC_VOLTAGE_MEASUREMENT()
            self.setStatus(self.dc_voltage_check_status)
            self.excel_handler.update_cell("DC VOLTAGE TEST", "FAIL")
            if dc_voltage_check:
                self.setStatus(self.dc_voltage_check_status, 1)
                self.excel_handler.update_cell("DC VOLTAGE TEST", "PASS")
            return dc_voltage_check
        elif test_number == int(self.test_order[6]):
            self.setStatus(self.dc_voltage_calib_status, 2)
            # dc_voltage_calib_variable = self.prompt.User_prompt("Do you want to pass this test and continue?")
            dc_voltage_calib_variable = self.CALIBRATE_DC_VOLTAGE()
            self.excel_handler.update_cell("DC VOLTAGE CALIBRATION", "FAIL")
            self.setStatus(self.dc_voltage_calib_status)
            if dc_voltage_calib_variable:
                self.setStatus(self.dc_voltage_calib_status, 1)
                self.excel_handler.update_cell("DC VOLTAGE CALIBRATION", "PASS")
            return dc_voltage_calib_variable
        elif test_number == int(self.test_order[7]):
            self.setStatus(self.dc_current_check_discharge_status, 2)
            # dc_current_discharge_variable = self.prompt.User_prompt("Do you want to pass this test and continue?")
            dc_current_discharge_variable = self.DC_CURRENT_MEASUREMENT_BATT_DISCHARGE()
            self.setStatus(self.dc_current_check_discharge_status)
            self.excel_handler.update_cell("DC CURRENT TEST", "FAIL")
            if dc_current_discharge_variable:
                self.setStatus(self.dc_current_check_discharge_status, 1)
                self.excel_handler.update_cell("DC CURRENT TEST", "PASS")
            return dc_current_discharge_variable
        elif test_number == int(self.test_order[8]):
            self.setStatus(self.smr_register_status, 2)
            # smr_registration_variable = self.prompt.User_prompt("Do you want to pass this test and continue?")
            smr_registration_variable = self.SMR_REGISTRATION()
            self.setStatus(self.smr_register_status)
            self.excel_handler.update_cell("SMR REGISTRATION TEST", "FAIL")
            if smr_registration_variable:
                self.setStatus(self.smr_register_status, 1)
                self.excel_handler.update_cell("SMR REGISTRATION TEST", "PASS")
            return smr_registration_variable
        elif test_number == int(self.test_order[9]):
            # dc_current_charge_variable = self.prompt.User_prompt("Do you want to pass this test and continue?")
            dc_current_charge_variable = self.DC_CURRENT_MEASUREMENT_BATT_CHARGE()
            # self.setStatus(self.dc_current_check_charge_status)
            self.excel_handler.update_cell("DC CURRENT CALIBRATION", "FAIL")
            if dc_current_charge_variable:
                self.setStatus(self.dc_current_check_charge_status, 1)
                self.excel_handler.update_cell("DC CURRENT CALIBRATION", "PASS")
            return dc_current_charge_variable
        elif test_number == int(self.test_order[10]):
            self.setStatus(self.dc_current_calib_status, 2)
            # dc_current_calib_variable = self.prompt.User_prompt("Do you want to pass this test and continue?")
            dc_current_calib_variable = self.CALIBRATE_DC_CURRENT()
            self.excel_handler.update_cell("DC CURRENT CALIBRATION", "FAIL")
            if dc_current_calib_variable:
                self.setStatus(self.dc_current_calib_status, 1)
                self.excel_handler.update_cell("DC CURRENT CALIBRATION", "PASS")
            return dc_current_calib_variable
        elif test_number == int(self.test_order[11]):
            self.setStatus(self.lvd_status, 2)
            # lvd_variable = self.prompt.User_prompt("Do you want to pass this test and continue?")
            lvd_variable = self.LVD_CONTACTOR_CHECK()
            self.excel_handler.update_cell("LVD TEST", "FAIL")
            if lvd_variable:
                self.setStatus(self.lvd_status, 1)
                self.excel_handler.update_cell("LVD TEST", "PASS")
            return lvd_variable
        elif test_number == int(self.test_order[12]):
            self.setStatus(self.ac_phase_status, 2)
            # ac_phase_variable = self.prompt.User_prompt("Do you want to pass this test and continue?")
            ac_phase_variable = self.PHASE_ALLOCATION()
            self.excel_handler.update_cell("AC PHASE ALLOCATION TEST", "FAIL")
            if ac_phase_variable:
                self.setStatus(self.ac_phase_status, 1)
                self.excel_handler.update_cell("AC PHASE ALLOCATION TEST", "PASS")
            return ac_phase_variable
        elif test_number == int(self.test_order[13]):
            self.setStatus(self.current_sharing_status, 2)
            # current_sharing_variable = self.prompt.User_prompt("Do you want to pass this test and continue?")
            current_sharing_variable = self.CURRENT_SHARING()
            self.excel_handler.update_cell("DC CURRENT SHARING/ BUS DROP TEST", "FAIL")
            if current_sharing_variable:
                self.setStatus(self.current_sharing_status, 1)
                self.excel_handler.update_cell("DC CURRENT SHARING/ BUS DROP TEST", "PASS")
            return current_sharing_variable
        elif test_number == int(self.test_order[14]):
            self.setStatus(self.rs485_status, 2)
            # rs485_variable = self.prompt.User_prompt("Do you want to pass this test and continue?")
            rs485_variable = self.RS_485_CHECK
            self.excel_handler.update_cell("RS-485 TEST", "FAIL")
            if rs485_variable:
                self.setStatus(self.rs485_status, 1)
                self.excel_handler.update_cell("RS-485 TEST", "PASS")
            return rs485_variable
        elif test_number == int(self.test_order[15]):
            self.setStatus(self.default_status, 2)
            # default_variable = self.prompt.User_prompt("Do you want to pass this test and continue?")
            default_variable = self.DEFAULT_SETTING()
            self.excel_handler.update_cell("DEFAULT SETTING", "FAIL")
            if default_variable:
                self.setStatus(self.default_status, 1)
                self.excel_handler.update_cell("DEFAULT SETTING", "PASS")
            return default_variable
        else:
            return False

    def setStatus(self, element, status=0, header=''):
        value = "FAIL"
        element.setText("FAIL")
        element.setStyleSheet("color:RED")
        if status:
            value = "PASS"
            element.setText("PASS")
            element.setStyleSheet("color:GREEN")
        if status == 2:
            element.setText("Testing...")
            element.setStyleSheet("color:blue")
            self.shadowFunction(element, (0, 0, 0, 255), 25, (0, 0))
        if status == 3:
            value = "NA"
            element.setText("NA")
            element.setStyleSheet("color:grey")
            self.shadowFunction(element, (0, 0, 0, 255), 25, (0, 0))

        if header != '' or value != '':
            self.excel_handler.update_cell(header, value)
        else:
            pass

    def print_console(self, text="", color="BLUE"):
        if color == "RED":
            self.log_window.setTextColor(QtCore.Qt.red)
        elif color == "BLUE":
            self.log_window.setTextColor(QtCore.Qt.blue)
        elif color == "GREEN":
            self.log_window.setTextColor(QtCore.Qt.darkGreen)
        self.log_window.append(str(text).upper())
        QtWidgets.qApp.processEvents()
        time.sleep(0.0001)
        self.log()

    def physical_check(self, BYPASS=False):
        try:
            if BYPASS:
                return True
            else:

                RESULT = []
                self.print_console("PHYSICAL CHECK TEST STARTED...")

                physical_state = self.prompt.User_prompt(
                    "Check the following: \n1. Is all bus-bar/ screws tight?\n2. Is AC/Battery/LOAD/PFC/RS-485(if any) connection tightly done?\n3. Is connection to optional AC MCB is correct?")
                if physical_state:
                    RESULT_TEMP = True
                else:
                    RESULT_TEMP = False
                RESULT.append(RESULT_TEMP)
                final_result = CALCULATE_RESULT(RESULT)
                self.print_console("PHYSICAL CHECK TEST FINISHED....")
                if final_result:
                    self.CLEAR_JIG()
                    self.CHECK_DEVICES()
                    if self.config_load['ate_initialization']:
                        self.INITIALIZE_JIG()
                    if not self.controller_health_method():
                        self.all_stop = True
                        return False
                    self.ConfigureATS()
                return final_result
        except TypeError as e:
            print(str(e))
        except AttributeError as e:
            print(str(e))
        except FileNotFoundError as e:
            print(str(e))
        except can.interfaces.ixxat.exceptions as err:
            print(err)
        except Exception as err:
            print(err)
            print(f'Type of error is : {type(err)}')
        except ZeroDivisionError as err:
            print(f"Handled ZeroDivisionError in outer function: {err}")
            self.all_stop = True
            self.print_console("ERROR IN COMMUNICATING WITH MCM", 'RED')
            self.print_console("STOPPING TEST", 'RED')
            return False

    def report_function(self, event):
        report = QtWidgets.QDialog()
        report.ui = Ui_report()
        report.ui.setupUi(report)
        report.exec_()
        report.show()

    def GETTIME(self):
        time_var = datetime.datetime.now()
        time_var = str(time_var.date()) + "_" + str(time_var.time().hour) + "_" + str(
            time_var.time().minute) + "_" + str(time_var.time().second)
        return time_var

    def log(self):
        global filename, final_status_label
        try:
            import sys
            root, extension = os.path.splitext(os.path.basename(sys.argv[0]))
            """Log Creation"""
            if os.path.exists(rf'D:\ATE-{str(SettingRead("STATION")["id"])}\logs'):
                pass
            else:
                os.chdir("D:")
                if os.path.exists(rf'D:\ATE-{str(SettingRead("STATION")["id"])}'):
                    pass
                else:
                    os.makedirs(f'ATE-{str(SettingRead("STATION")["id"])}\logs')

            formatted_start_time = self.start_time_edit.text()[0:2] + "_" + self.start_time_edit.text()[3:5] + "_" + self.start_time_edit.text()[6:10] + "_" + self.start_time_edit.text()[11:13] + "_" + self.start_time_edit.text()[14:16] + "_" + self.start_time_edit.text()[17:19]
            if self.final_status.text() == "":
                self.final_status.setText("Under Testing...")
                final_status_label = self.final_status.text()
            elif self.final_status.text() == "ABORTED" or self.final_status.text() == "PASS" or self.final_status.text() == "FAIL":
                final_status_label = self.final_status.text()

                os.system(f'ren "{self.filename}" "log_{str(self.part_number).upper()}#{str(self.serial_number).upper()}_{str(self.final_status.text())}_{str(self.associate_name_edit.text()).upper()}_{str(formatted_start_time)}.txt"')

            self.filename = rf"D:\ATE-{str(SettingRead('STATION')['id'])}\\logs\\log_" + str(self.part_number).upper() + "#" + str(
                self.serial_number).upper() + "_" + str(final_status_label) + "_" + str(
                self.associate_name_edit.text()).upper() + "_" + str(formatted_start_time) + '.txt'
            print(final_status_label, self.filename)
            myfile = open(self.filename, 'w')
            myfile.write("DUT SERIAL NUMBER: " + self.dut_serial_number_edit.text().upper())
            myfile.write('\n\n')
            myfile.write(f"DUT PART NUMBER : {self.system_part_no_edit.text().upper()}")
            myfile.write('\n\n')
            myfile.write("Testing Engg. Name: " + self.associate_name_edit.text().upper())
            myfile.write('\n\n')
            myfile.write("ATE Version: " + root)
            myfile.write('\n\n')
            myfile.write(self.log_window.toPlainText())
            if self.test_executed:
                myfile.write('\n')
                myfile.write(f"Test Ended : {self.get_current_datetime()}")
            myfile.close()

        except exception as e:
            print(str(e))

    def upload_log_on_server(self, filename):
        try:
            self.test_executed = True
            self.print_console("Log Saved")
            print(filename)
            shutil.copy(filename,
                        rf'\\slice\Test_Reports_NPI\F3\DCT ATE\DCT ATE {str(SettingRead("STATION")["id"])}\logs_ate_{str(SettingRead("STATION")["id"])}\\')
        except:
            pass

    def get_current_datetime(self):
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_datetime

    def controller_health_method(self):
        try:
            global SITE_ID, RESULT
            self.print_console("ATE Initialization CHECK TEST STARTED...")
            status = False
            retry_count = 0
            self.ipCheck()

            time.sleep(10)

            while not status and retry_count < 40:
                print("statsu :", status, retry_count)
                print(self.mcm_type)
                if self.mcm_type == 2:
                    status = self.M2000.LOGIN_MCM()[0]
                elif self.mcm_type == 1:
                    status = bool(M1000Telnet.open_telnet())
                else:
                    status = self.M1KLC.Login()
                time.sleep(1)
                retry_count += 1
                if retry_count in [5, 10, 15, 20, 25]:
                    self.print_console("Trying to communicate with the MCM, kindly check CABLE Connection!")
                if retry_count == 26:
                    retry_count = 50

                if gui_global.test_stop:
                    return False

            print("final :", status)
            if not status:
                self.print_console("TEST Stopped due to No Communication with MCM", 'RED')
                self.print_console("ATE Initialization Test aborted", 'RED')
                return status
            if self.mcm_type == 2:
                self.mac_id = self.MCM_READ_COMMAND(section='6048', pool=1)
            if self.mcm_type == 3:
                self.mac_id = "NA"
            if self.mcm_type == 1:
                self.mac_id = self.MCM_READ_COMMAND(section='TAB.9017.0', pool=1)
            if status:
                self.TEST_MODE_M1000()

                SITE_ID = self.MCM_READ_COMMAND("SYSTEM CONFIG", 'site id')
                RESULT = []
                if SITE_ID is not None:
                    self.print_console("Controller Healthy")
                    self.excel_handler.update_cell("CONTROLLER TEST", "PASS")
                    RESULT_TEMP = True
                else:
                    self.print_console("Controller OFF")
                    self.excel_handler.update_cell("CONTROLLER TEST", "FAIL")
                    RESULT_TEMP = False

                self.TEST_MODE_M1000()

                RESULT.append(RESULT_TEMP)

            self.print_console("CONTROLLER_HEALTH_CHECK TEST FINISHED.")
            if not status:
                self.print_console("Controller OFF or not communicating", "RED")
                return False
            return CALCULATE_RESULT(RESULT)

        except TypeError as e:

            if gui_global.test_stop:
                self.all_stop = True
                return False

            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except AttributeError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except FileNotFoundError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except ZeroDivisionError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except can.interfaces.ixxat.exceptions as err:
            print(err)
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except Exception as err:
            print(err)
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(f'Type of error is : {type(err)}')
            return False
        except (AllException, AttributeError, RuntimeError) as err:
            print(err)
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            self.all_stop = True
            return False

    def ipCheck(self):
        import subprocess
        import re

        def get_interface_by_ip(target_ip):
            try:
                # Execute the netsh command
                command = "netsh interface ip show ipaddresses"
                result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
                output = result.stdout
                pattern = rf"Interface (\d+): (.*?)\nManual .*?{target_ip}"
                match = re.search(pattern, output, re.IGNORECASE | re.DOTALL)
                if match:
                    interface_name = match.group(2)
                    return interface_name.split("Interface ")[-1].split(": ")[1].split("\n")[0]
                else:
                    print(f"IP address {target_ip} not found.")
                    return None
            except Exception as e:
                print(f"Error executing netsh command: {e}")
                return None

        try:
            if self.mcm_type == 1:
                current_ip = SettingRead('SETTING')['m1000_ip address']
                # port_name = get_interface_by_ip(current_ip[:-1])
                if self.part_number.upper() == "HE531191":
                    if '192.168.100.1' in current_ip:
                        return True
                    else:
                        self.prompt.Message("WARNING", 'KINDLY CHANGE M1000 IP ADDRESS TO <b>\"192.168.100.101\"</b> IN BOTH HARDWARE MANAGEMENT AND IPV4 SETTING\r'
                                                       'IF DONE SO, KINDLY CHECK HARDWARE MANAGEMENT SETTING')
                        self.print_console("STOPPING TEST")
                        self.all_stop = True
                        gui_global.test_stop = True
                        return False
                else:
                    if current_ip == '172.16.66.50':
                        return True
                    else:
                        self.prompt.Message("WARNING", 'KINDLY CHANGE M1000 IP ADDRESS TO <b>\"172.16.66.51\"</b> IN BOTH HARDWARE MANAGEMENT AND IPV4 SETTING\r'
                                                       'IF DONE SO, KINDLY CHECK HARDWARE MANAGEMENT SETTING')
                        self.print_console("STOPPING TEST")
                        self.all_stop = True
                        gui_global.test_stop = True
                        return False
        except TypeError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except AttributeError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except FileNotFoundError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except ZeroDivisionError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except can.interfaces.ixxat.exceptions as err:
            print(err)
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except Exception as err:
            print(err)
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(f'Type of error is : {type(err)}')
            return False
        except (AllException, AttributeError, RuntimeError) as err:
            print(err)
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            self.all_stop = True
            return False

    def RTC_SET(self):
        try:
            self.print_console("RTC SET STARTED...")
            date_time = self.MCM_READ_COMMAND('SYSTEM COMMANDS', 'rtc date')
            print(date_time)
            date_time1 = self.MCM_READ_COMMAND('SYSTEM COMMANDS', 'rtc time')
            print(date_time1)
            # date_time = M1000Telnet.telnet_get_command(OIDRead("SYSTEM COMMANDS")['rtc date time'])
            print("SYSTEM Time and Date: " + str(date_time))
            now = get_date_time(date=1, time=1)
            print(now, now.split(" "))
            date = now.split(" ")[0].split("-")
            time = now.split(" ")[1]
            self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'rtc date', date[0] + '/' + date[1] + '/' + date[2])
            self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'rtc date', time)
            # M1000Telnet.telnet_set_command(OIDRead('SYSTEM COMMANDS')['rtc date time'], now)
            self.print_console("RTC SET COMPLETED...")
        except exception as e:
            print(str(e))

    def INITIALIZE_JIG(self):
        try:
            self.print_console("INITIALIZING JIG TEST STARTED...")
            self.pfc.pfc_set(0, 'pfc 2', 1)
            self.pfc.pfc_set(0, 'battery_mains', 1)
            self.pfc.pfc_set(0, "battery_1", 1)
            self.print_console("INITIALIZING JIG TEST FINISHED....")
        except TypeError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except AttributeError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except FileNotFoundError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except can.interfaces.ixxat.exceptions as err:
            print(err)
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except Exception as err:
            print(err)
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(f'Type of error is : {type(err)}')
            return False
        except (AllException, AttributeError, RuntimeError) as err:
            print(err)
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            self.all_stop = True
            return False


    def ConfigureATS(self):
        try:
            global battery_capacity, bcl_factor
            if self.mcm_type == 1:
                M1000Telnet.telnet_set_command(OIDRead('SYSTEM COMMANDS')['ate test'], "TEST_M1000_ATE")
                # M1000Telnet.telnet_set_command(OIDRead('SYSTEM COMMANDS')['factory restore'], 1)
                # time.sleep(5)
                # M1000Telnet.telnet_set_command(OIDRead('SYSTEM COMMANDS')['system reset'], 1)
                # time.sleep(15)
                # self.print_console("RESET DONE")
                self.print_console("CONFIGURING ATS...")
                config = configparser.ConfigParser()
                cfgfile = open(f"{gui_global.files_directory_location}config.ini", 'w')
                config.add_section("DUT CONFIGURATION")
                if self.custom_check.isChecked():
                    if DefaultRead("DEFAULT SETTING STATE")['max smr count'] == "YES":
                        max_smr_count = int(DefaultRead('DEFAULT SETTING')["max smr count"])
                        M1000Telnet.telnet_set_command(OIDRead('SYSTEM CONFIG')['smr count'], max_smr_count)

                phase_type = int(M1000Telnet.telnet_get_command(OIDRead("SYSTEM CONFIG")['ac phases type']))
                if phase_type == 0:
                    phase_type = 'SINGLE PHASE'
                elif phase_type == 1:
                    phase_type = 'THREE PHASE'
                config.set("DUT CONFIGURATION", 'ac phases type', phase_type)

                battery_fuses_count = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['no. of battery fuses']))
                config.set('DUT CONFIGURATION', 'no. of battery fuses', str(battery_fuses_count))

                battery_lvd_count = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['no. of battery lvd']))
                config.set('DUT CONFIGURATION', 'no. of battery lvd', str(battery_lvd_count))

                load_lvd_count = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['no. of load lvd']))
                config.set('DUT CONFIGURATION', 'no. of load lvd',
                           '0' if self.part_number == "HE518607" else str(load_lvd_count))

                load_current_count = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['no. of load current']))
                config.set('DUT CONFIGURATION', 'no. of load current', str(load_current_count))

                load_current_sensor_state = int(
                    M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['load current sensor']))
                if load_current_sensor_state == 0:
                    load_current_sensor_state = 'DISABLE'
                elif load_current_sensor_state == 1:
                    load_current_sensor_state = 'ENABLE'
                # PRINT_CONSOLE(self,load_current_sensor_state)
                config.set('DUT CONFIGURATION', 'load current sensor', str(load_current_sensor_state))

                dcif_card_state = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['dcif card']))
                if dcif_card_state == 0:
                    dcif_card_state = 'DISABLE'
                elif dcif_card_state == 1:
                    dcif_card_state = 'PRESENT'
                config.set('DUT CONFIGURATION', 'dcif card', str(dcif_card_state))

                dcif_type = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['dcif card type']))
                config.set('DUT CONFIGURATION', 'dcif card type number', str(dcif_type))
                if dcif_type == 0:
                    dcif_type = 'HALL EFFECT'
                    for count in range(1, load_current_count + 1):
                        load_hall_effect_value = int(M1000Telnet.telnet_get_command(
                            OIDRead('SYSTEM CONFIG')['load' + str(count) + ' hall effect value']))
                        config.set('DUT CONFIGURATION', 'channel ' + str(count) + ' hall effect value',
                                   str(load_hall_effect_value))
                    for count in range(load_current_count + 1, load_current_count + battery_lvd_count + 1):
                        batt_hall_effect_value = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')[
                                                                                        'batt' + str(
                                                                                            count - load_current_count) + ' hall effect value']))
                        config.set('DUT CONFIGURATION', 'channel ' + str(count) + ' hall effect value',
                                   str(batt_hall_effect_value))

                elif dcif_type == 1:
                    dcif_type = 'SHUNT'
                    for count in range(1, load_current_count + 1):
                        load_hall_effect_value = int(
                            M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['load' + str(count) + ' shunt value']))
                        config.set('DUT CONFIGURATION', 'channel ' + str(count) + ' shunt value',
                                   str(load_hall_effect_value))
                        load_hall_effect_value = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')[
                                                                                        'load' + str(
                                                                                            count) + ' shunt mv value']))
                        config.set('DUT CONFIGURATION', 'channel ' + str(count) + ' shunt mv value',
                                   str(load_hall_effect_value))
                    for count in range(load_current_count + 1, load_current_count + battery_lvd_count + 1):
                        batt_hall_effect_value = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')[
                                                                                        'batt' + str(
                                                                                            count - load_current_count) + ' shunt value']))
                        config.set('DUT CONFIGURATION', 'channel ' + str(count) + ' shunt value',
                                   str(batt_hall_effect_value))
                        batt_hall_effect_value = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')[
                                                                                        'batt' + str(
                                                                                            count - load_current_count) + ' shunt mv value']))
                        config.set('DUT CONFIGURATION', 'channel ' + str(count) + ' shunt mv value',
                                   str(batt_hall_effect_value))

                elif dcif_type == 2 or dcif_type == 3:  # added dcif type 3 to logic ,17/06/2019
                    dcif_type = 'SHUNT SMALL'
                    for count in range(1, load_current_count + 1):
                        load_hall_effect_value = int(
                            M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['load' + str(count) + ' shunt value']))
                        config.set('DUT CONFIGURATION', 'channel ' + str(count) + ' shunt value',
                                   str(load_hall_effect_value))
                        load_hall_effect_value = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')[
                                                                                        'load' + str(
                                                                                            count) + ' shunt mv value']))
                        config.set('DUT CONFIGURATION', 'channel ' + str(count) + ' shunt mv value',
                                   str(load_hall_effect_value))
                    for count in range(load_current_count + 1, load_current_count + battery_lvd_count + 1):
                        batt_hall_effect_value = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')[
                                                                                        'batt' + str(
                                                                                            count - load_current_count) + ' shunt value']))
                        config.set('DUT CONFIGURATION', 'channel ' + str(count) + ' shunt value',
                                   str(batt_hall_effect_value))
                        batt_hall_effect_value = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')[
                                                                                        'batt' + str(
                                                                                            count - load_current_count) + ' shunt mv value']))
                        config.set('DUT CONFIGURATION', 'channel ' + str(count) + ' shunt mv value',
                                   str(batt_hall_effect_value))

                config.set('DUT CONFIGURATION', 'dcif card type', str(dcif_type))

                hvlv_card_state = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['hvlv card']))
                if hvlv_card_state == 0:
                    hvlv_card_state = 'DISABLE'
                elif hvlv_card_state == 1:
                    hvlv_card_state = 'PRESENT'
                config.set('DUT CONFIGURATION', 'hvlv card', str(hvlv_card_state))

                dcif_ip_card_state = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['dcif ip card']))
                if dcif_ip_card_state == 0:
                    dcif_ip_card_state = 'DISABLE'
                elif dcif_ip_card_state == 1:
                    dcif_ip_card_state = 'PRESENT'
                config.set('DUT CONFIGURATION', 'dcif ip card', str(dcif_ip_card_state))

                dcif_op_card_state = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['dcif op card']))
                if dcif_op_card_state == 0:
                    dcif_op_card_state = 'DISABLE'
                elif dcif_op_card_state == 1:
                    dcif_op_card_state = 'PRESENT'
                config.set('DUT CONFIGURATION', 'dcif op card', str(dcif_op_card_state))

                batt_temperature_state = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['temperature1']))
                if batt_temperature_state == 0:
                    batt_temperature_state = 'DISABLE'
                elif batt_temperature_state == 1:
                    batt_temperature_state = 'PRESENT'
                config.set('DUT CONFIGURATION', 'temperature1', str(batt_temperature_state))

                room_temperature1_state = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['temperature2']))
                if room_temperature1_state == 0:
                    room_temperature1_state = 'DISABLE'
                elif room_temperature1_state == 1:
                    room_temperature1_state = 'PRESENT'
                config.set('DUT CONFIGURATION', 'temperature2', str(room_temperature1_state))

                room_temperature2_state = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['temperature3']))
                if room_temperature2_state == 0:
                    room_temperature2_state = 'DISABLE'
                elif room_temperature2_state == 1:
                    room_temperature2_state = 'PRESENT'
                config.set('DUT CONFIGURATION', 'temperature3', str(room_temperature2_state))

                pfc_io_card_state = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['pfc io card']))
                if pfc_io_card_state == 0:
                    pfc_io_card_state = 'DISABLE'
                elif pfc_io_card_state == 1:
                    pfc_io_card_state = 'PRESENT'
                config.set('DUT CONFIGURATION', 'pfc io card', str(pfc_io_card_state))

                smr_count = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['smr count']))
                config.set('DUT CONFIGURATION', 'smr count', str(smr_count))

                smr_type = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['smr type']))
                if smr_type == 0:
                    smr_type = '100A'
                elif smr_type == 1:
                    smr_type = '3KW'
                elif smr_type == 2:
                    smr_type = '25A'
                config.set('DUT CONFIGURATION', 'smr type', str(smr_type))

                battery_type = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['battery type']))
                if battery_type == 0:
                    battery_type = 'VRLA'
                elif battery_type == 1:
                    battery_type = 'VRLA+LION'
                elif battery_type == 2:
                    battery_type = 'LION'
                config.set('DUT CONFIGURATION', 'battery type', str(battery_type))

                if battery_type == 'VRLA':
                    battery_capacity = int(
                        M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['vrla battery capacity']))
                    bcl_factor = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['vrla bcl factor']))
                if battery_type == 'LION' or battery_type == 'VRLA+LION':
                    battery_capacity = int(
                        M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['lion battery capacity']))
                    bcl_factor = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['lion bcl factor']))
                    module_count = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['lion module count']))
                    config.set('DUT CONFIGURATION', 'lion module count', str(module_count))
                config.set('DUT CONFIGURATION', 'battery capacity', str(battery_capacity))
                config.set('DUT CONFIGURATION', 'bcl factor', str(bcl_factor))

                ac_ip_voltage_source = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['ac ip voltage source']))
                if ac_ip_voltage_source == 1:
                    ac_ip_voltage_source = 'ACIF '
                elif ac_ip_voltage_source == 2:
                    ac_ip_voltage_source = 'HVLV PN'
                elif ac_ip_voltage_source == 3:
                    ac_ip_voltage_source = 'HVLV PP'
                elif ac_ip_voltage_source == 4:
                    ac_ip_voltage_source = 'SMR 1P'
                elif ac_ip_voltage_source == 5:
                    ac_ip_voltage_source = 'SMR 3P'
                config.set('DUT CONFIGURATION', 'ac ip voltage source', str(ac_ip_voltage_source))

                ac_ip_current_source = int(M1000Telnet.telnet_get_command(OIDRead('SYSTEM CONFIG')['ac ip current source']))
                if ac_ip_current_source == 0:
                    ac_ip_current_source = 'NO SENSING '
                elif ac_ip_current_source == 1:
                    ac_ip_current_source = 'ACIF '
                elif ac_ip_current_source == 2:
                    ac_ip_current_source = 'HVLV PN'
                elif ac_ip_current_source == 3:
                    ac_ip_current_source = 'HVLV PP'
                elif ac_ip_current_source == 4:
                    ac_ip_current_source = 'SMR 1P'
                elif ac_ip_current_source == 5:
                    ac_ip_current_source = 'SMR 3P'
                config.set('DUT CONFIGURATION', 'ac ip current source', str(ac_ip_current_source))

                lower_port_baudrate = int(M1000Telnet.telnet_get_command(OIDRead('RS 485')['lower port baudrate']))
                config.set('DUT CONFIGURATION', 'lower port baudrate', str(lower_port_baudrate))

                upper_port_baudrate = int(M1000Telnet.telnet_get_command(OIDRead('RS 485')['upper port baudrate']))
                config.set('DUT CONFIGURATION', 'upper port baudrate', str(upper_port_baudrate))

                modbus_comm_port = int(M1000Telnet.telnet_get_command(OIDRead('RS 485')['modbus comm']))
                config.set('DUT CONFIGURATION', 'modbus comm', str(modbus_comm_port))

                lithium_ion_comm_port = int(M1000Telnet.telnet_get_command(OIDRead('RS 485')['lithium ion comm']))
                config.set('DUT CONFIGURATION', 'lithium ion comm', str(lithium_ion_comm_port))

                acem_comm_port = int(M1000Telnet.telnet_get_command(OIDRead('RS 485')['acem comm']))
                config.set('DUT CONFIGURATION', 'acem comm', str(acem_comm_port))

                dg_amf_comm_port = int(M1000Telnet.telnet_get_command(OIDRead('RS 485')['dg amf comm']))
                config.set('DUT CONFIGURATION', 'dg amf comm', str(dg_amf_comm_port))

                solar_hvlv_comm_port = int(M1000Telnet.telnet_get_command(OIDRead('RS 485')['solar hvlv comm']))
                config.set('DUT CONFIGURATION', 'solar hvlv comm', str(solar_hvlv_comm_port))

                ext_dcem_comm_port = int(M1000Telnet.telnet_get_command(OIDRead('RS 485')['ext dcem comm']))
                config.set('DUT CONFIGURATION', 'ext dcem comm', str(ext_dcem_comm_port))

                bnms_comm_port = int(M1000Telnet.telnet_get_command(OIDRead('RS 485')['bnms comm']))
                config.set('DUT CONFIGURATION', 'bnms comm', str(bnms_comm_port))

                config.write(cfgfile)
                cfgfile.close()
                self.print_console("ATS CONFIGURED...")
                return True

            elif self.mcm_type == 2:
                self.print_console("CONFIGURING ATS....")
                config = configparser.ConfigParser()
                cfgfile = open(f"{gui_global.files_directory_location}config.ini", 'w')
                config.add_section("DUT CONFIGURATION")
                if self.custom_check.isChecked():
                    if DefaultRead('DEFAULT SETTING STATE')['max smr count'] == "YES":
                        max_smr_count = int(DefaultRead("DEFAULT SETTING")['max smr count'])
                        self.M2000.MCM_SET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['smr count'], str(max_smr_count))

                phase_type = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'ac phases type'))
                if phase_type == 0:
                    phase_type = 'SINGLE PHASE'
                elif phase_type == 1:
                    phase_type = 'THREE PHASE'
                elif phase_type == 2:
                    phase_type == 'DELTA'
                # PRINT_CONSOLE(self,phase_type)
                config.set('DUT CONFIGURATION', 'ac phases type', str(phase_type))

                battery_lvd_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'no. of battery lvd'))
                config.set('DUT CONFIGURATION', 'no. of battery lvd', str(battery_lvd_count))

                battery_fuses_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'no. of battery fuses'))
                config.set('DUT CONFIGURATION', 'no. of battery fuses', str(battery_fuses_count))

                load_lvd_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'no. of load lvd'))
                config.set('DUT CONFIGURATION', 'no. of load lvd', str(load_lvd_count))

                load_current_count = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['no. of load current']))
                config.set('DUT CONFIGURATION', 'no. of load current', str(load_current_count))

                load_current_sensor_state = int(
                    self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['load current sensor']))
                if load_current_sensor_state == 0:
                    load_current_sensor_state = 'DISABLE'
                elif load_current_sensor_state == 1:
                    load_current_sensor_state = 'ENABLE'
                if (self.part_number.lower() == "he531154") == 1:
                    load_current_sensor_state = 'ENABLE'
                # PRINT_CONSOLE(self,load_current_sensor_state)
                config.set('DUT CONFIGURATION', 'load current sensor', str(load_current_sensor_state))

                dcif_card_state = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['dcif card']))
                if dcif_card_state == 0:
                    dcif_card_state = 'DISABLE'
                elif dcif_card_state == 1:
                    dcif_card_state = 'PRESENT'
                config.set('DUT CONFIGURATION', 'dcif card', dcif_card_state)

                dcif_type = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['dcif card type']))
                config.set('DUT CONFIGURATION', 'dcif card type number', str(dcif_type))
                if dcif_type == 0:
                    dcif_type = 'HALL EFFECT'
                    for count in range(1, load_current_count + 1):
                        load_hall_effect_value = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')[
                                                                                    'load' + str(
                                                                                        count) + ' hall effect value']))
                        config.set('DUT CONFIGURATION', 'channel ' + str(count) + ' hall effect value',
                                   str(load_hall_effect_value))
                    for count in range(load_current_count + 1, load_current_count + battery_lvd_count + 1):
                        batt_hall_effect_value = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')[
                                                                                    'batt' + str(
                                                                                        count - load_current_count) + ' hall effect value']))
                        config.set('DUT CONFIGURATION', 'channel ' + str(count) + ' hall effect value',
                                   str(batt_hall_effect_value))

                elif dcif_type == 1:
                    dcif_type = 'SHUNT'
                    for count in range(1, load_current_count + 1):
                        load_hall_effect_value = int(
                            self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['load' + str(count) + ' shunt value']))
                        config.set('DUT CONFIGURATION', 'channel ' + str(count) + ' shunt value', str(load_hall_effect_value))
                        load_hall_effect_value = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')[
                                                                                    'load' + str(
                                                                                        count) + ' shunt mv value']))
                        config.set('DUT CONFIGURATION', 'channel ' + str(count) + ' shunt mv value', str(load_hall_effect_value))
                    for count in range(load_current_count + 1, load_current_count + battery_lvd_count + 1):
                        batt_hall_effect_value = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')[
                                                                                    'batt' + str(
                                                                                        count - load_current_count) + ' shunt value']))
                        config.set('DUT CONFIGURATION', 'channel' + str(count) + ' shunt value', str(batt_hall_effect_value))
                        batt_hall_effect_value = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')[
                                                                                    'batt' + str(
                                                                                        count - load_current_count) + ' shunt mv value']))
                        config.set('DUT CONFIGURATION', 'channel' + str(count) + ' shunt mv value', str(batt_hall_effect_value))

                elif dcif_type == 2 or dcif_type == 3:  # added dcif type 3 to logic ,17/06/2019
                    dcif_type = 'SHUNT SMALL'
                    for count in range(1, load_current_count + 1):
                        load_hall_effect_value = int(
                            self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['load' + str(count) + ' shunt value']))
                        config.set('DUT CONFIGURATION', 'channel' + str(count) + ' shunt value',
                                   str(load_hall_effect_value))
                        load_hall_effect_value = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')[
                                                                                    'load' + str(
                                                                                        count) + ' shunt mv value']))
                        config.set('DUT CONFIGURATION', 'channel' + str(count) + ' shunt mv value',
                                   str(load_hall_effect_value))
                    for count in range(load_current_count + 1, load_current_count + battery_lvd_count + 1):
                        batt_hall_effect_value = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')[
                                                                                    'batt' + str(
                                                                                        count - load_current_count) + ' shunt value']))
                        config.set('DUT CONFIGURATION', 'channel' + str(count) + ' shunt value',
                                   str(batt_hall_effect_value))
                        batt_hall_effect_value = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')[
                                                                                    'batt' + str(
                                                                                        count - load_current_count) + ' shunt mv value']))
                        config.set('DUT CONFIGURATION', 'channel' + str(count) + ' shunt mv value',
                                   str(batt_hall_effect_value))

                config.set('DUT CONFIGURATION', 'dcif card type', str(dcif_type))

                hvlv_card_state = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'hvlv card'))
                if hvlv_card_state == 0:
                    hvlv_card_state = 'DISABLE'
                elif hvlv_card_state == 1:
                    hvlv_card_state = 'PRESENT'
                else:
                    hvlv_card_state = '1234567890'
                config.set('DUT CONFIGURATION', 'hvlv card', str(hvlv_card_state))

                dcif_ip_card_state = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['dcif ip card']))
                if dcif_ip_card_state == 0:
                    dcif_ip_card_state = 'DISABLE'
                elif dcif_ip_card_state == 1:
                    dcif_ip_card_state = 'PRESENT'
                config.set('DUT CONFIGURATION', 'dcif ip card', str(dcif_ip_card_state))

                dcif_op_card_state = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['dcif op card']))
                if dcif_op_card_state == 0:
                    dcif_op_card_state = 'DISABLE'
                elif dcif_op_card_state == 1:
                    dcif_op_card_state = 'PRESENT'
                config.set('DUT CONFIGURATION', 'dcif op card', str(dcif_op_card_state))

                batt_temperature_state = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['temperature1']))
                if batt_temperature_state == 1:
                    batt_temperature_state = 'DISABLE'
                elif batt_temperature_state == 0:
                    batt_temperature_state = 'PRESENT'
                if self.part_number.lower() == "he518750":
                    batt_temperature_state = 'DISABLE'
                if self.part_number.lower() == 'he531154':
                    batt_temperature_state = 'DISABLE'
                config.set('DUT CONFIGURATION', 'temperature1', str(batt_temperature_state))

                room_temperature1_state = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['temperature2']))
                if room_temperature1_state == 0:
                    room_temperature1_state = 'DISABLE'
                elif room_temperature1_state == 1:
                    room_temperature1_state = 'PRESENT'
                if self.part_number.lower() == 'he531154':
                    room_temperature1_state = 'PRESENT'
                config.set('DUT CONFIGURATION', 'temperature2', str(room_temperature1_state))

                room_temperature2_state = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['temperature3']))
                if room_temperature2_state == 0:
                    room_temperature2_state = 'DISABLE'
                elif room_temperature2_state == 1:
                    room_temperature2_state = 'PRESENT'
                if self.part_number.lower() == "he518750":
                    room_temperature2_state = 'PRESENT'
                if self.part_number.lower() == 'he531154':
                    room_temperature2_state = 'DISABLE'
                config.set('DUT CONFIGURATION', 'temperature3', str(room_temperature2_state))

                pfc_io_card_state = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['pfc io card']))
                if pfc_io_card_state == 0:
                    pfc_io_card_state = 'DISABLE'
                elif pfc_io_card_state == 1:
                    pfc_io_card_state = 'PRESENT'
                config.set('DUT CONFIGURATION', 'pfc io card', str(pfc_io_card_state))

                smr_count = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['smr count']))
                config.set('DUT CONFIGURATION', 'smr count', str(smr_count))

                smr_type = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['smr type']))
                if smr_type == 0:
                    smr_type = '100A'
                elif smr_type == 1:
                    smr_type = '3KW'
                elif smr_type == 2:
                    smr_type = '25A'
                elif smr_type == 3:
                    smr_type = '25A'
                elif smr_type == 6:
                    smr_type = '4KW'
                config.set('DUT CONFIGURATION', 'smr type', smr_type)

                battery_type = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['battery type']))
                if battery_type == 0:
                    battery_type = 'VRLA'
                elif battery_type == 1:
                    battery_type = 'VRLA+LION'
                elif battery_type == 2:
                    battery_type = 'LION'
                config.set('DUT CONFIGURATION', 'battery type', battery_type)

                if battery_type == 'VRLA':
                    battery_capacity = int(
                        self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['vrla battery capacity']))
                    bcl_factor = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['vrla bcl factor']))
                if battery_type == 'LION' or battery_type == 'VRLA+LION':
                    battery_capacity = int(
                        self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['lion battery capacity']))
                    bcl_factor = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['lion bcl factor']))
                    module_count = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['lion module count']))
                    config.set('DUT CONFIGURATION', 'lion module count', str(module_count))
                config.set('DUT CONFIGURATION', 'battery capacity', str(battery_capacity))
                config.set('DUT CONFIGURATION', 'bcl factor', str(bcl_factor))

                ac_ip_voltage_source = int(
                    self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['ac ip voltage source']))
                if ac_ip_voltage_source == 1:
                    ac_ip_voltage_source = 'ACIF '
                elif ac_ip_voltage_source == 2:
                    ac_ip_voltage_source = 'HVLV PN'
                elif ac_ip_voltage_source == 3:
                    ac_ip_voltage_source = 'HVLV PP'
                elif ac_ip_voltage_source == 4:
                    ac_ip_voltage_source = 'SMR 1P'
                elif ac_ip_voltage_source == 5:
                    ac_ip_voltage_source = 'SMR 3P'
                config.set('DUT CONFIGURATION', 'ac ip voltage source', ac_ip_voltage_source)

                ac_ip_current_source = int(
                    self.M2000.MCM_GET_COMMAND(M2000OIDRead('SYSTEM CONFIG')['ac ip current source']))
                if ac_ip_current_source == 0:
                    ac_ip_current_source = 'NO SENSING '
                elif ac_ip_current_source == 1:
                    ac_ip_current_source = 'ACIF '
                elif ac_ip_current_source == 2:
                    ac_ip_current_source = 'HVLV PN'
                elif ac_ip_current_source == 3:
                    ac_ip_current_source = 'HVLV PP'
                elif ac_ip_current_source == 4:
                    ac_ip_current_source = 'SMR 1P'
                elif ac_ip_current_source == 5:
                    ac_ip_current_source = 'SMR 3P'
                config.set('DUT CONFIGURATION', 'ac ip current source', ac_ip_current_source)

                lower_port_baudrate = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('RS 485')['lower port baudrate']))
                if lower_port_baudrate == 0:
                    lower_port_baudrate = 9600
                elif lower_port_baudrate == 1:
                    lower_port_baudrate = 19200
                elif lower_port_baudrate == 2:
                    lower_port_baudrate = 115200
                config.set('DUT CONFIGURATION', 'lower port baudrate', str(lower_port_baudrate))

                upper_port_baudrate = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('RS 485')['upper port baudrate']))

                if upper_port_baudrate == 0:
                    upper_port_baudrate = 9600
                elif upper_port_baudrate == 1:
                    upper_port_baudrate = 19200
                elif upper_port_baudrate == 2:
                    upper_port_baudrate = 115200
                config.set('DUT CONFIGURATION', 'upper port baudrate', str(upper_port_baudrate))
                modbus_comm_port = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('RS 485')['modbus comm']))
                config.set('DUT CONFIGURATION', 'modbus comm', str(modbus_comm_port))

                lithium_ion_comm_port = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('RS 485')['lithium ion comm']))
                config.set('DUT CONFIGURATION', 'lithium ion comm', str(lithium_ion_comm_port))

                acem_comm_port = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('RS 485')['acem comm']))
                config.set('DUT CONFIGURATION', 'acem comm', str(acem_comm_port))

                dg_amf_comm_port = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('RS 485')['dg amf comm']))
                config.set('DUT CONFIGURATION', 'dg amf comm', str(dg_amf_comm_port))

                solar_hvlv_comm_port = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('RS 485')['solar hvlv comm']))
                config.set('DUT CONFIGURATION', 'solar hvlv comm', str(solar_hvlv_comm_port))

                ext_dcem_comm_port = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('RS 485')['ext dcem comm']))
                config.set('DUT CONFIGURATION', 'ext dcem comm', str(ext_dcem_comm_port))

                bnms_comm_port = int(self.M2000.MCM_GET_COMMAND(M2000OIDRead('RS 485')['bnms comm']))
                config.set('DUT CONFIGURATION', 'bnms comm', str(bnms_comm_port))

                config.write(cfgfile)
                cfgfile.close()
                self.print_console("ATS CONFIGURED...")
                return True

            elif 3 == self.mcm_type:
                # self.MCM_WRITE_COMMAND("SYSTEM COMMANDS",'system reset', 1)
                # time.sleep(5)
                # self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'system reset', 1)
                # status = False
                # while not status:
                #     status = self.M2000.LOGIN_MCM()[0]
                #     time.sleep(1)
                # self.print_console("RESET DONE")
                self.print_console("CONFIGURING ATS....")
                config = configparser.ConfigParser()
                cfgfile = open(f"{gui_global.files_directory_location}config.ini", 'w')
                config.add_section("DUT CONFIGURATION")
                phase_type = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'ac phases type'))
                if phase_type == 0:
                    phase_type = 'SINGLE PHASE'
                elif phase_type == 1:
                    phase_type = 'THREE PHASE'
                # PRINT_CONSOLE(self,phase_type)
                config.set('DUT CONFIGURATION', 'ac phases type', phase_type)

                battery_lvd_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'no. of battery lvd'))
                config.set('DUT CONFIGURATION', 'no. of battery lvd', str(battery_lvd_count))

                battery_fuses_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'no. of battery fuses'))
                config.set('DUT CONFIGURATION', 'no. of battery fuses', str(battery_fuses_count))

                load_lvd_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'no. of load lvd'))
                config.set('DUT CONFIGURATION', 'no. of load lvd', str(load_lvd_count))

                load_current_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'no. of load current'))
                config.set('DUT CONFIGURATION', 'no. of load current', str(load_current_count))

                load_current_sensor_state = int(
                    self.MCM_READ_COMMAND('SYSTEM CONFIG', 'load current sensor'))
                if load_current_sensor_state == 0:
                    load_current_sensor_state = 'DISABLE'
                elif load_current_sensor_state == 1:
                    load_current_sensor_state = 'ENABLE'
                # PRINT_CONSOLE(self,load_current_sensor_state)
                config.set('DUT CONFIGURATION', 'load current sensor', load_current_sensor_state)

                for count in range(1, load_current_count + 1):
                    load_hall_effect_value = int(self.MCM_READ_COMMAND('SYSTEM CONFIG',
                                                                       'load' + str(
                                                                           count) + ' hall effect value'))
                    config.set('DUT CONFIGURATION', 'channel ' + str(count) + ' hall effect value',
                               str(load_hall_effect_value))
                for count in range(load_current_count + 1, load_current_count + battery_lvd_count + 1):
                    batt_hall_effect_value = int(self.MCM_READ_COMMAND('SYSTEM CONFIG',
                                                                       'batt' + str(
                                                                           count - load_current_count) + ' hall effect value'))
                    config.set('DUT CONFIGURATION', 'channel ' + str(count) + ' hall effect value',
                               str(batt_hall_effect_value))

                batt_temperature_state = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'temperature1'))
                if batt_temperature_state == 1:
                    batt_temperature_state = 'DISABLE'
                elif batt_temperature_state == 0:
                    batt_temperature_state = 'PRESENT'
                config.set('DUT CONFIGURATION', 'temperature1', str(batt_temperature_state))

                room_temperature1_state = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'temperature2'))
                if room_temperature1_state == 0:
                    room_temperature1_state = 'DISABLE'
                elif room_temperature1_state == 1:
                    room_temperature1_state = 'PRESENT'
                config.set('DUT CONFIGURATION', 'temperature2', str(room_temperature1_state))

                room_temperature2_state = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'temperature3'))
                if room_temperature2_state == 0:
                    room_temperature2_state = 'DISABLE'
                elif room_temperature2_state == 1:
                    room_temperature2_state = 'PRESENT'
                config.set('DUT CONFIGURATION', 'temperature3', str(room_temperature2_state))

                smr_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'smr count'))
                config.set('DUT CONFIGURATION', 'smr count', str(smr_count))

                smr_type = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'smr type'))
                if smr_type == 0:
                    smr_type = '100A'
                elif smr_type == 1:
                    smr_type = '3KW'
                elif smr_type == 2:
                    smr_type = '25A'
                elif smr_type == 3:
                    smr_type = '25A'
                elif smr_type == 6:
                    smr_type = '4KW'
                config.set('DUT CONFIGURATION', 'smr type', smr_type)

                battery_type = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'battery type'))
                if battery_type == 0:
                    battery_type = 'VRLA'
                elif battery_type == 1:
                    battery_type = 'VRLA+LION'
                elif battery_type == 2:
                    battery_type = 'LION'
                config.set('DUT CONFIGURATION', 'battery type', battery_type)

                if battery_type == 'VRLA':
                    battery_capacity = int(
                        self.MCM_READ_COMMAND('SYSTEM CONFIG', 'vrla battery capacity'))
                    bcl_factor = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'vrla bcl factor'))
                if battery_type == 'LION' or battery_type == 'VRLA+LION':
                    battery_capacity = int(
                        self.MCM_READ_COMMAND('SYSTEM CONFIG', 'lion battery capacity'))
                    bcl_factor = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'lion bcl factor'))
                    module_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'lion module count'))
                    config.set('DUT CONFIGURATION', 'lion module count', str(module_count))
                config.set('DUT CONFIGURATION', 'battery capacity', str(battery_capacity))
                config.set('DUT CONFIGURATION', 'bcl factor', str(bcl_factor))

                ac_ip_voltage_source = int(
                    self.MCM_READ_COMMAND('SYSTEM CONFIG', 'ac ip voltage source'))
                if ac_ip_voltage_source == 1:
                    ac_ip_voltage_source = 'ACIF '
                elif ac_ip_voltage_source == 2:
                    ac_ip_voltage_source = 'HVLV PN'
                elif ac_ip_voltage_source == 3:
                    ac_ip_voltage_source = 'HVLV PP'
                elif ac_ip_voltage_source == 4:
                    ac_ip_voltage_source = 'SMR 1P'
                elif ac_ip_voltage_source == 5:
                    ac_ip_voltage_source = 'SMR 3P'
                config.set('DUT CONFIGURATION', 'ac ip voltage source', ac_ip_voltage_source)

                ac_ip_current_source = int(
                    self.MCM_READ_COMMAND('SYSTEM CONFIG', 'ac ip current source'))
                if ac_ip_current_source == 0:
                    ac_ip_current_source = 'NO SENSING '
                elif ac_ip_current_source == 1:
                    ac_ip_current_source = 'ACIF '
                elif ac_ip_current_source == 2:
                    ac_ip_current_source = 'HVLV PN'
                elif ac_ip_current_source == 3:
                    ac_ip_current_source = 'HVLV PP'
                elif ac_ip_current_source == 4:
                    ac_ip_current_source = 'SMR 1P'
                elif ac_ip_current_source == 5:
                    ac_ip_current_source = 'SMR 3P'
                config.set('DUT CONFIGURATION', 'ac ip current source', ac_ip_current_source)
                config.write(cfgfile)
                cfgfile.close()
                self.print_console("ATS CONFIGURED...")
                return True
        except TypeError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except AttributeError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except FileNotFoundError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except ZeroDivisionError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except can.interfaces.ixxat.exceptions as err:
            print(err)
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            return False
        except Exception as err:
            print(err)
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(f'Type of error is : {type(err)}')
            return False
        except (AllException, AttributeError, RuntimeError) as err:
            print(err)
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            self.all_stop = True
            return False

    def CARD_COMMUNICATION(self):
        try:
            self.print_console("CARD COMMUNICATION TEST STARTED....")
            RESULT = []
            hvlv_card_state = ConfigRead("DUT CONFIGURATION")['hvlv card']
            dcif_card_state = ConfigRead("DUT CONFIGURATION")['dcif card']
            pfcio_card_state = ""  # ConfigRead("DUT CONFIGURATION")['pfc op card']  # not in he518561
            ac_phase_type = ConfigRead("DUT CONFIGURATION")['ac phases type']
            # time.sleep(15)
            if self.config_load['config_match']:
                self.config_file_found = str(self.MCM_READ_COMMAND("SYSTEM COMMANDS", 'config file version'))

                print(len(self.config_file_found), len(self.config_load['config_version']))

                if str(self.config_file_found) == str(self.config_load['config_version']):
                    self.print_console("Config File Version matches with the reference file version!", "GREEN")
                    RESULT.append(True)
                else:
                    self.print_console("MCM Current file Config file Version:" + str(self.config_file_found), 'RED')
                    self.print_console("File Version in Customer DB is " + str(self.config_load['config_version']), 'RED')
                    RESULT.append(False)
                    self.all_stop = True
                    return False
            if self.mcm_type == 2:
                self.print_console("waiting for 20 seconds MCM stabilizing!")
                for i in range(21):
                    time.sleep(1)
            if self.config_load['can_comm']:
                alarm_comm_fail = int(self.MCM_READ_COMMAND("ALARM", "can comm fail"))
                if alarm_comm_fail == 0:
                    self.print_console("CAN COMM OK", 'GREEN')
                    self.excel_handler.update_cell("UNIT COMMUNICATION", "PASS")
                    RESULT_TEMP = True
                else:
                    RESULT_TEMP = False
                    self.print_console('CAN COMM FAIL')
                    self.excel_handler.update_cell("UNIT COMMUNICATION", "FAIL")
                RESULT.append(RESULT_TEMP)
            if self.config_load['hvlv_comm']:
                if hvlv_card_state == "PRESENT":
                    if ac_phase_type == "SINGLE PHASE":
                        print("Single phase voltage")
                        ACSET(self.pfc, 1, 1)
                    else:
                        ACSET(self.pfc, 3, 1)
                    time.sleep(8)
                    self.print_console("HVLV CARD IS PRESENT")
                    alarm_comm_fail = int(self.MCM_READ_COMMAND("ALARM", "hvlv comm fail"))
                    if alarm_comm_fail == 0:
                        RESULT_TEMP = True
                        self.print_console("HVLV COMM OK", "GREEN")
                    else:
                        RESULT_TEMP = False
                        self.print_console("HVLV COMM FAIL", "RED")
                    ACSET(self.pfc, 3, 0)
            else:
                self.print_console("HVLV CARD IS NOT PRESENT")
                RESULT_TEMP = True
            RESULT.append(RESULT_TEMP)
            if self.config_load['dcif_comm']:
                if dcif_card_state == "PRESENT":
                    alarm_comm_fail = int(self.MCM_READ_COMMAND("ALARM", 'dcif comm fail'))
                    if alarm_comm_fail == 0:
                        RESULT_TEMP = True
                        self.print_console("DCIF COMM OK", 'GREEN')
                    else:
                        RESULT_TEMP = False
                        self.print_console("DCIF COMM FAIL", "RED")
            else:
                RESULT_TEMP = True
            RESULT.append(RESULT_TEMP)
            if self.config_load['pfc_io_comm']:
                if pfcio_card_state == "PRESENT":
                    alarm_comm_fail = int(self.MCM_READ_COMMAND('ALARM', 'pfc1 comm fail'))
                    if alarm_comm_fail == 0:
                        RESULT_TEMP = True
                        self.print_console("CAN PFC IO COMM OK", "GREEN")
                    else:
                        RESULT_TEMP = False
                        self.print_console("CAN PFC IO COMM FAIL", "RED")
            else:
                RESULT_TEMP = True
            RESULT.append(RESULT_TEMP)

            config_list = ['dgbc_comm', 'acif_comm', 'nms_comm']
            param_list = ['dgbc comm fail', 'acif comm fail', 'modem comm fail']

            def comm_check(index_value):
                if self.config_load[config_list[index_value]]:
                    alarm_comm_fail = int(self.MCM_READ_COMMAND('ALARM', param_list[index_value]))
                    if not alarm_comm_fail:
                        result = ["OK", "GREEN", True]
                    else:
                        result = ['FAIL', 'RED', False]
                    self.print_console(f"{config_list[index_value]} {result[0]}", result[1])
                    RESULT.append(result[2])

            for value in range(0, 3):
                comm_check(value)

            if self.customer_name_edit.text() == "BHARTI":
                alarm_comm_fail = int(self.MCM_READ_COMMAND('ALARM', 'lcu comm fail'))
                if not alarm_comm_fail:
                    self.print_console("lcu comm OK", "GREEN")
                    RESULT.append(True)
                else:
                    RESULT.append(False)
                    self.print_console("lcu comm Fail", "RED")

            self.print_console("CARD COMMUNICATION TEST FINISHED....")
            return CALCULATE_RESULT(RESULT)


        except ZeroDivisionError as err:
            print(f"Handled ZeroDivisionError in outer function: {err}")
            self.all_stop = True
            self.print_console("ERROR IN COMMUNICATING WITH MCM", 'RED')
            self.print_console("STOPPING TEST", 'RED')
            return False
        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False

    def TEMPERATURE_MEASUREMENT(self):
        try:
            global temperature_text
            RESULT = []
            self.print_console("TEMPERATURE MEASUREMENT TEST STARTED....")
            if self.config_load['temperature_test']:
                for temp in range(1, 4):
                    if temp == 1:
                        temperature_text = "BATTERY TEMPERATURE"
                    elif temp == 2:
                        temperature_text = "ROOM TEMPERATURE 1"
                    elif temp == 3:
                        temperature_text = "ROOM TEMPERATURE 2"
                    temperature_state = ConfigRead("DUT CONFIGURATION")['temperature' + str(temp)]
                    if temperature_state == "DISABLE":
                        self.print_console(f"{temperature_text} sensor not applicable")
                        RESULT_TEMP = True
                        RESULT.append(RESULT_TEMP)
                    else:
                        temperature = float(self.MCM_READ_COMMAND('READ TEMPERATURE', 'temperature' + str(temp)))
                        if temperature == 0:
                            temperature = float(self.MCM_READ_COMMAND('READ TEMPERATURE', 'temperature' + str(2)))
                        # self.print_console(self.part_number)

                        if self.config_load['fan_temperature_test']:
                            temperature = self.MCM_READ_COMMAND('READ TEMPERATURE', 'temp')
                            # self.print_console(temperature)
                        if temperature < 9 or temperature > 40:
                            self.print_console(f"{temperature_text} cable not installed/ faulty", "RED")
                            RESULT_TEMP = False
                            RESULT.append(RESULT_TEMP)
                            # self.print_console(f"{temperature_text} : {temperature}")
                        else:
                            temperature_list = []
                            for i in range(1, 5):
                                temperature = float(self.MCM_READ_COMMAND('READ TEMPERATURE', 'temperature' + str(temp)))
                                if temperature == 0:
                                    temperature = float(self.MCM_READ_COMMAND('READ TEMPERATURE', 'temperature' + str(2)))
                                temperature_list.append(temperature)
                            # self.print_console(f"{temperature_list}")
                            if self.config_load["fan_temperature_test"]:
                                self.print_console(
                                    "Temperature from FAN CARD:" + str(self.MCM_READ_COMMAND('READ TEMPERATURE', 'temp')))
                            temperature_minimum = float(min(temperature_list))
                            temperature_maximum = float(max(temperature_list))
                            if abs(temperature_maximum - temperature_minimum) < 2:
                                RESULT_TEMP = True
                                self.print_console(f"{temperature_text} CABLE OK", 'GREEN')
                                temperature = float(self.MCM_READ_COMMAND('READ TEMPERATURE', 'temperature' + str(temp)))
                                if temperature == 0:
                                    temperature = float(self.MCM_READ_COMMAND('READ TEMPERATURE', 'temperature' + str(2)))
                                self.print_console(f"Temperature value: {temperature}")
                            else:
                                RESULT_TEMP = False
                                self.print_console(f"{temperature_text} CABLE FAULTY", "RED")
                            RESULT.append(RESULT_TEMP)
            else:
                RESULT.append(True)
            self.print_console("TEMPERATURE MEASUREMENT TEST FINISHED...")
            return CALCULATE_RESULT(RESULT)
        except ZeroDivisionError as err:
            print(f"Handled ZeroDivisionError in outer function: {err}")
            self.all_stop = True
            self.print_console("ERROR IN COMMUNICATING WITH MCM", 'RED')
            self.print_console("STOPPING TEST", 'RED')
            return False
        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False

    def OP_PFC_CHECK(self):
        """
        TEST BLOCK OF OUTPUT PFC
        DEFINES AND TEST OUTPUT PFC(S) OR LVD(S) OF THE RACK SYSTEM
        :return: STATUS OF THE FUNCTION BLOCK IN BOOLEAN FORM (TRUE OR FALSE)
        @return:
        """

        RESULT = []
        RESULT_1 = []
        RESULT_2 = []
        self.print_console("OP_PFC_CHECK TEST STARTED...")
        pfcio_card_state = ConfigRead("DUT CONFIGURATION")['pfc io card']
        dcif_op_card_state = ConfigRead("DUT CONFIGURATION")['dcif op card']
        dcif_type_number = int(ConfigRead('DUT CONFIGURATION')['dcif card type number'])
        if dcif_type_number == 1 or dcif_type_number == 2:
            if self.mcm_type == 1:
                M1000Telnet.telnet_set_command(OIDRead('SYSTEM COMMANDS')['ate test'], "TEST_M1000_ATE")

            for op_pfc in range(1, 3):
                set_dut_pfc = pow(2, op_pfc + 4)
                if self.mcm_type == 1:
                    M1000Telnet.telnet_set_command(OIDRead('DCIF 2 OP PFC')['pfc'], set_dut_pfc)
                elif self.mcm_type == 2:
                    self.M2000.MCM_SET_COMMAND(M2000OIDRead('DCIF 2 OP PFC')['pfc'], set_dut_pfc)
                if dcif_op_card_state == "PRESENT":
                    set_dcif_pfc = pow(2, op_pfc - 1)
                    if self.mcm_type == 1:
                        M1000Telnet.telnet_set_command(OIDRead('DCIF 8 OP PFC')['pfc'], set_dcif_pfc)
                    elif self.mcm_type == 2:
                        self.M2000.MCM_SET_COMMAND(M2000OIDRead('DCIF 8 OP PFC')['pfc'], set_dcif_pfc)
                time.sleep(2)
                print(f"Checking for pfc {op_pfc}")
                for op_pfc_check in range(1, 3):
                    jig_pfc = (2 * op_pfc_check) - 1

                    if op_pfc == op_pfc_check:
                        print("same PFC")
                        if self.pfc.read_pfc(card_id=self.contact.CARD2, pfc_number=jig_pfc) == 0:
                            RESULT_TEMP = True
                            self.print_console(f"LVD PFC {op_pfc_check} NC is OK")
                        else:
                            RESULT_TEMP = False
                            self.print_console(f"LVD OP PFC {op_pfc} NC SLOT IS FAULTY", 'RED')
                        RESULT_1.append(RESULT_TEMP)
                        if self.pfc.read_pfc(self.contact.CARD2, pfc_number=jig_pfc + 1) == 1:
                            RESULT_TEMP = True
                            self.print_console(f"LVD PFC {op_pfc_check} NC IS OK")
                        else:
                            RESULT_TEMP = False
                            self.print_console(f"LVD OP PFC {op_pfc} NC SLOT IS FAULTY", 'RED')
                        RESULT_1.append(RESULT_TEMP)
                    else:
                        print("Different PFC")
                        if self.pfc.read_pfc(self.contact.CARD2, jig_pfc) == 1:
                            RESULT_TEMP = True
                        else:
                            RESULT_TEMP = False
                            self.print_console(f"LVD OP PFC {op_pfc_check} NC SLOT IS SHORT WITH OP PFC {op_pfc}",
                                               "RED")
                        RESULT_1.append(RESULT_TEMP)
                        if self.pfc.read_pfc(self.contact.CARD2, jig_pfc + 1) == 0:
                            RESULT_TEMP = True
                        else:
                            RESULT_TEMP = False
                            self.print_console(f"LVD OP PFC {op_pfc_check} NC SLOT IS SHORT WITH OP PFC {op_pfc}",
                                               "RED")
                        RESULT_1.append(RESULT_TEMP)
                if self.mcm_type == 1:
                    M1000Telnet.telnet_set_command(OIDRead('DCIF 2 OP PFC')['pfc'], 0)
                    M1000Telnet.telnet_set_command(OIDRead('DCIF 8 OP PFC')['pfc'], 0)
                elif self.mcm_type == 2:
                    self.M2000.MCM_SET_COMMAND(M2000OIDRead('DCIF 2 OP PFC')['pfc'], 0)
                    self.M2000.MCM_SET_COMMAND(M2000OIDRead('DCIF 8 OP PFC')['pfc'], 0)

            RESULT.append(CALCULATE_RESULT(RESULT_1))

            if dcif_op_card_state == "PRESENT":
                for op_pfc in range(1, 9):
                    if op_pfc < 3:
                        set_dut_pfc = pow(2, op_pfc + 4)
                        if self.mcm_type == 1:
                            M1000Telnet.telnet_set_command(OIDRead('DCIF 2 OP PFC')['pfc'], set_dut_pfc)
                        elif self.mcm_type == 2:
                            self.M2000.MCM_SET_COMMAND(M2000OIDRead('DCIF 2 OP PFC')['pfc'], set_dut_pfc)
                    set_dcif_pfc = pow(2, op_pfc - 1)
                    if self.mcm_type == 1:
                        M1000Telnet.telnet_set_command(OIDRead('DCIF 8 OP PFC')['pfc'], set_dcif_pfc)
                    elif self.mcm_type == 2:
                        self.M2000.MCM_SET_COMMAND(M2000OIDRead('DCIF 8 OP PFC')['pfc'], set_dcif_pfc)
                    time.sleep(2)
                    for op_pfc_check in range(1, 9):
                        jig_pfc_no = (2 * op_pfc_check) - 1
                        if op_pfc == op_pfc_check:
                            if self.pfc.read_pfc(self.contact.CARD2, jig_pfc_no) == 0:
                                RESULT_TEMP = True
                                self.print_console(f"DCIF OP PFC {op_pfc} NC SLOT IS OK")
                            else:
                                RESULT_TEMP = False
                                self.print_console(f"DCIF OP PFC {op_pfc} NC SLOT IS FAULTY", "RED")
                            RESULT_2.append(RESULT_TEMP)
                            if self.pfc.read_pfc(self.contact.CARD2, jig_pfc_no + 1) == 1:
                                RESULT_TEMP = True
                                self.print_console(f"DCIF OP PFC {op_pfc} NO SLOT IS OK")
                            else:
                                RESULT_TEMP = False
                                self.print_console(f"DCIF OP PFC {op_pfc} NO SLOT IS FAULTY", "RED")
                            RESULT_2.append(RESULT_TEMP)
                        else:
                            if self.pfc.read_pfc(self.contact.CARD2, jig_pfc_no) == 1:
                                RESULT_TEMP = True
                                # self.print_console(f"DCIF OP PFC {op_pfc} NC SLOT IS S")
                            else:
                                RESULT_TEMP = False
                                self.print_console(f"DCIF OP PFC {op_pfc} NC SLOT IS SHORT WITH OP PFC", "RED")
                            RESULT_2.append(RESULT_TEMP)
                            if self.pfc.read_pfc(self.contact.CARD2, jig_pfc_no + 1) == 0:
                                RESULT_TEMP = True
                                self.print_console(f"DCIF OP PFC {op_pfc} NO SLOT IS OK")
                            else:
                                RESULT_TEMP = False
                                self.print_console(f"DCIF OP PFC {op_pfc} NO SLOT IS SHORT WITH OP PFC", "RED")
                            RESULT_2.append(RESULT_TEMP)
                    if self.mcm_type == 1:
                        M1000Telnet.telnet_set_command(OIDRead('DCIF 8 OP PFC')['pfc'], 0)
                        if op_pfc < 3:
                            M1000Telnet.telnet_set_command(OIDRead('DCIF 2 OP PFC')['pfc'], 0)
                    elif self.mcm_type == 2:
                        self.M2000.MCM_SET_COMMAND(M2000OIDRead('DCIF 8 OP PFC')['pfc'], 0)
                        if op_pfc < 3:
                            self.M2000.MCM_SET_COMMAND(M2000OIDRead('DCIF 2 OP PFC')['pfc'], 0)
                RESULT.append(CALCULATE_RESULT(RESULT_2))
            else:
                self.print_console("DCIF 8 OP PFC CARD NOT APPLICABLE")
                RESULT_TEMP = True
                RESULT_2.append(RESULT_TEMP)
                RESULT.append(CALCULATE_RESULT(RESULT_2))
            self.print_console("OP_PFC_CHECK TEST FINISHED...")
            return CALCULATE_RESULT(RESULT)

        else:
            self.print_console("DCIF 8 OP PFC CARD TEST NOT APPLICABLE")
            RESULT_TEMP = True
            RESULT.append(RESULT_TEMP)
        self.print_console("OP_PFC_CHECK TEST FINISHED...")
        return CALCULATE_RESULT(RESULT)

    def IP_PFC_CHECK(self):
        try:
            """
            TEST BLOCK OF INPUT PFC
    
            DEFINES, TEST INPUT PFC(S) OR LVD(S) OF THE RACK SYSTEM
    
            :return: STATUS OF THE FUNCTION BLOCK IN BOOLEAN FORM (TRUE OR FALSE)
            """

            global RESULT_TEMP, RESULT_TEMP_DOOR_TRIP, temp_value
            self.print_console("IP_PFC_CHECK TEST STARTED...")
            RESULT = [True]

            self.TEST_MODE_M1000()

            IP_PFC_CHECK_LIST = [self.SPD_CHECK, self.NTWRK_TEST, self.DOOR_TEST, self.SMOKE_TEST, self.AVIATION_LAMP]

            for test in IP_PFC_CHECK_LIST:
                if not CALCULATE_RESULT(RESULT):
                    self.print_console("Previous test failed, exiting IP PFC Test Block", "RED")
                    break
                self.print_console(F"START TIME FOR INPUT PFC SUBTEST : {test.__name__} is : {datetime.datetime.now()}")
                test_result = self.RETRY_FUNCTION(5, test)
                self.print_console(F"END TIME FOR INPUT PFC SUBTEST : {test.__name__} is : {datetime.datetime.now()}")
                RESULT.append(test_result)

            self.print_console("IP_PFC_CHECK TEST FINISHED...")

        except ZeroDivisionError as err:
            print(f"Handled ZeroDivisionError in outer function: {err}")
            self.all_stop = True
            self.print_console("ERROR IN COMMUNICATING WITH MCM", 'RED')
            self.print_console("STOPPING TEST", 'RED')
            return False

        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False
        return CALCULATE_RESULT(RESULT)

    def TEST_MODE_M1000(self):
        if self.mcm_type == 1:
            M1000Telnet.telnet_set_command(OIDRead('SYSTEM COMMANDS')['ate test'], "TEST_M1000_ATE")

    def AVIATION_LAMP(self):
        RESULT = [True]
        if self.config_load['aviation_lamp']:
            self.print_console("aviation lamp test started...")
            aviation_on_ = {
                'aviation lamp state': 0,
                'on hour': 0,
                'on min': 0,
                'off hour': 23,
                'off min': 59
            }
            for i in aviation_on_.keys():
                self.MCM_WRITE_COMMAND('AVIATION LAMP', i, aviation_on_[i])

            time.sleep(1)
            self.MCM_WRITE_COMMAND('AVIATION LAMP', 'aviation lamp state', 1)
            # time.sleep(1)

            temp_value = 0
            if str(SettingRead("STATION")['id']) in ["C", "E"]:
                temp_value = pfc_control.read_pfc(0x60A, 1)
                if temp_value:
                    self.print_console(f'Aviation Lamp is : OK', "GREEN")
                    RESULT.append(True)
                else:
                    self.print_console(f'Aviation Lamp is : FAIL', "RED")
                    RESULT.append(False)
            else:
                temp_value = self.prompt.user_value_2("Enter Voltage Value from Aviation CKT", "V")
                if float(temp_value) > 48:
                    self.print_console(f'Aviation Lamp is : OK', "GREEN")
                    RESULT.append(True)
                else:
                    self.print_console(f'Aviation Lamp is : FAIL', "RED")
                    RESULT.append(False)

            aviation_off_ = {
                'on hour': 18,
                'on min': 0,
                'off hour': 6,
                'off min': 00
            }

            for i in aviation_off_.keys():
                self.MCM_WRITE_COMMAND('AVIATION LAMP', i, aviation_off_[i])

            self.print_console("aviation lamp test finished...")

        else:
            self.print_console("AVIATION LAMP TEST IS NOT APPLICABLE")

        return CALCULATE_RESULT(RESULT)

    def SMOKE_TEST(self):
        global RESULT_TEMP_DOOR_TRIP
        RESULT = [True]
        if not self.config_load['smoke_alarm']:
            self.print_console("SMOKE ALARM TEST NOT APPLICABLE")
        else:
            self.print_console("SMOKE ALARM TEST STARTED...")
            ip_pfc_state = True
            while ip_pfc_state:
                if not ip_pfc_state:
                    self.prompt.Message(prompt=f"ip_pfc_state {ip_pfc_state}")
                else:
                    ip_pfc_state = False
                    self.prompt.Message(prompt="GENERATE SMOKE ALARM AND PRESS OK!", buzzer=0, response_time=90)
                    TimerPrompt(self, "WAIT FOR 6 SECONDS", 7)
                    if int(self.MCM_READ_COMMAND('ALARM', 'smoke alarm')) == 1:
                        RESULT_TEMP_DOOR_TRIP = True
                        self.print_console("SMOKE ALARM TESTED OK")
                    else:
                        RESULT_TEMP_DOOR_TRIP = False
                        self.print_console("SMOKE ALARM TEST FAIL", 'RED')
                if self.mcm_type == 1:
                    self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'system reset', 1)
            RESULT.append(RESULT_TEMP_DOOR_TRIP)
            self.print_console("SMOKE ALARM TEST FINISHED...")

        return CALCULATE_RESULT(RESULT)

    def DOOR_TEST(self):
        global RESULT_TEMP_DOOR_TRIP
        RESULT = [True]
        if self.config_load['door_alarm']:
            self.print_console("DOOR OPEN ALARM TEST STARTED...")
            read_restore_time = int(self.MCM_READ_COMMAND('DOOR SETTING', 'door open restore time'))
            self.MCM_WRITE_COMMAND('DOOR SETTING', 'door open restore time', 2)
            ip_pfc_state = True
            while ip_pfc_state:
                if not ip_pfc_state:
                    self.prompt.Message(prompt=f"ip_pfc_state {ip_pfc_state}")
                else:
                    RESULT_TEMP_DOOR_TRIP = False
                    retry_count = 0
                    self.prompt.Message(prompt="Kindly Close Door(s)! for Door Alarm Test!")
                    while not RESULT_TEMP_DOOR_TRIP and retry_count < 5:
                        try:
                            if int(self.MCM_READ_COMMAND('ALARM', 'door open alarm')) == 0:
                                RESULT_TEMP_DOOR_TRIP = True
                                self.print_console("DOOR OPEN ACTIVE TESTED OK")
                            else:
                                RESULT_TEMP_DOOR_TRIP = False
                                self.print_console("DOOR OPEN ACTIVE TESTED FAIL", "RED")
                                self.prompt.Message(prompt="Kindly Close Door Switch!")
                            retry_count += 1
                        except Exception as err:
                            print(err)
                            time.sleep(5)

                    RESULT.append(RESULT_TEMP_DOOR_TRIP)
                    # self.prompt.Message(prompt="CLEAR DOOR OPEN ALARM. PRESS ENTER KEY TO PROCEED")
                    ip_pfc_state = False
                    self.prompt.Message(prompt="OPEN THE DOOR. PRESS ENTER KEY TO PROCEED")
                    TimerPrompt(self, "WAIT FOR 6 SECONDS", 7)

                    if int(self.MCM_READ_COMMAND('ALARM', 'door open alarm')) == 1:
                        RESULT_TEMP_DOOR_TRIP = True
                        self.print_console("DOOR OPEN ALARM TESTED OK")
                    else:
                        RESULT_TEMP_DOOR_TRIP = False
                        self.print_console("DOOR OPEN ALARM TEST FAIL", 'RED')
                self.MCM_WRITE_COMMAND('DOOR SETTING', 'door open restore time', read_restore_time)
            RESULT.append(RESULT_TEMP_DOOR_TRIP)
            self.print_console("DOOR ALARM TEST FINISHED...")
        else:
            self.print_console("DOOR OPEN ALARM TEST NOT APPLICABLE")

        return CALCULATE_RESULT(RESULT)

    def NTWRK_TEST(self):
        RESULT = [True]
        if self.customer_name_edit.text() == "BHARTI":
            user_prompt = self.prompt.User_prompt("Is Signal Strength Coming, If Yes Press OK else Fail", buzzer=1, response_time=60)
            if user_prompt:
                temp_value = self.MCM_READ_COMMAND('MODEM', 'signal strength')
                try:
                    if float(temp_value[3:5]) > 5:
                        color = "GREEN"
                        RESULT.append(True)
                    else:
                        color = "RED"
                        RESULT.append(False)
                except ValueError as err:
                    RESULT.append(False)
                    color = 'RED'
                self.print_console(f"signal strength of the DUT is : {temp_value}", color)
            else:
                self.print_console("Signal Not arrived, Check for SIM Network or Modem Card!")
                RESULT.append(False)
        else:
            self.print_console("NETWORK STRENGTH TEST NOT APPLICABLE...")

        return CALCULATE_RESULT(RESULT)

    def FAN_TEST(self):
        """
        Perform the FAN test based on the configuration and MCM type.
        Returns the overall result of the FAN test.
        """
        RESULT = []

        # Check if the fan test is enabled and if preliminary conditions are met
        if not self.config_load.get('fan_test'):
            self.print_console("FAN Test bypassed...")
            RESULT.append(True)
            return CALCULATE_RESULT(RESULT)

        self.print_console("FAN TEST STARTED...")

        # Helper function for retry logic
        def perform_retest(prompt_message):
            retry_count = 5
            for _ in range(retry_count):
                TEMP_LIST = [True]
                self.prompt.Message(title="ALERT", prompt=prompt_message, buzzer=0)
                if int(self.MCM_READ_COMMAND('ALARM', 'fan_sense_fail')) == 1:
                    self.print_console("FAN FAIL SENSE TESTED OK!")
                    TEMP_LIST.append(True)
                else:
                    self.print_console("FAN FAIL SENSE TESTED FAILED!", "RED")
                    TEMP_LIST.append(False)

                if CALCULATE_RESULT(TEMP_LIST):
                    return True
                elif not self.prompt.User_prompt("Do you want to retest FAN FAIL SENSE TEST?"):
                    break
            return False

        # MCM Type 2 Logic
        if self.mcm_type == 2:
            if int(self.MCM_READ_COMMAND(section='4078', pool=1)) == 0:
                # Test fan fail sense without a fan control card
                prompt_message = ("1. KINDLY INCREASE TEMPERATURE TO MAKE FAN RUNNING!\n"
                                  "2. THEN TURN OFF DOOR SENSOR\n"
                                  "3. GENERATE FAN SENSE ALARM, KEEP ALARM ACTIVE AND PRESS OK")
                RESULT.append(perform_retest(prompt_message))
            else:
                # Test fan count logic with custom values
                temperature_value = self.MCM_READ_COMMAND('WRITE TEMPERATURE', 'temp')
                fan_count_init = self.MCM_READ_COMMAND('WRITE TEMPERATURE', 'fan active')

                self.RETRY_FUNCTION(5, self.READ_FAN_TEMP)

                self.MCM_WRITE_COMMAND('WRITE TEMPERATURE', 'temp', '20')
                self.MCM_WRITE_COMMAND('WRITE TEMPERATURE', 'fan active', "4")
                time.sleep(2)
                fan_count = float(self.MCM_READ_COMMAND('WRITE TEMPERATURE', 'fan'))

                if fan_count == 4:
                    self.print_console(f"fan count = {fan_count}")
                    self.print_console("FAN TEST OK")
                    RESULT.append(True)
                else:
                    self.print_console("FAN TEST FAILED", 'RED')
                    RESULT.append(False)

                # Restore original values
                self.MCM_WRITE_COMMAND('WRITE TEMPERATURE', 'temp', str(temperature_value))
                self.MCM_WRITE_COMMAND('WRITE TEMPERATURE', 'fan active', str(fan_count_init))

        # MCM Type 1 Logic
        elif self.mcm_type == 1:
            temperature_value = self.MCM_READ_COMMAND(section='TAB.3011.0', pool=1)
            self.MCM_WRITE_COMMAND('WRITE TEMPERATURE', 'temp', '30.0')
            self.prompt.Message(prompt="Raise the Temperature of the System and Press OK When Fans are ON!")
            user_input = self.prompt.User_prompt("Are the fans running?")
            if user_input:
                self.print_console("FAN TEST OK")
                RESULT.append(True)
            else:
                self.print_console("FAN TEST FAILED", 'RED')
                RESULT.append(False)

            # Restore original temperature
            self.MCM_WRITE_COMMAND('WRITE TEMPERATURE', 'temp', str(float(temperature_value)))

        # Final result
        self.print_console("FAN TEST FINISHED...")
        return CALCULATE_RESULT(RESULT)

    def READ_FAN_TEMP(self):
        loop_count = 10
        loop_counter = 0
        while float(self.MCM_READ_COMMAND('READ TEMPERATURE', 'temp')) <= 20.0 and loop_counter < loop_count:
            self.prompt.Message(title='ALERT', prompt='Kindly raise Temperature above 20 Degrees')
            loop_counter += 1
        if loop_counter == 10:
            return False
        return True

    def SPD_CHECK(self):
        """
        Perform the SPD (Surge Protection Device) check based on the configuration and parameters.
        Returns the overall result of the SPD check.
        """
        RESULT = []
        ac_phase_type = ConfigRead("DUT CONFIGURATION")['ac phases type']

        if self.customer_name == "RELIANCE" or self.part_number.lower() == 'he518750':
            associate_variable_ = '2'
        elif self.mcm_type == 1:
            associate_variable_ = ''
        else:
            associate_variable_ = ""

        def check_spu_alarm(phase_name, associate_variable):
            """
            Check the SPU alarm status for a given phase.
            """
            if int(self.MCM_READ_COMMAND('ALARM', f'spu fail{associate_variable}')) == 1:
                self.print_console(f"SPU ALARM FOR {phase_name} OK")
                return True
            else:
                self.print_console(f"SPU ALARM FOR {phase_name} FAIL", 'RED')
                return False

        # Define phase configurations
        if ac_phase_type == "SINGLE PHASE" and (self.config_load.get('SPD 1/3') or self.part_number.lower() == 'he518750'):
            phases = ['R PHASE', 'NEUTRAL PHASE']
            self.prompt.Message(prompt="REMOVE R PHASE SPD")
            time.sleep(1)
        elif ac_phase_type == "THREE PHASE" and self.config_load.get('SPD 1/3'):
            phases = ['R PHASE', 'Y PHASE', 'B PHASE', 'NEUTRAL PHASE']
            self.prompt.Message(prompt="REMOVE R PHASE SPD")
            time.sleep(1)
        else:
            phases = []

        # Perform SPU alarm checks for each phase
        for phase in phases:
            RESULT.append(check_spu_alarm(phase, associate_variable_))

        if self.config_load.get("SPD 1/3"):
            alarm = True
            self.prompt.Message(prompt="INSERT BACK ALL SPD(S)")
            while alarm:
                time.sleep(0.5)
                if int(self.MCM_READ_COMMAND('ALARM', f'spu fail{associate_variable_}')) == 0:
                    alarm = False
                """
                ADDITION OF PROMPT IN CASE OF SPD ALARM STATUS ACTIVE
                CODE WAS STUCK IN LOOP WITHOUT INTIMATION TO USER FOR SPD ALARM ACTIVE
                """
                self.prompt.Message(title="WARNING", prompt="INSERT BACK ALL SPDS!")
        else:
            self.print_console("SPD Test Bypassed...")
            RESULT.append(True)

        return CALCULATE_RESULT(RESULT)

    def DC_VOLTAGE_MEASUREMENT(self):
        try:
            """
            TEST BLOCK OF DC VOLTAGE MEASUREMENT
    
            DEFINES, TEST DC VOLTAGES FOR THE RACK SYSTEM
    
            :return: STATUS OF THE FUNCTION BLOCK IN BOOLEAN FORM (TRUE OR FALSE)
            """

            if self.config_load['dc_voltage']:
                pass
            else:
                return True

            global count_temp
            self.TEST_MODE_M1000()
            test_sub_id = 0
            self.print_console("DC_VOLTAGE_MEASUREMENT TEST STARTED...")
            RESULT = []
            RESULT_1 = []
            RESULT_2 = []

            # self.pfc.pfc_set(0, 'bus', 1)
            self.pfc.pfc_set(0, 'battery_1', 1)

            self.smrcan.SMR_BATTERY_SET_VOLTAGE(53.5)
            self.dcload.DC_LOAD_SET_CURRENT_CC(20, "BATT")

            ATE_LOAD_COUNT = int(SettingRead('SETTING')['ate load count'])

            if ATE_LOAD_COUNT != 1:  # ONLY 1 LOAD IS CONFIGURED, 19/08/2016
                self.dcload.DC_LOAD_SET_CURRENT_CC(10, "BATT")

            if self.mcm_type == 3:
                self.dcload.DC_LOAD_SET_CURRENT_CC(10, "BATT")

            self.pfc.pfc_set(0, 'load_mains', 1)
            self.pfc.pfc_set(0, 'n_p_load_1', 1)

            batt_fuse_count = int(DefaultRead('DEFAULT SETTING')["battery ah"])
            print("battery Fuse Count =", batt_fuse_count)
            batt_lvd_count = int(ConfigRead('DUT CONFIGURATION')['no. of battery lvd'])
            load_current_count = int(ConfigRead('DUT CONFIGURATION')['no. of load current'])
            DCIF_CARD_TYPE = ConfigRead('DUT CONFIGURATION')['dcif card type']

            # CURRENT GAIN AND OFFSET IS MADE 0.
            bypass = True  # Changed to a boolean for clarity
            if DCIF_CARD_TYPE == 'HALL EFFECT' or bypass:
                total_channels = load_current_count + batt_lvd_count
                for channel in range(1, total_channels + 1):
                    gain = self.MCM_READ_COMMAND('CALIBRATE CURRENT', f'channel{channel} gain')
                    offset = self.MCM_READ_COMMAND('CALIBRATE CURRENT', f'channel{channel} offset')

                    self.print_console(f"CURRENT CHANNEL {channel} GAIN: {gain}")
                    self.print_console(f"CURRENT CHANNEL {channel} OFFSET: {offset}")

                    # Reset gain and offset if they are not zero
                    if gain != '0' or offset != '0':
                        self.MCM_WRITE_COMMAND('CALIBRATE CURRENT', f'channel{channel} gain', 0)
                        self.MCM_WRITE_COMMAND('CALIBRATE CURRENT', f'channel{channel} offset', 0)

                        # Re-read and log the updated values
                        gain = self.MCM_READ_COMMAND('CALIBRATE CURRENT', f'channel{channel} gain')
                        offset = self.MCM_READ_COMMAND('CALIBRATE CURRENT', f'channel{channel} offset')

                        self.print_console(f"CURRENT CHANNEL {channel} GAIN AFTER RESET: {gain}")
                        self.print_console(f"CURRENT CHANNEL {channel} OFFSET AFTER RESET: {offset}")

            if batt_fuse_count > 1 and batt_lvd_count == 1:
                self.prompt.Message(prompt='Switch OFF Battery MCBs/Remove Fuses')
                # self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'system reset', 1)
            else:
                None

            SET_INDI_BATTERY_PATH(1)

            for count in range(1, batt_fuse_count + 1):
                if self.part_number == "HE531053":
                    self.pfc.pfc_set(0, 'battery_mains', 0)
                    time.sleep(0.5)
                    self.pfc.pfc_set(0, 'battery_mains', 1)
                    time.sleep(10)
                    M1000Telnet.open_telnet()

                self.print_console("CHECKING FOR BATTERY: " + str(count))

                SET_INDI_BATTERY_PATH(count)
                SET_INDI_BATTERY_ISOLATE(self, count, 1)
                '''
                added time to observe and know real failure
                Author              : Paras
                Failure Observed    : In RAILTEL contactors are weld even after isolation!
                Date                : 06/08/2024
                '''
                time.sleep(10)
                for count_temp in range(1, batt_fuse_count + 1):
                    if count == count_temp:
                        actual_voltage = float(READ_DC_VOLTAGE(self, "BATT"))
                        DUT_batt_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'batt' + str(count_temp)))
                        print("Battery Passed voltage read by mcm = ", DUT_batt_volt)
                        RESULT_TEMP = True if abs(actual_voltage - DUT_batt_volt) < 5 else False
                        color = "GREEN" if RESULT_TEMP else "RED"
                        self.print_console("BATTERY " + str(count) + " VOLTAGE:" + str(DUT_batt_volt), color)
                        self.print_console("METER VOLTAGE:" + str(actual_voltage), color)
                        RESULT_1.append(RESULT_TEMP)
                    else:
                        DUT_batt_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'batt' + str(count_temp)))
                        retry_count = 0
                        while DUT_batt_volt > 2 and retry_count < 15:
                            DUT_batt_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'batt' + str(count_temp)))
                            time.sleep(1)
                            retry_count += 1
                        self.print_console("BATTERY " + str(count_temp) + " VOLTAGE:" + str(DUT_batt_volt))
                        if DUT_batt_volt > 10:
                            RESULT_TEMP = False
                            self.print_console("BATT " + str(count_temp) + "battery sense is short with BATT " + str(count), "RED")
                            RESULT_1.append(RESULT_TEMP)
                            return RESULT_1
                        else:
                            RESULT_TEMP = True
                        RESULT_1.append(RESULT_TEMP)
                DUT_bus_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'bus'))
                count_var = 0
                self.print_console("Checking Bus Voltage")
                if self.mcm_type == 3:
                    self.prompt.Message(prompt='Switch OFF Battery MCBs/Remove Fuses')
                while DUT_bus_volt > 5 and count_var <= 50 and (not self.part_number.lower() == 'he518750'):
                    DUT_bus_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'bus'))
                    time.sleep(1)
                    print("DUT V:", DUT_batt_volt)
                    count_var += 1
                self.print_console("BUS VOLTAGE:" + str(DUT_bus_volt))
                if self.part_number == "HE518916" or self.part_number == "HE518996" or self.part_number == "HE518750":
                    pass
                else:
                    if DUT_bus_volt <= 0:
                        RESULT_TEMP = True
                    else:
                        RESULT_TEMP = False
                        self.print_console("check BATT " + str(count_temp) + " LVD contactor wiring", "RED")
                    RESULT_1.append(RESULT_TEMP)
                SET_INDI_BATTERY_ISOLATE(self, count, 0)
                time.sleep(5)

            RESULT.append(CALCULATE_RESULT(RESULT_1))

            SET_INDI_BATTERY_PATH(1)

            if batt_fuse_count > 1 and batt_lvd_count == 1:
                self.prompt.Message(prompt='Switch ON Battery MCBs/Insert Fuses')

            if self.mcm_type == 3:
                self.prompt.Message(prompt='Switch ON Battery MCBs/Remove Fuses')

            for count in range(1, batt_fuse_count + 1):
                SET_INDI_BATTERY_PATH(count)
                time.sleep(2)
                for count_temp in range(1, batt_fuse_count + 1):
                    SET_INDI_BATTERY_PATH(count_temp)
                    time.sleep(2)
                    actual_voltage = float(READ_DC_VOLTAGE("BATT"))
                    DUT_batt_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'batt' + str(count_temp)))
                    if abs(actual_voltage - DUT_batt_volt) < 5:
                        RESULT_TEMP = True
                    else:
                        RESULT_TEMP = False
                    RESULT_2.append(RESULT_TEMP)
                    color = "GREEN" if RESULT_TEMP else "RED"
                    self.print_console("actual voltage: " + str(actual_voltage), color)
                    self.print_console("Battery Voltage " + str(count_temp) + ": " + str(DUT_batt_volt), color)

                DUT_bus_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'bus'))
                check_count = 0
                while DUT_bus_volt < 10 and check_count < 20:
                    DUT_bus_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'bus'))
                    time.sleep(1)
                    check_count += 1
                self.print_console("BUS Voltage: " + str(DUT_bus_volt))
                actual_voltage = float(READ_DC_VOLTAGE("BATT"))
                if abs(actual_voltage - DUT_bus_volt) < 5:
                    RESULT_TEMP = True
                    self.print_console("Bus Voltage OK!", "GREEN")
                else:
                    RESULT_TEMP = False
                    self.print_console("Bus Voltage FAIL!", "RED")
                RESULT_2.append(RESULT_TEMP)
            SET_BATTERY_ISOLATE(self, batt_lvd_count, 0)
            self.print_console("DC_VOLTAGE_MEASUREMENT TEST FINISHED...")
            self.excel_handler.update_cell("DC VOLTAGE TEST", CALCULATE_RESULT(RESULT_2))
            self.dcload.DC_LOAD_SET_CURRENT_CC(0, "LOAD")
            self.pfc.pfc_set(0, "bus", 0)

            RESULT.append(CALCULATE_RESULT(RESULT_2))
            return CALCULATE_RESULT(RESULT)

        except ZeroDivisionError as err:
            print(f"Handled ZeroDivisionError in outer function: {err}")
            self.all_stop = True
            self.print_console("ERROR IN COMMUNICATING WITH MCM", 'RED')
            self.print_console("STOPPING TEST", 'RED')
            return False
        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False

    def CALIBRATE_DC_VOLTAGE(self):
        try:
            if self.config_load['dc_voltage_calibration']:
                pass
            else:
                return True

            DCIF_CARD_TYPE = ConfigRead("DUT CONFIGURATION")['dcif card type']

            self.pfc.pfc_set(0, "battery_mains", 1)

            self.TEST_MODE_M1000()

            RESULT = []

            self.print_console("CALIBRATE DC VOLTAGE TEST STARTED...")

            self.MCM_WRITE_COMMAND('CALIBRATE DC VOLTAGE', 'channel1 deadband', 50)

            self.dcload.DC_LOAD_SET_CURRENT_CC(5)

            self.smrcan.SMR_BATTERY_SET_VOLTAGE(53.5)
            battery_fuse_count = int(DefaultRead('DEFAULT SETTING')[
                                         "battery ah"])  # int(ConfigRead("DUT CONFIGURATION")['no. of battery fuses'])

            DC_VOLTAGE_CALIBRATION_TOLERANCE = float(CalibrateSetting("GENERAL FACTORS")['dc voltage calibration tolerance'])

            for i in range(1, battery_fuse_count + 1):
                self.pfc.pfc_set(0, 'battery_' + str(i), 1)

            self.MCM_WRITE_COMMAND("CALIBRATE DC VOLTAGE", 'channel1 gain', 0)

            time.sleep(1)

            for i in range(0, 6):
                self.print_console("RESETTING VOLTAGE GAIN AND DEADBAND")
                self.MCM_WRITE_COMMAND('CALIBRATE DC VOLTAGE', f'channel{i + 1} deadband', 50)
                self.print_console(f"CHANNEL {i + 1} VOLTAGE DEADBAND: {self.MCM_READ_COMMAND('CALIBRATE DC VOLTAGE', f'channel{i + 1} deadband')}")
                self.MCM_WRITE_COMMAND("CALIBRATE DC VOLTAGE", f"channel{i + 1} gain", 0)
                self.print_console(f"CHANNEL {i + 1} VOLTAGE GAIN: {self.MCM_READ_COMMAND('CALIBRATE DC VOLTAGE', f'channel{i + 1} gain')}")
            if DCIF_CARD_TYPE != "SHUNT SMALL":
                actual_voltage = float(self.dcload.DC_LOAD_READ_OUTPUT_VOLTAGE())
                for i in range(1, battery_fuse_count + 1):
                    self.MCM_WRITE_COMMAND("CALIBRATE DC VOLTAGE", f"batt{i + 1}", actual_voltage)
                self.MCM_WRITE_COMMAND("CALIBRATE DC VOLTAGE", 'bus', actual_voltage)

            self.print_console("VERIFY VOLTAGE CALIBRATION")

            self.smrcan.SMR_BATTERY_SET_VOLTAGE(48)

            for i in range(1, battery_fuse_count + 1):
                DUTT_BATT_VOLT = float(self.MCM_READ_COMMAND("DC READ VOLTAGE", f'batt{i}'))
                while DUTT_BATT_VOLT < 48:
                    self.print_console(f'DUT: {DUTT_BATT_VOLT}')
                    DUTT_BATT_VOLT = float(self.MCM_READ_COMMAND("DC READ VOLTAGE", f'batt{i}'))
                actual_voltage = AVG_METER_VOLTAGE(self, "BATT")
                actual_voltage = round(actual_voltage, 2)

                if abs(DUTT_BATT_VOLT - actual_voltage) < DC_VOLTAGE_CALIBRATION_TOLERANCE:
                    RESULT_TEMP = True
                else:
                    RESULT_TEMP = False

                if RESULT_TEMP:
                    self.print_console(f'BATTERY {i} VOLTAGE: {DUTT_BATT_VOLT}', "GREEN")
                    self.print_console(f'METER VOLTAGE: {actual_voltage}', "GREEN")
                    self.print_console(f"BATTERY {i} VOLTAGE CALIBRATION OK", "GREEN")
                else:
                    self.print_console(f'BATTERY {i} VOLTAGE: {DUTT_BATT_VOLT}', "RED")
                    self.print_console(f'METER VOLTAGE: {actual_voltage}', "RED")
                    self.print_console(f"BATTERY {i} VOLTAGE CALIBRATION FAIL", "RED")
                RESULT.append(RESULT_TEMP)

            DUT_BUS_VOLTAGE = float(self.MCM_READ_COMMAND("DC READ VOLTAGE", 'bus'))
            actual_voltage = round(float(READ_DC_VOLTAGE("BATT")), 2)

            if abs(DUT_BUS_VOLTAGE - actual_voltage) < DC_VOLTAGE_CALIBRATION_TOLERANCE:
                RESULT_TEMP = True
            else:
                RESULT_TEMP = False

            time.sleep(1)

            if RESULT_TEMP:
                self.print_console(f'BUS VOLTAGE: {DUT_BUS_VOLTAGE}', "GREEN")
                self.print_console(f'METER VOLTAGE: {actual_voltage}', "GREEN")
                self.print_console(f"BUS VOLTAGE CALIBRATION OK", "GREEN")
            else:
                self.print_console(f'BUS VOLTAGE: {DUT_BUS_VOLTAGE}', "RED")
                self.print_console(f'METER VOLTAGE: {actual_voltage}', "RED")
                self.print_console(f"BUS VOLTAGE CALIBRATION FAIL", "RED")
            RESULT.append(RESULT_TEMP)

            self.smrcan.SMR_BATTERY_SET_VOLTAGE(56)
            time.sleep(2)

            for i in range(1, battery_fuse_count + 1):
                DUTT_BATT_VOLT = float(self.MCM_READ_COMMAND("DC READ VOLTAGE", f'batt{i}'))

                actual_voltage = AVG_METER_VOLTAGE(self, "BATT")
                actual_voltage = round(actual_voltage, 2)

                if abs(DUTT_BATT_VOLT - actual_voltage) < DC_VOLTAGE_CALIBRATION_TOLERANCE:
                    RESULT_TEMP = True
                else:
                    RESULT_TEMP = False

                if RESULT_TEMP:
                    self.print_console(f'BATTERY {i} VOLTAGE: {DUTT_BATT_VOLT}', "GREEN")
                    self.print_console(f'METER VOLTAGE: {actual_voltage}', "GREEN")
                    self.print_console(f"BATTERY {i} VOLTAGE CALIBRATION OK", "GREEN")
                else:
                    self.print_console(f'BATTERY {i} VOLTAGE: {DUTT_BATT_VOLT}', "RED")
                    self.print_console(f'METER VOLTAGE: {actual_voltage}', "RED")
                    self.print_console(f"BATTERY {i} VOLTAGE CALIBRATION FAIL", "RED")
                RESULT.append(RESULT_TEMP)

            DUT_BUS_VOLTAGE = float(self.MCM_READ_COMMAND("DC READ VOLTAGE", 'bus'))
            actual_voltage = round(float(READ_DC_VOLTAGE("BATT")), 2)

            if abs(DUT_BUS_VOLTAGE - actual_voltage) < DC_VOLTAGE_CALIBRATION_TOLERANCE:
                RESULT_TEMP = True
            else:
                RESULT_TEMP = False

            time.sleep(1)

            if RESULT_TEMP:
                self.print_console(f'BUS VOLTAGE: {DUT_BUS_VOLTAGE}', "GREEN")
                self.print_console(f'METER VOLTAGE: {actual_voltage}', "GREEN")
                self.print_console(f"BUS VOLTAGE CALIBRATION OK", "GREEN")
            else:
                self.print_console(f'BUS VOLTAGE: {DUT_BUS_VOLTAGE}', "RED")
                self.print_console(f'METER VOLTAGE: {actual_voltage}', "RED")
                self.print_console(f"BUS VOLTAGE CALIBRATION FAIL", "RED")
            RESULT.append(RESULT_TEMP)
            self.dcload.DC_LOAD_SET_CURRENT_CC(0, "LOAD")
            self.pfc.pfc_set(0, "bus", 0)


            """DG TEST"""
            if self.customer_name_edit.text() == "BHARTI":
                RESULT.append(self.RETRY_FUNCTION(5, self.DG_CKT_TEST))

            return CALCULATE_RESULT(RESULT)

        except ZeroDivisionError as err:
            print(f"Handled ZeroDivisionError in outer function: {err}")
            self.all_stop = True
            self.print_console("ERROR IN COMMUNICATING WITH MCM", 'RED')
            self.print_console("STOPPING TEST", 'RED')
            return False
        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False

    def DG_CKT_TEST(self):
        RESULT = []

        self.print_console("DG Contactor Test Started...")
        self.smrcan.SMR_BATTERY_SET_VOLTAGE(46.0)
        time.sleep(2)
        self.dcload.DC_LOAD_SET_CURRENT_CC(30)
        time.sleep(2)
        self.prompt.Message(prompt="Turn DGBC UNIT TO MANUAL MODE")

        MANUAL_START_STOP = {
            'START': 'GREEN',
            'STOP': 'RED'
        }

        for item in MANUAL_START_STOP.keys():
            if self.prompt.User_prompt(f'PRESS {item} BUTTON AND CHECK {MANUAL_START_STOP[item]} LED LIGHT, IS IT ON?'):
                RESULT.append(True)
                self.print_console(f'Manual {item} PULSE is OK', "GREEN")
            else:
                RESULT.append(False)
                self.print_console(f'Manual {item} PULSE is not OK', 'RED')

        self.prompt.Message(prompt="Turn BACK DGBC UNIT TO AUTO MODE")

        ACSET(self.pfc, 3, 1)

        self.prompt.Message(prompt="Switch off mains mccb\nTurn on dg mccb.".upper())

        RESULT.append(self.RETRY_FUNCTION(5, self.REGISTER_SMRS))

        dg_cont_on = self.MCM_READ_COMMAND("ALARM", 'dg contactor on')
        if dg_cont_on:
            RESULT.append(True)
            self.print_console("dg Cont ON", "GREEN")
        else:
            RESULT.append(False)
            self.print_console("dg CONT FAIL", "RED")

        time.sleep(2)

        config_smr_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'smr count'))
        if int(self.MCM_READ_COMMAND(section="TAB.1441.0", pool=1)) == config_smr_count:
            self.print_console("ALL CONNECTIONS OK", 'GREEN')
        else:
            for smr_count in range(1, config_smr_count + 1):
                smr_status = int(self.MCM_READ_COMMAND('SMR COMMANDS', 'smr' + str(smr_count) + " status"))
                print("status of smr is :", smr_status)
                if smr_status == 1:
                    RESULT.append(True)
                    self.print_console("SMR " + str(smr_count) + " WIRING OK", "GREEN")
                else:
                    RESULT.append(False)
                    self.print_console("SMR " + str(smr_count) + " WIRING FAULTY ", 'RED')

        RESULT.append(self.RETRY_FUNCTION(5, self.DG_AC_PARAM))

        RESULT.append(self.RETRY_FUNCTION(5, self.DG_BATTERY_TEST))

        RESULT.append(self.RETRY_FUNCTION(5, self.DG_ALARMS))

        ACSET(self.pfc, 3, 0)

        self.prompt.Message(prompt="Switch ON mains mccb\nTurn OFF dg mccb.")

        return CALCULATE_RESULT(RESULT)


    def DG_ALARMS(self):
        RESULT = []

        if str(SettingRead("STATION")['id']) in ["C", "E"]:
            self.print_console("DG Alarm Test Check Started...")

            alarm_dict_dg = {
                'pfc 15': 'LLOP FAULT',
                'pfc 3': 'DG DOOR OPEN',
                'pfc 4': 'DG V BELT BREAK',
                'pfc 6': 'DG FUEL LOW 1 FAULT',
                'pfc 7': 'DG FUEL LOW 2 FAULT',
                'pfc 8': 'DG HCT FAULT'
            }

            for i in alarm_dict_dg.keys():
                self.print_console(f'Checking for {alarm_dict_dg[i]} Alarm')
                self.pfc.pfc_set(0, f'{i}', 1)

                """TIME-SAVING LOGIC WITH RETRY"""
                alarm_status = self.DG_ALARM_CHECK(alarm_dict_dg[i])
                retry_count = 0
                while not alarm_status and retry_count < 20:
                    if not alarm_status:
                        time.sleep(1)
                    alarm_status = self.DG_ALARM_CHECK(alarm_dict_dg[i])
                    retry_count += 1

                if alarm_status:
                    RESULT.append(True)
                    self.print_console(f"ALARM STATUS FOR {alarm_dict_dg[i]} IS OK", "GREEN")
                else:
                    RESULT.append(False)
                    self.print_console(f"ALARM STATUS FOR {alarm_dict_dg[i]} IS FAIL", "RED")

                self.pfc.pfc_set(0, f'{i}', 0)
                time.sleep(3)

        else:
            self.print_console("KINDLY CHECK DG ALARM MANUALLY!")
            RESULT.append(True)

        return CALCULATE_RESULT(RESULT)


    def DG_AC_PARAM(self):
        RESULT = []
        temp_value = self.prompt.user_value_2("Enter Single Phase Voltage via DMM\nOnly Enter INTEGER VALUE", "V")
        self.print_console(f"Voltage entered is : {temp_value}")
        temp_value1 = self.MCM_READ_COMMAND("DG READ VOLTAGE", 'r phase')
        if abs(float(temp_value) - float(temp_value1)) < 10:
            RESULT.append(True)
            self.print_console(f"DG input Voltage is OK: {temp_value1}", 'GREEN')
        else:
            RESULT.append(False)
            self.print_console(f"DG input Voltage is not OK: {temp_value1}", 'RED')

        temp_value1 = self.MCM_READ_COMMAND("DG READ CURRENT", 'r phase')
        if float(temp_value1) > 0:
            RESULT.append(True)
            self.print_console(f"DG input Current is OK: {temp_value1}", 'GREEN')
        else:
            RESULT.append(False)
            self.print_console(f"DG input Current is not OK: {temp_value1}", 'RED')

        return CALCULATE_RESULT(RESULT)

    def DG_BATTERY_TEST(self):
        self.prompt.Message(prompt="CONNECT 12VDC BATTERY")
        time.sleep(2)
        temp_value1 = self.MCM_READ_COMMAND(section="TAB.4480.0", pool=1)
        if float(temp_value1) > 8:
            self.print_console(f"DG Battery Voltage is OK: {temp_value1}", 'GREEN')
            return True
        else:
            self.print_console(f"DG Battery Voltage is not OK: {temp_value1}", 'RED')
            self.print_console("It should be more than 12V, kindly check Battery Voltage")
            return False

    def RETRY_FUNCTION(self, RETRY_COUNT, FUNC):
        retry_count = 0
        while retry_count < RETRY_COUNT:
            function_status = FUNC()
            if function_status:
                return True
            if not self.prompt.User_prompt(f"Do you want to retry the test : {FUNC.__name__}?"):
                return False
            retry_count += 1
        return False

    def REGISTER_SMRS(self):
        RESULT = []
        smr_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'smr count'))
        self.MCM_WRITE_COMMAND("SMR COMMANDS", 'deregister all smr', str(1))
        TimerPrompt(self, f"TESTING FOR {smr_count} SMR(S). SWITCH ON SMR ONE BY ONE TO REGISTER. AFTER REGISTRATION, PRESS ENTER KEY!", 500)

        for count in range(1, smr_count + 1):
            if self.MCM_READ_COMMAND('SMR COMMANDS', f'smr{count} id') != "":
                self.print_console(f"SMR {count} REGISTERED", "GREEN")
                RESULT_TEMP = True
            else:
                self.print_console(f"SMR {count} NOT REGISTERED", "RED")
                RESULT_TEMP = False
            RESULT.append(RESULT_TEMP)

        return CALCULATE_RESULT(RESULT)

    def DG_ALARM_CHECK(self, alarm_name):
        # define DGALT_BIT_POS       0x0001
        # define DGHCT_BIT_POS       0x0002
        # define DGLLOP_BIT_POS      0x0004
        # define DGFUEL_LOW_BITPOS   0x0008
        # define DGFLT_START_BITPOS  0x0010
        # define DGFLT_STOP_BITPOS   0x0020
        # define DGFLT_EMRG_BITPOS   0x0040
        # define DG_FREQABN          0x0080
        # define DGFUEL_LOW1         0x0100
        # define DGFUEL_LOW2         0x0200
        # define DG_VBELTBREAK       0x0400
        # define DGFLT_COMMONBIT    0x0800
        # define DGDOOROPEN          0x8000

        DG_ALARM_LIST = ['ALTERNATOR FAULT', 'DG HCT FAULT', 'LLOP FAULT', 'DG FUEL LOW FAULT',
                         'DG START', 'DG STOP', 'DG EMERGENCY FAULT', 'DG FREQUENCY ABNORMAL',
                         'DG FUEL LOW 1 FAULT', 'DG FUEL LOW 2 FAULT', 'DG V BELT BREAK', 'DG FAULT',
                         'reserved', 'reserved', 'reserved', 'DG DOOR OPEN']
        DG_ALARM_LIST_2 = ['reserved', 'reserved', 'reserved', 'reserved',
                           'reserved', 'reserved', 'reserved', 'reserved',
                           'reserved', 'reserved', 'reserved', 'reserved',
                           'reserved', 'reserved', 'reserved', 'DG DOOR OPEN']

        if alarm_name != 'DG DOOR OPEN':
            alarm_byte = int(self.MCM_READ_COMMAND('DG', 'dg alarm byte'))

        else:
            alarm_byte = int(self.MCM_READ_COMMAND('DG', 'dg alarm byte2'))

        for item in DG_ALARM_LIST:
            if alarm_name == item:
                alarm_bit_location = pow(2, int(DG_ALARM_LIST.index(item)))
        # self.print_console(f'{alarm_bit_location}, : {alarm_byte}')
        if alarm_byte & alarm_bit_location == alarm_bit_location:
            return True
        else:
            return False

    def DC_CURRENT_MEASUREMENT_BATT_DISCHARGE(self):
        try:
            if self.config_load['dc_current_discharge']:
                pass
            else:
                return True

            global RESULT_TEMP_MCB_TRIP, count_temp
            if self.mcm_type == 1:
                self.MCM_WRITE_COMMAND("SYSTEM COMMANDS", 'ate test', 'TEST_M1000_ATE')

            test_sub_id = 0

            self.print_console("DC CURRENT MEASUREMENT BATT DISCHARGE TEST STARTED...")

            batt_fuse_count = int(DefaultRead('DEFAULT SETTING')[
                                      "battery ah"])  # int(ConfigRead('DUT CONFIGURATION')['no. of battery fuses'])
            batt_lvd_count = int(ConfigRead('DUT CONFIGURATION')['no. of battery lvd'])
            load_lvd_count = int(ConfigRead('DUT CONFIGURATION')['no. of load lvd'])
            load_current_count = int(ConfigRead('DUT CONFIGURATION')['no. of load current'])
            load_current_sensor_state = ConfigRead('DUT CONFIGURATION')['load current sensor']
            DC_CURRENT_FACTOR_PERCENTAGE = float(CalibrateSetting('GENERAL FACTORS')['dc current check factor percentage'])
            DC_CURRENT_TOLERANCE_PERCENTAGE = float(
                CalibrateSetting('GENERAL FACTORS')['dc current check tolerance percentage'])
            DCIF_CARD_TYPE = ConfigRead('DUT CONFIGURATION')['dcif card type']

            if DCIF_CARD_TYPE == "HALL EFFECT":
                CURRENT_SENSOR_VALUE = int(ConfigRead("DUT CONFIGURATION")['channel1 hall effect value'])
            else:
                CURRENT_SENSOR_VALUE = int(ConfigRead("DUT CONFIGURATION")['channel1 shunt value'])

            LOAD_SET_CURRENT = int(CURRENT_SENSOR_VALUE * (float(DC_CURRENT_FACTOR_PERCENTAGE) / 100))
            LOAD_CURRENT_OFFSET = int(CURRENT_SENSOR_VALUE * (float(DC_CURRENT_TOLERANCE_PERCENTAGE) / 100))
            self.smrcan.SMR_BATTERY_SET_VOLTAGE(53.5)
            print("LOAD VALUE :", LOAD_SET_CURRENT)
            self.dcload.DC_LOAD_SET_CURRENT_CC(0, "LOAD")
            RESULT = []
            self.pfc.pfc_set(0, 'battery_mains', 1)
            SET_INDI_BATTERY_PATH(1)  ## NEED TO MODIFY PFC PART CODE
            self.pfc.pfc_set(0, 'load_mains', 1)
            for i in range(1, 5):
                self.pfc.pfc_set(0, 'bus', 0)
            if load_lvd_count == 1:
                self.pfc.pfc_set(0, 'p_load', 1)
                print("primary load")
            else:
                self.pfc.pfc_set(0, 'p_load', 0)
                print("primary load not ok")

            self.pfc.pfc_set(0, 'r_phase', 0)
            self.pfc.pfc_set(0, 'y_phase', 0)
            self.pfc.pfc_set(0, 'b_phase', 0)
            for i in range(1, 4):
                self.pfc.pfc_set(0, 'n_p_load_1', 1)
            self.dcload.DC_LOAD_SET_CURRENT_CC(LOAD_SET_CURRENT, "LOAD")
            for i in range(1, load_lvd_count + 2):
                self.pfc.pfc_set(0, 'n_p_load_' + str(i), 1)

            for count in range(1, batt_lvd_count + 1):
                self.print_console(f"CHECKING BATTERY {count} DISCHARGE CURRENT")
                SET_INDI_BATTERY_PATH(count)
                time.sleep(2)

                for count_temp in range(1, batt_lvd_count + 1):
                    if count == count_temp or batt_lvd_count < 2:
                        actual_current = float(READ_DC_CURRENT("LOAD"))
                        if actual_current > (LOAD_SET_CURRENT - LOAD_CURRENT_OFFSET):
                            actual_current = -1 * actual_current
                            self.print_console(f"METER CURRENT {actual_current}")
                            DUT_BATT_CURRENT = float(self.MCM_READ_COMMAND("DC READ CURRENT", f'batt{count_temp}'))
                            self.print_console(f'DUT BATTERY CURRENT: {DUT_BATT_CURRENT}')
                            if abs(actual_current - DUT_BATT_CURRENT) < LOAD_CURRENT_OFFSET:
                                self.print_console(f"BATTERY {count} CURRENT SENSOR/CABLE IS OK")
                                RESULT.append(True)
                            else:
                                self.print_console(f"BATTERY {count} CURRENT SENSOR/CABLE IS FAULTY", 'RED')
                                RESULT.append(False)

                        else:
                            actual_voltage = float(READ_DC_VOLTAGE("LOAD"))
                            self.print_console(f'METER VOLTAGE: {actual_voltage}')
                            battery_voltage = self.MCM_READ_COMMAND("DC READ VOLTAGE", f'batt{count_temp}')
                            dut_batt_volt = float(battery_voltage if battery_voltage is not None else 0)
                            self.print_console(f"DUT BATT VOLTAGE: {dut_batt_volt}")
                            if abs(actual_voltage - dut_batt_volt) < 10:
                                self.print_console("LOAD LVD CONTACTOR IS FAULTY", 'RED')
                            else:
                                self.print_console(f"BATTERY {count_temp} LVD CONTACTOR IS FAULT", 'RED')
                            RESULT.append(False)
                    elif count != count_temp and batt_lvd_count > 1:
                        DUT_BATT_CURRENT = float(self.MCM_READ_COMMAND("DC READ CURRENT", f'batt{count_temp}'))
                        if DUT_BATT_CURRENT < -5:
                            RESULT_TEMP = False
                        else:
                            RESULT_TEMP = True
                        RESULT.append(RESULT_TEMP)
                load_current_sum = 0
                if load_current_count < 2:
                    DUT_load_current = float(self.MCM_READ_COMMAND('DC READ CURRENT', f'load{1}'))
                    load_current_sum += DUT_load_current
                    self.print_console(f"DUT LOAD CURRENT{DUT_load_current}")
                    if load_current_sensor_state == 'ENABLE':
                        actual_current = float(READ_DC_CURRENT("LOAD"))
                        if actual_current > (LOAD_SET_CURRENT - LOAD_CURRENT_OFFSET):
                            # RESULT_TEMP = COMPARE(actual_current, load_current_sum, LOAD_CURRENT_OFFSET)
                            if abs(actual_current - load_current_sum) < LOAD_CURRENT_OFFSET:
                                self.print_console("LOAD CURRENT SENSOR 1 is OK")
                                RESULT.append(True)
                            else:
                                self.print_console("LOAD CURRENT SENSOR 1 is FAULTY", "RED")
                                RESULT.append(False)
                        else:
                            actual_voltage = float(READ_DC_VOLTAGE("LOAD"))
                            self.print_console(f"actual voltage: {actual_current}")
                            DUT_batt_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', f'batt{count_temp}'))
                            if abs(actual_voltage - DUT_batt_volt) > 5:
                                self.print_console("Load LVD contactor is faulty", "RED")
                                RESULT_TEMP = False
                            else:
                                self.print_console("Battery " + str(count_temp) + " LVD contactor is faulty", "RED")
                                RESULT_TEMP = False
                            RESULT.append(RESULT_TEMP)
                            self.print_console(str(RESULT))
                    else:
                        self.print_console("Load CURRENT SENSOR NOT AVAILABLE")
                        RESULT_TEMP = True
                        RESULT.append(RESULT_TEMP)

                else:
                    for i in range(1, load_current_count + 1):  ##CODE TO BE ADDED FOR INDIVIDUAL LOAD PATH CURRENT CHECK
                        SET_INDI_LOAD_PATH(self, i)
                        time.sleep(2)
                        DUT_load_current = float(self.MCM_READ_COMMAND('DC READ CURRENT', 'load' + str(i)))
                        load_current_sum += DUT_load_current
                        actual_current = float(READ_DC_CURRENT("LOAD"))
                        self.print_console("DUT LOAD CURRENT " + str(i) + ": " + str(DUT_load_current))
                        self.print_console("actual_current: " + str(actual_current))
                        self.print_console("LOAD_CURRENT_OFFSET: " + str(LOAD_CURRENT_OFFSET))
                        if load_current_sensor_state == 'ENABLE':
                            if actual_current > (LOAD_SET_CURRENT - LOAD_CURRENT_OFFSET):
                                # RESULT_TEMP = COMPARE(actual_current, DUT_load_current, LOAD_CURRENT_OFFSET)
                                if abs(actual_current - DUT_load_current) > LOAD_CURRENT_OFFSET:
                                    self.print_console("LOAD CURRENT SENSOR " + str(i) + " is FAULTY", "RED")
                                    RESULT.append(False)
                                else:
                                    RESULT.append(True)
                                    self.print_console("LOAD CURRENT SENSOR " + str(i) + " is OK")


                            else:
                                # PRINT_CONSOLE(self,"CHECKING ELSE CONDITION")
                                actual_voltage = float(READ_DC_VOLTAGE("LOAD"))
                                self.print_console("actual voltage: " + str(actual_voltage))
                                DUT_batt_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'batt' + str(count_temp)))
                                if abs(actual_voltage - DUT_batt_volt) < 5:
                                    self.print_console("Load " + str(i) + " LVD contactor is faulty", "RED")
                                    RESULT_TEMP = False
                                else:
                                    self.print_console("Battery " + str(count_temp) + " LVD contactor is faulty", "RED")
                                    RESULT_TEMP = False
                                RESULT.append(RESULT_TEMP)
                                self.print_console(str(RESULT))
                        # load_current_sum+=DUT_load_current

                        else:
                            self.print_console("Load CURRENT SENSOR NOT AVAILABLE")
                            RESULT_TEMP = True
                            RESULT.append(RESULT_TEMP)

                        self.print_console(f"load_current_sum: {load_current_sum}")
                        self.print_console(f"Load CURRENT {i} : {DUT_load_current}")
                actual_current = float(READ_DC_CURRENT("LOAD"))
                self.print_console(f"METER CURRENT {actual_current}")

            # if load_lvd_count > 1:
            #     self.prompt.Message(prompt="SWITCH ON SYSTEM PRIORITY LOAD MCBs FOR ALL OPERATORS")
            ## this is for critical load
            if load_lvd_count != 0 and load_current_sensor_state == 'ENABLE':
                self.pfc.pfc_set(0, 'p_load', 1)
                load_current_sum = 0
                SET_LOAD_ISOLATE(self, load_current_count, 1)
                for i in range(1, load_current_count + 1):
                    self.pfc.pfc_set(0, 'n_p_load_' + str(i), 0)
                time.sleep(3)
                for i in range(1, load_current_count + 1):
                    DUT_load_current = float(self.MCM_READ_COMMAND('DC READ CURRENT', 'load' + str(i)))
                    load_current_sum += DUT_load_current
                actual_current = float(READ_DC_CURRENT("LOAD"))

                self.print_console("load_current_sum: " + str(load_current_sum))
                self.print_console("actual_current: " + str(actual_current))
                self.print_console("LOAD_CURRENT_OFFSET: " + str(LOAD_CURRENT_OFFSET))
                if actual_current > (LOAD_SET_CURRENT - LOAD_CURRENT_OFFSET):
                    if abs(actual_current - load_current_sum) > LOAD_CURRENT_OFFSET:
                        self.print_console("PL LOAD NOT OK", "RED")
                        RESULT.append(False)
                    else:
                        self.print_console("PL LOAD OK")
                        RESULT.append(True)
                        # raw_input("check")


                else:
                    actual_voltage = float(READ_DC_VOLTAGE("LOAD"))
                    self.print_console("actual voltage: " + str(actual_voltage))
                    DUT_batt_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'batt' + str(count_temp)))
                    if abs(actual_voltage - DUT_batt_volt) < 5:
                        self.print_console("Load LVD contactor is faulty", "RED")
                        RESULT_TEMP = False
                    else:
                        self.print_console("Battery " + str(count_temp) + " LVD contactor is faulty", "RED")
                        RESULT_TEMP = False
                    RESULT.append(RESULT_TEMP)
                    self.print_console(str(RESULT))
            SET_LOAD_ISOLATE(self, load_current_count, 0)
            for i in range(1, load_current_count + 1):
                self.pfc.pfc_set(0, 'n_p_load_' + str(i), 1)

            self.print_console("DC_CURRENT_MEASUREMENT_BATT_DISCHARGE TEST FINISHED...")
            if not self.config_load['mccb_trip']:
                self.print_console("LOAD FUSE FAIL/ DC MCCB TRIP ALARM NOT APPLICABLE")
                RESULT_TEMP_MCB_TRIP = True
            else:
                print("Testing Load MCB TRIP alarm")
                self.print_console("LOAD FUSE FAIL/DC MCB TRIP ALARM TEST STARTED...")
                ip_pfc_state = True
                while ip_pfc_state:
                    if int(self.MCM_READ_COMMAND('DCIF 8 IP PFC', 'pfc')) != 0:
                        self.prompt.Message(prompt="CLEAR IP PFC ALARM BEFORE STARTING TEST")
                    else:
                        ip_pfc_state = False
                        self.prompt.Message(prompt="SWITCH OFF LOAD MCBs!")
                        self.print_console("WAITING FOR 5 SECONDS! ")
                        time.sleep(5)
                        if int(self.MCM_READ_COMMAND('ALARM', 'dccb trip')) == 1:
                            RESULT_TEMP_MCB_TRIP = True
                            self.print_console("DCCB TRIP ALARM TESTED OK ")
                        else:
                            RESULT_TEMP_MCB_TRIP = False
                            self.print_console("DCCB TRIP ALARM TEST FAIL ", "RED")

                self.prompt.Message(prompt="SWITCH 'ON' LOAD MCBs!")
                self.print_console("LOAD FUSE FAIL/DC MCB TRIP ALARM TEST FINISHED...")

            RESULT.append(RESULT_TEMP_MCB_TRIP)
            self.pfc.pfc_set(0, 'p_load', 0)
            return CALCULATE_RESULT(RESULT)
        except ZeroDivisionError as err:
            print(f"Handled ZeroDivisionError in outer function: {err}")
            self.all_stop = True
            self.print_console("ERROR IN COMMUNICATING WITH MCM", 'RED')
            self.print_console("STOPPING TEST", 'RED')
            return False
        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False

    def MCCB_TRIP(self):
        global color
        self.print_console("LOAD FUSE FAIL/DC MCB TRIP ALARM TEST STARTED...")

        while int(self.MCM_READ_COMMAND('DCIF 8 IP PFC', 'pfc')) != 0:
            self.prompt.Message(prompt="CLEAR IP PFC ALARM BEFORE STARTING TEST")

        self.prompt.Message(prompt="SWITCH OFF LOAD MCBs!")
        self.print_console("WAITING FOR 5 SECONDS!")
        time.sleep(5)
        color = "GREEN" if int(self.MCM_READ_COMMAND('ALARM', 'dccb trip')) == 1 else "RED"
        self.print_console(f"DCCB TRIP ALARM TESTED {'OK' if color == 'GREEN' else 'FAULTY'}", color)
        self.prompt.Message(prompt="SWITCH 'ON' LOAD MCBs!")

        self.print_console("LOAD FUSE FAIL/DC MCB TRIP ALARM TEST FINISHED...")
        return color == 'GREEN'

    def DC_CURRENT_DISCHARGE(self):
        RESULT = []
        self.print_console("DC CURRENT MEASUREMENT BATT DISCHARGE TEST STARTED...")

        # Load configuration and calibration settings
        config = ConfigRead('DUT CONFIGURATION')
        calibration = CalibrateSetting('GENERAL FACTORS')

        batt_lvd_count = int(config['no. of battery lvd'])
        load_lvd_count = int(config['no. of load lvd'])
        load_current_count = int(config['no. of load current'])
        load_current_sensor_state = config['load current sensor']
        DCIF_CARD_TYPE = config['dcif card type']
        DC_CURRENT_FACTOR_PERCENTAGE = float(calibration['dc current check factor percentage'])
        DC_CURRENT_TOLERANCE_PERCENTAGE = float(calibration['dc current check tolerance percentage'])

        CURRENT_SENSOR_VALUE = int(config['channel1 hall effect value'] if DCIF_CARD_TYPE == "HALL EFFECT" else config['channel1 shunt value'])
        LOAD_SET_CURRENT = int(CURRENT_SENSOR_VALUE * (DC_CURRENT_FACTOR_PERCENTAGE / 100))
        LOAD_CURRENT_OFFSET = int(CURRENT_SENSOR_VALUE * (DC_CURRENT_TOLERANCE_PERCENTAGE / 100))

        self.smrcan.SMR_BATTERY_SET_VOLTAGE(53.5)
        self.dcload.DC_LOAD_SET_CURRENT_CC(0, "LOAD")
        self.pfc.pfc_set(0, 'battery_mains', 1)
        self.pfc.pfc_set(0, 'load_mains', 1)
        self.pfc.pfc_set(0, 'bus', 0)

        # Set primary load
        self.pfc.pfc_set(0, 'p_load', 1 if load_lvd_count == 1 else 0)
        if load_lvd_count != 1:
            self.print_console("Primary load not ok")

        # AC Supply check
        if self.pfc.read_pfc_output(0x60A, 'r_phase'):
            ACSET(self.pfc, 3, 0)

        # Activate load paths
        for i in range(1, 3):
            self.pfc.pfc_set(0, 'n_p_load_1', 1)

        self.dcload.DC_LOAD_SET_CURRENT_CC(LOAD_SET_CURRENT, "LOAD")
        for i in range(1, load_lvd_count + 2):
            self.pfc.pfc_set(0, f'n_p_load_{i}', 1)

        # Battery discharge test
        for count in range(1, batt_lvd_count + 1):
            self.print_console(f"CHECKING BATTERY {count} DISCHARGE CURRENT")
            SET_INDI_BATTERY_PATH(count)
            time.sleep(2)

            for count_temp in range(1, batt_lvd_count + 1):
                is_main_battery = count == count_temp or batt_lvd_count < 2
                actual_current = float(READ_DC_CURRENT("LOAD"))

                if is_main_battery:
                    if actual_current > (LOAD_SET_CURRENT - LOAD_CURRENT_OFFSET):
                        actual_current = -actual_current
                        self.print_console(f"METER CURRENT {actual_current}")
                        DUT_BATT_CURRENT = float(self.MCM_READ_COMMAND("DC READ CURRENT", f'batt{count_temp}'))
                        color = "GREEN" if abs(actual_current - DUT_BATT_CURRENT) < LOAD_CURRENT_OFFSET else "RED"
                        self.print_console(f'DUT BATTERY CURRENT: {DUT_BATT_CURRENT}', color)
                        self.print_console(f"BATTERY {count} CURRENT SENSOR/CABLE IS {'OK' if color == 'GREEN' else 'FAULTY'}", color)
                        RESULT.append(color == "GREEN")
                    else:
                        actual_voltage = float(READ_DC_VOLTAGE("LOAD"))
                        self.print_console(f'METER VOLTAGE: {actual_voltage}')
                        battery_voltage = self.MCM_READ_COMMAND("DC READ VOLTAGE", f'batt{count_temp}')
                        dut_batt_volt = float(battery_voltage or 0)
                        if abs(actual_voltage - dut_batt_volt) < 10:
                            self.print_console("LOAD LVD CONTACTOR IS FAULTY", 'RED')
                        else:
                            self.print_console(f"BATTERY {count_temp} LVD CONTACTOR IS FAULT", 'RED')
                        RESULT.append(False)
                elif DUT_BATT_CURRENT := float(self.MCM_READ_COMMAND("DC READ CURRENT", f'batt{count_temp}')):
                    RESULT.append(DUT_BATT_CURRENT >= -5)

            # Load current checks
            def check_load_current():
                load_current_sum = 0
                for i in range(1, load_current_count + 1):
                    DUT_load_current = float(self.MCM_READ_COMMAND('DC READ CURRENT', f'load{i}'))
                    load_current_sum += DUT_load_current
                    actual_current = float(READ_DC_CURRENT("LOAD"))
                    if load_current_sensor_state == 'ENABLE' and abs(actual_current - DUT_load_current) > LOAD_CURRENT_OFFSET:
                        self.print_console(f"LOAD CURRENT SENSOR {i} IS FAULTY", "RED")
                        RESULT.append(False)
                    else:
                        self.print_console(f"LOAD CURRENT SENSOR {i} IS OK", "GREEN")
                        RESULT.append(True)
                return load_current_sum

            load_current_sum = check_load_current()

        # Final load validation
        actual_current = float(READ_DC_CURRENT("LOAD"))
        if load_lvd_count and load_current_sensor_state == 'ENABLE':
            SET_LOAD_ISOLATE(self, load_current_count, 1)
            for i in range(1, load_current_count + 1):
                DUT_load_current = float(self.MCM_READ_COMMAND('DC READ CURRENT', f'load{i}'))
                load_current_sum += DUT_load_current
            if abs(actual_current - load_current_sum) > LOAD_CURRENT_OFFSET:
                self.print_console("PL LOAD NOT OK", "RED")
                RESULT.append(False)
            else:
                self.print_console("PL LOAD OK")
                RESULT.append(True)
        SET_LOAD_ISOLATE(self, load_current_count, 0)

        self.print_console("DC CURRENT MEASUREMENT BATT DISCHARGE TEST FINISHED...")

        self.pfc.pfc_set(0, 'p_load', 0)

        return CALCULATE_RESULT(RESULT)

    def SMR_REGISTRATION(self):
        try:
            if not self.config_load['smr_registration']:
                return True

            self.TEST_MODE_M1000()

            self.dcload.DC_LOAD_SET_CURRENT_CC(10, "LOAD")

            RESULT = []

            self.print_console("SMR REGISTRATION TEST STARTED...")

            smr_count = int(DefaultRead("DUT CONFIGURATION")['smr count'])

            if self.custom_check.isChecked():
                if DefaultRead('DEFAULT SETTING STATE')['comm smr count'] == "YES":
                    smr_count = int(DefaultRead("DEFAULT SETTING")['comm smr count'])
                    self.MCM_WRITE_COMMAND("SYSTEM CONFIG", 'smr count', str(smr_count))

            if self.mcm_type == 3:
                if self.prompt.User_prompt("Kindly check for Mains Fail Alarm, Press OK if coming?"):
                    self.print_console("MAINS fail alarm OK", "GREEN")
                    RESULT.append(True)
                else:
                    self.print_console("MAINS fail alarm FAIL", "RED")
                    RESULT.append(False)

            if self.customer_name_edit.text() != 'BHARTI':
                ac_phase_type = ConfigRead('DUT CONFIGURATION')['ac phases type']
                hvlv_card_type = ConfigRead('DUT CONFIGURATION')['ac ip voltage source']

                phase_mapping = {'SINGLE PHASE': 1, 'THREE PHASE': 3}
                ACSET(self.pfc, phase_mapping.get(ac_phase_type, 1), 1)

                self.smrcan.SMR_BATTERY_SET_VOLTAGE(50.5)
                self.dcload.DC_LOAD_SET_CURRENT_CC(10, "LOAD")

                time.sleep(10) if hvlv_card_type == "HVLV PP" else time.sleep(0.1)

                if self.part_number.lower() == "he518750":
                    self.prompt.Message("Warning", 'Kindly Turn ON ~120VAC Supply Manually!')

                RESULT.append(self.RETRY_FUNCTION(5, self.REGISTER_SMRS))

                max_smr_count = int(DefaultRead('DEFAULT SETTING')["max smr count"])

                if smr_count - max_smr_count > 0:
                    self.prompt.Message(prompt=f"Turn OFF Last {smr_count - max_smr_count} SMR(s).PRESS ENTER TO PROCEED!")

                if self.mcm_type == 3:
                    color = "GREEN" if self.prompt.User_prompt("KINDLY REMOVE ONE RECTIFIER AND CHECK RECTIFIER ALARM IN OUTPUT PFC, PRESS OK IF COMING?", buzzer=1, response_time=180) else "RED"
                    self.print_console(f"RECTIFIER FAIL ALARM {'OK' if color == 'GREEN' else 'FAIL'}", color)
                    RESULT.append(color == "GREEN")
                    self.prompt.Message(prompt="KINDLY PLUG BACK THE SMR AS WELL", buzzer=0)

                self.MCM_WRITE_COMMAND('SYSTEM CONFIG', 'smr count', str(max_smr_count))
                self.print_console("SMR REGISTRATION TEST FINISHED...")
            else:
                self.print_console("SMR Registration already Done")

            if not self.config_load['battery_sense']:
                self.print_console("BATTERY SENSE TEST NOT APPLICABLE")
            else:
                RESULT.append(self.RETRY_FUNCTION(5, self.BATTERY_SENSE))

            """
            SOLAR SMR TESTING BLOCK
            """
            if self.config_load["solar"]:
                RESULT.append(self.RETRY_FUNCTION(5, self.SOLAR_CHARGER))

            return CALCULATE_RESULT(RESULT)

        except ZeroDivisionError as err:
            print(f"Handled ZeroDivisionError in outer function: {err}")
            self.all_stop = True
            self.print_console("ERROR IN COMMUNICATING WITH MCM", 'RED')
            self.print_console("STOPPING TEST", 'RED')
            return False
        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False

    def SOLAR_CHARGER(self):
        RESULT = [True]
        solar_smr_count = int(self.MCM_READ_COMMAND('SOLAR', 'total s-charger'))
        solar_test_status = int(self.MCM_READ_COMMAND('SOLAR', 'solar present'))
        if not solar_test_status:
            pass
        else:
            global run_status
            self.print_console("TESTING FOR SOLAR SMR(S)")
            self.prompt.Message(prompt="MAKE SURE DC CONNECTIONS ARE NOT LOOSE AND CONNECTED PROPERLY",
                                response_time=300)
            run_status = True
            self.thread2 = threading.Thread(target=self.run_solar)
            self.thread2.start()
            TimerPrompt(self, f"Testing for {solar_smr_count} Solar SMR(s). Turn ON each one by one for registration. Then Press Enter Key!", "200")
            for i in range(1, solar_smr_count + 1):
                color = 'GREEN' if int(self.MCM_READ_COMMAND("SOLAR", f's-charger {i}')) else "RED"
                self.print_console(f'Charger {i} is {"ok" if color == "GREEN" else "FAIL"}', color)
                RESULT.append(color == 'GREEN')

            active_charger = int(self.MCM_READ_COMMAND("SOLAR", "active"))
            color = 'GREEN' if (solar_smr_count == active_charger) else "RED"
            self.print_console(f'Active solar Charger count is {active_charger}: {"ok" if color == "GREEN" else "FAIL"}', color)
            RESULT.append(color == 'GREEN')
            run_status = False
            self.thread2.join()
            time.sleep(2)

        return CALCULATE_RESULT(RESULT)

    def BATTERY_SENSE(self):
        self.print_console('BATTERY SENSE TEST STARTED...')
        self.prompt.Message(prompt="SWITCH <b>OFF</b> BATTERY MCB/REMOVE BATTERY FUSE. PRESS ENTER TO PROCEED!")
        TimerPrompt(self, "WAIT FOR 20 SECONDS...", '20', 'WAIT', False)
        alarm_list = ['', '1', '2', '3']
        return_list = []
        for alarm_index in alarm_list:
            return_list.append(int(self.MCM_READ_COMMAND('ALARM', f"batt{alarm_index} fuse fail")))

        color = "GREEN" if (return_list[0] and (return_list[1] or return_list[2] or return_list[3])) else "RED"
        self.print_console(f"BATTERY FUSE SENSE {'OK' if color == 'GREEN' else 'FAIL'}", color)
        self.print_console("BATTERY SENSE TEST FINISHED...")
        self.prompt.Message(prompt="SWITCH <b>ON</b> BATTERY MCB/ REMOVE BATTERY FUSE. PRESS ENTER TO PROCEED!")
        return color == "GREEN"


    def DC_CURRENT_MEASUREMENT_BATT_CHARGE(self):
        try:
            if not self.config_load["dc_current_charge"]:
                return True

            self.TEST_MODE_M1000()

            self.print_console("DC_CURRENT_MEASUREMENT_BATT_CHARGE TEST STARTED...")
            batt_lvd_count = int(ConfigRead('DUT CONFIGURATION')['no. of battery lvd'])
            load_lvd_count = int(ConfigRead('DUT CONFIGURATION')['no. of load lvd'])
            DC_CURRENT_FACTOR_PERCENTAGE = float(CalibrateSetting('GENERAL FACTORS')['dc current check factor percentage'])
            DC_CURRENT_TOLERANCE_PERCENTAGE = float(CalibrateSetting('GENERAL FACTORS')['dc current check tolerance percentage'])
            DCIF_CARD_TYPE = ConfigRead('DUT CONFIGURATION')['dcif card type']
            ac_phase_type = ConfigRead('DUT CONFIGURATION')['ac phases type']

            CURRENT_SENSOR_VALUE = int(ConfigRead('DUT CONFIGURATION')['channel1 hall effect value']) if DCIF_CARD_TYPE == "HALL EFFECT" else int(ConfigRead('DUT CONFIGURATION')['channel1 shunt value'])
            LOAD_SET_CURRENT = int(CURRENT_SENSOR_VALUE * (float(DC_CURRENT_FACTOR_PERCENTAGE) / 100))
            if self.mcm_type == 3:
                LOAD_SET_CURRENT = 10
            LOAD_CURRENT_OFFSET = int(CURRENT_SENSOR_VALUE * (float(DC_CURRENT_TOLERANCE_PERCENTAGE) / 100))
            self.smrcan.SMR_BATTERY_SET_VOLTAGE(47.5)
            RESULT = []
            self.pfc.pfc_set(0, 'battery_mains', 1)
            SET_INDI_BATTERY_PATH(1)
            self.pfc.pfc_set(0, 'load_mains', 0)
            self.pfc.pfc_set(0, 'bus', 1)

            phase_mapping = {'SINGLE PHASE': 1, 'THREE PHASE': 3}
            ACSET(self.pfc, phase_mapping.get(ac_phase_type, 1), 1)

            self.pfc.pfc_set(0, 'p_load', 1) if load_lvd_count != 0 else self.pfc.pfc_set(0, 'p_load', 0)

            self.dcload.DC_LOAD_SET_CURRENT_CC(LOAD_SET_CURRENT, "BATT")
            while abs(
                    float(self.dcload.DC_LOAD_READ_OUTPUT_CURRENT("BATT").split('\n')[0]) - float(LOAD_SET_CURRENT)) > 0.5:
                print("achieving load")

            for count in range(1, batt_lvd_count + 1):
                self.print_console("CHECKING BATTERY " + str(count) + " CHARGE CURRENT ")
                SET_INDI_BATTERY_PATH(count)
                time.sleep(3)
                if self.customer_name_edit.text() == "BHARTI":
                    self.prompt.Message(prompt="Wait for the Voltage to build to consume load!")
                for count_temp in range(1, batt_lvd_count + 1):
                    # PRINT_CONSOLE(self, "count temp: "+str(count_temp))
                    if count == count_temp or batt_lvd_count < 2:
                        actual_current = float(READ_DC_CURRENT("BATT"))  # READ BATTERY CHARGE CURRENT IN BATTERY PATH LOAD.
                        if actual_current > (LOAD_SET_CURRENT - LOAD_CURRENT_OFFSET):
                            self.print_console("METER CURRENT: " + str(actual_current))
                            retry_count = 0
                            while retry_count < 15:
                                DUT_batt_current = float(self.MCM_READ_COMMAND('DC READ CURRENT', f'batt{count_temp}'))
                                if abs(DUT_batt_current - actual_current) < 1.5:
                                    self.print_console("BATTERY " + str(count) + " CURRENT: " + str(DUT_batt_current), "GREEN")
                                    break
                                time.sleep(1)
                                retry_count += 1
                            else:
                                self.print_console("Retry limit reached; target current not achieved.", "RED")

                            if abs(actual_current - DUT_batt_current) > LOAD_CURRENT_OFFSET:
                                color = "RED"
                            else:
                                color = "GREEN"
                            self.print_console(f"BATTERY {count} CURRENT SENSOR/CABLE IS {'OK' if color=='GREEN' else 'FAULTY'}", color)
                            RESULT.append(color == 'GREEN')

                            RESULT.append(self.RETRY_FUNCTION(5, self.CHARGER_BYPASS))

                        else:
                            actual_voltage = float(READ_DC_VOLTAGE("LOAD"))
                            self.print_console("METER VOLTAGE: " + str(actual_voltage))
                            DUT_batt_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'batt' + str(count_temp)))
                            if abs(actual_voltage - DUT_batt_volt) < 10:
                                self.print_console("Load LVD contactor is faulty", "RED")
                            else:
                                self.print_console("Battery " + str(count_temp) + " LVD contactor is faulty", "RED")

                            RESULT.append(False)
                    elif count != count_temp and batt_lvd_count > 1:
                        RESULT.append(float(self.MCM_READ_COMMAND('DC READ CURRENT', 'batt' + str(count_temp))) < 5)

            self.pfc.pfc_set(0, 'bus', 0)
            self.pfc.pfc_set(0, 'load_mains', 1)
            self.print_console("DC_CURRENT_MEASUREMENT_BATT_CHARGE TEST FINISHED...")

            RESULT.append(self.RETRY_FUNCTION(5, self.DROPPER_DIODE))

            return CALCULATE_RESULT(RESULT)
        except ZeroDivisionError as err:
            print(f"Handled ZeroDivisionError in outer function: {err}")
            self.all_stop = True
            self.print_console("ERROR IN COMMUNICATING WITH MCM", 'RED')
            self.print_console("STOPPING TEST", 'RED')
            return False
        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False


    def DROPPER_DIODE(self):
        if self.config_load["dropper_diode"]:
            self.print_console("Checking Dropper Diode Section")
            self.pfc.pfc_set(0, 'battery_mains', 0)
            self.pfc.pfc_set(0, 'battery_1', 1)

            self.prompt.Message(prompt="Set Extended Mode Enabled and press OK!")

            self.dcload.DC_LOAD_SET_CURRENT_CC(10, "LOAD")

            bus_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'bus'))
            batt_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'batt1'))

            if 53 < bus_volt < 56:
                color = "GREEN"
            else:
                color = "RED"

            self.print_console(f"DROPPER CKT TEST IS {'OK' if color == 'GREEN' else 'FAULTY'}, voltage at Load side is: " + str(bus_volt), color)
            self.print_console(f"DROPPER CKT TEST IS {'OK' if color == 'GREEN' else 'FAULTY'}, voltage at Battery side is: " + str(batt_volt), color)

            return color == 'GREEN'

        return True


    def CHARGER_BYPASS(self):
        if self.config_load["charger_bypass"]:
            self.prompt.Message(prompt='Turn On Charger ByPass Switch!, then Press OK!')

            if float(self.MCM_READ_COMMAND('GENERAL DATA', 'total batt current')) < 1.5:
                self.print_console("Charger BYPASS OK!")
                color = 'GREEN'
            else:
                color = 'RED'
            self.print_console(f"CHARGER BYPASS IS {'OK' if color == 'GREEN' else 'FAULTY'}", color)
            RESULT.append(color == 'GREEN')
            self.prompt.Message(prompt='Turn OFF Charger ByPASS Switch!')
            return color == 'GREEN'

        return True

    def CALIBRATE_DC_CURRENT(self):
        try:
            if self.config_load["dc_current_calibration"]:
                pass
            else:
                return True
            global RESULT_TEMP
            if self.mcm_type == 1:
                self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'ate test', "TEST_M1000_ATE")
            test_sub_id = 0
            self.pfc.pfc_set(0, 'battery_mains', 1)
            self.print_console("CALIBRATE_DC_CURRENT TEST STARTED...")
            batt_fuse_count = int(DefaultRead('DEFAULT SETTING')[
                                      "battery ah"])  # int(ConfigRead('DUT CONFIGURATION')['no. of battery fuses'])
            batt_lvd_count = int(ConfigRead('DUT CONFIGURATION')['no. of battery lvd'])
            load_lvd_count = int(ConfigRead('DUT CONFIGURATION')['no. of load lvd'])
            load_current_count = int(ConfigRead('DUT CONFIGURATION')['no. of load current'])
            load_current_sensor_state = ConfigRead('DUT CONFIGURATION')['load current sensor']
            battery_capacity = int(ConfigRead('DUT CONFIGURATION')['battery capacity'])
            battery_type = ConfigRead('DUT CONFIGURATION')['battery type']
            DCIF_CARD_TYPE = ConfigRead('DUT CONFIGURATION')['dcif card type']
            ac_phase_type = ConfigRead('DUT CONFIGURATION')['ac phases type']
            if battery_type == 'VRLA':
                battery_capacity = int(ConfigRead('DUT CONFIGURATION')['battery capacity'])
                self.MCM_WRITE_COMMAND('SYSTEM CONFIG', 'vrla battery capacity', 5000)
            elif battery_type == 'LION':
                module_count = ConfigRead('DUT CONFIGURATION')['lion module count']
                self.MCM_WRITE_COMMAND('SYSTEM CONFIG', 'lion module count', 10)
            self.smrcan.SMR_BATTERY_SET_VOLTAGE(48.0)
            self.MCM_WRITE_COMMAND('SYSTEM CONFIG', 'eco mode', 0)
            if DCIF_CARD_TYPE == 'HALL EFFECT':
                for channel_number in range(1, load_current_count + batt_lvd_count + 1):
                    if (self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' gain') != '0') \
                            or (self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(
                        channel_number) + ' offset') != '0'):  # or (TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' deadband'])!='0'):
                        self.print_console("Resetting offset and gain again")
                        # TELNET_SET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' deadband'],0)
                        # time.sleep(1)
                        self.MCM_WRITE_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' gain', 0)
                        # time.sleep(1)
                        self.MCM_WRITE_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' offset', 0)
                        # time.sleep(1)
                        self.print_console("CURRENT CHANNEL " + str(channel_number) + " GAIN: " + str(
                            self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' gain')))
                        self.print_console("CURRENT CHANNEL " + str(channel_number) + " OFFSET: " + str(
                            self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' offset')))
                        # PRINT_CONSOLE(self,"CURRENT CHANNEL "+str(channel_number)+" DEADBAND: "+str(TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' deadband'])))

            # raw_input("ALL BATTERY FUSES SHOULD BE INSERTED/SWITCH ON LOAD/BATTERY MCB. Press any key to continue")
            RESULT = []
            RESULT_1 = []
            RESULT_2 = []
            self.pfc.pfc_set(0, 'battery_mains', 1)
            for batt in range(1, batt_fuse_count + 1):
                self.pfc.pfc_set(0, 'battery_' + str(batt), 1)
            self.pfc.pfc_set(0, 'load_mains', 1)
            for load in range(1, load_current_count + 1):
                self.pfc.pfc_set(0, 'n_p_load_' + str(load), 1)
            SET_INDI_BATTERY_PATH(1)
            if ac_phase_type == 'SINGLE PHASE':
                self.pfc.pfc_set(0, 'r_phase', 1)
            elif ac_phase_type == 'THREE PHASE':
                self.pfc.pfc_set(0, 'r_phase', 1)
                self.pfc.pfc_set(0, 'y_phase', 1)
                self.pfc.pfc_set(0, 'b_phase', 1)
            if load_lvd_count == 1:
                self.pfc.pfc_set(0, 'p_load', 1)
            else:
                self.pfc.pfc_set(0, 'p_load', 0)
            # SET_JIG_PFC_OP(self.can,'AC',0)
            self.dcload.DC_LOAD_SET_CURRENT_CC(10, "LOAD")
            ATE_LOAD_COUNT = int(SettingRead("SETTING")['ate load count'])
            if ATE_LOAD_COUNT != 1:  # SINGLE LOAD IS CONFIGURED, 19/08/2016
                self.dcload.DC_LOAD_SET_CURRENT_CC(10, "BATT")
            # time.sleep(2)

            ### ADDING LOGIC FOR SINGLE LOAD CONFIGURATION

            for count in range(load_current_count + 1, load_current_count + batt_lvd_count + 1):
                # self.print_console("calibrate dc current" + str(load_current_count + 1)+ " " +str(load_current_count + batt_lvd_count + 1))
                self.print_console("count: " + str(count))
                SET_INDI_BATTERY_PATH(count - load_current_count)
                time.sleep(1)
                self.print_console("Start battery calibration")
                if DCIF_CARD_TYPE == 'HALL EFFECT':
                    RESULT_TEMP = CALIBRATE_CURRENT_PATH_HALL_EFFECT(self, count, 'BATT')
                elif DCIF_CARD_TYPE == 'SHUNT':
                    RESULT_TEMP = CALIBRATE_CURRENT_PATH_SHUNT(self, count, 'BATT')
                elif DCIF_CARD_TYPE == 'SHUNT SMALL':
                    if load_current_sensor_state == 'DISABLE' and self.MCM_READ_COMMAND("BATTERY CURRENT CHANNEL MAP",
                                                                                        'channel 1 map') == '1':
                        count = count - 1
                    self.print_console("count: " + str(count))
                    RESULT_TEMP = CALIBRATE_CURRENT_PATH_SHUNT_SMALL(self, count, 'BATT')

                RESULT_1.append(RESULT_TEMP)
                if self.mcm_type == 3:
                    break

            RESULT.append(CALCULATE_RESULT(RESULT_1))

            if ATE_LOAD_COUNT == 1:
                self.print_console("RESETTING FOR LOAD PATH")
                self.pfc.pfc_set(0, 'bus', 0)
                self.pfc.pfc_set(0, 'load_mains', 1)

            if load_current_sensor_state == 'DISABLE':
                self.print_console("CALIBRATION NOT REQUIRED")
            else:
                for i in range(1, load_current_count + 1):
                    SET_INDI_LOAD_PATH(self, i)
                    time.sleep(2)
                    if DCIF_CARD_TYPE == 'HALL EFFECT':
                        RESULT_TEMP = CALIBRATE_CURRENT_PATH_HALL_EFFECT(self, i, 'LOAD')
                    elif DCIF_CARD_TYPE == 'SHUNT':
                        RESULT_TEMP = CALIBRATE_CURRENT_PATH_SHUNT(self, i, 'LOAD')
                    elif DCIF_CARD_TYPE == 'SHUNT SMALL':
                        RESULT_TEMP = CALIBRATE_CURRENT_PATH_SHUNT_SMALL(self, i, 'LOAD')
                    RESULT_2.append(RESULT_TEMP)
            RESULT.append(CALCULATE_RESULT(RESULT_2))
            self.print_console("CALIBRATE_DC_CURRENT TEST FINISHED...")
            if load_lvd_count == 1:
                self.pfc.pfc_set(0, 'p_load', 1)
            else:
                self.pfc.pfc_set(0, 'p_load', 0)
            return CALCULATE_RESULT(RESULT)
        except ZeroDivisionError as err:
            print(f"Handled ZeroDivisionError in outer function: {err}")
            self.all_stop = True
            self.print_console("ERROR IN COMMUNICATING WITH MCM", 'RED')
            self.print_console("STOPPING TEST", 'RED')
            return False
        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False

    def LVD_CONTACTOR_CHECK(self):
        try:
            if self.config_load["lvd_contactor"]:
                pass
            else:
                return True
            if self.mcm_type == 1:
                self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'ate test', "TEST_M1000_ATE")
            test_sub_id = 0
            RESULT_1 = []
            RESULT_2 = []
            self.print_console("LVD_CONTACTOR_CHECK TEST STARTED...")
            batt_fuse_count = int(DefaultRead('DEFAULT SETTING')[
                                      "battery ah"])  # int(ConfigRead('DUT CONFIGURATION')['no. of battery fuses'])
            batt_lvd_count = int(ConfigRead('DUT CONFIGURATION')['no. of battery lvd'])
            load_lvd_count = int(ConfigRead('DUT CONFIGURATION')['no. of load lvd'])
            load_current_count = int(ConfigRead('DUT CONFIGURATION')['no. of load current'])
            self.smrcan.SMR_BATTERY_SET_VOLTAGE(53.5)
            # raw_input("ALL BATTERY FUSES SHOULD BE INSERTED/SWITCH ON LOAD/BATTERY MCB. Press any key to continue")
            RESULT = []
            self.dcload.DC_LOAD_SET_CURRENT_CC(5, "BATT")
            self.pfc.pfc_set(0, 'battery_mains', 1)
            SET_INDI_BATTERY_PATH(1)
            print("function start time ", time.time())
            self.pfc.pfc_set(0, 'load_mains', 1)
            self.pfc.pfc_set(0, 'n_p_load_1', 1)
            self.pfc.pfc_set(0, 'n_p_load_2', 1)
            self.pfc.pfc_set(0, 'n_p_load_3', 1)
            self.pfc.pfc_set(0, 'n_p_load_4', 1)
            self.pfc.pfc_set(0, 'p_load', 0)
            self.pfc.pfc_set(0, 'r_phase', 0)
            self.pfc.pfc_set(0, 'y_phase', 0)
            self.pfc.pfc_set(0, 'b_phase', 0)
            print("function end time ", time.time())
            if self.part_number.lower() == "he518750":
                self.prompt.Message(title="Warning", prompt='Kindly Turn OFF ~120VAC Supply Manually!', buzzer=0, response_time=300)
            self.dcload.DC_LOAD_SET_CURRENT_CC(30, "LOAD")
            # time.sleep(3)
            # SET_BATTERY_ISOLATE(self,batt_lvd_count,1)
            ## current path will be checked in discharging state

            """LOAD LVD SECTION"""
            if load_lvd_count == load_current_count and load_lvd_count != 0:
                for count_temp in range(1, load_lvd_count + 1):
                    self.print_console("count temp: " + str(count_temp))
                    SET_INDI_LOAD_PATH(self, count_temp)
                    time.sleep(2)
                    actual_current = float(READ_DC_CURRENT("LOAD"))
                    DUT_load_current = float(self.MCM_READ_COMMAND('DC READ CURRENT', 'load' + str(count_temp)))
                    retry_count = 0
                    while DUT_load_current < 25 and retry_count < 500:
                        DUT_load_current = float(self.MCM_READ_COMMAND('DC READ CURRENT', 'load' + str(count_temp)))
                        print("current z:" + str(DUT_load_current))
                        retry_count += 1
                    if abs(actual_current - DUT_load_current) < 5.0:
                        temp_var = True
                    else:
                        temp_var = False
                    if actual_current > 25 and temp_var:
                        self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'ate test', "TEST_M1000_ATE")
                        self.smrcan.SMR_BATTERY_SET_VOLTAGE(45)
                        SET_INDI_LOAD_PATH_ISO(self, count_temp)
                        time.sleep(3)
                        DUT_load_current = float(self.MCM_READ_COMMAND('DC READ CURRENT', 'load' + str(count_temp)))
                        if -20 < DUT_load_current < 20:
                            RESULT_TEMP = True
                            self.print_console("Load " + str(count_temp) + " LVD contactor is OK")
                        else:
                            RESULT_TEMP = False
                            self.print_console("Load " + str(count_temp) + " LVD contactor is faulty", "RED")
                    else:
                        actual_voltage = float(READ_DC_VOLTAGE(self, "LOAD"))
                        self.print_console("actual voltage: " + str(actual_voltage))
                        DUT_batt_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'batt1'))
                        if abs(actual_voltage - DUT_batt_volt) < 5:
                            self.print_console("Load " + str(count_temp) + " LVD contactor is faulty", "RED")
                        else:
                            self.print_console("Battery 1 LVD contactor is faulty", "RED")
                        RESULT_TEMP = False
                    self.smrcan.SMR_BATTERY_SET_VOLTAGE(53.5)
                    SET_INDI_LOAD_ISOLATE(self, count_temp, 0)
                    time.sleep(3)
                    RESULT_2.append(RESULT_TEMP)
            elif load_lvd_count < 2 and 1 < load_current_count:
                for count_temp in range(1, load_lvd_count + 1):
                    self.print_console("count temp: " + str(count_temp))
                    actual_current = float(READ_DC_CURRENT("BATT"))
                    load_current_sum = 0
                    for load_current in range(1, load_current_count + 1):
                        DUT_load_current = float(self.MCM_READ_COMMAND('DC READ CURRENT', 'load' + str(count_temp)))
                        load_current_sum += DUT_load_current
                    if abs(actual_current - load_current_sum) < 2:
                        temp_var = True
                    else:
                        temp_var = False
                    if actual_current > 25 and temp_var == True:
                        SET_INDI_LOAD_ISOLATE(count_temp, 1)
                        time.sleep(5)
                        load_current_sum = 0
                        for load_current in range(1, load_current_count + 1):
                            DUT_load_current = float(self.MCM_READ_COMMAND('DC READ CURRENT', 'load' + str(count_temp)))
                            load_current_sum += DUT_load_current
                        if -2 < load_current_sum < 2:
                            RESULT_TEMP = True
                        else:
                            RESULT_TEMP = False
                            self.print_console("Load " + str(count_temp) + " LVD contactor is faulty", "RED")
                    else:
                        actual_voltage = float(READ_DC_VOLTAGE("LOAD"))
                        self.print_console("actual voltage: " + str(actual_voltage))
                        DUT_batt_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'batt1'))
                        if abs(actual_voltage - DUT_batt_volt) < 5:
                            self.print_console("Load " + str(count_temp) + " LVD contactor is faulty", "RED")
                        else:
                            self.print_console("Battery 1 LVD contactor is faulty", "RED")
                        RESULT_TEMP = False
                        RESULT_2.append(RESULT_TEMP)
                    SET_INDI_LOAD_ISOLATE(count_temp, 0)

            if self.mcm_type == 3:
                load_lvd_count = 0
                load_current_count = 0
                self.pfc.pfc_set(0, 'pfc 2', 0)
                self.pfc.pfc_set(0, "battery_mains", 1)
                self.pfc.pfc_set(0, "battery_1", 1)
                time.sleep(6)
                self.M1KLC.Login()
                time.sleep(1)

            if self.part_number.lower() == "he518750":
                self.prompt.Message(prompt="Turn ON ~120V AC Supply to restore LOAD LVD and Battery LVD", buzzer=0, response_time=300)
                self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'factory restore', 1)
                self.prompt.Message(prompt="Kindly wait, Once rebooted PRESS OK!, and Turn OFF 120VAC Supply", buzzer=0, response_time=300)
                self.M2000.LOGIN_MCM()[0]
                time.sleep(1)

            """BATTERY LVD SECTION"""
            self.dcload.DC_LOAD_SET_CURRENT_CC(30, "LOAD")
            self.pfc.pfc_set(0, 'load_mains', 1)
            self.pfc.pfc_set(0, 'n_p_load_1', 1)

            for count_temp in range(1, batt_lvd_count + 1):
                self.print_console("count temp: " + str(count_temp))
                voltage = float(self.MCM_READ_COMMAND('BATTERY SETTING', "battery lvd set"))
                SET_INDI_BATTERY_PATH(count_temp)
                TimerPrompt(self, "Setting up battery path", "3")
                actual_current = float(READ_DC_CURRENT("LOAD"))
                DUT_batt_current = float(self.MCM_READ_COMMAND('DC READ CURRENT', 'batt' + str(count_temp)))
                actual_current = -1 * actual_current
                if actual_current < -20 and abs(
                        actual_current - DUT_batt_current) < 7.0:  # check if current is flowing through load and battery
                    self.smrcan.SMR_BATTERY_SET_VOLTAGE(voltage - 2)
                    SET_INDI_BATTERY_ISOLATE(self, count_temp, 1)  # if yes, check for battery lvd contactor
                    TimerPrompt(self, "Press OK when battery is isolated", "30")
                    DUT_batt_current = float(self.MCM_READ_COMMAND('DC READ CURRENT', 'batt' + str(count_temp)))
                    print("dut current =", DUT_batt_current)
                    if -20 < DUT_batt_current < 20:
                        RESULT_TEMP = True
                        self.print_console("Battery " + str(count_temp) + " LVD contactor is OK")
                        if self.config_load["battery_lvd"]:
                            dut_bus_voltage = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'bus'))
                            retry_count = 0
                            while dut_bus_voltage > 0 and retry_count < 50:
                                dut_bus_voltage = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'bus'))
                                retry_count += 1
                            self.prompt.Message(prompt="Switch ON Batt LVD BYPASS")
                            load_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'bus'))
                            retry_count = 0
                            while retry_count < 50 and ((voltage - 2) < load_volt < (voltage)):
                                self.print_console("Battery By pass switch is OK")
                                self.prompt.Message(prompt="Kindly Switch off the Battery By Pass Switch!", buzzer=0)
                                # retry_count += 1
                                self.smrcan.SMR_BATTERY_SET_VOLTAGE(53.5)
                                load_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'bus'))
                    else:
                        RESULT_TEMP = False
                        self.print_console("Battery " + str(count_temp) + " LVD contactor is faulty", "RED")
                else:
                    actual_voltage = float(READ_DC_VOLTAGE(self, "LOAD"))
                    # self.print_console("actual voltage: " + str(actual_voltage))
                    DUT_batt_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'batt' + str(count_temp)))

                    if abs(actual_voltage - DUT_batt_volt) < 5:
                        DUT_bus_volt = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'bus'))
                        if abs(actual_voltage - DUT_bus_volt) < 2:
                            self.print_console("Battery " + str(count_temp) + " CURRENT SENSOR is faulty", "RED")
                        else:
                            self.print_console("Load LVD contactor is faulty", "RED")
                    else:
                        self.print_console("Battery " + str(count_temp) + " LVD contactor is faulty", "RED")
                    RESULT_TEMP = False
                self.smrcan.SMR_BATTERY_SET_VOLTAGE(53.5)
                SET_INDI_BATTERY_ISOLATE(self, count_temp, 0)
                time.sleep(2)
                RESULT_1.append(RESULT_TEMP)
            RESULT.append(CALCULATE_RESULT(RESULT_1))

            self.smrcan.SMR_BATTERY_SET_VOLTAGE(53.5)

            RESULT.append(CALCULATE_RESULT(RESULT_2))
            self.print_console("LVD_CONTACTOR_CHECK TEST FINISHED...")

            for i in range(1, load_lvd_count + 1):
                self.pfc.pfc_set(0, 'LOAD' + str(i), 1)

            return CALCULATE_RESULT(RESULT)
        except ZeroDivisionError as err:
            print(f"Handled ZeroDivisionError in outer function: {err}")
            self.all_stop = True
            self.print_console("ERROR IN COMMUNICATING WITH MCM", 'RED')
            self.print_console("STOPPING TEST", 'RED')
            return False
        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False

    def PHASE_ALLOCATION(self):
        try:
            if self.config_load['ac_phase']:
                pass
            else:
                return True
            global phase, temp_result, temp_value
            if self.mcm_type == 1:
                self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'ate test', "TEST_M1000_ATE")

            ac_phase_type = ConfigRead('DUT CONFIGURATION')['ac phases type']
            if ac_phase_type == "SINGLE PHASE":
                return True  # Bypasses the current sharing

            test_sub_id = 0
            self.dcload.DC_LOAD_SET_CURRENT_CC(5, "BATT")
            self.print_console("PHASE_ALLOCATION TEST STARTED...")
            batt_fuse_count = int(DefaultRead('DEFAULT SETTING')[
                                      "battery ah"])
            batt_lvd_count = int(ConfigRead('DUT CONFIGURATION')['no. of battery lvd'])
            load_lvd_count = int(ConfigRead('DUT CONFIGURATION')['no. of load lvd'])
            load_current_count = int(ConfigRead('DUT CONFIGURATION')['no. of load current'])
            ac_phase_type = ConfigRead('DUT CONFIGURATION')['ac phases type']
            hvlv_card_state = ConfigRead('DUT CONFIGURATION')['hvlv card']
            hvlv_card_type = ConfigRead('DUT CONFIGURATION')['ac ip voltage source']
            self.smrcan.SMR_BATTERY_SET_VOLTAGE(50.5)
            self.dcload.DC_LOAD_SET_CURRENT_CC(10, "LOAD")
            self.dcload.DC_LOAD_SET_CURRENT_CC(15, "BATT")
            phase_voltage = 0

            self.pfc.pfc_set(0, 'battery_mains', 1)
            for batt in range(1, batt_fuse_count + 1):
                self.pfc.pfc_set(0, 'battery_' + str(batt), 1)
            self.pfc.pfc_set(0, 'load_mains', 1)
            for load in range(1, load_current_count + 1):
                self.pfc.pfc_set(0, 'n_p_load_' + str(load), 1)
            RESULT = []

            if ac_phase_type == 'SINGLE PHASE':
                self.pfc.pfc_set(0, 'r_phase', 1)
                self.pfc.pfc_set(0, 'y_phase', 0)
                self.pfc.pfc_set(0, 'b_phase', 0)
                # AC_SOURCE_SET_VOLTAGE(self, 230, ac_phase_type)
            elif ac_phase_type == 'THREE PHASE':
                self.pfc.pfc_set(0, 'r_phase', 1)
                self.pfc.pfc_set(0, 'y_phase', 1)
                self.pfc.pfc_set(0, 'b_phase', 1)

            if hvlv_card_state == 'PRESENT':
                time.sleep(3)
                phase_voltage = 75
                alarm_hvlv_comm_fail = int(self.MCM_READ_COMMAND('ALARM', 'hvlv comm fail'))
                if alarm_hvlv_comm_fail == 0:
                    RESULT_TEMP = True
                else:
                    RESULT_TEMP = False
                    self.print_console("HVLV Card not communicating with Controller", "RED")
            else:
                phase_voltage = 0
                RESULT_TEMP = True
            RESULT.append(RESULT_TEMP)

            if hvlv_card_type == 'HVLV PP':
                time.sleep(5)
                if self.custom_check.isChecked():
                    # MESSAGE_PROMPT(self,"Custom settings will be programmed to controller")
                    if DefaultRead('DEFAULT SETTING STATE')["comm smr count"] == 'YES':
                        smr_count = int(DefaultRead('DEFAULT SETTING')["comm smr count"])
                        self.MCM_WRITE_COMMAND('SYSTEM CONFIG', 'smr count', str(smr_count))
                    else:
                        smr_count = int(ConfigRead('DUT CONFIGURATION')['smr count'])

                # smr_count=SMR_COUNT(self)
                else:
                    smr_count = int(ConfigRead('DUT CONFIGURATION')['smr count'])

                max_smr_count = int(DefaultRead('DEFAULT SETTING')["max smr count"])
                remain_smr_count = smr_count - max_smr_count

                if remain_smr_count > 0:
                    self.prompt.Message(prompt="Turn ON Last " + str(remain_smr_count) + " SMR(s).PRESS ENTER TO PROCEED!")

                config_smr_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'smr count'))

                for i in range(1, config_smr_count + 1):
                    smr_status = int(self.MCM_READ_COMMAND('SMR COMMANDS', 'smr' + str(i) + " status"))
                    print("status of smr is :", smr_status)
                    # self.print_console(SMR_STATUS_TEXT(smr_status))
                    if smr_status == 1:
                        RESULT_TEMP = True
                        self.print_console("SMR " + str(i) + " WIRING OK ")
                    else:
                        RESULT_TEMP = False
                        if hvlv_card_state == 'PRESENT':
                            self.print_console("SMR " + str(i) + " HVLV RELAY / WIRING FAULTY ", "RED")
                        elif hvlv_card_state != 'PRESENT':
                            self.print_console("SMR " + str(i) + " WIRING FAULTY ", 'RED')
                    RESULT.append(RESULT_TEMP)

                max_smr_count = int(DefaultRead('DEFAULT SETTING')["max smr count"])
                remain_smr_count = smr_count - max_smr_count

                if remain_smr_count > 0:
                    self.prompt.Message(prompt="Turn OFF Last " + str(remain_smr_count) + " SMR(s).PRESS ENTER TO PROCEED!")

                self.MCM_WRITE_COMMAND('SYSTEM CONFIG', 'smr count', max_smr_count)

                self.print_console(str(RESULT))
                self.print_console("PHASE_ALLOCATION TEST FINISHED...")
                return CALCULATE_RESULT(RESULT)

            if ac_phase_type == "THREE PHASE" and self.customer_name_edit.text().upper() == "BHARTI":
                RESULT.append(self.AC_PHASE_ALLOCATION_IPMS())

            if ac_phase_type == 'THREE PHASE' and self.customer_name_edit.text() != "BHARTI":
                for phase_no in range(1, 4):
                    # AC_SOURCE_SET_VOLTAGE(self, 230, ac_phase_type)
                    if phase_no == 1:
                        phase = 'R PHASE'
                        self.pfc.pfc_set(0, 'r_phase', 1)
                        self.pfc.pfc_set(0, 'y_phase', 0)
                        self.pfc.pfc_set(0, 'b_phase', 0)
                    elif phase_no == 2:
                        self.pfc.pfc_set(0, 'r_phase', 0)
                        self.pfc.pfc_set(0, 'y_phase', 1)
                        self.pfc.pfc_set(0, 'b_phase', 0)
                        phase = 'Y PHASE'
                    elif phase_no == 3:
                        self.pfc.pfc_set(0, 'r_phase', 0)
                        self.pfc.pfc_set(0, 'y_phase', 0)
                        self.pfc.pfc_set(0, 'b_phase', 1)
                        phase = 'B PHASE'

                    # self.print_console("Setting IP voltage to " + str(phase_voltage))
                    # AC_SOURCE_SET_VOLTAGE(self, phase_voltage, phase)
                    time.sleep(20)
                    """# alarm_phase_fail = int(self.MCM_READ_COMMAND('ALARM', phase.lower() + ' fail'))
                    # if alarm_phase_fail == 1:
                    #     RESULT_TEMP = True
                    # else:
                    #     RESULT_TEMP = False
                    #     if hvlv_card_state == 'PRESENT':
                    #         self.print_console("CHECK HVLV IP VOLTAGE SENSE WIRING", "RED")
                    # RESULT.append(RESULT_TEMP)
                    # self.print_console(str(RESULT))
                    # voltage_phase = int(self.MCM_READ_COMMAND('MAINS READ VOLTAGE', phase.lower()))
                    # if phase_voltage + 3 > voltage_phase > phase_voltage - 3:
                    #     RESULT_TEMP = True
                    # else:
                    #     RESULT_TEMP = False
                    #     if hvlv_card_state == 'PRESENT':
                    #         self.print_console("CHECK HVLV " + str(phase) + " IP VOLTAGE SENSE WIRING", "RED")
                    # 
                    # RESULT.append(RESULT_TEMP)
                    # self.print_console(str(RESULT))"""
                    config_smr_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'smr count'))
                    for i in range(phase_no, config_smr_count + 1, 3):
                        smr_status = int(
                            self.MCM_READ_COMMAND('SMR COMMANDS', 'smr' + str(i) + " status"))
                        # self.print_console(SMR_STATUS_TEXT(smr_status))
                        if smr_status == 1:
                            RESULT_TEMP = True
                            self.print_console("SMR " + str(i) + " WIRING OK ")
                        else:
                            RESULT_TEMP = False
                            if hvlv_card_state == 'PRESENT':
                                self.print_console("SMR " + str(i) + " HVLV RELAY / WIRING FAULTY ", "RED")
                            elif hvlv_card_state != 'PRESENT':
                                self.print_console("SMR " + str(i) + " WIRING FAULTY ", "RED")
                        RESULT.append(RESULT_TEMP)

                if self.config_load['phase_switchers']:
                    self.pfc.pfc_set(0, 'r_phase', 1)
                    self.pfc.pfc_set(0, 'y_phase', 1)
                    self.pfc.pfc_set(0, 'b_phase', 1)
                    self.prompt.Message(prompt="Switch All Phase Selector to R Phase Only. Then Press OK!")
                    self.pfc.pfc_set(0, 'b_phase', 0)
                    self.pfc.pfc_set(0, 'y_phase', 0)
                    self.pfc.pfc_set(0, 'r_phase', 1)
                    self.print_console("Testing R Phase only")
                    # time.sleep(20)
                    config_smr_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'smr count'))
                    for i in range(1, config_smr_count + 1):
                        smr_status = int(
                            self.MCM_READ_COMMAND('SMR COMMANDS', 'smr' + str(i) + " status"))
                        self.print_console(SMR_STATUS_TEXT(smr_status))
                        if smr_status == 1:
                            RESULT_TEMP = True
                            self.print_console("SMR " + str(i) + " WIRING OK ")
                        else:
                            RESULT_TEMP = False
                            if hvlv_card_state == 'PRESENT':
                                self.print_console("SMR " + str(i) + " HVLV RELAY / WIRING FAULTY ", "RED")
                            elif hvlv_card_state != 'PRESENT':
                                self.print_console("SMR " + str(i) + " WIRING FAULTY ", "RED")
                        RESULT.append(RESULT_TEMP)

                    self.pfc.pfc_set(0, 'r_phase', 1)
                    self.pfc.pfc_set(0, 'b_phase', 1)
                    self.pfc.pfc_set(0, 'y_phase', 1)
                    self.prompt.Message(prompt="Switch All Phase Selector to Y Phase Only. Then Press OK!")
                    self.pfc.pfc_set(0, 'r_phase', 0)
                    self.pfc.pfc_set(0, 'b_phase', 0)
                    self.pfc.pfc_set(0, 'y_phase', 1)
                    self.print_console("Testing Y Phase only")
                    time.sleep(10)
                    config_smr_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'smr count'))
                    for i in range(1, config_smr_count + 1):
                        smr_status = int(
                            self.MCM_READ_COMMAND('SMR COMMANDS', 'smr' + str(i) + " status"))
                        self.print_console(SMR_STATUS_TEXT(smr_status))
                        if smr_status == 1:
                            RESULT_TEMP = True
                            self.print_console("SMR " + str(i) + " WIRING OK ")
                        else:
                            RESULT_TEMP = False
                            if hvlv_card_state == 'PRESENT':
                                self.print_console("SMR " + str(i) + " HVLV RELAY / WIRING FAULTY ", "RED")
                            elif hvlv_card_state != 'PRESENT':
                                self.print_console("SMR " + str(i) + " WIRING FAULTY ", "RED")
                        RESULT.append(RESULT_TEMP)

                    self.pfc.pfc_set(0, 'r_phase', 1)
                    self.pfc.pfc_set(0, 'b_phase', 1)
                    self.pfc.pfc_set(0, 'y_phase', 1)
                    self.prompt.Message(prompt="Switch All Phase Selector to B Phase Only. Then Press OK!")
                    self.pfc.pfc_set(0, 'r_phase', 0)
                    self.pfc.pfc_set(0, 'b_phase', 1)
                    self.pfc.pfc_set(0, 'y_phase', 0)
                    time.sleep(10)
                    self.print_console("Testing B Phase only")
                    config_smr_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'smr count'))
                    for i in range(1, config_smr_count + 1):
                        smr_status = int(
                            self.MCM_READ_COMMAND('SMR COMMANDS', 'smr' + str(i) + " status"))
                        self.print_console(SMR_STATUS_TEXT(smr_status))
                        if smr_status == 1:
                            RESULT_TEMP = True
                            self.print_console("SMR " + str(i) + " WIRING OK ")
                        else:
                            RESULT_TEMP = False
                            if hvlv_card_state == 'PRESENT':
                                self.print_console("SMR " + str(i) + " HVLV RELAY / WIRING FAULTY ", "RED")
                            elif hvlv_card_state != 'PRESENT':
                                self.print_console("SMR " + str(i) + " WIRING FAULTY ", "RED")
                        RESULT.append(RESULT_TEMP)

                    self.pfc.pfc_set(0, 'r_phase', 1)
                    self.pfc.pfc_set(0, 'y_phase', 1)
                    self.pfc.pfc_set(0, 'b_phase', 1)
                    time.sleep(5)

            # self.print_console(str(RESULT))
            self.print_console("PHASE_ALLOCATION TEST FINISHED...")
            return CALCULATE_RESULT(RESULT)
        except ZeroDivisionError as err:
            print(f"Handled ZeroDivisionError in outer function: {err}")
            self.all_stop = True
            self.print_console("ERROR IN COMMUNICATING WITH MCM", 'RED')
            self.print_console("STOPPING TEST", 'RED')
            return False
        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False

    def AC_PHASE_ALLOCATION_IPMS(self):
        global temp_result
        r = self.prompt.user_value_2("Enter R Phase Voltage via DMM", "V")
        y = self.prompt.user_value_2("Enter Y Phase Voltage via DMM", "V")
        b = self.prompt.user_value_2("Enter B Phase Voltage via DMM", "V")
        input_phase = [r, y, b]

        self.print_console(f"DMM Value of R Phase is: {r}")
        self.print_console(f"DMM Value of Y Phase is: {y}")
        self.print_console(f"DMM Value of B Phase is: {b}")
        phase_sequence = {
            'R': ['r_phase'],
            'Y': ['y_phase'],
            'B': ['b_phase'],
            'R and Y': ['r_phase', 'y_phase'],
            'Y and B': ['y_phase', 'b_phase'],
            'R and B': ['r_phase', 'b_phase'],
            'RYB': ['r_phase', 'y_phase', 'b_phase'],
        }
        contact_sequence = {
            'R': 'K1/K4/K5',
            'Y': 'K2/K4/K5',
            'B': 'K3/K4/K5',
            'R and Y': 'K1/K2/K5',
            'Y and B': 'K2/K3/K4',
            'R and B': 'K1/K3/K5',
            'RYB': 'K1/K2/K3',
        }

        def ac_phase_on_sequence(phase_list):
            all_phases = ['r_phase', 'y_phase', 'b_phase']
            for i in all_phases:
                if i in phase_list:
                    self.pfc.pfc_set(0, i, 1)
                else:
                    self.pfc.pfc_set(0, i, 0)

        time_value = '60'
        for i in phase_sequence.keys():
            block_status = False
            count = 0
            while not block_status and count < 4:
                temp_result = [True]
                ac_phase_on_sequence(phase_sequence[i])
                self.print_console(f"Switched to {i} phase")
                self.print_console(f'Contactor {contact_sequence[i]} is ON')
                self.print_console(f'Waiting for {time_value} seconds for SMR to get Active on {i} phase!')
                self.dcload.DC_LOAD_SET_CURRENT_CC(40.0)
                TimerPrompt(self, f"Wait for {time_value} Seconds for SMRs to get Active on {i} phase", time_value, button_status=False)
                eb_cont_on = self.MCM_READ_COMMAND("ALARM", 'eb contactor on')
                if eb_cont_on:
                    self.print_console("EB Cont ON", "GREEN")
                else:
                    self.print_console("EB CONT FAIL", "RED")
                phases = ['R', 'Y', 'B']
                for j in phases:
                    if j in i:
                        current_value = self.MCM_READ_COMMAND('MAINS READ CURRENT', f'{str(j).lower()} phase')
                        if 0.0 < float(current_value):
                            temp_result.append(True)
                            self.print_console(f'Current Value at {j} Phase is: {current_value}', "GREEN")
                        else:
                            temp_result.append(False)
                            self.print_console('Current Connection is not OK', 'RED')

                        voltage_value = self.MCM_READ_COMMAND('MAINS READ VOLTAGE', f'{str(j).lower()} phase')
                        if abs(float(voltage_value) - float(r)) < 10:
                            temp_result.append(True)
                            self.print_console(f'voltage Value at {j} Phase is: {voltage_value}', "GREEN")
                        else:
                            temp_result.append(False)
                            self.print_console('voltage Connection is not OK', 'RED')

                    else:
                        current_value = self.MCM_READ_COMMAND('MAINS READ CURRENT', f'{str(j).lower()} phase')
                        self.print_console(f'Current Value at {j} Phase is: {current_value}')
                        voltage_value = self.MCM_READ_COMMAND('MAINS READ VOLTAGE', f'{str(j).lower()} phase')
                        self.print_console(f'voltage Value at {j} Phase is: {voltage_value}')

                config_smr_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'smr count'))
                time.sleep(2)
                if int(self.MCM_READ_COMMAND(section="TAB.1441.0", pool=1)) == config_smr_count:
                    self.print_console("ALL Connection OK")
                else:
                    for smr_count in range(1, config_smr_count + 1):
                        smr_status = int(self.MCM_READ_COMMAND('SMR COMMANDS', 'smr' + str(smr_count) + " status"))
                        print("status of smr is :", smr_status)
                        if smr_status == 1:
                            RESULT_TEMP = True
                            self.print_console("SMR " + str(smr_count) + " WIRING OK ")
                        else:
                            RESULT_TEMP = False
                            if hvlv_card_state == 'PRESENT':
                                self.print_console("SMR " + str(smr_count) + " HVLV RELAY / WIRING FAULTY ", "RED")
                            elif hvlv_card_state != 'PRESENT':
                                self.print_console("SMR " + str(smr_count) + " WIRING FAULTY ", 'RED')
                        temp_result.append(RESULT_TEMP)

                if i == "B":
                    self.print_console("DRIVE CHECK Test Started...")
                    temp_result.append(self.RETRY_FUNCTION(RETRY_COUNT=5, FUNC=lambda: self.drive_check(True, ['C'], 3, "AC1")))

                if i == "R and Y":
                    temp_result.append(self.RETRY_FUNCTION(RETRY_COUNT=5, FUNC=lambda: self.drive_check(True, ['C', 'E'], 4, "AC2")))
                    temp_result.append(self.RETRY_FUNCTION(RETRY_COUNT=5, FUNC=lambda: self.drive_check(False, ['C', "E"], 2, "LCU")))

                    self.prompt.Message(prompt="Kindly Re-connect Temperature Cable Connector back to system!")
                time.sleep(1)

                ac_phase_on_sequence([""])

                "WILL SAVE 15 SECONDS"
                if i == "RYB":
                    pass
                else:
                    TimerPrompt(self, "Wait for 15 seconds for SMRs to turn OFF", "15", button_status=False)
                if CALCULATE_RESULT(temp_result):
                    block_status = True
                    count = 0
                else:
                    response = self.prompt.User_prompt(f'DO YOU WANT TO RETRY FOR \"{i.upper()}\"', buzzer=1, response_time=30)
                    if response:
                        count += 1
                    else:
                        block_status = True
                        count = 4
                        temp_result.append(False)

        return CALCULATE_RESULT(temp_result)

    def drive_check(self, temp_prompt: bool, checklist: list, pfc_read: int, text: str):
        if temp_prompt:
            self.prompt.Message(prompt="Remove Temperature Cable Connector")
        time.sleep(5)
        if str(SettingRead("STATION")['id']) in checklist:
            temp_value = pfc_control.read_pfc(0x60A, pfc_number=pfc_read)
            if temp_value:
                color = 'GREEN'
            else:
                color = 'RED'
        else:
            temp_value = self.prompt.user_value_2(f"Enter Voltage Value from {text} Drive", "V")
            if float(temp_value) > 48:
                color = 'GREEN'
            else:
                color = 'RED'

        self.print_console(f"{text} Drive is {'OK' if color == 'GREEN' else 'NOT OK'}", "GREEN" if color == 'GREEN' else "RED")

        return color == 'GREEN'


    def CURRENT_SHARING(self):
        try:
            if self.config_load["current_sharing"]:
                pass
            else:
                return True
            ac_phase_type = ConfigRead('DUT CONFIGURATION')['ac phases type']
            if ac_phase_type == "SINGLE PHASE" or ac_phase_type == "THREE PHASE" or self.part_number.lower() == 'he518750':
                # self.prompt.Message(prompt="Just for check")
                return self.BUS_DROP()  # Bypasses the current sharing
            global SYSTEM_LOAD
            result_list = []
            try:
                if self.mcm_type == 1:
                    self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'ate test', "TEST_M1000_ATE")
                self.pfc.pfc_set(0, 'r_phase', 1)
                self.pfc.pfc_set(0, 'y_phase', 1)
                self.pfc.pfc_set(0, 'b_phase', 1)
                # self.pfc.pfc_set(0, 'bus', 1)
                self.pfc.pfc_set(0, 'battery_1', 1)
                self.smrcan.SMR_BATTERY_SET_VOLTAGE(47.0)
                self.dcload.DC_LOAD_SET_CURRENT_CC(5, "BATT")
                ATE_LOAD_COUNT = int(SettingRead("SETTING")['ate load count'])
                if ATE_LOAD_COUNT == 1:
                    self.pfc.pfc_set(0, 'load_mains', 1)
                time.sleep(2)
                self.print_console("CURRENT SHARING TEST STARTED...")
                TOTAL_SMR_CURRENT = 0.0
                smr_count = int(ConfigRead('DUT CONFIGURATION')['smr count'])
                smr_type = ConfigRead('DUT CONFIGURATION')['smr type']
                self.MCM_WRITE_COMMAND('SYSTEM CONFIG', 'eco mode', 0)
                if smr_type == '3KW':
                    SYSTEM_LOAD = 55.2 * 0.40 * smr_count
                elif smr_type == '25A':
                    SYSTEM_LOAD = 25 * .80 * smr_count  # 0.8-0.3
                elif smr_type == '100A':
                    SYSTEM_LOAD = 100 * 0.40 * smr_count
                elif smr_type == '4KW':
                    SYSTEM_LOAD = 70 * 0.35 * smr_count

                BATTERY_LOAD = float(SYSTEM_LOAD) / 2
                BUS_LOAD = float(SYSTEM_LOAD) / 2
                REF_SMR_AVG_CURRENT = float(SYSTEM_LOAD) / smr_count
                self.pfc.pfc_set(0, 'battery_mains', 0)
                self.dcload.DC_LOAD_SET_CURRENT_CC(BATTERY_LOAD, "BATT")
                self.dcload.DC_LOAD_SET_CURRENT_CC(BUS_LOAD, "LOAD")
                self.prompt.Message(
                    prompt=f"CHECK INDIVIDUAL SMR CURRENT IN {'M2000' if self.mcm_type == 2 else 'M1000'}. PRESS ENTER KEY TO PROCEED!")
                # self.print_console("CURRENT SHARING TIME: 15 seconds")
                # time.sleep(15)
                SMR_CURRENT = []
                SMR_CURRENT_DEVIATION = []
                INDI_SMR_CURRENT_DEVIATION = 0
                for smr_number in range(1, smr_count + 1):
                    INDI_SMR_CURRENT = float(self.MCM_READ_COMMAND('SMR COMMANDS', 'smr' + str(smr_number) + ' current'))
                    SMR_CURRENT.append(INDI_SMR_CURRENT)
                    TOTAL_SMR_CURRENT += INDI_SMR_CURRENT
                ACTUAL_SMR_AVG_CURRENT = float(TOTAL_SMR_CURRENT) / smr_count
                for smr_number in range(1, smr_count + 1):
                    INDI_SMR_CURRENT_DEVIATION = (float(
                        abs(ACTUAL_SMR_AVG_CURRENT - SMR_CURRENT[smr_number - 1])) / ACTUAL_SMR_AVG_CURRENT) * 100
                    SMR_CURRENT_DEVIATION.append(INDI_SMR_CURRENT_DEVIATION)
                if max(SMR_CURRENT_DEVIATION) < 10:
                    result_list.append(True)
                    self.print_console('SMR CURRENT DEVIATION: ' + str(max(SMR_CURRENT_DEVIATION)))
                    self.print_console('CURRENT DEVIATION PASS.')
                else:
                    result_list.append(False)
                    smr_number = 0
                    self.print_console('CURRENT DEVIATION FAIL.', "RED")
                    for CURRENT_DEVIATION in SMR_CURRENT_DEVIATION:
                        smr_number += 1
                        if CURRENT_DEVIATION > 10:
                            self.print_console('SMR NUMBER:' + str(smr_number) + ' current deviation is :' + str(
                                CURRENT_DEVIATION), "RED")
                            self.print_console(
                                'SMR CURRENT:' + str(SMR_CURRENT[smr_number - 1]) + ' AVG CURRENT is :' + str(
                                    ACTUAL_SMR_AVG_CURRENT))

                self.MCM_WRITE_COMMAND('SYSTEM CONFIG', 'eco mode', 1)
                self.dcload.DC_LOAD_SET_CURRENT_CC(5, "BATT")
                self.dcload.DC_LOAD_SET_CURRENT_CC(5, "LOAD")
                if ATE_LOAD_COUNT == 1:
                    self.pfc.pfc_set(0, 'load_mains', 0)
                self.print_console("CURRENT SHARING TEST FINISHED...")
                if CALCULATE_RESULT(result_list):
                    result_list.append(self.BUS_DROP())

            except:
                RESULT = False
            self.pfc.pfc_set(0, "battery_mains", 1)
            return CALCULATE_RESULT(result_list)
        except ZeroDivisionError as err:
            print(f"Handled ZeroDivisionError in outer function: {err}")
            self.all_stop = True
            self.print_console("ERROR IN COMMUNICATING WITH MCM", 'RED')
            self.print_console("STOPPING TEST", 'RED')
            return False
        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False

    def BUS_DROP(self):
        try:
            global SYSTEM_LOAD
            try:
                if self.mcm_type == 1:
                    self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'ate test', "TEST_M1000_ATE")
                self.print_console("BUS DROP TEST STARTED...")
                self.pfc.pfc_set(0, 'battery_1', 1)
                RESULT = []
                DUT_BATT_VOLATGE = []
                smr_count = int(ConfigRead('DUT CONFIGURATION')['smr count'])
                smr_type = ConfigRead('DUT CONFIGURATION')['smr type']
                self.MCM_WRITE_COMMAND('SYSTEM CONFIG', 'eco mode', 0)
                batt_fuse_count = int(DefaultRead('DEFAULT SETTING')[
                                          "battery ah"])  # int(ConfigRead('DUT CONFIGURATION')['no. of battery fuses'])
                ATE_LOAD_COUNT = int(SettingRead("SETTING")['ate load count'])
                if ATE_LOAD_COUNT == 1:
                    self.pfc.pfc_set(0, 'load_mains', 1)

                self.smrcan.SMR_BATTERY_SET_VOLTAGE(48.0)
                if smr_type == '3KW':
                    SYSTEM_LOAD = 55.2 * 0.60 * smr_count
                elif smr_type == '25A':
                    SYSTEM_LOAD = 25 * 0.70 * smr_count  # changed to 0.3 from 0.6
                elif smr_type == '100A':
                    SYSTEM_LOAD = 100 * 0.60 * smr_count
                elif smr_type == '4KW' or smr_type == '4':
                    SYSTEM_LOAD = 70 * 0.35 * smr_count
                else:
                    SYSTEM_LOAD = 120

                if SYSTEM_LOAD > 200:
                    SYSTEM_LOAD = 200
                BATTERY_LOAD = float(SYSTEM_LOAD) / 2
                BUS_LOAD = float(SYSTEM_LOAD) / 2
                if self.mcm_type == 3:
                    BATTERY_LOAD = 10
                    BUS_LOAD = 10
                    self.pfc.pfc_set(0, "load_mains", 1)
                    self.pfc.pfc_set(0, 'n_p_load_1', 1)

                self.dcload.DC_LOAD_SET_CURRENT_CC(BATTERY_LOAD, "BATT")
                self.dcload.DC_LOAD_SET_CURRENT_CC(BUS_LOAD, "LOAD")
                time.sleep(5)

                METER_READ_BATT_VOLTAGE = float(READ_DC_VOLTAGE(self, "BATT"))

                METER_READ_LOAD_VOLTAGE = float(READ_DC_VOLTAGE(self, "LOAD"))

                for batt_number in range(1, batt_fuse_count + 1):
                    INDI_DUT_BATT_VOLTAGE = float(
                        self.MCM_READ_COMMAND('DC READ VOLTAGE', 'batt' + str(batt_number)))
                    DUT_BATT_VOLATGE.append(INDI_DUT_BATT_VOLTAGE)
                DUT_BUS_VOLTAGE = float(self.MCM_READ_COMMAND('DC READ VOLTAGE', 'bus'))
                min_BATT_VOLTAGE = min(DUT_BATT_VOLATGE)
                max_BATT_VOLTAGE = max(DUT_BATT_VOLATGE)
                RESULT_TEMP = abs(min_BATT_VOLTAGE - max_BATT_VOLTAGE) < 0.20
                RESULT.append(RESULT_TEMP)
                RESULT_TEMP = abs(min_BATT_VOLTAGE - DUT_BUS_VOLTAGE) < 0.40
                RESULT.append(RESULT_TEMP)
                RESULT_TEMP = abs(max_BATT_VOLTAGE - DUT_BUS_VOLTAGE) < 0.40
                RESULT.append(RESULT_TEMP)
                #     RESULT_TEMP=COMPARE(METER_READ_BATT_VOLTAGE, DUT_BUS_VOLTAGE,0.20)
                #     RESULT.append(RESULT_TEMP)
                #     RESULT_TEMP=COMPARE(METER_READ_LOAD_VOLTAGE, DUT_BUS_VOLTAGE,0.20)
                #     RESULT.append(RESULT_TEMP)
                if CALCULATE_RESULT(RESULT) == False:
                    self.print_console('BUS VOLTAGE DROP FAIL.CHECK BATTERY BUS BAR ALIGNMENT/SCREWS', 'RED')
                    self.print_console('MIN BATTERY V: ' + str(min_BATT_VOLTAGE))
                    self.print_console('MAX BATTERY V: ' + str(max_BATT_VOLTAGE))
                    self.print_console('BUS V: ' + str(DUT_BUS_VOLTAGE))
                    self.print_console('METER BATT V: ' + str(METER_READ_BATT_VOLTAGE))
                    self.print_console('METER BUS V: ' + str(METER_READ_LOAD_VOLTAGE))
                else:
                    self.print_console('BUS VOLTAGE DROP PASS.')
                    self.print_console('MIN BATTERY V: ' + str(min_BATT_VOLTAGE))
                    self.print_console('MAX BATTERY V: ' + str(max_BATT_VOLTAGE))
                    self.print_console('BUS V: ' + str(DUT_BUS_VOLTAGE))
                    self.print_console('METER BATT V: ' + str(METER_READ_BATT_VOLTAGE))
                    self.print_console('METER BUS V: ' + str(METER_READ_LOAD_VOLTAGE))

                self.print_console("BUS DROP TEST FINISHED...")
                self.dcload.DC_LOAD_SET_CURRENT_CC(5, "BATT")
                self.dcload.DC_LOAD_SET_CURRENT_CC(5, "LOAD")

                if ATE_LOAD_COUNT == 1:
                    self.pfc.pfc_set(0, 'load_mains', 0)
            except:
                return False
            return CALCULATE_RESULT(RESULT)
        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False

    def RS_485_CHECK(self):
        try:
            if self.config_load["rs_485"]:
                pass
            else:
                return True
            if self.mcm_type == 1:
                self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'ate test', "TEST_M1000_ATE")
            test_sub_id = 0
            self.print_console("RS_485_CHECK TEST STARTED...")

            RESULT = []
            lower_port_number = 1
            if self.customer_name_edit.text() == "RELIANCE":
                lower_port_number = 1
            upper_port_number = 2
            if self.customer_name_edit.text() == "RELIANCE":
                upper_port_number = 2
            none_port_number = 255
            if self.mcm_type == 1:
                lower_port_number = 4
                upper_port_number = 0

            lower_port_baudrate = int(ConfigRead('DUT CONFIGURATION')['lower port baudrate'])
            upper_port_baudrate = int(ConfigRead('DUT CONFIGURATION')['upper port baudrate'])
            lithium_ion_comm_port = int(ConfigRead('DUT CONFIGURATION')['lithium ion comm'])
            acem_comm_port = int(ConfigRead('DUT CONFIGURATION')['acem comm'])
            dg_amf_comm_port = int(ConfigRead('DUT CONFIGURATION')['dg amf comm'])
            solar_hvlv_comm_port = int(ConfigRead('DUT CONFIGURATION')['solar hvlv comm'])
            ext_dcem_comm_port = int(ConfigRead('DUT CONFIGURATION')['ext dcem comm'])
            bnms_comm_port = int(ConfigRead('DUT CONFIGURATION')['bnms comm'])
            modbus_comm_port = int(ConfigRead('DUT CONFIGURATION')['modbus comm'])

            """
            PORTING VARIABLES
            """
            dg = self.MCM_READ_COMMAND('RS 485', 'dg amf comm')
            acem = self.MCM_READ_COMMAND('RS 485', 'acem comm')
            li = self.MCM_READ_COMMAND('RS 485', 'lithium ion comm')

            if acem_comm_port == lower_port_number or lithium_ion_comm_port == lower_port_number or dg_amf_comm_port == lower_port_number or modbus_comm_port == lower_port_number or str(self.part_number.lower()) == "he518713":

                if self.customer_name_edit.text() != "RELIANCE":
                    self.MCM_WRITE_COMMAND('RS 485', 'acem comm', 0)
                    self.MCM_WRITE_COMMAND('RS 485', 'lithium ion comm', 0)
                    self.MCM_WRITE_COMMAND('RS 485', 'dg amf comm', 0)
                    self.MCM_WRITE_COMMAND('RS 485', 'bnms comm', 0)

                if self.mcm_type == 1 and self.customer_name_edit.text() == "RELIANCE":
                    self.MCM_WRITE_COMMAND('RS 485', 'acem comm', 255)
                    self.MCM_WRITE_COMMAND('RS 485', 'lithium ion comm', 255)
                    self.MCM_WRITE_COMMAND('RS 485', 'dg amf comm', 255)
                    self.MCM_WRITE_COMMAND('RS 485', 'bnms comm', 255)

                self.MCM_WRITE_COMMAND('RS 485', 'modbus comm', lower_port_number)

                charge_voltage_telnet = float(self.MCM_READ_COMMAND('BATTERY SETTING', 'charge voltage'))
                charge_voltage_modbus = float(MODBUS_CHECK('lower', lower_port_baudrate)) / 10
                if charge_voltage_modbus == charge_voltage_telnet:
                    RESULT_TEMP = True
                    self.print_console("MODBUS CHARGE VOLTAGE:" + str(charge_voltage_modbus))
                    self.print_console("TELNET CHARGE VOLTAGE:" + str(charge_voltage_telnet))
                    self.print_console("LOWER PORT TESTED OK")
                elif abs(charge_voltage_modbus - charge_voltage_telnet) < 0.8:
                    RESULT_TEMP = True
                    self.print_console("MODBUS CHARGE VOLTAGE:" + str(charge_voltage_modbus))
                    self.print_console("TELNET CHARGE VOLTAGE:" + str(charge_voltage_telnet))
                    self.print_console("LOWER PORT TESTED OK")
                else:
                    RESULT_TEMP = False
                    self.print_console("MODBUS CHARGE VOLTAGE:" + str(charge_voltage_modbus))
                    self.print_console("TELNET CHARGE VOLTAGE:" + str(charge_voltage_telnet))
                    self.print_console("LOWER PORT TESTED FAIL", "RED")
                RESULT.append(RESULT_TEMP)

                if self.mcm_type == 1 and self.customer_name_edit.text() == "RELIANCE":
                    self.MCM_WRITE_COMMAND('RS 485', 'acem comm', acem)
                    self.MCM_WRITE_COMMAND('RS 485', 'lithium ion comm', li)
                    self.MCM_WRITE_COMMAND('RS 485', 'dg amf comm', dg)
                    self.MCM_WRITE_COMMAND('RS 485', 'modbus comm', 255)

            else:
                RESULT_TEMP = True
                self.print_console("LOWER PORT TESTING NOT APPLICABLE")

            if upper_port_number == acem_comm_port or lithium_ion_comm_port == upper_port_number or dg_amf_comm_port == upper_port_number or modbus_comm_port == upper_port_number or str(self.part_number.lower()) == "he518713":
                if self.customer_name_edit.text() != "RELIANCE":
                    self.MCM_WRITE_COMMAND('RS 485', 'acem comm', 0)
                    self.MCM_WRITE_COMMAND('RS 485', 'lithium ion comm', 0)
                    self.MCM_WRITE_COMMAND('RS 485', 'dg amf comm', 0)
                    self.MCM_WRITE_COMMAND('RS 485', 'bnms comm', 0)

                if self.mcm_type == 1 and self.customer_name_edit.text() == "RELIANCE":
                    self.MCM_WRITE_COMMAND('RS 485', 'acem comm', 255)
                    self.MCM_WRITE_COMMAND('RS 485', 'lithium ion comm', 255)
                    self.MCM_WRITE_COMMAND('RS 485', 'dg amf comm', 255)
                    self.MCM_WRITE_COMMAND('RS 485', 'bnms comm', 255)

                self.MCM_WRITE_COMMAND('RS 485', 'modbus comm', upper_port_number)

                voltage = self.MCM_READ_COMMAND("BATTERY SETTING", 'charge voltage')
                charge_voltage_telnet = float(voltage if voltage is not None else 0)
                charge_voltage_modbus = float(MODBUS_CHECK('upper', upper_port_baudrate)) / 10

                if charge_voltage_modbus == charge_voltage_telnet:
                    RESULT_TEMP = True
                    self.print_console("MODBUS CHARGE VOLTAGE:" + str(charge_voltage_modbus))
                    self.print_console("TELNET CHARGE VOLTAGE:" + str(charge_voltage_telnet))
                    self.print_console("UPPER PORT TESTED OK")
                else:
                    RESULT_TEMP = False
                    self.print_console("MODBUS CHARGE VOLTAGE:" + str(charge_voltage_modbus))
                    self.print_console("TELNET CHARGE VOLTAGE:" + str(charge_voltage_telnet))
                    self.print_console("UPPER PORT TESTED FAIL", "RED")

                if self.mcm_type == 1 and self.customer_name_edit.text() == "RELIANCE":
                    self.MCM_WRITE_COMMAND('RS 485', 'acem comm', acem)
                    self.MCM_WRITE_COMMAND('RS 485', 'lithium ion comm', li)
                    self.MCM_WRITE_COMMAND('RS 485', 'dg amf comm', dg)
                    self.MCM_WRITE_COMMAND('RS 485', 'modbus comm', 255)

                RESULT.append(RESULT_TEMP)
            else:
                RESULT_TEMP = True
                self.print_console("UPPER PORT TESTING NOT APPLICABLE")
            self.print_console("RS_485_CHECK TEST FINISHED...")

            self.MCM_WRITE_COMMAND('RS 485', 'acem comm', acem)
            self.MCM_WRITE_COMMAND('RS 485', 'lithium ion comm', li)
            self.MCM_WRITE_COMMAND('RS 485', 'dg amf comm', dg)
            self.MCM_WRITE_COMMAND('RS 485', 'modbus comm', 0)

            return CALCULATE_RESULT(RESULT)
        except ZeroDivisionError as err:
            print(f"Handled ZeroDivisionError in outer function: {err}")
            self.all_stop = True
            self.print_console("ERROR IN COMMUNICATING WITH MCM", 'RED')
            self.print_console("STOPPING TEST", 'RED')
            return False
        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False

    def DEFAULT_SETTING(self):
        try:
            if self.config_load["default"]:
                pass
            else:
                return True
            self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'factory restore', 1)

            if self.mcm_type == 1:
                self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'ate test', "TEST_M1000_ATE")

            site_id = self.MCM_READ_COMMAND('SYSTEM CONFIG', 'site id')
            self.print_console("Controller Healthy") if site_id is not None else self.print_console("Controller OFF")
            RESULT_TEMP: bool = True if site_id is not None else False

            if self.custom_check.isChecked():
                self._set_custom_settings()
            else:
                self._set_default_settings()

            float_voltage, charge_voltage, battery_lvd_set, battery_lvd_restore, load_lvd_count, \
                load_lvd_set, load_lvd_restore, dc_v_low_set, dc_v_low_restore, \
                main_low_fail_set, main_low_fail_restore, main_high_fail_set, \
                main_high_fail_restore, smr_count, m1000_serial_number, s_charger = self._get_battery_settings()

            # self.print_console("MAC ID -  : " + self.MCM_READ_COMMAND(m1000_mac_id))
            battery_capacity_vrla, bcl_factor_vrla = self._get_battery_config_vrla()
            battery_capacity, bcl_factor, module_count = self._get_battery_config_lion()
            dc_v_low_restore = eval(str(dc_v_low_set)) + eval(str(dc_v_low_restore))
            if self.mcm_type == 2:
                battery_lvd_restore = eval(str(battery_lvd_restore)) + eval(str(battery_lvd_set))
                load_lvd_restore = eval(str(load_lvd_set)) + eval(str(load_lvd_restore))
            main_low_fail_restore = eval(str(main_low_fail_set)) + eval(str(main_low_fail_restore))
            main_high_fail_restore = eval(str(main_high_fail_set)) + eval(str(main_high_fail_restore))

            if int(ConfigRead('DUT CONFIGURATION')['no. of load lvd']) == 0:
                load_lvd_set = "NA"
                load_lvd_restore = "NA"
            else:
                pass

            if self.mcm_type == 1 and self.customer_name.lower() == 'reliance':
                self.smr_variable = str(smr_count)
            else:
                if len(s_charger) == 0:
                    self.smr_variable = str(smr_count)
                else:
                    self.smr_variable = str(smr_count) + '/' + str(s_charger)
                print("SMR_VARIABLE")
                print(len(self.smr_variable), self.smr_variable, s_charger, len(s_charger))

            # self._prevent_gui_hang()
            self.left_over_list = [str(float_voltage), str(charge_voltage), str(battery_lvd_set) + "/" + str(battery_lvd_restore),
                                   str(load_lvd_set) + '/' + str(load_lvd_restore), str(dc_v_low_set) + '/' + str(dc_v_low_restore),
                                   str(main_low_fail_set) + '/' + str(main_low_fail_restore),
                                   str(main_high_fail_set) + '/' + str(main_high_fail_restore),
                                   self.smr_variable, str(battery_capacity_vrla) + '/' + str(bcl_factor_vrla),
                                   str(battery_capacity) + '/' + str(bcl_factor) + '/' + str(module_count)]
            self._update_excel_handler(float_voltage, charge_voltage, battery_lvd_set, battery_lvd_restore,
                                       load_lvd_set, load_lvd_restore, dc_v_low_set, dc_v_low_restore,
                                       main_low_fail_set, main_low_fail_restore, main_high_fail_set,
                                       main_high_fail_restore, smr_count, self.mac_id, m1000_serial_number,
                                       battery_capacity_vrla, bcl_factor_vrla, battery_capacity, bcl_factor, module_count,
                                       s_charger)

            return RESULT_TEMP
        except ZeroDivisionError as err:
            print(f"Handled ZeroDivisionError in outer function: {err}")
            self.all_stop = True
            self.print_console("ERROR IN COMMUNICATING WITH MCM", 'RED')
            self.print_console("STOPPING TEST", 'RED')
            return False
        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False

    def _prevent_gui_hang(self):
        QtGui.qApp.processEvents()

    def _set_custom_settings(self):
        try:
            self.print_console("Custom settings will be programmed to controller")
            default_settings = DefaultRead('DEFAULT SETTING')
            default_state = DefaultRead('DEFAULT SETTING STATE')
            for setting in ['smr count', 'system overload']:
                if default_state[setting] == 'YES':
                    self.MCM_WRITE_COMMAND('SYSTEM CONFIG', setting, int(default_settings[setting]))
        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False

    def _set_default_settings(self):
        self.print_console("Default setting are as per Config file")

    def _get_battery_settings(self):
        try:
            settings = ['float voltage', 'charge voltage', 'battery lvd set', 'battery lvd restore',
                        'no. of load lvd', 'load1 lvd set', 'load1 lvd restore', 'dc voltage low set',
                        'dc voltage low restore', 'mains low fail set', 'mains low fail restore',
                        'mains high fail set', 'mains high fail restore', 'smr count',
                        'serial number']
            data_list = []
            for setting in settings:
                data_list.append(self.MCM_READ_COMMAND('BATTERY SETTING', setting))

            if self.config_load["solar"]:
                if int(self.MCM_READ_COMMAND('SOLAR', 'solar present')):
                    data_list.append(self.MCM_READ_COMMAND('BATTERY SETTING', 's charger'))
            else:
                data_list.append("")
            print("battery")
            print(data_list)
            return data_list
        except (AllException, AttributeError) as err:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(err)
            self.all_stop = True
            return False

    def _get_battery_config_vrla(self):
        return int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'vrla battery capacity')), \
            int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'vrla bcl factor'))

    def _get_battery_config_lion(self):
        return int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'lion battery capacity')), \
            int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'lion bcl factor')), \
            int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'lion module count'))

    def _update_excel_handler(self, float_voltage, charge_voltage, battery_lvd_set, battery_lvd_restore,
                              load_lvd_set, load_lvd_restore, dc_v_low_set, dc_v_low_restore,
                              main_low_fail_set, main_low_fail_restore, main_high_fail_set,
                              main_high_fail_restore, smr_count, m1000_mac_id, m1000_serial_number,
                              battery_capacity_vrla, bcl_factor_vrla, battery_capacity, bcl_factor, module_count,
                              s_charger):
        try:
            print(float_voltage, charge_voltage, battery_lvd_set, battery_lvd_restore,
                  load_lvd_set, load_lvd_restore, dc_v_low_set, dc_v_low_restore,
                  main_low_fail_set, main_low_fail_restore, main_high_fail_set,
                  main_high_fail_restore, smr_count, m1000_mac_id, m1000_serial_number,
                  battery_capacity_vrla, bcl_factor_vrla, battery_capacity, bcl_factor, module_count, s_charger)
            self.excel_handler.update_cell("FLOAT VOLTAGE (VDC)", str(float_voltage))
            self.excel_handler.update_cell("M1000 MAC ID", str(m1000_mac_id))
            self.excel_handler.update_cell("CHARGE VOLTAGE (VDC)", str(charge_voltage))
            self.excel_handler.update_cell("BATTERY LVD SET(VDC)/RESTORE(VDC)", f"{battery_lvd_set}/{battery_lvd_restore}")
            self.excel_handler.update_cell("LOAD LVD SET(VDC)/RESTORE(VDC)", f"{load_lvd_set}/{load_lvd_restore}")
            self.excel_handler.update_cell("DC VOLTAGE LOW(VDC)/RESTORE(VDC)", f"{dc_v_low_set}/{dc_v_low_restore}")
            self.excel_handler.update_cell("AC LOW CUT-OFF(VAC)/CUT-IN(VAC)",
                                           f"{main_low_fail_set}/{main_low_fail_restore}")
            self.excel_handler.update_cell("AC HIGH CUT-OFF(VAC)/CUT-IN(VAC)",
                                           f"{main_high_fail_set}/{main_high_fail_restore}")

            if self.mcm_type == 1 and self.customer_name.lower() == 'reliance':
                self.smr_variable = str(smr_count)
            else:
                self.smr_variable = str(smr_count) + '/' + str(s_charger)

            self.excel_handler.update_cell("SMR COUNT/ SOLAR CHARGER COUNT", f"{self.smr_variable}")
            self.excel_handler.update_cell("VRLA: BATTERY CAPACITY/ FACTOR", f"{battery_capacity_vrla}/{bcl_factor_vrla}")
            self.excel_handler.update_cell("LI-ON BATTERY/ FACTOR", f"{battery_capacity}/{bcl_factor}/{module_count}")
            # self._prevent_gui_hang()
        except exception as e:
            print(str(e))

    def DEFAULT_SETTING1(self):

        try:
            global battery_capacity_vrla, bcl_factor_vrla, battery_capacity, bcl_factor, module_count
            self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'factory restore', 1)
            QtGui.qApp.processEvents()  # ADDED TO PREVENT GUI HANG PROBLEM,PARAS MITTAL
            time.sleep(5)
            QtGui.qApp.processEvents()  # ADDED TO PREVENT GUI HANG PROBLEM,PARAS MITTAL
            if self.mcm_type == 1:
                self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'ate test', "TEST_M1000_ATE")
            site_id = self.MCM_READ_COMMAND('SYSTEM CONFIG', 'site id')
            if site_id is not None:
                self.print_console("Controller Healthy")
                RESULT_TEMP = True
            else:
                self.print_console("Controller OFF")
                RESULT_TEMP = False
            '''
            ## TO BE OPENED AFTER SERIAL NUMBER/PART NUMBER IMPLEMENTATION IN 15.XX/10.XX
            DUT_Part_Number=str(self.lineEdit_DUTPartNumber.text())
            DUT_Serial_Number=str(self.lineEdit_DUTSerialNumber.text())
    
            TELNET_SET_COMMAND(self.telnet,OIDRead('SYSTEM COMMANDS')['system part number'],DUT_Part_Number)
            PRINT_CONSOLE(self, "SYSTEM PART NUMBER ENTERED IN M1000: "+DUT_Part_Number)
    
            TELNET_SET_COMMAND(self.telnet,OIDRead('SYSTEM COMMANDS')['system serial number'],DUT_Serial_Number)
            PRINT_CONSOLE(self, "SYSTEM SERIAL NUMBER ENTERED IN M1000: "+DUT_Serial_Number)
            '''

            if self.custom_check.isChecked():
                self.print_console("Custom settings will be programmed to controller")
                # MESSAGE_PROMPT(self,"Custom settings will be programmed to controller")
                if DefaultRead('DEFAULT SETTING STATE')["smr count"] == 'YES':
                    default_smr_count = int(DefaultRead('DEFAULT SETTING')["smr count"])
                    self.MCM_WRITE_COMMAND('SYSTEM CONFIG', 'smr count', default_smr_count)
                if DefaultRead('DEFAULT SETTING STATE')["system overload"] == 'YES':
                    default_system_overload = int(DefaultRead('DEFAULT SETTING')["system overload"])
                    self.MCM_WRITE_COMMAND('SYSTEM CONFIG', 'system overload', default_system_overload)
                # if DefaultRead('DEFAULT SETTING STATE')["battery ah"] == 'YES':
                #     default_battery_ah = int(DefaultRead('DEFAULT SETTING')["battery ah"])
                #     self.MCM_WRITE_COMMAND('SYSTEM CONFIG', 'vrla battery capacity', default_battery_ah)
            else:
                self.print_console("Default setting are as per Config file")
                # MESSAGE_PROMPT(self,"Default setting are as per Config file ")

            ## load default setting for report
            float_voltage = float(self.MCM_READ_COMMAND('BATTERY SETTING', 'float voltage'))
            charge_voltage = float(self.MCM_READ_COMMAND('BATTERY SETTING', 'charge voltage'))
            battery_lvd_set = float(self.MCM_READ_COMMAND('BATTERY SETTING', 'battery lvd set'))
            battery_lvd_restore = float(self.MCM_READ_COMMAND('BATTERY SETTING', 'battery lvd restore'))
            load_lvd_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'no. of load lvd'))
            if load_lvd_count != 0:
                load_lvd_set = float(self.MCM_READ_COMMAND('BATTERY SETTING', 'load1 lvd set'))
                load_lvd_restore = float(self.MCM_READ_COMMAND('BATTERY SETTING', 'load1 lvd restore'))

            else:
                load_lvd_set = 'NA'
                load_lvd_restore = 'NA'
            dc_v_low_set = float(self.MCM_READ_COMMAND('BATTERY SETTING', 'dc voltage low set'))
            dc_v_low_restore = float(self.MCM_READ_COMMAND('BATTERY SETTING', 'dc voltage low restore'))
            dc_v_low_restore += dc_v_low_set
            main_low_fail_set = int(self.MCM_READ_COMMAND('MAINS SETTING', 'mains low fail set'))
            main_low_fail_restore = int(self.MCM_READ_COMMAND('MAINS SETTING', 'mains low fail restore'))
            main_low_fail_restore = main_low_fail_set + main_low_fail_restore
            main_high_fail_set = int(self.MCM_READ_COMMAND('MAINS SETTING', 'mains high fail set'))
            main_high_fail_restore = int(self.MCM_READ_COMMAND('MAINS SETTING', 'mains high fail restore'))
            main_high_fail_restore = main_high_fail_set + main_high_fail_restore
            smr_count = self.MCM_READ_COMMAND('SYSTEM CONFIG', 'smr count')
            m1000_mac_id = self.MCM_READ_COMMAND('SYSTEM COMMANDS', 'm1000 mac id')
            m1000_serial_number = self.MCM_READ_COMMAND('SYSTEM COMMANDS', 'serial number')
            QtGui.qApp.processEvents()  # ADDED TO PREVENT GUI HANG PROBLEM, PARAS MITTAL, 12/03/2024
            battery_type = ConfigRead('DUT CONFIGURATION')['battery type']
            if battery_type == 'VRLA':
                battery_capacity_vrla = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'vrla battery capacity'))
                bcl_factor_vrla = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'vrla bcl factor'))

            elif battery_type == 'LION':
                battery_capacity = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'lion battery capacity'))
                module_count = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'lion module count'))
                bcl_factor = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'lion bcl factor'))
                battery_capacity_vrla = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'vrla battery capacity'))
                bcl_factor_vrla = int(self.MCM_READ_COMMAND('SYSTEM CONFIG', 'vrla bcl factor'))
            RESULT_DEFAULT = True
            test_sub_id = 0
            test_sub_id += 1

            QtGui.qApp.processEvents()  # ADDED TO PREVENT GUI HANG PROBLEM,Paras MITTAL,24/10/2016
            self.excel_handler.update_cell("FLOAT VOLTAGE (VDC)", str(float_voltage))
            self.excel_handler.update_cell("M1000 MAC ID", str(m1000_mac_id))
            self.excel_handler.update_cell("CHARGE VOLTAGE (VDC)", str(charge_voltage))
            self.excel_handler.update_cell("BATTERY LVD SET(VDC)/RESTORE(VDC)",
                                           str(battery_lvd_set) + "/" + str(battery_lvd_restore))
            self.excel_handler.update_cell("LOAD LVD SET(VDC)/RESTORE(VDC)",
                                           str(load_lvd_set) + "/" + str(load_lvd_restore))
            self.excel_handler.update_cell("DC VOLTAGE LOW(VDC)/RESTORE(VDC)",
                                           str(dc_v_low_set) + "/" + str(dc_v_low_restore))
            self.excel_handler.update_cell("AC LOW CUT-OFF(VAC)/CUT-IN(VAC)",
                                           str(main_low_fail_set) + "/" + str(main_low_fail_restore))
            self.excel_handler.update_cell("AC HIGH CUT-OFF(VAC)/CUT-IN(VAC)",
                                           str(main_high_fail_set) + "/" + str(main_high_fail_restore))
            self.excel_handler.update_cell("SMR COUNT/ SOLAR CHARGER COUNT", str(smr_count) + "/" + str("NA"))
            self.excel_handler.update_cell("VRLA: BATTERY CAPACITY/ FACTOR",
                                           str(battery_capacity_vrla) + "/" + str(bcl_factor_vrla))
            self.excel_handler.update_cell("LI-ON BATTERY/ FACTOR",
                                           str(battery_capacity) + "/" + str(bcl_factor) + "/" + str(module_count))
            QtGui.qApp.processEvents()  # ADDED TO PREVENT GUI HANG PROBLEM,Paras MITTAL,24/4/2024
            return RESULT_TEMP
        except exception as e:
            print((str(e)))

    def run_solar(self):
        global run_status
        while run_status:
            CanModule.CAN.CAN_WRITE_SOLO(CanModule.CAN, 1, 0x610, packet=[0x02DA01F0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         bitrate=125000)

    def CHECK_DEVICES(self):
        try:
            self.print_console("CHECK DEVICES TEST STARTED....")
            self.HEALTH_CHECK_SMR_BATTERY()
            self.HEALTH_CHECK_DC_LOAD()
            # self.dcload.DC_LOAD_SET_CURRENT_CC()
            self.dcload.DC_LOAD_SET_CURRENT_CC(0, load_type="LOAD")
            self.dcload.DC_LOAD_SET_CURRENT_CC(0, load_type="BATT")
            self.print_console("CHECK DEVICES TEST FINISHED...")
        except TypeError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
        except RuntimeError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
        except AttributeError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
        except FileNotFoundError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
        except can.interfaces.ixxat.exceptions as err:
            print(err)
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
        except Exception as err:
            print(err)
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(f'Type of error is : {type(err)}')

    def ATS_INITIALIZE(self):
        try:
            self.print_console("ATS INITIALIZING....")
            self.HEALTH_CHECK_SMR_BATTERY()
            InitChromaLoad(self.dcload.DC_LOAD, "LOAD")
            InitChromaLoad(self.dcload.DC_LOAD, "BATT")
            self.INITIAL_LOAD(type="LOAD")
            self.INITIAL_LOAD(type="BATT")
            self.print_console("ATS INITIALIZED....")
            return True
        except exception as e:
            print(e)

    def HEALTH_CHECK_SMR_BATTERY(self):
        try:
            if gui_global.test_stop:
                return False
            print('health smr started')
            self.smrcan.SMR_BATTERY_SET_VOLTAGE(50.0)
            print('health smr finished')
        except RuntimeError as err:
            print(err)
            raise RuntimeError
        except exception as e:
            print(e)

    def HEALTH_CHECK_DC_LOAD(self):
        try:
            if gui_global.test_stop:
                return False
            print("load health check started")
            self.dcload.DC_LOAD.DC_LOAD_READ_COMMAND(self.dcload.DC_LOAD, self.dcload.identify_unit)
            print("load health check  finished")

        except TypeError:

            raise TypeError

    def CLEAR_JIG(self):
        try:
            self.print_console('CLEARING JIG....')
            self.pfc.pfc_set("0", "pfc 2", 0)  ## PENDING DCLOAD RESET
            self.dcload.DC_LOAD.DC_LOAD_SET_COMMAND(self.dcload.DC_LOAD, self.dcload.load_OFF)
            self.dcload.DC_LOAD.DC_LOAD_SET_COMMAND(self.dcload.DC_LOAD, self.dcload.load_OFF, "BATT")
            self.print_console("JIG CLEARED....")
        except TypeError as e:
            self.prompt.Message(prompt="Communication with DC Load not OK")
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(str(e))
        except RuntimeError as e:
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(str(e))
        except AttributeError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
        except FileNotFoundError as e:
            print(str(e))
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
        except can.interfaces.ixxat.exceptions as err:
            print(err)
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
        except Exception as err:
            print(err)
            self.print_console(f"error occurred in function : {inspect.currentframe().f_code.co_name}")
            print(f'Type of error is : {type(err)}')

    def MCM_READ_COMMAND(self, command='', section="", pool=0):
        try:
            recall_value = None
            '''
            added recall_value variable to handle MCM read exceptions
            '''
            if self.mcm_type == 1 and pool == 0:
                recall_value = M1000Telnet.telnet_get_command(OIDRead(command)[section])
            elif self.mcm_type == 1 and pool == 1:
                recall_value = M1000Telnet.telnet_get_command(section)
            elif self.mcm_type == 2 and pool == 1:
                recall_value = self.M2000.MCM_GET_COMMAND(section)
            elif self.mcm_type == 2:
                recall_value = self.M2000.MCM_GET_COMMAND(M2000OIDRead(command)[section])
            elif self.mcm_type == 3 and pool == 0:
                recall_value = self.M1KLC.MCM_GET_COMMAND(M2000OIDRead(command)[section])
            elif self.mcm_type == 3 and pool == 1:
                recall_value = self.M1KLC.MCM_GET_COMMAND(section)

            if gui_global.telnet_connection_not_restablished or gui_global.communication_lost:
                self.print_console("MCM COMMUNICATION LOST, NOT RE-ESTABLISHING", "RED")
                self.print_console("STOPPING TEST.....", "RED")
                self.all_stop = True
                self.stop_function()
                return []

            """
            FOR MCM 1000 IF SOME OID VALUE IS NOT AVAILABLE
            """
            if "OID Not Found" in str(recall_value):
                return str(0)

            return str(0) if recall_value is None else recall_value
        except ZeroDivisionError as zero_division:
            print("error in mcm read command", zero_division)
            raise
        except exception as e:
            print(e)
            self.all_stop = True
            return str(0)

    def MCM_WRITE_COMMAND(self, command='', section='', value=''):
        try:
            if self.mcm_type == 1:
                M1000Telnet.telnet_set_command(OIDRead(command)[section], value)
            elif self.mcm_type == 2:
                self.M2000.MCM_SET_COMMAND(M2000OIDRead(command)[section], value)
            else:
                print("")
        except ZeroDivisionError as zero_division:
            print("error in mcm read command", zero_division)
            raise
        except exception as e:
            print(str(e))
            self.all_stop = True
            if gui_global.telnet_connection_not_restablished or gui_global.communication_lost:
                self.print_console("MCM COMMUNICATION LOST, NOT RE-ESTABLISHING", "RED")
                self.print_console("STOPPING TEST.....", "RED")
                self.all_stop = True
                self.stop_function()
                return 88888


def SET_INDI_LOAD_ISOLATE(self, load_no, state):
    self.MCM_WRITE_COMMAND('LOAD ISOLATE', 'load' + str(load_no), state)


def CALIBRATE_CURRENT_PATH_HALL_EFFECT(self, channel_number, load_type):
    try:
        if self.mcm_type == 1:
            self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'ate test', "TEST_M1000_ATE")
        RESULT = []
        self.smrcan.SMR_BATTERY_SET_VOLTAGE(53.5)
        if self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' gain') != '0' or (
                self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(
                    channel_number) + ' offset') != '0'):  # or (TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' deadband'])!='0')
            self.print_console("Resetting offset and gain again")
            # TELNET_SET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' deadband'],0)
            # time.sleep(1)
            self.MCM_WRITE_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' gain', 0)
            # time.sleep(1)
            self.MCM_WRITE_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' offset', 0)
            time.sleep(0.5)
            self.print_console("CURRENT CHANNEL " + str(channel_number) + " GAIN: " + str(
                self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' gain')))
            self.print_console("CURRENT CHANNEL " + str(channel_number) + " OFFSET: " + str(
                self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' offset')))
            # PRINT_CONSOLE(self,"CURRENT CHANNEL "+str(channel_number)+" DEADBAND: "+str(TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' deadband'])))

        channel_hall_effect_value = int(
            ConfigRead('DUT CONFIGURATION')['channel' + str(channel_number) + ' hall effect value'])
        SET_CURRENT_LOW = int(CalibrateSetting('HALL EFFECT')['current low'])
        SET_CURRENT_HIGH = int(CalibrateSetting('HALL EFFECT')['current high'])
        NUMBER_OF_BITS = int(CalibrateSetting('HALL EFFECT')['number of bits'])
        FACTOR = float(CalibrateSetting('HALL EFFECT')['factor'])
        ADC_MULTIPLIER = int(CalibrateSetting('HALL EFFECT')['adc multiplier'])
        DEADBAND = int(CalibrateSetting('HALL EFFECT')['deadband'])
        VERIFY_CURRENT_LOW = int(CalibrateSetting('HALL EFFECT')['verify current low'])
        VERIFY_CURRENT_MID = int(CalibrateSetting('HALL EFFECT')['verify current mid'])
        VERIFY_CURRENT_HIGH = int(CalibrateSetting('HALL EFFECT')['verify current high'])
        CURRENT_TOLERANCE = float(CalibrateSetting('HALL EFFECT')['current tolerance'])
        NEGATIVE_SET_CURRENT_LOW = int(CalibrateSetting('HALL EFFECT')['negative current low'])
        NEGATIVE_CURRENT_CAL = str(CalibrateSetting('HALL EFFECT')['negative current cal'])

        if load_type == 'BATT' and NEGATIVE_CURRENT_CAL == 'YES':
            ATE_LOAD_COUNT = int(SettingRead("SETTING")['ate load count'])
            if ATE_LOAD_COUNT == 1:  # ADDED FOR SINGLE LOAD CONFIGURATION, KUSHAGRA MITTAL 06/09/2016
                # self.pfc.pfc_set(0, 'DC LOAD', 0)
                self.pfc.pfc_set(0, 'load_mains', 1)
                # time.sleep(1)

            self.MCM_WRITE_COMMAND('BATTERY SETTING', 'float voltage', 51)
            self.MCM_WRITE_COMMAND('BATTERY SETTING', 'charge voltage', 51.5)
            self.MCM_WRITE_COMMAND('BATTERY SETTING', 'lion charge voltage', 51)
            # SET_JIG_PFC_OP(self.can,'AC',0)

            self.dcload.DC_LOAD_SET_CURRENT_CC(NEGATIVE_SET_CURRENT_LOW, "LOAD")
            time.sleep(2)
            METER_READ_CURRENT_LOW = float(READ_DC_CURRENT("LOAD"))
            METER_READ_CURRENT_LOW = (-1 * METER_READ_CURRENT_LOW) - float(
                CalibrateSetting('HALL EFFECT')['batt discharge compensation'])
        else:
            ATE_LOAD_COUNT = int(SettingRead("SETTING")['ate load count'])
            if ATE_LOAD_COUNT == 1 and load_type == 'BATT':
                self.print_console("RESETTING FOR BATTERY PATH")
                # ADDED FOR SINGLE LOAD CONFIGURATION, KUSHAGRA MITTAL 06/09/2016
                self.pfc.pfc_set(0, 'load_mains', 1)
                # self.pfc.pfc_set(0, 'DC LOAD', 1)
                # time.sleep(1)
            self.dcload.DC_LOAD_SET_CURRENT_CC(SET_CURRENT_LOW, load_type)
            time.sleep(2)
            METER_READ_CURRENT_LOW = float(READ_DC_CURRENT(load_type))

        DUT_READ_CURRENT_LOW = float(self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number))) / 10
        BATT_CHARGE_CURRENT_COMPENSATION = 0
        self.print_console("CH :" + str(channel_number) + " DUT LOW: " + str(DUT_READ_CURRENT_LOW))
        self.print_console("CH :" + str(channel_number) + " METER LOW: " + str(METER_READ_CURRENT_LOW))
        if load_type == 'BATT' and NEGATIVE_CURRENT_CAL == 'YES':
            self.dcload.DC_LOAD_SET_CURRENT_CC(5, "LOAD")
            self.dcload.DC_LOAD_SET_CURRENT_CC(5, "BATT")
            ATE_LOAD_COUNT = int(SettingRead("SETTING")['ate load count'])
            if ATE_LOAD_COUNT == 1:  # ADDED FOR SINGLE LOAD CONFIGURATION, PARAS MITTAL 06/09/2016
                self.pfc.pfc_set(0, 'load_mains', 1)
                # self.pfc.pfc_set(0, 'DC LOAD', 1)
                # time.sleep(1)

            self.MCM_WRITE_COMMAND('BATTERY SETTING', 'charge voltage', 55.2)
            self.MCM_WRITE_COMMAND('BATTERY SETTING', 'float voltage', 54)
            self.MCM_WRITE_COMMAND('BATTERY SETTING', 'lion charge voltage', 54)

            time.sleep(2)
            self.dcload.SMR_BATTERY_SET_VOLTAGE(47.0)

            # SET_JIG_PFC_OP(self.can,'AC',1)
            BATT_CHARGE_CURRENT_COMPENSATION = float(CalibrateSetting('HALL EFFECT')['batt charge compensation'])
            # time.sleep(2)
        # time.sleep(5)
        ATE_LOAD_COUNT = int(SettingRead("SETTING")['ate load count'])
        if ATE_LOAD_COUNT == 1:  # ADDED FOR SINGLE LOAD CONFIGURATION, KUSHAGRA MITTAL 06/09/2016
            load_type = "LOAD"

        self.dcload.DC_LOAD_SET_CURRENT_CC(SET_CURRENT_HIGH, str(load_type))

        time.sleep(2)
        self.prompt.Message(prompt="WAIT FOR THE LOAD TO BUILD...")
        DUT_READ_CURRENT_HIGH = float(self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number))) / 10
        METER_READ_CURRENT_HIGH = float(READ_DC_CURRENT(load_type)) + BATT_CHARGE_CURRENT_COMPENSATION
        self.print_console("CH :" + str(channel_number) + " DUT HIGH: " + str(DUT_READ_CURRENT_HIGH))
        self.print_console("CH :" + str(channel_number) + " METER HIGH: " + str(METER_READ_CURRENT_HIGH))
        self.dcload.DC_LOAD_SET_CURRENT_CC(SET_CURRENT_LOW, str(load_type))

        try:
            SLOPE = ((DUT_READ_CURRENT_HIGH - DUT_READ_CURRENT_LOW) / (
                    METER_READ_CURRENT_HIGH - METER_READ_CURRENT_LOW)) * (
                            float(NUMBER_OF_BITS) / (channel_hall_effect_value * FACTOR))
            self.print_console("CH :" + str(channel_number) + " SLOPE: " + str(SLOPE))
            Z_OFFSET = ((DUT_READ_CURRENT_HIGH * NUMBER_OF_BITS) / (
                    channel_hall_effect_value * FACTOR)) - SLOPE * METER_READ_CURRENT_HIGH
            self.print_console("CH :" + str(channel_number) + " Z_OFFSET: " + str(Z_OFFSET))
            GAIN_OFFSET = (FACTOR * channel_hall_effect_value * (((METER_READ_CURRENT_HIGH - METER_READ_CURRENT_LOW) / (
                    DUT_READ_CURRENT_HIGH - DUT_READ_CURRENT_LOW)) - 1)) / 1
            GAIN_OFFSET = round(GAIN_OFFSET, 0)
            self.print_console("CH :" + str(channel_number) + " GAIN OFFSET: " + str(GAIN_OFFSET))
            ZERO_OFFSET = -1 * ADC_MULTIPLIER * Z_OFFSET / SLOPE
            ZERO_OFFSET = round(ZERO_OFFSET, 0)
            self.print_console("CH :" + str(channel_number) + " ZERO OFFSET: " + str(ZERO_OFFSET))
        except:
            SLOPE = 0
            Z_OFFSET = 0
            GAIN_OFFSET = 0
            ZERO_OFFSET = 0
            self.print_console("EXCEPTION OCCURRED.TEST FAILED.CALIBRATION WILL BE DONE AGAIN", "RED")
            self.print_console("CH :" + str(channel_number) + " SLOPE: " + str(SLOPE))
            self.print_console("CH :" + str(channel_number) + " Z_OFFSET: " + str(Z_OFFSET))
            self.print_console("CH :" + str(channel_number) + " GAIN OFFSET: " + str(GAIN_OFFSET))
            self.print_console("CH :" + str(channel_number) + " ZERO OFFSET: " + str(ZERO_OFFSET))

        CALIBRATION_NOT_DONE = True
        cal_try_count = 0
        while CALIBRATION_NOT_DONE and cal_try_count < 5:
            cal_try_count = cal_try_count + 1
            self.MCM_WRITE_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' gain', GAIN_OFFSET)
            # time.sleep(2)
            self.MCM_WRITE_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' offset',
                                   ZERO_OFFSET)
            # time.sleep(2)
            self.MCM_WRITE_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' deadband',
                                   DEADBAND)
            # time.sleep(2)
            if (float(self.MCM_READ_COMMAND('CALIBRATE CURRENT', "channel" + str(channel_number) + " gain")) != GAIN_OFFSET) \
                    or (float(
                self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' offset')) != ZERO_OFFSET) \
                    or (self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' deadband') != str(
                DEADBAND)):
                CALIBRATION_NOT_DONE = True
            else:
                CALIBRATION_NOT_DONE = False

        #     TELNET_SET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' gain'],GAIN_OFFSET)
        #     time.sleep(1)
        #     TELNET_SET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' offset'],ZERO_OFFSET)
        #     time.sleep(1)
        #     TELNET_SET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' deadband'],DEADBAND)
        #     time.sleep(1)
        self.print_console("PROGRAMMED CURRENT CHANNEL " + str(channel_number) + " GAIN: " + str(
            self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' gain')))
        self.print_console("PROGRAMMED CURRENT CHANNEL " + str(channel_number) + " OFFSET: " + str(
            self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' offset')))
        self.print_console("PROGRAMMED CURRENT CHANNEL " + str(channel_number) + " DEADBAND: " + str(
            self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' deadband')))

        ## verify current calibration
        self.dcload.DC_LOAD_SET_CURRENT_CC(VERIFY_CURRENT_LOW, load_type)
        time.sleep(3)
        DUT__VERIFY_READ_CURRENT_LOW = float(
            self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number))) / 10
        METER__VERIFY_READ_CURRENT_LOW = float(READ_DC_CURRENT(load_type)) + BATT_CHARGE_CURRENT_COMPENSATION
        RESULT_TEMP = (abs(DUT__VERIFY_READ_CURRENT_LOW - METER__VERIFY_READ_CURRENT_LOW) < CURRENT_TOLERANCE and (
                abs(METER__VERIFY_READ_CURRENT_LOW - VERIFY_CURRENT_LOW) < 3))
        if RESULT_TEMP == False:
            COLOR_STATUS = "RED"
        else:
            COLOR_STATUS = 'BLUE'

        self.print_console("CH :" + str(channel_number) + " CURRENT_TOLERANCE: " + str(CURRENT_TOLERANCE), COLOR_STATUS)
        self.print_console(
            "CH :" + str(channel_number) + " METER__VERIFY_READ_CURRENT_LOW: " + str(METER__VERIFY_READ_CURRENT_LOW),
            COLOR_STATUS)
        self.print_console(
            "CH :" + str(channel_number) + " DUT__VERIFY_READ_CURRENT_LOW: " + str(DUT__VERIFY_READ_CURRENT_LOW),
            COLOR_STATUS)
        RESULT.append(RESULT_TEMP)

        self.dcload.DC_LOAD_SET_CURRENT_CC(VERIFY_CURRENT_MID, str(load_type))
        time.sleep(3)
        DUT__VERIFY_READ_CURRENT_MID = float(
            self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number))) / 10
        METER__VERIFY_READ_CURRENT_MID = float(READ_DC_CURRENT(load_type)) + BATT_CHARGE_CURRENT_COMPENSATION
        RESULT_TEMP = (abs(DUT__VERIFY_READ_CURRENT_MID - METER__VERIFY_READ_CURRENT_MID) < CURRENT_TOLERANCE and (
                abs(METER__VERIFY_READ_CURRENT_MID - VERIFY_CURRENT_MID) < 3))
        if RESULT_TEMP == False:
            COLOR_STATUS = "RED"
        else:
            COLOR_STATUS = 'BLUE'
        self.print_console("CH :" + str(channel_number) + " CURRENT_TOLERANCE: " + str(CURRENT_TOLERANCE), COLOR_STATUS)
        self.print_console("CH :" + str(channel_number) + " METER__VERIFY_READ_CURRENT_MID: " + str(
            METER__VERIFY_READ_CURRENT_MID), COLOR_STATUS)
        self.print_console(
            "CH :" + str(channel_number) + " DUT__VERIFY_READ_CURRENT_MID: " + str(DUT__VERIFY_READ_CURRENT_MID),
            COLOR_STATUS)
        RESULT.append(RESULT_TEMP)

        self.dcload.DC_LOAD_SET_CURRENT_CC(VERIFY_CURRENT_HIGH, load_type)
        time.sleep(3)
        DUT__VERIFY_READ_CURRENT_HIGH = float(
            self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number))) / 10
        METER__VERIFY_READ_CURRENT_HIGH = float(READ_DC_CURRENT(load_type)) + BATT_CHARGE_CURRENT_COMPENSATION
        RESULT_TEMP = (abs(DUT__VERIFY_READ_CURRENT_HIGH - METER__VERIFY_READ_CURRENT_HIGH) < CURRENT_TOLERANCE and (
                abs(METER__VERIFY_READ_CURRENT_HIGH - VERIFY_CURRENT_HIGH) < 3))
        if RESULT_TEMP == False:
            COLOR_STATUS = "RED"
        else:
            COLOR_STATUS = 'BLUE'
        self.print_console("CH :" + str(channel_number) + " CURRENT_TOLERANCE: " + str(CURRENT_TOLERANCE), COLOR_STATUS)
        self.print_console(
            "CH :" + str(channel_number) + " METER__VERIFY_READ_CURRENT_HIGH: " + str(METER__VERIFY_READ_CURRENT_HIGH),
            COLOR_STATUS)
        self.print_console(
            "CH :" + str(channel_number) + " DUT__VERIFY_READ_CURRENT_HIGH: " + str(DUT__VERIFY_READ_CURRENT_HIGH),
            COLOR_STATUS)
        RESULT.append(RESULT_TEMP)
        # PRINT_CONSOLE(self,"RESULT: "+str(RESULT))
        self.dcload.DC_LOAD_SET_CURRENT_CC(10, "LOAD")
        self.dcload.DC_LOAD_SET_CURRENT_CC(10, "BATT")
        return CALCULATE_RESULT(RESULT)
    except exception as e:
        print(str(e))


def CALIBRATE_CURRENT_PATH_SHUNT(self, channel_number, load_type):
    try:
        global check_shunt_value
        if self.mcm_type == 1:
            self.MCM_READ_COMMAND('SYSTEM COMMANDS', 'ate test', 'TEST_M1000_ATE')
        RESULT = []
        self.smrcan.SMR_BATTERY_SET_VOLTAGE(53.5)
        if (self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' gain') != '0') or (
                self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(
                    channel_number) + ' offset') != '0'):  # or (TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' deadband'])!='0'):
            self.print_console("Resetting offset and gain again")
            self.MCM_WRITE_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' deadband', 0)
            # time.sleep(2)
            self.MCM_WRITE_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' gain', 0)
            # time.sleep(2)
            self.MCM_WRITE_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' offset', 0)
            # time.sleep(2)
            self.print_console("CURRENT CHANNEL " + str(channel_number) + " GAIN: " + str(
                self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' gain')))
            self.print_console("CURRENT CHANNEL " + str(channel_number) + " OFFSET: " + str(
                self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' offset')))
            # PRINT_CONSOLE(self,"CURRENT CHANNEL "+str(channel_number)+" DEADBAND: "+str(TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' deadband'])))

        channel_shunt_value = int(ConfigRead('DUT CONFIGURATION')['channel' + str(channel_number) + ' shunt value'])
        print("channel shunt value: " + str(channel_shunt_value))
        # SET_CURRENT_LOW=int(CalibrateSetting('SHUNT')['current low'])
        # SET_CURRENT_HIGH=int(CalibrateSetting('SHUNT')['current high'])
        NUMBER_OF_BITS = int(CalibrateSetting('SHUNT')['number of bits'])
        FACTOR = float(CalibrateSetting('SHUNT')['factor'])
        ADC_MULTIPLIER = int(CalibrateSetting('SHUNT')['adc multiplier'])
        DEADBAND_PERCENTAGE = float(CalibrateSetting('SHUNT')['deadband percentage'])
        DEADBAND = int(channel_shunt_value * DEADBAND_PERCENTAGE) / 100
        CURRENT_TOLERANCE_PERCENTAGE = float(CalibrateSetting('SHUNT')['current tolerance percentage'])
        CURRENT_TOLERANCE = float(channel_shunt_value * CURRENT_TOLERANCE_PERCENTAGE) / 100
        NEGATIVE_CURRENT_CAL = str(CalibrateSetting('SHUNT')['negative current cal'])

        if channel_shunt_value <= 50:
            check_shunt_value = 50
        elif 100 >= channel_shunt_value > 50:
            check_shunt_value = 100
        elif 200 >= channel_shunt_value > 100:
            check_shunt_value = 200
        elif 400 >= channel_shunt_value > 200:
            check_shunt_value = 400
        elif 600 >= channel_shunt_value > 400:
            check_shunt_value = 600
        elif 800 >= channel_shunt_value > 600:
            check_shunt_value = 800
        elif 1000 >= channel_shunt_value > 800:
            check_shunt_value = 1000
        elif 1200 >= channel_shunt_value > 1000:
            check_shunt_value = 1200
        elif 2100 >= channel_shunt_value > 1900:
            check_shunt_value = 2100

        SET_CURRENT_LOW = int(CalibrateSetting('SHUNT')['current low upto ' + str(check_shunt_value)])
        SET_CURRENT_HIGH = int(CalibrateSetting('SHUNT')['current high upto ' + str(check_shunt_value)])
        VERIFY_CURRENT_LOW = int(CalibrateSetting('SHUNT')['verify current low upto ' + str(check_shunt_value)])
        VERIFY_CURRENT_MID = int(CalibrateSetting('SHUNT')['verify current mid upto ' + str(check_shunt_value)])
        VERIFY_CURRENT_HIGH = int(CalibrateSetting('SHUNT')['verify current high upto ' + str(check_shunt_value)])
        NEGATIVE_SET_CURRENT_LOW = int(CalibrateSetting('SHUNT')['negative current low upto ' + str(check_shunt_value)])

        if load_type == 'BATT' and NEGATIVE_CURRENT_CAL == 'YES':
            ATE_LOAD_COUNT = int(SettingRead("SETTING")['ate load count'])
            if ATE_LOAD_COUNT == 1:  # ADDED FOR SINGLE LOAD CONFIGURATION, KUSHAGRA MITTAL 06/09/2016
                # self.pfc.pfc_set(0, 'DC LOAD', 0)
                self.pfc.pfc_set(0, 'load_mains', 1)
                # time.sleep(1)

            self.MCM_WRITE_COMMAND('BATTERY SETTING', 'float voltage', 51)
            self.MCM_WRITE_COMMAND('BATTERY SETTING', 'charge voltage', 51.5)
            self.MCM_WRITE_COMMAND('BATTERY SETTING', 'lion charge voltage', 51)
            # SET_JIG_PFC_OP(self.can,'AC',0)

            self.dcload.DC_LOAD_SET_CURRENT_CC(NEGATIVE_SET_CURRENT_LOW, "LOAD")
            time.sleep(2)

            METER_READ_CURRENT_LOW = float(READ_DC_CURRENT("LOAD"))
            METER_READ_CURRENT_LOW = (-1 * METER_READ_CURRENT_LOW) - float(
                CalibrateSetting('SHUNT')['batt discharge compensation'])
        else:
            ATE_LOAD_COUNT = int(SettingRead("SETTING")['ate load count'])
            if ATE_LOAD_COUNT == 1 and load_type == 'BATT':
                self.print_console("RESETTING FOR BATTERY PATH")
                # ADDED FOR SINGLE LOAD CONFIGURATION, KUSHAGRA MITTAL 06/09/2016
                # self.pfc.pfc_set(0, 'LOAD COMMON', 0)
                self.pfc.pfc_set(0, 'load_mains', 1)
                # time.sleep(1)
            self.dcload.DC_LOAD_SET_CURRENT_CC(SET_CURRENT_LOW, load_type)
            time.sleep(2)
            METER_READ_CURRENT_LOW = float(READ_DC_CURRENT(load_type))

        DUT_READ_CURRENT_LOW = float(self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number)))
        BATT_CHARGE_CURRENT_COMPENSATION = 0
        self.print_console("CH :" + str(channel_number) + " DUT LOW: " + str(DUT_READ_CURRENT_LOW))
        self.print_console("CH :" + str(channel_number) + " METER LOW: " + str(METER_READ_CURRENT_LOW))
        if load_type == 'BATT' and NEGATIVE_CURRENT_CAL == 'YES':
            self.dcload.DC_LOAD_SET_CURRENT_CC(5, "LOAD")
            self.dcload.DC_LOAD_SET_CURRENT_CC(5, "BATT")
            ATE_LOAD_COUNT = int(SettingRead("SETTING")['ate load count'])
            if ATE_LOAD_COUNT == 1:  # ADDED FOR SINGLE LOAD CONFIGURATION, KUSHAGRA MITTAL 06/09/2016
                # self.pfc.pfc_set(0, 'LOAD COMMON', 0)
                self.pfc.pfc_set(0, 'load_mains', 1)
                # time.sleep(1)

            self.MCM_WRITE_COMMAND('BATTERY SETTING', 'charge voltage', 55.2)
            self.MCM_WRITE_COMMAND('BATTERY SETTING', 'float voltage', 54)
            self.MCM_WRITE_COMMAND('BATTERY SETTING', 'lion charge voltage', 54)

            time.sleep(3)
            self.smrcan.SMR_BATTERY_SET_VOLTAGE(47.0)

            # SET_JIG_PFC_OP(self.can,'AC',1)
            BATT_CHARGE_CURRENT_COMPENSATION = float(CalibrateSetting('SHUNT')['batt charge compensation'])
            # time.sleep(2)
        # time.sleep(5)
        ATE_LOAD_COUNT = int(SettingRead("SETTING")['ate load count'])
        if ATE_LOAD_COUNT == 1:  # ADDED FOR SINGLE LOAD CONFIGURATION, KUSHAGRA MITTAL 06/09/2016
            load_type = "LOAD"

        self.dcload.DC_LOAD_SET_CURRENT_CC(SET_CURRENT_HIGH, load_type)

        time.sleep(4)
        DUT_READ_CURRENT_HIGH = float(self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number)))
        METER_READ_CURRENT_HIGH = float(READ_DC_CURRENT(load_type)) + BATT_CHARGE_CURRENT_COMPENSATION
        self.print_console("CH :" + str(channel_number) + " DUT HIGH: " + str(DUT_READ_CURRENT_HIGH))
        self.print_console("CH :" + str(channel_number) + " METER HIGH: " + str(METER_READ_CURRENT_HIGH))
        self.dcload.DC_LOAD_SET_CURRENT_CC(SET_CURRENT_LOW, load_type)

        try:
            SLOPE = ((DUT_READ_CURRENT_HIGH - DUT_READ_CURRENT_LOW) / (
                    METER_READ_CURRENT_HIGH - METER_READ_CURRENT_LOW)) * (
                            float(NUMBER_OF_BITS) / (channel_shunt_value * FACTOR))
            self.print_console("CH :" + str(channel_number) + " SLOPE: " + str(SLOPE))
            Z_OFFSET = ((DUT_READ_CURRENT_HIGH * NUMBER_OF_BITS) / (
                    channel_shunt_value * FACTOR)) - SLOPE * METER_READ_CURRENT_HIGH
            self.print_console("CH :" + str(channel_number) + " Z_OFFSET: " + str(Z_OFFSET))
            GAIN_OFFSET = (FACTOR * channel_shunt_value * (((METER_READ_CURRENT_HIGH - METER_READ_CURRENT_LOW) / (
                    DUT_READ_CURRENT_HIGH - DUT_READ_CURRENT_LOW)) - 1)) / 1
            GAIN_OFFSET = round(GAIN_OFFSET, 0)
            self.print_console("CH :" + str(channel_number) + " GAIN OFFSET: " + str(GAIN_OFFSET))
            ZERO_OFFSET = -1 * ADC_MULTIPLIER * Z_OFFSET / SLOPE
            ZERO_OFFSET = round(ZERO_OFFSET, 0)
            self.print_console("CH :" + str(channel_number) + " ZERO OFFSET: " + str(ZERO_OFFSET))
        except:
            SLOPE = 0
            Z_OFFSET = 0
            GAIN_OFFSET = 0
            ZERO_OFFSET = 0
            self.print_console("EXCEPTION OCCURRED.TEST FAILED.CALIBRATION WILL BE DONE AGAIN")
            self.print_console("CH :" + str(channel_number) + " SLOPE: " + str(SLOPE))
            self.print_console("CH :" + str(channel_number) + " Z_OFFSET: " + str(Z_OFFSET))
            self.print_console("CH :" + str(channel_number) + " GAIN OFFSET: " + str(GAIN_OFFSET))
            self.print_console("CH :" + str(channel_number) + " ZERO OFFSET: " + str(ZERO_OFFSET))

        CALIBRATION_NOT_DONE = True
        cal_try_count = 0
        while CALIBRATION_NOT_DONE and cal_try_count < 5:
            cal_try_count = cal_try_count + 1
            self.MCM_WRITE_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' gain', GAIN_OFFSET)
            # time.sleep(2)
            self.MCM_WRITE_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' offset', ZERO_OFFSET)
            # time.sleep(2)
            self.MCM_WRITE_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' deadband', DEADBAND)
            # time.sleep(2)
            if (float(self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' gain')) != GAIN_OFFSET) \
                    or (float(
                self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' offset')) != ZERO_OFFSET) \
                    or (self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' deadband') != str(
                DEADBAND)):
                CALIBRATION_NOT_DONE = True
            else:
                CALIBRATION_NOT_DONE = False

        #     TELNET_SET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' gain'],GAIN_OFFSET)
        #     time.sleep(1)
        #     TELNET_SET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' offset'],ZERO_OFFSET)
        #     time.sleep(1)
        #     TELNET_SET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' deadband'],DEADBAND)
        #     time.sleep(1)
        self.print_console("PROGRAMMED CURRENT CHANNEL " + str(channel_number) + " GAIN: " + str(
            self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' gain')))
        self.print_console("PROGRAMMED CURRENT CHANNEL " + str(channel_number) + " OFFSET: " + str(
            self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' offset')))
        self.print_console("PROGRAMMED CURRENT CHANNEL " + str(channel_number) + " DEADBAND: " + str(
            self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' deadband')))

        ## verify current calibration
        self.dcload.DC_LOAD_SET_CURRENT_CC(VERIFY_CURRENT_LOW, load_type)
        time.sleep(1)
        DUT__VERIFY_READ_CURRENT_LOW = float(self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number)))
        METER__VERIFY_READ_CURRENT_LOW = float(READ_DC_CURRENT(load_type)) + BATT_CHARGE_CURRENT_COMPENSATION
        RESULT_TEMP = (abs(DUT__VERIFY_READ_CURRENT_LOW - METER__VERIFY_READ_CURRENT_LOW) < CURRENT_TOLERANCE and (
                abs(METER__VERIFY_READ_CURRENT_LOW - VERIFY_CURRENT_LOW) < 3))
        if RESULT_TEMP == False:
            COLOR_STATUS = "RED"
        else:
            COLOR_STATUS = 'BLUE'
        self.print_console("CH :" + str(channel_number) + " CURRENT_TOLERANCE: " + str(CURRENT_TOLERANCE), COLOR_STATUS)
        self.print_console("CH :" + str(channel_number) + " METER__VERIFY_READ_CURRENT_LOW: " + str(
            METER__VERIFY_READ_CURRENT_LOW), COLOR_STATUS)
        self.print_console(
            "CH :" + str(channel_number) + " DUT__VERIFY_READ_CURRENT_LOW: " + str(DUT__VERIFY_READ_CURRENT_LOW),
            COLOR_STATUS)
        RESULT.append(RESULT_TEMP)

        self.dcload.DC_LOAD_SET_CURRENT_CC(VERIFY_CURRENT_MID, load_type)
        time.sleep(1)
        DUT__VERIFY_READ_CURRENT_MID = float(self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number)))
        METER__VERIFY_READ_CURRENT_MID = float(READ_DC_CURRENT(load_type)) + BATT_CHARGE_CURRENT_COMPENSATION
        RESULT_TEMP = (abs(DUT__VERIFY_READ_CURRENT_MID - METER__VERIFY_READ_CURRENT_MID) < CURRENT_TOLERANCE and (
                abs(METER__VERIFY_READ_CURRENT_MID - VERIFY_CURRENT_MID) < 3))
        if RESULT_TEMP == False:
            COLOR_STATUS = "RED"
        else:
            COLOR_STATUS = 'BLUE'
        self.print_console("CH :" + str(channel_number) + " CURRENT_TOLERANCE: " + str(CURRENT_TOLERANCE), COLOR_STATUS)
        self.print_console(
            "CH :" + str(channel_number) + " METER__VERIFY_READ_CURRENT_MID: " + str(METER__VERIFY_READ_CURRENT_MID),
            COLOR_STATUS)
        self.print_console(
            "CH :" + str(channel_number) + " DUT__VERIFY_READ_CURRENT_MID: " + str(DUT__VERIFY_READ_CURRENT_MID),
            COLOR_STATUS)
        RESULT.append(RESULT_TEMP)

        self.dcload.DC_LOAD_SET_CURRENT_CC(VERIFY_CURRENT_HIGH, load_type)
        time.sleep(1)
        DUT__VERIFY_READ_CURRENT_HIGH = float(self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number)))
        METER__VERIFY_READ_CURRENT_HIGH = float(READ_DC_CURRENT(load_type)) + BATT_CHARGE_CURRENT_COMPENSATION
        RESULT_TEMP = (abs(DUT__VERIFY_READ_CURRENT_HIGH - METER__VERIFY_READ_CURRENT_HIGH) < CURRENT_TOLERANCE and (
                abs(METER__VERIFY_READ_CURRENT_HIGH - VERIFY_CURRENT_HIGH) < 3))
        if RESULT_TEMP == False:
            COLOR_STATUS = "RED"
        else:
            COLOR_STATUS = 'BLUE'
        self.print_console("CH :" + str(channel_number) + " CURRENT_TOLERANCE: " + str(CURRENT_TOLERANCE), COLOR_STATUS)
        self.print_console("CH :" + str(channel_number) + " METER__VERIFY_READ_CURRENT_HIGH: " + str(
            METER__VERIFY_READ_CURRENT_HIGH), COLOR_STATUS)
        self.print_console("CH :" + str(channel_number) + " DUT__VERIFY_READ_CURRENT_HIGH: " + str(
            DUT__VERIFY_READ_CURRENT_HIGH), COLOR_STATUS)
        RESULT.append(RESULT_TEMP)
        # PRINT_CONSOLE(self,"RESULT: "+str(RESULT))
        self.dcload.DC_LOAD_SET_CURRENT_CC(10, "LOAD")
        self.dcload.DC_LOAD_SET_CURRENT_CC(10, "BATT")
        return CALCULATE_RESULT(RESULT)
    except exception as e:
        print(str(e))


def CALIBRATE_CURRENT_PATH_SHUNT_SMALL(self, channel_number, load_type):
    try:
        global check_shunt_value
        if self.mcm_type == 1:
            self.MCM_WRITE_COMMAND('SYSTEM COMMANDS', 'ate test', "TEST_M1000_ATE")
        RESULT = []
        self.smrcan.SMR_BATTERY_SET_VOLTAGE(48.5)
        dcif_type_number = int(ConfigRead('DUT CONFIGURATION')['dcif card type number'])
        load_current_count = int(ConfigRead('DUT CONFIGURATION')['no. of load current'])
        #     if (TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' gain'])!='0') or (TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' offset'])!='0'):# or (TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' deadband'])!='0'):
        #         PRINT_CONSOLE(self,"Resetting offset and gain again")
        #         TELNET_SET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' deadband'],0)
        #         time.sleep(2)
        #         TELNET_SET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' gain'],0)
        #         time.sleep(2)
        #         TELNET_SET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' offset'],0)
        #         time.sleep(2)
        #         PRINT_CONSOLE(self,"CURRENT CHANNEL "+str(channel_number)+" GAIN: "+str(TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' gain'])))
        #         PRINT_CONSOLE(self,"CURRENT CHANNEL "+str(channel_number)+" OFFSET: "+str(TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' offset'])))
        #         #PRINT_CONSOLE(self,"CURRENT CHANNEL "+str(channel_number)+" DEADBAND: "+str(TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' deadband'])))
        #
        #
        channel_shunt_value = int(ConfigRead('DUT CONFIGURATION')['channel' + str(channel_number) + ' shunt value'])
        # print
        # "channel shunt value: " + str(channel_shunt_value)

        #     NUMBER_OF_BITS=int(CalibrateSetting('SHUNT')['number of bits'])
        #     FACTOR=float(CalibrateSetting('SHUNT')['factor'])
        #     ADC_MULTIPLIER=int(CalibrateSetting('SHUNT')['adc multiplier'])
        DEADBAND_PERCENTAGE = float(CalibrateSetting('SHUNT')['deadband percentage'])
        DEADBAND = (int(channel_shunt_value * DEADBAND_PERCENTAGE) / 100) * 10
        CURRENT_TOLERANCE_PERCENTAGE = float(CalibrateSetting('SHUNT')['current tolerance percentage'])
        CURRENT_TOLERANCE = float(channel_shunt_value * CURRENT_TOLERANCE_PERCENTAGE) / 100
        NEGATIVE_CURRENT_CAL = str(CalibrateSetting('SHUNT')['negative current cal'])

        if channel_shunt_value <= 50:
            check_shunt_value = 50
        elif 100 >= channel_shunt_value > 50:
            check_shunt_value = 100
        elif 200 >= channel_shunt_value > 100:
            check_shunt_value = 200
        elif 400 >= channel_shunt_value > 200:
            check_shunt_value = 400
        elif 600 >= channel_shunt_value > 400:
            check_shunt_value = 600
        elif 800 >= channel_shunt_value > 600:
            check_shunt_value = 800
        elif 1000 >= channel_shunt_value > 800:
            check_shunt_value = 1000
        elif 1200 >= channel_shunt_value > 1000:
            check_shunt_value = 1200
        elif 2100 >= channel_shunt_value > 1900:
            check_shunt_value = 2100

        # print
        # "check_shunt_value: " + str(check_shunt_value)
        SET_CURRENT_LOW = int(CalibrateSetting('SHUNT')['current low upto ' + str(check_shunt_value)])
        SET_CURRENT_HIGH = int(CalibrateSetting('SHUNT')['current high upto ' + str(check_shunt_value)])
        VERIFY_CURRENT_LOW = int(CalibrateSetting('SHUNT')['verify current low upto ' + str(check_shunt_value)])
        VERIFY_CURRENT_MID = int(CalibrateSetting('SHUNT')['verify current mid upto ' + str(check_shunt_value)])
        VERIFY_CURRENT_HIGH = int(CalibrateSetting('SHUNT')['verify current high upto ' + str(check_shunt_value)])
        if str(self.part_number) == "he518713":
            VERIFY_CURRENT_HIGH = 75
        NEGATIVE_SET_CURRENT_LOW = int(CalibrateSetting('SHUNT')['negative current low upto ' + str(check_shunt_value)])
        #
        #
        #     if load_type=='BATT' and NEGATIVE_CURRENT_CAL=='YES':
        #         if ATE_LOAD_COUNT==1: # ADDED FOR SINGLE LOAD CONFIGURATION, KUSHAGRA MITTAL 06/09/2016
        #             SET_JIG_PFC_OP(self.can,'DC LOAD',0)
        #             SET_JIG_PFC_OP(self.can,'LOAD COMMON',1)
        #             time.sleep(3)
        #
        #         TELNET_SET_COMMAND(self.telnet,OIDRead('BATTERY SETTING')['float voltage'],51)
        #         TELNET_SET_COMMAND(self.telnet,OIDRead('BATTERY SETTING')['charge voltage'],51.5)
        #         TELNET_SET_COMMAND(self.telnet,OIDRead('BATTERY SETTING')['lion charge voltage'],51)
        #         #SET_JIG_PFC_OP(self.can,'AC',0)
        #
        #         DC_LOAD_SET_CURRENT_CC(self.dcload,NEGATIVE_SET_CURRENT_LOW,LOAD)
        #         time.sleep(4)
        #
        #         METER_READ_CURRENT_LOW=float(READ_DC_CURRENT(self,LOAD))
        #         METER_READ_CURRENT_LOW=(-1*METER_READ_CURRENT_LOW)-float(CalibrateSetting('SHUNT')['batt discharge compensation'])
        #     else:
        #         DC_LOAD_SET_CURRENT_CC(self.dcload,SET_CURRENT_LOW,load_type)
        #         time.sleep(4)
        #         METER_READ_CURRENT_LOW=float(READ_DC_CURRENT(self,load_type))
        #
        #     DUT_READ_CURRENT_LOW=float(TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)]))
        #     BATT_CHARGE_CURRENT_COMPENSATION=0
        #     PRINT_CONSOLE(self,"CH :"+str(channel_number)+" DUT LOW: "+str(DUT_READ_CURRENT_LOW))
        #     PRINT_CONSOLE(self,"CH :"+str(channel_number)+" METER LOW: "+str(METER_READ_CURRENT_LOW))
        #     if load_type=='BATT' and NEGATIVE_CURRENT_CAL=='YES':
        #         DC_LOAD_SET_CURRENT_CC(self.dcload,5,LOAD)
        #         DC_LOAD_SET_CURRENT_CC(self.dcload,5,BATT)
        test_load_type = 'LOAD'
        ATE_LOAD_COUNT = int(SettingRead("SETTING")['ate load count'])
        if ATE_LOAD_COUNT == 1 and load_type == 'BATT':
            self.print_console("RESETTING FOR BATTERY PATH")
            # ADDED FOR SINGLE LOAD CONFIGURATION, KUSHAGRA MITTAL 06/09/2016
            start_time = time.perf_counter()
            self.pfc.pfc_set(0, 'load_mains', 0)
            end_time = time.perf_counter()
            print("time to complete above operation", end_time - start_time)
            self.pfc.pfc_set(0, 'bus', 1)
            self.pfc.pfc_set(0, "battery_mains", 1)
            time.sleep(1)
            test_load_type = 'BATT'
        #
        #         TELNET_SET_COMMAND(self.telnet,OIDRead('BATTERY SETTING')['charge voltage'],55.2)
        #         TELNET_SET_COMMAND(self.telnet,OIDRead('BATTERY SETTING')['float voltage'],54)
        #         TELNET_SET_COMMAND(self.telnet,OIDRead('BATTERY SETTING')['lion charge voltage'],54)
        #
        #         time.sleep(10)
        #         SMR_BATTERY_SET_VOLTAGE(self.can,47.0)
        #
        #         #SET_JIG_PFC_OP(self.can,'AC',1)
        # BATT_CHARGE_CURRENT_COMPENSATION=float(CalibrateSetting('SHUNT')['batt charge compensation'])
        #         #time.sleep(2)
        #     #time.sleep(5)
        #
        ATE_LOAD_COUNT = int(SettingRead("SETTING")['ate load count'])
        if ATE_LOAD_COUNT == 1:  # ADDED FOR SINGLE LOAD CONFIGURATION, KUSHAGRA MITTAL 06/09/2016
            load_type = "LOAD"
        #
        #     DC_LOAD_SET_CURRENT_CC(self.dcload,SET_CURRENT_HIGH,load_type)
        #
        #     time.sleep(4)
        #     DUT_READ_CURRENT_HIGH=float(TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)]))
        #     METER_READ_CURRENT_HIGH=float(READ_DC_CURRENT(self,load_type))+BATT_CHARGE_CURRENT_COMPENSATION
        #     PRINT_CONSOLE(self,"CH :"+str(channel_number)+" DUT HIGH: "+str(DUT_READ_CURRENT_HIGH))
        #     PRINT_CONSOLE(self,"CH :"+str(channel_number)+" METER HIGH: "+str(METER_READ_CURRENT_HIGH))
        #     DC_LOAD_SET_CURRENT_CC(self.dcload,SET_CURRENT_LOW,load_type)
        #
        #     try:
        #         #SLOPE=((DUT_READ_CURRENT_HIGH-DUT_READ_CURRENT_LOW)/(METER_READ_CURRENT_HIGH-METER_READ_CURRENT_LOW))*(float(NUMBER_OF_BITS)/(channel_shunt_value*FACTOR))
        #         PRINT_CONSOLE(self,"CH :"+str(channel_number)+" SLOPE: "+str(SLOPE))
        #         #Z_OFFSET=((DUT_READ_CURRENT_HIGH*NUMBER_OF_BITS)/(channel_shunt_value*FACTOR))-SLOPE*METER_READ_CURRENT_HIGH
        #         PRINT_CONSOLE(self,"CH :"+str(channel_number)+" Z_OFFSET: "+str(Z_OFFSET))
        #         GAIN_OFFSET=(METER_READ_CURRENT_HIGH-METER_READ_CURRENT_LOW)/(DUT_READ_CURRENT_HIGH-DUT_READ_CURRENT_LOW)
        #         CAL_GAIN_OFFSET=int((GAIN_OFFSET-1)*1000)
        #         PRINT_CONSOLE(self,"CH :"+str(channel_number)+" CAL_GAIN_OFFSET: "+str(CAL_GAIN_OFFSET))
        #         ZERO_OFFSET=DUT_READ_CURRENT_LOW-(DUT_READ_CURRENT_LOW *(METER_READ_CURRENT_HIGH-METER_READ_CURRENT_LOW)/(DUT_READ_CURRENT_HIGH-DUT_READ_CURRENT_LOW) )
        #         CAL_ZERO_OFFSET=int(ZERO_OFFSET*100)
        #         PRINT_CONSOLE(self,"CH :"+str(channel_number)+" CAL_ZERO_OFFSET: "+str(CAL_ZERO_OFFSET))
        #     except:
        #         GAIN_OFFSET=0
        #         ZERO_OFFSET=0
        #         CAL_GAIN_OFFSET=0
        #         CAL_ZERO_OFFSET=0
        #

        #         PRINT_CONSOLE(self,"EXCEPTION OCCURRED.TEST FAILED.CALIBRATION WILL BE DONE AGAIN")
        #         PRINT_CONSOLE(self,"CH :"+str(channel_number)+" GAIN_OFFSET: "+str(GAIN_OFFSET))
        #         PRINT_CONSOLE(self,"CH :"+str(channel_number)+" ZERO_OFFSET: "+str(ZERO_OFFSET))
        #         PRINT_CONSOLE(self,"CH :"+str(channel_number)+" CAL_GAIN_OFFSET: "+str(CAL_GAIN_OFFSET))
        #         PRINT_CONSOLE(self,"CH :"+str(channel_number)+" CAL_ZERO_OFFSET: "+str(CAL_ZERO_OFFSET))
        #
        CALIBRATION_NOT_DONE = True
        cal_try_count = 0
        while CALIBRATION_NOT_DONE and cal_try_count < 5:
            cal_try_count = cal_try_count + 1
            #         TELNET_SET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' gain'],GAIN_OFFSET)
            #         time.sleep(2)
            #         TELNET_SET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' offset'],ZERO_OFFSET)
            #         time.sleep(2)
            self.MCM_WRITE_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' deadband', DEADBAND)
            # time.sleep(2)
            # if (float(TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' gain']))!=GAIN_OFFSET) or (float(TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' offset']))!=ZERO_OFFSET) or (TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' deadband'])!=str(DEADBAND)):
            if self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' deadband') != str(DEADBAND):
                CALIBRATION_NOT_DONE = True
            else:
                CALIBRATION_NOT_DONE = False

        #     TELNET_SET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' gain'],GAIN_OFFSET)
        #     time.sleep(1)
        #     TELNET_SET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' offset'],ZERO_OFFSET)
        #     time.sleep(1)
        #     TELNET_SET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' deadband'],DEADBAND)
        #     time.sleep(1)
        # PRINT_CONSOLE(self,"PROGRAMMED CURRENT CHANNEL "+str(channel_number)+" GAIN: "+str(TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' gain'])))
        # PRINT_CONSOLE(self,"PROGRAMMED CURRENT CHANNEL "+str(channel_number)+" OFFSET: "+str(TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)+' offset'])))
        self.print_console("PROGRAMMED CURRENT CHANNEL " + str(channel_number) + " DEADBAND: " + str(
            self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number) + ' deadband')))
        ## verify current calibration
        #     DC_LOAD_SET_CURRENT_CC(self.dcload,VERIFY_CURRENT_LOW,load_type)
        #     time.sleep(6)
        #     DUT__VERIFY_READ_CURRENT_LOW=float(TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)]))/10
        #     METER__VERIFY_READ_CURRENT_LOW=float(READ_DC_CURRENT(self,load_type))#+BATT_CHARGE_CURRENT_COMPENSATION
        #     RESULT_TEMP=COMPARE(DUT__VERIFY_READ_CURRENT_LOW, METER__VERIFY_READ_CURRENT_LOW,CURRENT_TOLERANCE )
        #     if RESULT_TEMP==False:
        #         COLOR_STATUS=WARNING
        #     else:
        #         COLOR_STATUS='BLUE'
        #     PRINT_CONSOLE(self,"CH :"+str(channel_number)+" CURRENT_TOLERANCE: "+str(CURRENT_TOLERANCE),COLOR_STATUS)
        #     PRINT_CONSOLE(self,"CH :"+str(channel_number)+" METER__VERIFY_READ_CURRENT_LOW: "+str(METER__VERIFY_READ_CURRENT_LOW),COLOR_STATUS)
        #     PRINT_CONSOLE(self,"CH :"+str(channel_number)+" DUT__VERIFY_READ_CURRENT_LOW: "+str(DUT__VERIFY_READ_CURRENT_LOW),COLOR_STATUS)
        #     RESULT.append(RESULT_TEMP)
        #
        #     DC_LOAD_SET_CURRENT_CC(self.dcload,VERIFY_CURRENT_MID,load_type)
        #     time.sleep(6)
        #     DUT__VERIFY_READ_CURRENT_MID=float(TELNET_GET_COMMAND(self.telnet,OIDRead('CALIBRATE CURRENT')['channel'+str(channel_number)]))/10
        #     METER__VERIFY_READ_CURRENT_MID=float(READ_DC_CURRENT(self,load_type))#+BATT_CHARGE_CURRENT_COMPENSATION
        #     RESULT_TEMP=COMPARE(DUT__VERIFY_READ_CURRENT_MID, METER__VERIFY_READ_CURRENT_MID,CURRENT_TOLERANCE )
        #     if RESULT_TEMP==False:
        #         COLOR_STATUS=WARNING
        #     else:
        #         COLOR_STATUS='BLUE'
        #     PRINT_CONSOLE(self,"CH :"+str(channel_number)+" CURRENT_TOLERANCE: "+str(CURRENT_TOLERANCE),COLOR_STATUS)
        #     PRINT_CONSOLE(self,"CH :"+str(channel_number)+" METER__VERIFY_READ_CURRENT_MID: "+str(METER__VERIFY_READ_CURRENT_MID),COLOR_STATUS)
        #     PRINT_CONSOLE(self,"CH :"+str(channel_number)+" DUT__VERIFY_READ_CURRENT_MID: "+str(DUT__VERIFY_READ_CURRENT_MID),COLOR_STATUS)
        #     RESULT.append(RESULT_TEMP)

        if self.mcm_type == 3:
            self.dcload.DC_LOAD_SET_CURRENT_CC("10", load_type)
        else:
            # time.sleep(1)
            self.dcload.DC_LOAD_SET_CURRENT_CC(VERIFY_CURRENT_HIGH, load_type)

        ## time to make smr current required current
        time.sleep(5)

        if dcif_type_number == 3:
            if test_load_type == 'BATT':
                temp_channel_count = 4 - load_current_count  ## added for DCIO channel selection, 03052019
                channel_number = channel_number + temp_channel_count
            DUT__VERIFY_READ_CURRENT_HIGH = float(
                self.MCM_READ_COMMAND('CALIBRATE CURRENT DCIO', 'channel' + str(channel_number)))
            retry_count = 0
            if self.mcm_type == 3:
                while DUT__VERIFY_READ_CURRENT_HIGH < 9 and retry_count < 100:
                    DUT__VERIFY_READ_CURRENT_HIGH = float(
                        self.MCM_READ_COMMAND('CALIBRATE CURRENT DCIO', 'channel' + str(channel_number)))
                    retry_count += 1
            else:
                while DUT__VERIFY_READ_CURRENT_HIGH < 69 and retry_count < 100:
                    DUT__VERIFY_READ_CURRENT_HIGH = float(
                        self.MCM_READ_COMMAND('CALIBRATE CURRENT DCIO', 'channel' + str(channel_number)))
                    retry_count += 1
        else:
            DUT__VERIFY_READ_CURRENT_HIGH = float(
                self.MCM_READ_COMMAND('CALIBRATE CURRENT', 'channel' + str(channel_number))) / 10
        METER__VERIFY_READ_CURRENT_HIGH = float(READ_DC_CURRENT(load_type))  # +BATT_CHARGE_CURRENT_COMPENSATION
        first = abs(DUT__VERIFY_READ_CURRENT_HIGH - METER__VERIFY_READ_CURRENT_HIGH) < CURRENT_TOLERANCE
        if self.mcm_type == 3:
            second = abs(METER__VERIFY_READ_CURRENT_HIGH - 10) < 3
        else:
            second = abs(METER__VERIFY_READ_CURRENT_HIGH - VERIFY_CURRENT_HIGH) < 3

        RESULT_TEMP = first and second
        if RESULT_TEMP == False:
            COLOR_STATUS = "RED"
        else:
            COLOR_STATUS = 'BLUE'
        self.print_console("CH :" + str(channel_number) + " CURRENT_TOLERANCE: " + str(CURRENT_TOLERANCE), COLOR_STATUS)
        self.print_console(
            "CH :" + str(channel_number) + " METER__VERIFY_READ_CURRENT_HIGH: " + str(METER__VERIFY_READ_CURRENT_HIGH),
            COLOR_STATUS)
        self.print_console(
            "CH :" + str(channel_number) + " DUT__VERIFY_READ_CURRENT_HIGH: " + str(DUT__VERIFY_READ_CURRENT_HIGH),
            COLOR_STATUS)
        RESULT.append(RESULT_TEMP)
        # PRINT_CONSOLE(self,"RESULT: "+str(RESULT))
        self.dcload.DC_LOAD_SET_CURRENT_CC(10, "LOAD")
        self.dcload.DC_LOAD_SET_CURRENT_CC(10, "BATT")
        ATE_LOAD_COUNT = int(SettingRead("SETTING")['ate load count'])
        if ATE_LOAD_COUNT == 1:
            # ADDED FOR SINGLE LOAD CONFIGURATION, KUSHAGRA MITTAL 06/09/2016
            self.print_console("RESETTING FOR LOAD PATH")
            self.pfc.pfc_set(0, 'load_mains', 1)
            # self.pfc.pfc_set(0, 'DC LOAD', 0)
            time.sleep(0.5)
        return CALCULATE_RESULT(RESULT)
    except exception as e:
        print(str(e))


def CALCULATE_RESULT(RESULT: object) -> object:
    for RESULT_TEMP in RESULT:
        if RESULT_TEMP == False:
            return False
    return True


def AVG_METER_VOLTAGE(self, load_type):
    sum = 0
    for i in range(0, 5):
        actual_voltage = float(CommandSetDcLoadUsb.DC_LOAD_READ_OUTPUT_VOLTAGE(load_type))
        sum += actual_voltage

    return float(sum) / 5


def SET_INDI_BATTERY_PATH(battery_number):
    batt_fuse_count = int(
        DefaultRead('DEFAULT SETTING')["battery ah"])  # int(ConfigRead('DUT CONFIGURATION')['no. of battery fuses'])
    # PRINT_CONSOLE(self,"batt fuse: "+str(batt_fuse_count))
    for count in range(1, batt_fuse_count + 1):
        if count == battery_number:
            PFC_control_done.pfc_control.pfc_set(0, 'battery_' + str(count), 1)

    for count in range(1, batt_fuse_count + 1):
        if count != battery_number:
            PFC_control_done.pfc_control.pfc_set(0, 'battery_' + str(count), 0)


def READ_DC_VOLTAGE(self, load_type='LOAD'):
    global DATA
    try:

        DATA = CommandSetDcLoadUsb.DC_LOAD_READ_OUTPUT_VOLTAGE(load_type)
        test_data = float(DATA)

    except:
        # (self, 'ELECTRONIC DC LOAD (' + str(load_type) + ') PATH RESPONDING GARBAGE VOLTAGE VALUES!',
        #               WARNING)
        self.print_console('VALUE IS: ' + str(DATA), "RED")
        DATA = 999992
        self.prompt('ELECTRONIC DC LOAD (' + str(load_type) + ') PATH RESPONDING GARBAGE VALUES!')
        pass

    return DATA


def SET_INDI_LOAD_PATH_ISO(self, load_number):
    load_current_count = int(ConfigRead('DUT CONFIGURATION')['no. of load current'])
    # PRINT_CONSOLE(self,"load current: "+str(load_current_count))
    for count in range(1, load_current_count + 1):
        if count == load_number:
            self.pfc.pfc_set(0, 'n_p_load_' + str(count), 0)


def SET_INDI_LOAD_PATH(self, load_number):
    load_current_count = int(ConfigRead('DUT CONFIGURATION')['no. of load current'])
    # PRINT_CONSOLE(self,"load current: "+str(load_current_count))
    for count in range(1, load_current_count + 1):
        if count == load_number:
            self.pfc.pfc_set(0, 'n_p_load_' + str(count), 1)

    for count in range(1, load_current_count + 1):
        if count != load_number:
            self.pfc.pfc_set(0, 'n_p_load_' + str(count), 0)


def SET_LOAD_ISOLATE(self, load_lvd_count, state):
    # PRINT_CONSOLE(self,"set load isolate")
    for i in range(1, load_lvd_count + 1):
        self.MCM_WRITE_COMMAND('LOAD ISOLATE', 'load' + str(i), state)


def READ_DC_CURRENT(load_type='LOAD'):
    global DATA
    try:
        DATA = CommandSetDcLoadUsb.DC_LOAD_READ_OUTPUT_CURRENT(load_type)
        test_data = float(DATA)

    except:
        Ui_Test.print_console(Ui_Test,
                              'ELECTRONIC DC LOAD (' + str(load_type) + ') PATH RESPONDING GARBAGE CURRENT VALUES!',
                              "RED")
        Ui_Test.print_console(Ui_Test, 'VALUE IS: ' + str(DATA), "RED")
        DATA = 999991
        Prompt.Message(title="ERROR!",
                       prompt='ELECTRONIC DC LOAD (' + str(load_type) + ') PATH RESPONDING GARBAGE VALUES!')
        pass

    return DATA


def SMR_STATUS_TEXT(smr_status):
    RECTIFIER_STATUS_TYPE_STRINGS = ["Comm Fail",
                                     "Ok",
                                     "Fail",
                                     "Fail-OV",
                                     "Fail-Fan",
                                     "Prot-Disabled",
                                     "Prot-SafeMode",
                                     "Prot-OL",
                                     "Prot-High Temp",
                                     "Prot-AC High",
                                     "Prot-Freq Abn",
                                     "Prot-Grid Abn",
                                     "Ok-InpV Derate",
                                     "Ok-Temp Derate",
                                     "Ok-OutV Derate",
                                     "Ok-Curr Limit",
                                     "Ok-UV",
                                     "HVLV Comm Fail",
                                     "Prot-HVLV"]

    return RECTIFIER_STATUS_TYPE_STRINGS[smr_status]


def InitChromaLoad(dcload, type_load: str):
    dcload.DC_LOAD_READ_COMMAND(id, type_load)
    dcload.DC_LOAD_SET_COMMAND(RESET, type_load)
    dcload.DC_LOAD_SET_COMMAND(set_load_sense, type_load)
    dcload.DC_LOAD_SET_COMMAND(load_ON, type_load)


def SET_INDI_BATTERY_ISOLATE(self, batt_no, state):
    self.MCM_WRITE_COMMAND('BATTERY ISOLATE', 'batt' + str(batt_no), state)


def SET_BATTERY_ISOLATE(self, batt_lvd_count, state):
    # PRINT_CONSOLE(self,"set battery isolate")
    for i in range(1, batt_lvd_count + 1):
        self.MCM_WRITE_COMMAND('BATTERY ISOLATE', 'batt' + str(i), state)


def ACSET(pfc, phase, state):
    if phase == 1:
        pfc.pfc_set(0, 'r_phase', state)
    elif phase == 3:
        pfc.pfc_set(0, 'r_phase', state)
        pfc.pfc_set(0, 'y_phase', state)
        pfc.pfc_set(0, 'b_phase', state)


def width(value: object) -> object:
    global w, factor
    return int(w * (value / 1366) * factor)


def height(value):
    global h, factor
    return int(h * (value / 768) * factor)


if __name__ == "__main__":
    import sys

    global ate_name
    app = QtWidgets.QApplication(sys.argv)
    ate_name = sys.argv[0].split("\\")[-1].split(".")[0]
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Test()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())

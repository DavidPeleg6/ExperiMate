# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
""" notes!:
        there is no verification of free ports yet
        sensors must not have the same name
        ports must not have the same name
        all sensors must return at least one result
"""
import sys
sys.path.append('../../../')
sys.path.append('../../../../')
sys.path.append('../../')
from PyQt5 import QtCore, QtGui, QtWidgets
from Menu import Menu
from BoardSensorManager import Board, Sensor
from ExperimentObserver import PlotObserver
import os
from Notepad import Notepad
from PlotWindow import PlotWindow


class Ui_main_window(QtWidgets.QWidget):

    def setupUi(self, main_window):
        # TODO generate a settings json for the user
        self.menu = Menu(settings_loc='../../settings2.json')
        self.board = Board(self.menu.get_default_frequency(), com_number=self.menu.get_default_com())
        self.used_sensors = 1
        self.sensors = {}
        self.main_window = main_window
        self.text_edit_on = False
        self.cur_plot = None
        # set main windows
        main_window.setObjectName("main_window")
        main_window.resize(1012, 807)
        # set icon of main window
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("images/index.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        main_window.setWindowIcon(self.icon)
        # set central widget
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")

        # add left side file tabs
        self.add_left_side_tabs()

        # add arduino image and sensor images
        self.add_sensor_images()

        # add the arduino settings tab
        self.sensors_tabs = {}
        self.add_arduino_settings_tabs()

        # add main experiment buttons
        self.add_main_experiment_buttons()

        # add upper menu bar
        self.add_main_menu_bar()

        self.retranslateUi(main_window)
        self.files_tabs_widget.setCurrentIndex(0)
        self.arduino_settings_tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "ExperiMate"))
        self.files_tabs_widget.setTabText(self.files_tabs_widget.indexOf(self.projects_tab), _translate("main_window", "projects"))
        self.files_tabs_widget.setTabText(self.files_tabs_widget.indexOf(self.results_tab), _translate("main_window", "results"))
        self.update_arduino_settings_btn.setText(_translate("main_window", "update"))
        self.add_sensor_label.setText(_translate("main_window", "Add sensor:"))
        self.read_results_checkbox.setToolTip(_translate("main_window", "save results recieved in file"))
        self.read_results_checkbox.setText(_translate("main_window", "Read results"))
        self.frequency_label.setText(_translate("main_window", "frequency:"))
        self.save_configuration_checkbox.setToolTip(_translate("main_window", "Save configuration as a project at the end of run"))
        self.save_configuration_checkbox.setText(_translate("main_window", "Save configuration"))
        self.arduino_settings_tabs.setTabText(self.arduino_settings_tabs.indexOf(self.arduino_settings), _translate("main_window", "Arduino settings"))
        self.start_btn.setToolTip(_translate("main_window", "start current configuration"))
        self.start_btn.setText(_translate("main_window", "start"))
        self.stop_btn.setToolTip(_translate("main_window", "stop ongoing experiment"))
        self.stop_btn.setText(_translate("main_window", "stop"))
        self.plot_btn.setToolTip(_translate("main_window", "plot ongoing experiment"))
        self.plot_btn.setText(_translate("main_window", "plot"))
        self.file_menu.setTitle(_translate("main_window", "File"))
        self.view_menu.setTitle(_translate("main_window", "View"))
        self.settings_menu.setTitle(_translate("main_window", "Settings"))
        self.choose_com_menu.setTitle(_translate("main_window", "Com number"))
        self.export_menu.setTitle(_translate("main_window", "Export"))
        self.delete_action.setText(_translate("main_window", "Delete"))
        self.delete_action.setToolTip(_translate("main_window", "Delete a sensor"))
        self.delete_action.setStatusTip(_translate("main_window", "Delete a sensor"))
        self.open_action.setTitle(_translate("main_window", "Open"))
        self.open_action.setToolTip(_translate("main_window", "Open"))
        self.open_action.setStatusTip(_translate("main_window", "open a project from the system"))
        self.save_action.setText(_translate("main_window", "Save"))
        self.save_action.setToolTip(_translate("main_window", "save current project"))
        self.save_action.setStatusTip(_translate("main_window", "save current project"))
        self.save_action.setShortcut(_translate("main_window", "Ctrl+S"))
        self.exit_program_action.setText(_translate("main_window", "Exit"))
        self.exit_program_action.setStatusTip(_translate("main_window", "close the program"))
        self.exit_program_action.setShortcut(_translate("main_window", "Ctrl+Q"))
        self.ide_open_action.setText(_translate("main_window", "IDE"))
        self.ide_open_action.setStatusTip(_translate("main_window", "show current project in code form"))
        self.ide_open_action.setShortcut(_translate("main_window", "Ctrl+E"))
        self.plot_action.setText(_translate("main_window", "Plot"))
        self.plot_action.setStatusTip(_translate("main_window", "choose a file from the results to plot"))
        for i in range(1, 9):
            self.action_com[i].setText(_translate("main_window", "COM" + str(i)))
        self.new_proj_action.setText(_translate("main_window", "New"))
        self.new_proj_action.setStatusTip(_translate("main_window", "create a new sensor from outside code"))
        self.export_results_action.setText(_translate("main_window", "Results"))
        self.export_plots_action.setText(_translate("main_window", "Plot"))
        self.frequency_spin_box.setSuffix(_translate("main_window", "Hz"))

    """ Main UI layout starting functions: these functions start UI element and use the functionality in the next
     segment to implement actions"""
    def add_sensor_images(self):
        # arduino image label
        self.main_img_label = QtWidgets.QLabel(self.central_widget)
        self.main_img_label.setGeometry(QtCore.QRect(390, 30, 381, 211))
        self.main_img_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.main_img_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_img_label.setPixmap(QtGui.QPixmap("images/ardu.jpg"))
        self.main_img_label.setScaledContents(True)
        self.main_img_label.setObjectName("main_img_label")
        # add the rest of the sensor images
        # start by defining the image
        # TODO add functionality of dynamic photos
        """
        self.pixel_map = QtGui.QPixmap("images/empty_spot.png").scaled(60, 100, QtCore.Qt.KeepAspectRatio)
        self.layoutWidget4 = QtWidgets.QWidget(self.central_widget)
        self.layoutWidget4.setGeometry(QtCore.QRect(230, 250, 691, 131))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.images_layout = QtWidgets.QHBoxLayout(self.layoutWidget4)
        self.images_layout.setContentsMargins(0, 0, 0, 0)
        self.images_layout.setObjectName("images_layout")
        self.image_sensor_label1 = QtWidgets.QLabel(self.layoutWidget4)
        self.image_sensor_label1.setAutoFillBackground(False)
        self.image_sensor_label1.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.image_sensor_label1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.image_sensor_label1.setPixmap(self.pixel_map)
        self.image_sensor_label1.setScaledContents(True)
        self.image_sensor_label1.setObjectName("image_sensor_label1")
        self.images_layout.addWidget(self.image_sensor_label1)
        self.image_sensor_label2 = QtWidgets.QLabel(self.layoutWidget4)
        self.image_sensor_label2.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.image_sensor_label2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.image_sensor_label2.setPixmap(self.pixel_map)
        self.image_sensor_label2.setScaledContents(True)
        self.image_sensor_label2.setObjectName("image_sensor_label2")
        self.images_layout.addWidget(self.image_sensor_label2)
        self.image_sensor_label3 = QtWidgets.QLabel(self.layoutWidget4)
        self.image_sensor_label3.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.image_sensor_label3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.image_sensor_label3.setPixmap(self.pixel_map)
        self.image_sensor_label3.setScaledContents(True)
        self.image_sensor_label3.setObjectName("image_sensor_label3")
        self.images_layout.addWidget(self.image_sensor_label3)
        self.image_sensor_label4 = QtWidgets.QLabel(self.layoutWidget4)
        self.image_sensor_label4.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.image_sensor_label4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.image_sensor_label4.setPixmap(self.pixel_map)
        self.image_sensor_label4.setScaledContents(True)
        self.image_sensor_label4.setObjectName("image_sensor_label4")
        self.images_layout.addWidget(self.image_sensor_label4)
        self.image_sensor_label5 = QtWidgets.QLabel(self.layoutWidget4)
        self.image_sensor_label5.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.image_sensor_label5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.image_sensor_label5.setPixmap(self.pixel_map)
        self.image_sensor_label5.setScaledContents(True)
        self.image_sensor_label5.setObjectName("image_sensor_label5")
        self.images_layout.addWidget(self.image_sensor_label5)
        """

    def add_left_side_tabs(self):
        # files tab (left side)
        self.files_tabs_widget = QtWidgets.QTabWidget(self.central_widget)
        self.files_tabs_widget.setGeometry(QtCore.QRect(10, 10, 201, 651))
        self.files_tabs_widget.setObjectName("files_tabs_widget")
        self.projects_tab = QtWidgets.QWidget()
        # initialize projects tab and add to  file tabs
        self.projects_tab.setObjectName("projects_tab")
        self.projects_list = QtWidgets.QListWidget(self.projects_tab)
        # self.projects_list = MyList(self.projects_tab)
        self.projects_list.setGeometry(QtCore.QRect(0, 11, 191, 601))
        self.projects_list.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.projects_list.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.projects_list.setLineWidth(0)
        self.projects_list.setMidLineWidth(0)
        self.projects_list.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.projects_list.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.projects_list.setObjectName("sensors_list")
        self.delete_experiment_action = QtWidgets.QAction('Delete')
        self.delete_experiment_action.setShortcut("Del")
        self.delete_experiment_action.triggered.connect(self.delete_experiment_action_handler)
        self.projects_list.addAction(self.delete_experiment_action)
        self.projects_list.doubleClicked.connect(self.project_double_clicked)
        self.projects_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.update_projects_list()
        self.files_tabs_widget.addTab(self.projects_tab, "")
        # initialize results tab and add to file tabs
        self.results_tab = QtWidgets.QWidget()
        self.results_tab.setObjectName("results_tab")
        self.results_list = QtWidgets.QListWidget(self.results_tab)
        self.results_list.setGeometry(QtCore.QRect(0, 11, 191, 601))
        self.results_list.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.results_list.setObjectName("results_list")
        self.results_list.doubleClicked.connect(self.result_double_clicked)
        self.delete_results_action = QtWidgets.QAction('Delete')
        self.delete_results_action.setShortcut("Del")
        self.delete_results_action.triggered.connect(self.delete_results_action_handler)
        self.results_list.addAction(self.delete_results_action)
        self.update_results_list()
        self.files_tabs_widget.addTab(self.results_tab, "")

    # TODO add export results functionality
    def add_board_settings_tab(self):
        # initialize arduino settings tab
        self.arduino_settings = QtWidgets.QWidget()
        self.arduino_settings.setObjectName("arduino_settings")
        self.update_arduino_settings_btn = QtWidgets.QPushButton(self.arduino_settings)
        self.update_arduino_settings_btn.setGeometry(QtCore.QRect(530, 30, 151, 161))
        self.update_arduino_settings_btn.clicked.connect(self.update_arduino_board)
        self.update_arduino_settings_btn.setObjectName("update_arduino_settings_btn")
        self.layoutWidget = QtWidgets.QWidget(self.arduino_settings)
        self.layoutWidget.setGeometry(QtCore.QRect(12, 16, 481, 201))
        self.layoutWidget.setObjectName("layoutWidget")
        self.arduino_settings_grid_layout = QtWidgets.QGridLayout(self.layoutWidget)
        self.arduino_settings_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.arduino_settings_grid_layout.setObjectName("arduino_settings_grid_layout")
        self.add_sensor_label = QtWidgets.QLabel(self.layoutWidget)
        self.add_sensor_label.setObjectName("add_sensor_label")
        self.arduino_settings_grid_layout.addWidget(self.add_sensor_label, 0, 0, 1, 1)
        self.add_sensor_combo_box = QtWidgets.QComboBox(self.layoutWidget)
        # add all sensors to the choice combobox
        self.add_sensor_combo_box.addItem("")
        for sensor in self.menu.get_sensors():
            self.add_sensor_combo_box.addItem(sensor)
        self.add_sensor_combo_box.setObjectName("add_sensor_combo_box")
        self.arduino_settings_grid_layout.addWidget(self.add_sensor_combo_box, 0, 1, 1, 1)

        self.frequency_spin_box = QtWidgets.QSpinBox(self.layoutWidget)
        self.frequency_spin_box.setGeometry(QtCore.QRect(360, 170, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.frequency_spin_box.setFont(font)
        self.frequency_spin_box.setWrapping(False)
        self.frequency_spin_box.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.frequency_spin_box.setMaximum(100)
        # set the default value by conversion of x[Hz] = 1000/x[ms]
        self.frequency_spin_box.setValue(1000 / self.board.frequency)
        self.frequency_spin_box.setObjectName("spinBox")
        self.arduino_settings_grid_layout.addWidget(self.frequency_spin_box, 1, 1, 1, 1)
        self.frequency_label = QtWidgets.QLabel(self.layoutWidget)
        self.frequency_label.setObjectName("frequency_label")
        self.arduino_settings_grid_layout.addWidget(self.frequency_label, 1, 0, 1, 1)
        # TODO make read results checkbox always checked or delete it
        self.read_results_checkbox = QtWidgets.QCheckBox(self.layoutWidget)
        self.read_results_checkbox.setObjectName("read_results_checkbox")
        self.read_results_checkbox.setChecked(True)
        self.arduino_settings_grid_layout.addWidget(self.read_results_checkbox, 2, 0, 1, 1)
        self.save_configuration_checkbox = QtWidgets.QCheckBox(self.layoutWidget)
        self.save_configuration_checkbox.setObjectName("save_configuration_checkbox")
        self.save_configuration_checkbox.setChecked(True)
        self.arduino_settings_grid_layout.addWidget(self.save_configuration_checkbox, 2, 1, 1, 1)
        self.arduino_settings_tabs.addTab(self.arduino_settings, "")

    # sensors_tabs is a dictionary with keys that are tab names and values that are sensor tab templates
    # (with all the functionality of a tab and its buttons)
    # TODO change the pin definitions to get more than 4 pins for digital/analog in the menu
    def add_sensor_settings_tab(self, sensor):
        sensor_settings_tab = QtWidgets.QWidget()
        name = self.get_free_sensor_name(sensor.name)
        self.sensors_tabs[name] = {'sensor': sensor}
        sensor_settings_tab.setObjectName("sensor_settings_tab_" + name)
        self.sensors_tabs[name]['tabs_name'] = "sensor_settings_tab_" + name
        self.sensors_tabs[name]['tab'] = sensor_settings_tab

        layoutWidget1 = QtWidgets.QWidget(sensor_settings_tab)
        layoutWidget1.setGeometry(QtCore.QRect(10, 190, 651, 41))
        layoutWidget1.setObjectName("layoutWidget1" + name)
        self.sensors_tabs[name]['layout1'] = layoutWidget1

        sensor_setting_btn_layout = QtWidgets.QHBoxLayout(layoutWidget1)
        sensor_setting_btn_layout.setContentsMargins(0, 0, 0, 0)
        sensor_setting_btn_layout.setObjectName("sensor_setting_btn_layout" + name)
        self.sensors_tabs[name]['btn_layoout'] = sensor_setting_btn_layout

        update_sensor_setting_btn = QtWidgets.QPushButton(layoutWidget1)
        update_sensor_setting_btn.setObjectName("update_sensor_setting_btn" + name)
        update_sensor_setting_btn.clicked.connect(self.update_sensor_btn_handler)
        self.sensors_tabs[name]['update_sensor_btn'] = update_sensor_setting_btn
        sensor_setting_btn_layout.addWidget(update_sensor_setting_btn)

        default_sensor_setting_btn = QtWidgets.QPushButton(layoutWidget1)
        default_sensor_setting_btn.setObjectName("default_sensor_setting_btn" + name)
        default_sensor_setting_btn.clicked.connect(self.set_sensor_default_options)
        self.sensors_tabs[name]['default_sensor_btn'] = default_sensor_setting_btn
        sensor_setting_btn_layout.addWidget(default_sensor_setting_btn)

        remove_sensor_btn = QtWidgets.QPushButton(layoutWidget1)
        remove_sensor_btn.setObjectName("remove_sensor_btn" + name)
        remove_sensor_btn.clicked.connect(self.remove_sensor_tab)
        self.sensors_tabs[name]['remove_sensor_btn'] = remove_sensor_btn
        sensor_setting_btn_layout.addWidget(remove_sensor_btn)

        layoutWidget2 = QtWidgets.QWidget(sensor_settings_tab)
        layoutWidget2.setGeometry(QtCore.QRect(10, 11, 651, 161))
        layoutWidget2.setObjectName("layoutWidget2" + name)
        self.sensors_tabs[name]['layout2'] = layoutWidget2

        sensor_setting_pin_layout = QtWidgets.QGridLayout(layoutWidget2)
        sensor_setting_pin_layout.setContentsMargins(0, 0, 0, 0)
        sensor_setting_pin_layout.setObjectName("sensor_setting_pin_layout" + name)
        self.sensors_tabs[name]['sensor_setting_pin_layout'] = sensor_setting_pin_layout

        dig_pins_label = QtWidgets.QLabel(layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(50)
        dig_pins_label.setFont(font)
        dig_pins_label.setObjectName("dig_pins_label" + name)
        self.sensors_tabs[name]['dig_pins_label'] = dig_pins_label
        sensor_setting_pin_layout.addWidget(dig_pins_label, 0, 0, 1, 1)

        dig_pin1_label = QtWidgets.QLabel(layoutWidget2)
        dig_pin1_label.setObjectName("dig_pin1_label" + name)
        sensor_setting_pin_layout.addWidget(dig_pin1_label, 0, 1, 1, 1)
        self.sensors_tabs[name]['dig_pin1_label'] = dig_pin1_label

        dig_pin1_combobox = QtWidgets.QComboBox(layoutWidget2)
        dig_pin1_combobox.setObjectName("dig_pin1_combobox" + name)
        self.add_sensor_combobox_options(dig_pin1_combobox, is_digital=True)
        sensor_setting_pin_layout.addWidget(dig_pin1_combobox, 0, 2, 1, 1)
        self.sensors_tabs[name]['dig_pin1_combobox'] = dig_pin1_combobox

        dig_pin2_label = QtWidgets.QLabel(layoutWidget2)
        dig_pin2_label.setObjectName("dig_pin2_label" + name)
        sensor_setting_pin_layout.addWidget(dig_pin2_label, 0, 3, 1, 1)
        self.sensors_tabs[name]['dig_pin2_label'] = dig_pin2_label

        dig_pin2_combobox = QtWidgets.QComboBox(layoutWidget2)
        dig_pin2_combobox.setObjectName("dig_pin2_combobox" + name)
        self.add_sensor_combobox_options(dig_pin2_combobox, is_digital=True)
        sensor_setting_pin_layout.addWidget(dig_pin2_combobox, 0, 4, 1, 1)
        self.sensors_tabs[name]['dig_pin2_combobox'] = dig_pin2_combobox

        dig_pin3_label = QtWidgets.QLabel(layoutWidget2)
        dig_pin3_label.setObjectName("dig_pin3_label" + name)
        sensor_setting_pin_layout.addWidget(dig_pin3_label, 0, 5, 1, 1)
        self.sensors_tabs[name]['dig_pin3_label'] = dig_pin3_label

        dig_pin3_combobox = QtWidgets.QComboBox(layoutWidget2)
        dig_pin3_combobox.setObjectName("dig_pin3_combobox" + name)
        self.add_sensor_combobox_options(dig_pin3_combobox, is_digital=True)
        sensor_setting_pin_layout.addWidget(dig_pin3_combobox, 0, 6, 1, 1)
        self.sensors_tabs[name]['dig_pin3_combobox'] = dig_pin3_combobox

        dig_pin4_label = QtWidgets.QLabel(layoutWidget2)
        dig_pin4_label.setObjectName("dig_pin4_label" + name)
        sensor_setting_pin_layout.addWidget(dig_pin4_label, 0, 7, 1, 1)
        self.sensors_tabs[name]['dig_pin4_label'] = dig_pin4_label

        dig_pin4_combobox = QtWidgets.QComboBox(layoutWidget2)
        dig_pin4_combobox.setObjectName("dig_pin4_combobox" + name)
        self.add_sensor_combobox_options(dig_pin4_combobox, is_digital=True)
        sensor_setting_pin_layout.addWidget(dig_pin4_combobox, 0, 8, 1, 1)
        self.sensors_tabs[name]['dig_pin4_combobox'] = dig_pin4_combobox

        dig_pin5_label = QtWidgets.QLabel(layoutWidget2)
        dig_pin5_label.setObjectName("dig_pin5_label" + name)
        sensor_setting_pin_layout.addWidget(dig_pin5_label, 1, 1, 1, 1)
        self.sensors_tabs[name]['dig_pin5_label'] = dig_pin5_label

        dig_pin5_combobox = QtWidgets.QComboBox(layoutWidget2)
        dig_pin5_combobox.setObjectName("dig_pin5_combobox" + name)
        self.add_sensor_combobox_options(dig_pin5_combobox, is_digital=True)
        sensor_setting_pin_layout.addWidget(dig_pin5_combobox, 1, 2, 1, 1)
        self.sensors_tabs[name]['dig_pin5_combobox'] = dig_pin5_combobox

        dig_pin6_label = QtWidgets.QLabel(layoutWidget2)
        dig_pin6_label.setObjectName("dig_pin6_label" + name)
        sensor_setting_pin_layout.addWidget(dig_pin6_label, 1, 3, 1, 1)
        self.sensors_tabs[name]['dig_pin6_label'] = dig_pin6_label

        dig_pin6_combobox = QtWidgets.QComboBox(layoutWidget2)
        dig_pin6_combobox.setObjectName("dig_pin6_combobox" + name)
        self.add_sensor_combobox_options(dig_pin6_combobox, is_digital=True)
        sensor_setting_pin_layout.addWidget(dig_pin6_combobox, 1, 4, 1, 1)
        self.sensors_tabs[name]['dig_pin6_combobox'] = dig_pin6_combobox

        dig_pin7_label = QtWidgets.QLabel(layoutWidget2)
        dig_pin7_label.setObjectName("dig_pin7_label" + name)
        sensor_setting_pin_layout.addWidget(dig_pin7_label, 1, 5, 1, 1)
        self.sensors_tabs[name]['dig_pin7_label'] = dig_pin7_label

        dig_pin7_combobox = QtWidgets.QComboBox(layoutWidget2)
        dig_pin7_combobox.setObjectName("dig_pin7_combobox" + name)
        self.add_sensor_combobox_options(dig_pin7_combobox, is_digital=True)
        sensor_setting_pin_layout.addWidget(dig_pin7_combobox, 1, 6, 1, 1)
        self.sensors_tabs[name]['dig_pin7_combobox'] = dig_pin7_combobox

        dig_pin8_label = QtWidgets.QLabel(layoutWidget2)
        dig_pin8_label.setObjectName("dig_pin8_label" + name)
        sensor_setting_pin_layout.addWidget(dig_pin8_label, 1, 7, 1, 1)
        self.sensors_tabs[name]['dig_pin8_label'] = dig_pin8_label

        dig_pin8_combobox = QtWidgets.QComboBox(layoutWidget2)
        dig_pin8_combobox.setObjectName("dig_pin8_combobox" + name)
        self.add_sensor_combobox_options(dig_pin8_combobox, is_digital=True)
        sensor_setting_pin_layout.addWidget(dig_pin8_combobox, 1, 8, 1, 1)
        self.sensors_tabs[name]['dig_pin8_combobox'] = dig_pin8_combobox

        anal_pins_label = QtWidgets.QLabel(layoutWidget2)
        anal_pins_label.setFont(font)
        anal_pins_label.setObjectName("anal_pins_label" + name)
        self.sensors_tabs[name]['anal_pins_label'] = anal_pins_label
        sensor_setting_pin_layout.addWidget(anal_pins_label, 2, 0, 1, 1)

        anal_pin1_label = QtWidgets.QLabel(layoutWidget2)
        anal_pin1_label.setObjectName("anal_pin1_label" + name)
        sensor_setting_pin_layout.addWidget(anal_pin1_label, 2, 1, 1, 1)
        self.sensors_tabs[name]['anal_pin1_label'] = anal_pin1_label

        anal_pin1_combobox = QtWidgets.QComboBox(layoutWidget2)
        anal_pin1_combobox.setObjectName("anal_pin1_combobox" + name)
        self.add_sensor_combobox_options(anal_pin1_combobox, is_digital=False)
        sensor_setting_pin_layout.addWidget(anal_pin1_combobox, 2, 2, 1, 1)
        self.sensors_tabs[name]['anal_pin1_combobox'] = anal_pin1_combobox

        anal_pin2_label = QtWidgets.QLabel(layoutWidget2)
        anal_pin2_label.setObjectName("anal_pin2_label" + name)
        sensor_setting_pin_layout.addWidget(anal_pin2_label, 2, 3, 1, 1)
        self.sensors_tabs[name]['anal_pin2_label'] = anal_pin2_label

        anal_pin2_combobox = QtWidgets.QComboBox(layoutWidget2)
        anal_pin2_combobox.setObjectName("anal_pin2_combobox" + name)
        self.add_sensor_combobox_options(anal_pin2_combobox, is_digital=False)
        sensor_setting_pin_layout.addWidget(anal_pin2_combobox, 2, 4, 1, 1)
        self.sensors_tabs[name]['anal_pin2_combobox'] = anal_pin2_combobox

        anal_pin3_label = QtWidgets.QLabel(layoutWidget2)
        anal_pin3_label.setObjectName("anal_pin3_label" + name)
        sensor_setting_pin_layout.addWidget(anal_pin3_label, 2, 5, 1, 1)
        self.sensors_tabs[name]['anal_pin3_label'] = anal_pin3_label

        anal_pin3_combobox = QtWidgets.QComboBox(layoutWidget2)
        anal_pin3_combobox.setObjectName("anal_pin3_combobox" + name)
        self.add_sensor_combobox_options(anal_pin3_combobox, is_digital=False)
        sensor_setting_pin_layout.addWidget(anal_pin3_combobox, 2, 6, 1, 1)
        self.sensors_tabs[name]['anal_pin3_combobox'] = anal_pin3_combobox

        anal_pin4_label = QtWidgets.QLabel(layoutWidget2)
        anal_pin4_label.setObjectName("anal_pin4_label" + name)
        sensor_setting_pin_layout.addWidget(anal_pin4_label, 2, 7, 1, 1)
        self.sensors_tabs[name]['anal_pin4_label'] = anal_pin4_label

        anal_pin4_combobox = QtWidgets.QComboBox(layoutWidget2)
        anal_pin4_combobox.setObjectName("anal_pin4_combobox" + name)
        self.add_sensor_combobox_options(anal_pin4_combobox, is_digital=False)
        sensor_setting_pin_layout.addWidget(anal_pin4_combobox, 2, 8, 1, 1)
        self.sensors_tabs[name]['anal_pin4_combobox'] = anal_pin4_combobox

        self.arduino_settings_tabs.addTab(sensor_settings_tab, "")

        update_sensor_setting_btn.setToolTip("update pin usage")
        update_sensor_setting_btn.setText("Update")
        default_sensor_setting_btn.setToolTip("Use the default pins for this sensor")
        default_sensor_setting_btn.setText("Default")
        remove_sensor_btn.setToolTip("Remove the sensor from the experiment")
        remove_sensor_btn.setText("Remove")
        dig_pins_label.setText("Digitals:")
        dig_pin1_label.setText("Pin1:")
        dig_pin2_label.setText("Pin2:")
        dig_pin3_label.setText("Pin3:")
        dig_pin4_label.setText("Pin4:")
        dig_pin5_label.setText("Pin5:")
        dig_pin6_label.setText("Pin6:")
        dig_pin7_label.setText("Pin7:")
        dig_pin8_label.setText("Pin8:")
        anal_pins_label.setText("Analogs:")
        anal_pin1_label.setText("Pin1:")
        anal_pin2_label.setText("Pin2:")
        anal_pin3_label.setText("Pin3:")
        anal_pin4_label.setText("Pin4:")
        self.arduino_settings_tabs.setTabText(self.arduino_settings_tabs.indexOf(sensor_settings_tab), name)
        self.sensors_tabs[name]['index'] = self.arduino_settings_tabs.indexOf(sensor_settings_tab)
        self.set_sensor_tab_pin_names(name)

    def add_arduino_settings_tabs(self):
        # arduino settings tabs
        self.arduino_settings_tabs = QtWidgets.QTabWidget(self.central_widget)
        self.arduino_settings_tabs.setGeometry(QtCore.QRect(220, 390, 721, 261))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.arduino_settings_tabs.setFont(font)
        self.arduino_settings_tabs.setAutoFillBackground(True)
        self.arduino_settings_tabs.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.arduino_settings_tabs.setTabBarAutoHide(True)
        self.arduino_settings_tabs.setObjectName("arduino_settings_tabs")
        # add the board settings
        self.add_board_settings_tab()

    def add_main_experiment_buttons(self):
        self.layoutWidget3 = QtWidgets.QWidget(self.central_widget)
        self.layoutWidget3.setGeometry(QtCore.QRect(10, 670, 941, 71))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.buttons_layout = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.buttons_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setObjectName("buttons_layout")
        self.start_btn = QtWidgets.QPushButton(self.layoutWidget3)
        self.start_btn.setObjectName("start_btn")
        self.start_btn.clicked.connect(self.start_experiment_handler)
        self.buttons_layout.addWidget(self.start_btn)
        self.stop_btn = QtWidgets.QPushButton(self.layoutWidget3)
        self.stop_btn.setObjectName("stop_btn")
        self.stop_btn.clicked.connect(self.stop_experiment_handler)
        self.buttons_layout.addWidget(self.stop_btn)
        self.plot_btn = QtWidgets.QPushButton(self.layoutWidget3)
        self.plot_btn.setObjectName("plot_btn")
        self.plot_btn.clicked.connect(self.plot_btn_handler)
        self.buttons_layout.addWidget(self.plot_btn)

    def add_file_menu(self):
        self.file_menu = QtWidgets.QMenu(self.menu_bar)
        self.file_menu.setObjectName("file_menu")
        self.delete_action = QtWidgets.QAction(main_window)
        self.delete_action.triggered.connect(self.delete_sensor)
        self.delete_action.setObjectName("delete_action_menu")
        # initialize the open action
        self.open_action = QtWidgets.QMenu(self.menu_bar)
        self.open_action.setObjectName("open_action")
        self.open_project_action = QtWidgets.QAction('Project', main_window)
        self.open_project_action.triggered.connect(self.open_project_handler)
        self.open_action.addAction(self.open_project_action)
        self.open_sensor_action = QtWidgets.QAction('Sensor', main_window)
        self.open_sensor_action.triggered.connect(self.open_sensor_handler)
        self.open_action.addAction(self.open_sensor_action)
        # initialize save action
        self.save_action = QtWidgets.QAction(main_window)
        self.save_action.triggered.connect(self.save_current_configuration)
        self.save_action.setObjectName("save_action")
        # initialize exit action
        self.exit_program_action = QtWidgets.QAction(main_window)
        self.exit_program_action.setObjectName("exit_program_action")
        self.exit_program_action.triggered.connect(self.close_application)
        # initialize add and delete actions
        self.new_proj_action = QtWidgets.QAction(main_window)
        self.new_proj_action.triggered.connect(self.new_sensor_handler)
        self.new_proj_action.setObjectName("new_proj_action")
        # add the actions
        self.file_menu.addAction(self.new_proj_action)
        self.file_menu.addMenu(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.delete_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_program_action)
        # add file menu to main menu
        self.menu_bar.addAction(self.file_menu.menuAction())

    def add_view_menu_bar(self):
        self.view_menu = QtWidgets.QMenu(self.menu_bar)
        self.view_menu.setObjectName("view_menu")
        # initialize open ide action
        self.ide_open_action = QtWidgets.QAction(main_window)
        self.ide_open_action.setObjectName("ide_open_action")
        # initialize plot action
        self.plot_action = QtWidgets.QAction(main_window)
        self.plot_action.setObjectName("plot_action")
        # add the actions
        self.view_menu.addAction(self.ide_open_action)
        self.view_menu.addAction(self.plot_action)
        # add view menu to main menu
        self.menu_bar.addAction(self.view_menu.menuAction())

    def add_settings_menu(self):
        self.settings_menu = QtWidgets.QMenu(self.menu_bar)
        self.settings_menu.setObjectName("settings_menu")
        self.choose_com_menu = QtWidgets.QMenu(self.settings_menu)
        self.choose_com_menu.setObjectName("choose_com_menu")
        # choose com actions
        self.com_action_group = QtWidgets.QActionGroup(self.main_window)
        self.action_com = {}
        for i in range(1, 9):
            self.action_com[i] = self.com_action_group.addAction(QtWidgets.QAction(main_window, checkable=True))
            self.action_com[i].setObjectName("actionCom" + str(i))
            self.action_com[i].triggered.connect(self.change_com_num)
            # add action to menu
            self.choose_com_menu.addAction(self.action_com[i])
        self.settings_menu.addAction(self.choose_com_menu.menuAction())
        # add settings menu to main menu
        self.menu_bar.addAction(self.settings_menu.menuAction())

    def add_export_menu(self):
        self.export_menu = QtWidgets.QMenu(self.menu_bar)
        self.export_menu.setObjectName("export_menu")
        # initialize export menu
        self.export_results_action = QtWidgets.QAction(main_window)
        self.export_results_action.setObjectName("export_results_action")
        self.export_plots_action = QtWidgets.QAction(main_window)
        self.export_plots_action.setObjectName("export_plots_action")
        self.export_menu.addAction(self.export_results_action)
        self.export_menu.addAction(self.export_plots_action)
        # add the export menu to main menu
        self.menu_bar.addAction(self.export_menu.menuAction())

    def add_main_menu_bar(self):
        main_window.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 1012, 26))
        self.menu_bar.setObjectName("menu_bar")
        # add all file menus
        self.add_file_menu()
        # add view menu
        self.add_view_menu_bar()
        # add settings menu
        self.add_settings_menu()
        # add export manu
        self.add_export_menu()
        main_window.setMenuBar(self.menu_bar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

    """ Main functionality methods: these methods define functionality stated in the UI layout"""
    def plot_btn_handler(self):
        try:
            observer = self.menu.get_current_plot()
            self.cur_plot = PlotWindow(name=self.board.cur_name, data_observer=observer,
                                       icon=self.icon, live=True)
        except SystemError as e:
            self.error_message(e.args[0])
            return

    def update_sensor_combobox(self):
        self.add_sensor_combo_box.clear()
        self.add_sensor_combo_box.addItem("")
        for sensor in self.menu.get_sensors():
            self.add_sensor_combo_box.addItem(sensor)

    def new_sensor_handler(self):
        self.information_message('Please note that the new Ino file should be inline with the tag instructions',
                                 '(see example file in Open->Sensor->example)')
        fname = QtWidgets.QFileDialog.getOpenFileName(self.main_window, 'Open file', 'c:/', "Ino files (*.ino)")
        if fname[0] == '':
            return
        self.menu.add_new_sensor(fname[0])
        self.update_sensor_combobox()

    def open_sensor_handler(self):
        self.open_sensor_dialog = QtWidgets.QDialog(self.main_window)
        self.open_sensor_dialog.setWindowTitle('Choose Sensor')
        self.open_sensor_dialog.resize(400, 120)
        question_label = QtWidgets.QLabel(self.open_sensor_dialog)
        question_label.setText('Choose a sensor to open:')
        question_label.move(10, 25)
        # create a combobox and position it correctly
        self.get_sensor_combobox = QtWidgets.QComboBox(self.open_sensor_dialog)
        # add all sensors to the choice combobox
        self.get_sensor_combobox.addItem("")
        self.get_sensor_combobox.addItem("example")
        for sensor in self.menu.get_sensors():
            self.get_sensor_combobox.addItem(sensor)
        self.get_sensor_combobox.setObjectName("get_sensor_combobox")
        self.get_sensor_combobox.move(200, 25)
        self.get_sensor_combobox.resize(150, 20)
        open_btn = QtWidgets.QPushButton('Open', self.open_sensor_dialog)
        open_btn.setObjectName('open_sensor_btn')
        open_btn.clicked.connect(self.open_sensor_btn)
        open_btn.move(200, 70)
        self.open_sensor_dialog.show()

    def open_sensor_btn(self):
        name = self.get_sensor_combobox.currentText()
        if name == '':
            return
        elif name == 'example':
            loc = self.menu.get_example_location()
        else:
            loc = self.menu.get_sensor_location(name)
        self.open_sensor_dialog.close()
        self.notepad = Notepad(name, loc, self.icon)

    def open_project_handler(self):
        self.open_sensor_dialog = QtWidgets.QDialog(self.main_window)
        self.open_sensor_dialog.setWindowTitle('Choose Project')
        self.open_sensor_dialog.resize(400, 120)
        question_label = QtWidgets.QLabel(self.open_sensor_dialog)
        question_label.setText('Choose a project to open:')
        question_label.move(10, 25)
        # create a combobox and position it correctly
        self.get_sensor_combobox = QtWidgets.QComboBox(self.open_sensor_dialog)
        # add all sensors to the choice combobox
        self.get_sensor_combobox.addItem("")
        for sensor in self.menu.get_projects():
            self.get_sensor_combobox.addItem(sensor)
        self.get_sensor_combobox.setObjectName("get_sensor_combobox")
        self.get_sensor_combobox.move(200, 25)
        self.get_sensor_combobox.resize(150, 20)
        open_btn = QtWidgets.QPushButton('Open', self.open_sensor_dialog)
        open_btn.setObjectName('open_sensor_btn')
        open_btn.clicked.connect(self.open_project_btn)
        open_btn.move(200, 70)
        self.open_sensor_dialog.show()

    def open_project_btn(self):
        name = self.get_sensor_combobox.currentText()
        if name == '':
            return
        loc = self.menu.get_project_location(name)
        self.open_sensor_dialog.close()
        self.notepad = Notepad(name, loc, self.icon)

    def delete_sensor(self):
        self.delete_sensor_dialog = QtWidgets.QDialog(self.main_window)
        self.delete_sensor_dialog.setWindowTitle('Choose Sensor')
        self.delete_sensor_dialog.resize(400, 120)
        question_label = QtWidgets.QLabel(self.delete_sensor_dialog)
        question_label.setText('Choose a sensor to delete:')
        question_label.move(10, 25)
        # create a combobox and position it correctly
        self.get_sensor_combobox = QtWidgets.QComboBox(self.delete_sensor_dialog)
        # add all sensors to the choice combobox
        self.get_sensor_combobox.addItem("")
        for sensor in self.menu.get_sensors():
            self.get_sensor_combobox.addItem(sensor)
        self.get_sensor_combobox.setObjectName("get_sensor_combobox")
        self.get_sensor_combobox.move(200, 25)
        self.get_sensor_combobox.resize(150, 20)
        delete_btn = QtWidgets.QPushButton('Delete', self.delete_sensor_dialog)
        delete_btn.setObjectName('delete_sensor_btn')
        delete_btn.clicked.connect(self.delete_sensor_btn_handler)
        delete_btn.move(80, 70)
        cancel_btn = QtWidgets.QPushButton('Cancel', self.delete_sensor_dialog)
        cancel_btn.setObjectName('cancel_delete_btn')
        cancel_btn.clicked.connect(self.cancel_btn)
        cancel_btn.move(250, 70)
        self.delete_sensor_dialog.show()

    def cancel_btn(self):
        self.delete_sensor_dialog.close()

    def delete_sensor_btn_handler(self):
        self.menu.delete_sensor(self.get_sensor_combobox.currentText())
        # reset items in combo box
        self.add_sensor_combo_box.clear()
        self.add_sensor_combo_box.addItem("")
        for sensor in self.menu.get_sensors():
            self.add_sensor_combo_box.addItem(sensor)
        self.delete_sensor_dialog.close()

    def save_current_configuration(self):
        text, result = QtWidgets.QInputDialog.getText(self.main_window, 'input name', 'Enter experiment name:')
        if result:
            if str(text) == '':
                self.error_message('name must not be empty')
                return
            if not self.board.sensors:
                self.error_message('no sensors were added to the experiment')
                return
            try:
                self.board.current_experiment = self.menu.combine2(self.board.sensors, str(text))
                self.board.cur_name = str(text)
                self.update_results_list()
                self.update_projects_list()
            except SystemError as e:
                self.error_message(e.args[0])
            except NotImplementedError as e:
                self.error_message(e.args[0])

    def close_application(self):
        # TODO find a way to also pop the question in case of pressing x to exit
        choice = QtWidgets.QMessageBox.question(self.main_window, 'exit window', "would you like to quit the application?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        # choice now holds a boolean
        if choice == QtWidgets.QMessageBox.Yes:
            self.stop_experiment_handler()
            sys.exit()

    def stop_experiment_handler(self):
        if self.board.current_experiment is None:
            return
        progress = self.upload_message_box('stopping experiment, please wait...')
        # combine all the sensors from all experiments defined
        QtWidgets.qApp.processEvents()
        try:
            progress.setValue(50)
            self.menu.stop(self.board.com_number)
            progress.setValue(90)
        except SystemError as e:
            self.error_message(e.args[0])
        if not self.board.save_configutarion:
            self.menu.delete_configuration(self.board.current_experiment)
        if not self.board.read_results:
            self.menu.delete_result(self.board.current_experiment)
        self.board.current_experiment = None
        self.update_results_list()
        self.update_projects_list()
        progress.setValue(100)

    def change_com_num(self):
        for num, action in self.action_com.items():
            if action.isChecked():
                self.board.com_number = num

    # updates the list in the results tab in the left pane
    def update_results_list(self):
        self.results_list.clear()
        for result in self.menu.get_results_names():
            self.results_list.addItem(result)

    # updates the list in the projects tab in the left pane
    def update_projects_list(self):
        self.projects_list.clear()
        for project in self.menu.get_projects():
            self.projects_list.addItem(project)

    # method to handle a double click on a project name in the left pane
    def project_double_clicked(self):
        self.dialog = QtWidgets.QDialog(self.main_window)
        self.dialog.setWindowTitle('Choose Action')
        self.dialog.resize(300, 120)
        question_label = QtWidgets.QLabel(self.dialog)
        question_label.setText('What would you like to do with this project?')
        question_label.move(10, 25)
        open_exper_btn = QtWidgets.QPushButton('Open', self.dialog)
        open_exper_btn.setObjectName('open_exper_btn')
        open_exper_btn.clicked.connect(self.open_experiment)
        open_exper_btn.move(10, 70)
        delete_exper_btn = QtWidgets.QPushButton('Delete', self.dialog)
        delete_exper_btn.setObjectName('delete_exper_btn')
        delete_exper_btn.clicked.connect(self.delete_experiment)
        delete_exper_btn.move(150, 70)
        self.dialog.show()

    def open_experiment(self):
        desc = self.menu.get_project_data(self.projects_list.selectedItems()[0].text())
        digital_pins = {pin['pin_name']: pin['number'] for pin in desc['pins'] if pin['type'] == 'digital'}
        analog_pins = {pin['pin_name']: pin['number'] for pin in desc['pins'] if pin['type'] == ['analog']}
        sensor = Sensor(desc['name'], digital_pins, analog_pins)
        self.board.frequency = desc["frequency"]
        self.frequency_spin_box.setValue(int(1000 / self.board.frequency))
        self.board.add_sensor_to_board(sensor)
        self.add_sensor_settings_tab(sensor)
        # change the combo box setting back to ""
        self.add_sensor_combo_box.setCurrentIndex(0)
        self.dialog.close()

    def delete_experiment(self):
        self.menu.delete_configuration(self.projects_list.selectedItems()[0].text())
        self.update_projects_list()
        self.dialog.close()

    def delete_experiment_action_handler(self):
        if not self.projects_list.selectedItems() or self.projects_list.selectedItems()[0] == '':
            return
        self.menu.delete_configuration(self.projects_list.selectedItems()[0].text())
        self.update_projects_list()

    def result_double_clicked(self):
        if not self.results_list.selectedItems() or self.results_list.selectedItems()[0] == '':
            return
        name = self.results_list.selectedItems()[0].text()
        results_df = self.menu.get_dataframe_results(name)
        self.saved_plot = PlotWindow(name, self.icon, PlotObserver(results_df))

    def delete_results_action_handler(self):
        if not self.results_list.selectedItems() or self.results_list.selectedItems()[0] == '':
            return
        self.menu.delete_result(self.results_list.selectedItems()[0].text())
        self.update_results_list()

    # gets a name an returns a name + number of times the name has been used (based on tabs in Qt designer)
    def get_free_sensor_name(self, name):
        counter = 0
        # while there are more tabs with the same name
        while self.arduino_settings_tabs.findChild(QtWidgets.QWidget, "sensor_settings_tab_" + name + str(counter)) != None:
            counter += 1
        return name + str(counter)

    # method to update the pin numbers of the sensor, only pins that were already in use are taken
    def update_sensor_btn_handler(self):
        name, tab = self.get_sensor_by_index(self.arduino_settings_tabs.currentIndex())
        counter = 1
        for pin_name, pin_num in self.sensors_tabs[name]['sensor'].dig_pins.items():
            new_num = self.sensors_tabs[name]['dig_pin' + str(counter) + '_combobox'].currentIndex()
            self.sensors_tabs[name]['sensor'].update_pin_num(pin_name, new_num, digital_bool=True)
            counter += 1
        counter = 1
        for pin_name, pin_num in self.sensors_tabs[name]['sensor'].anal_pins.items():
            new_num = self.sensors_tabs[name]['anal_pin' + str(counter) + '_combobox'].currentIndex()
            self.sensors_tabs[name]['sensor'].update_pin_num(pin_name, new_num, digital_bool=False)
            counter += 1

    def add_sensor_combobox_options(self, combo_box, is_digital):
        combo_box.addItem('')
        if is_digital:
            for i in range(13):
                combo_box.addItem(str(i + 1))
        else:
            for i in range(6):
                combo_box.addItem(str(i + 1))

    def set_sensor_default_options(self):
        name, tab = self.get_sensor_by_index(self.arduino_settings_tabs.currentIndex())
        desc = self.menu.get_sensor_data(tab['sensor'].name)
        digital_pins = {pin['pin_name']: pin['number'] for pin in desc['pins'] if pin['type'] == 'digital'}
        analog_pins = {pin['pin_name']: pin['number'] for pin in desc['pins'] if pin['type'] == ['analog']}
        # create a new sensor object based on the default json
        sensor = Sensor(desc['name'], digital_pins, analog_pins)
        # replace the old sensor settings with the new sensor
        self.board.update_sensor(self.sensors_tabs[name]['sensor'], sensor)
        self.sensors_tabs[name]['sensor'] = sensor
        # reset combobox default options and set them according to the sensor
        for i in range(4):
            self.sensors_tabs[name]['dig_pin' + str(i + 1) + '_combobox'].setCurrentIndex(0)
        for i in range(4):
            self.sensors_tabs[name]['anal_pin' + str(i + 1) + '_combobox'].setCurrentIndex(0)
        self.set_sensor_tab_pin_names(name)

    def set_sensor_tab_pin_names(self, name):
        counter = 1
        for pin_name, pin_num in self.sensors_tabs[name]['sensor'].dig_pins.items():
            self.sensors_tabs[name]['dig_pin' + str(counter) + '_label'].setText(pin_name)
            self.sensors_tabs[name]['dig_pin' + str(counter) + '_combobox'].setCurrentIndex(int(pin_num))
            counter += 1
        counter = 1
        for pin_name, pin_num in self.sensors_tabs[name]['sensor'].anal_pins.items():
            self.sensors_tabs[name]['anal_pin' + str(counter) + '_label'].setText(pin_name)
            self.sensors_tabs[name]['anal_pin' + str(counter) + '_combobox'].setCurrentIndex(int(pin_num))
            counter += 1

    def update_arduino_board(self):
        # update board's frequency as chosen in spin box
        self.board.frequency = int(1000 / self.frequency_spin_box.value())
        self.board.read_results = self.read_results_checkbox.isChecked()
        self.board.save_configutarion = self.save_configuration_checkbox.isChecked()
        # get sensor description from combo box and initialize sensor from it
        if self.add_sensor_combo_box.currentText() != "":
            desc = self.menu.get_sensor_data(str(self.add_sensor_combo_box.currentText()))
            digital_pins = {pin['pin_name']: pin['number'] for pin in desc['pins'] if pin['type'] == 'digital'}
            analog_pins = {pin['pin_name']: pin['number'] for pin in desc['pins'] if pin['type'] == ['analog']}
            self.board.frequency = desc["frequency"]
            self.frequency_spin_box.setValue(int(1000 / self.board.frequency))
            sensor = Sensor(desc['name'], digital_pins, analog_pins)
            self.board.add_sensor_to_board(sensor)
            self.add_sensor_settings_tab(sensor)
            # change the combo box setting back to ""
            self.add_sensor_combo_box.setCurrentIndex(0)

    # remove sensor from board and tabs
    def remove_sensor_tab(self):
        index = self.arduino_settings_tabs.currentIndex()
        key, tab = self.get_sensor_by_index(index)
        self.board.remove_sensor_from_board(tab['sensor'])
        # remove the tab where the button was clicked
        self.arduino_settings_tabs.removeTab(index)
        # update the indices of the other tabs
        for name, tabs in self.sensors_tabs.items():
            tabs['index'] = self.arduino_settings_tabs.indexOf(tabs['tab'])
        # remove the deleted tab from dict
        del self.sensors_tabs[key]

    # get the sensor tab by the tab index
    def get_sensor_by_index(self, index):
        for key in self.sensors_tabs.keys():
            if self.sensors_tabs[key]['index'] == index:
                return key, self.sensors_tabs[key].copy()

    def start_experiment_handler(self):
        if not self.board.sensors:
            self.error_message('no sensors were added to the experiment')
            return
        if self.board.current_experiment is not None:
            self.stop_experiment_handler()
        text, result = QtWidgets.QInputDialog.getText(self.main_window, 'input name', 'Enter experiment name:')
        if result:
            if str(text) == '':
                self.error_message('name must not be empty')
                return
            progress = self.upload_message_box("Uploading arduino project, please wait...")
            # combine all the sensors from all experiments defined
            QtWidgets.qApp.processEvents()
            try:
                self.board.current_experiment = self.menu.combine2(self.board.sensors, str(text))
                progress.setValue(50)
                QtWidgets.qApp.processEvents()
                self.menu.activate_project(self.board.current_experiment, frequency=self.board.frequency,
                                           com_number=self.board.com_number)
                self.update_results_list()
                self.update_projects_list()
            except SystemError as e:
                self.error_message(e.args[0])
            except NotImplementedError as e:
                self.error_message(e.args[0])
            finally:
                progress.setValue(100)

    def error_message(self, message):
        msg = QtWidgets.QMessageBox(self.main_window)
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.resize(300, 250)
        msg.setText(message)
        #msg.setInformativeText(message)
        msg.setWindowTitle("Error window")
        msg.exec_()

    def information_message(self, message, additional_info=''):
        msg = QtWidgets.QMessageBox(self.main_window)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.resize(300, 250)
        msg.setText(message)
        msg.setInformativeText(additional_info)
        msg.setWindowTitle("Info window")
        msg.exec_()

    # TODO find a way to update progress bar more dynamically
    def upload_message_box(self, name):
        progress = QtWidgets.QProgressDialog(name, "Cancel", 0, 100, self.main_window)
        # progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setAutoClose(True)
        progress.setMinimum(0)
        progress.setMaximum(100)
        progress.resize(300, 250)
        progress.setCancelButton(None)
        progress.setWindowTitle("Compilation window")
        progress.show()
        progress.setValue(0)
        return progress


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_main_window()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())


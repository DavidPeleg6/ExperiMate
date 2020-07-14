import os
import time
import FileIO
import PyArduinoBuilder
import threading
import serial

pin_types = {'digital': 'digital', 'analog': 'analog'}
bandwidth = 9600


class Experiment:
    """
    a class responsible for managing the ongoing experiment including initializing and saving results to different formats
    such as graph or result file
    """
    # constructor gets a name, a settings file and a boolean to determine whether or not to save results given
    def __init__(self, name, settings, read_result=False):
        self.name = name
        self.settings = settings
        self.analogs, self.digitals = get_default_pins(settings, name)
        self.observer_thread = ObserverThread(None, None)
        self.read_result = read_result
        self.observers = []

    def get_pin_names(self, pin_type):
        if pin_type == pin_types['digital'] and self.digitals:
            return [pin for pin in self.digitals.values()]
        elif pin_type == pin_types['analog'] and self.analogs:
            return [pin for pin in self.analogs.values()]
        return 0

    # returns a pin by the pin name
    def get_pin(self, name):
        if name in self.digitals.keys():
            return self.digitals[name]
        if name in self.analogs.keys():
            return self.analogs[name]
        return 0

    # add a new observer to send results to
    def add_observer(self, observer):
        if self.read_result:
            self.observers.append(observer)

    # initialize the experiment in a new thread while updating listeners about results
    def start_experiment(self, com_num=False):
        if not com_num:
            com_num = self.settings["port_COM"]
        path = os.path.join(self.settings["projects"], self.name, self.name + ".ino")
        PyArduinoBuilder.build_ino(self.settings["arduino_compiler"], self.settings["arduino_libraries"], path, com_num)
        # start a serial connection
        ser = serial.Serial('COM' + str(com_num), bandwidth, timeout=None)
        if self.read_result:
            read_amount = get_read_amount(self.settings, self.name)
            self.observer_thread = ObserverThread(ser=ser, observers=self.observers.copy(), variable_amonut=read_amount)
            self.observer_thread.daemon = True
            self.observer_thread.start()

    # end the ongoing experiment by replacing it with an empty loop
    def end_experiment(self, com_num):
        # if the experiment is supposed to update on results, stop all observers
        if self.read_result:
            self.observer_thread.stop()
        stop_ongoing_ino(self.settings, com_num)
        # path = os.path.join(self.settings["stop_file"], os.path.basename(self.settings["stop_file"]) + ".ino")
        # PyArduinoBuilder.build_ino(self.settings["arduino_compiler"], self.settings["arduino_libraries"], path, com_num)

    def get_results(self):
        return self.observers


def stop_ongoing_ino(settings, com_num):
    path = os.path.join(settings["stop_file"], os.path.basename(settings["stop_file"]) + ".ino")
    PyArduinoBuilder.build_ino(settings["arduino_compiler"], settings["arduino_libraries"], path, com_num)


# get the default values of the pins of a given sensor
def get_default_pins(settings, name):
    exper_settings = FileIO.get_settings(os.path.join(settings["projects"], name, name + '.json'))
    analog = {pin["pin_name"]: pin for pin in exper_settings["pins"] if pin["type"] == pin_types["analog"]}
    digital = {pin["pin_name"]: pin for pin in exper_settings["pins"] if pin["type"] == pin_types["digital"]}
    return analog, digital


# get the settings and name of experiment and return the amount of results to expect from this experiment
def get_read_amount(settings, name):
    return FileIO.get_settings(os.path.join(settings["projects"], name, name + '.json'))["results_num"]


time_delta = lambda past_time: time.time() - past_time


class ObserverThread(threading.Thread):
    """
    a class responsible for running the observers (the listeners in a different thread
    """
    # gets a serial, and a list of observers to update. also gets the amount of values it should receive from the arduino
    def __init__(self, ser, observers, variable_amonut=0):
        super(ObserverThread, self).__init__()
        self.ser = ser
        self.observers = observers
        self.var_amount = variable_amonut
        self.cur_time = 0
        self.timer = time.time()

    def run(self):
        while True:
            data = {}
            # read the from the arduino and create a dict of values
            for i in range(self.var_amount):
                try:
                    data[self.ser.readline().decode('ascii', errors='ignore').rstrip()] = \
                        self.ser.readline().decode('ascii', errors='ignore').rstrip()
                except:
                    return
            # add timestamp to the data
            self.cur_time += time_delta(self.timer)
            self.timer = time.time()
            data["time"] = self.cur_time
            for observer in self.observers:
                observer.update(data)

    def stop(self):
        # at the end of the loop
        for observer in self.observers:
            observer.update(None)
        self.ser.close()


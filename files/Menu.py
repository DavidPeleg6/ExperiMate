import FileIO
from Experiment import Experiment, stop_ongoing_ino
from ExperimentObserver import CSVObserver, ConsoleObserver, PlotObserver
from InoFile import InoFile
import pandas as pd
import json
import os


class Menu:
    """
    a class responsible for managing the menu = starting stopping experiments and saving results. only one experiment
    can be running at each given moment this class serves as an api for the entire program and is used by the GUI
    """

    # the constructors receives a settings file location containing all parameters and locations needed for running
    def __init__(self, settings_loc):
        self.settings = FileIO.get_settings(settings_loc)
        self.sensors_loc = os.path.relpath(self.settings["sensors_location"])
        self.results_loc = os.path.relpath(self.settings["results"])
        self.experiments = None
        self.current_plot = PlotObserver()
        self.options = ['get default frequency', 'get sensor data', 'get sensors', 'print results', 'activate',
                        'add description', 'add sensor', 'stop', 'exit']

    def get_sensors(self):
        return FileIO.get_sensors(self.settings["sensors_location"])

    def get_dataframe_results(self, name):
        return pd.read_csv(os.path.join(self.settings["results"], name + '.csv'))

    def get_projects(self):
        return FileIO.get_sensors(self.settings["projects"])

    def get_results_names(self):
        return [os.path.splitext(f)[0] for f in os.listdir(self.settings["results"])]

    def get_default_frequency(self):
        return self.settings["default_frequency"]

    def get_default_com(self):
        return int(self.settings["port_COM"])

    def get_sensor_data(self, name):
        description_json = json.loads(FileIO.get_sensor_string(os.path.join(self.settings["sensors_location"], name,
                                                                            name + '.json')))
        return description_json

    def get_project_data(self, name):
        description_json = json.loads(FileIO.get_sensor_string(os.path.join(self.settings["projects"], name,
                                                                            name + '.json')))
        return description_json

    def get_sensor_location(self, name):
        return os.path.join(self.settings["sensors_location"], name, name + '.ino')

    def get_project_location(self, name):
        return os.path.join(self.settings["projects"], name, name + '.ino')

    def get_example_location(self):
        return self.settings["example"]

    def get_current_plot(self):
        return self.current_plot

    # creates a new description file for a sensor by getting a list of pins in json format and a sensor name
    # the format for a pin will be given as an example in separate folder
    def add_description(self, name, pins=None, read_amount=0):
        if not os.path.exists(os.path.join(self.settings["sensors_location"], name)):
            raise Exception("Error, no such sensor")
        if pins is None:
            raise Exception("Error no pins given")
        read_result = False
        if read_amount > 0:
            read_result = True
        json_desc = {"name": name, "pins": pins, "read_results": read_result, "results_num": read_amount}
        FileIO.create_json(os.path.join(self.settings["sensors_location"], name, name + ".json"), json_desc)

    # gets a description dictionary and 2 pins dictionaries and updates the dictionary with them
    def update_description_pins(self, description, dig_pins, anal_pins):
        for pin in description['pins']:
            if pin['type'] == 'digital':
                pin['number'] = dig_pins[pin['pin_name']]
            elif pin['type'] == 'analog':
                print(pin)
                print(anal_pins)
                print(dig_pins)
                pin['number'] = anal_pins[pin['pin_name']]
        return description

    # stop the ongoing experiment. -1 for default
    def stop(self, com_num=-1):
        if com_num == -1:
            com_num = self.settings["port_COM"]
        # if there are no running experiments
        if self.experiments is None:
            stop_ongoing_ino(self.settings, com_num)
            return
        # make the experiment currently running exit and quit safely
        self.experiments.end_experiment(com_num)
        self.experiments = None

    def delete_sensor(self, name):
        FileIO.delete_folder(os.path.join(self.settings["sensors_location"], name))

    def delete_project(self, name):
        FileIO.delete_folder(os.path.join(self.settings["projects"], name))

    def delete_result(self, result):
        FileIO.delete_file(os.path.join(self.settings["results"], result + '.csv'))

    def delete_description(self, name):
        FileIO.delete_file(os.path.join(self.settings["sensors_location"], name, name + '.json'))

    def add_sensor(self, name, code_path=None, image_path=None):
        if image_path is None:
            image_path = self.settings['image']
        if code_path is None:
            pass
        FileIO.add_folder(base_address=self.settings["sensors_location"], name=name, source_code=code_path,
                          files=[image_path])

    def delete_configuration(self, name):
        FileIO.delete_folder(os.path.join(self.settings["projects"], name))

    def get_experiment(self):
        return self.experiments

    def add_new_sensor(self, location):
        full_name = os.path.basename(location)
        name = full_name.split('.')[0]
        ino_file = InoFile(name, FileIO.get_sensor_string(location))
        FileIO.add_folder(base_address=self.settings["sensors_location"], name=name,
                          string_code=str(ino_file), files=[self.settings['image']])
        FileIO.create_json(os.path.join(self.settings["sensors_location"], name, name + ".json"),
                           ino_file.get_description())

    # gets a list of sensor names and parses it into an experiment
    def combine(self, sensors, name=None):
        for sensor in sensors:
            if sensor not in self.get_sensors():
                raise Exception("Error, sensor not found")
        # create ino object for the first sensor
        description_json = json.loads(FileIO.get_sensor_string(os.path.join(self.settings["sensors_location"],
                                                                            sensors[0], sensors[0] + '.json')))
        ino_file = InoFile(sensors[0], FileIO.get_sensor_string(
            os.path.join(self.settings["sensors_location"], sensors[0], sensors[0] + ".ino")), description_json)
        # create more ino files and combine the with the first one by one
        for i in range(1, len(sensors)):
            description_json1 = json.loads(FileIO.get_sensor_string(
                os.path.join(self.settings["sensors_location"], sensors[i], sensors[i] + '.json')))
            ino_file1 = InoFile(sensors[i], FileIO.get_sensor_string(
                os.path.join(self.settings["sensors_location"], sensors[i], sensors[i] + ".ino")), description_json1)
            ino_file.combine(ino_file1)

        # add the combined experiment
        if name is not None:
            description_json['name'] = name
        exper_name = description_json['name']
        FileIO.add_folder(base_address=self.settings["sensors_location"], name=exper_name, string_code=str(ino_file),
                          files=[self.settings['image']])
        FileIO.create_json(os.path.join(self.settings["sensors_location"],
                                        exper_name, exper_name + ".json"), ino_file.get_description())

    # gets a list of sensor objects, parse's sensors and combines them into an experiment
    # this will be used for project adding
    # and returns the experiment name received
    def combine2(self, sensors, name=None):
        for sensor in sensors:
            if sensor.name not in self.get_sensors() and sensor.name not in self.get_projects():
                raise SystemError("Error, sensor not found")
        # TODO find a way to add multiple sensors of the same kind
        sensor_names = [sensor.name for sensor in sensors]
        for sens_name in sensor_names:
            if sensor_names.count(sens_name) > 1:
                raise NotImplementedError('you can only have one instance of each sensor')
        # try finding the configuration in sensors and if its not there, find it in projects
        try:
            # create ino object for the first sensor
            description_json = json.loads(FileIO.get_sensor_string(os.path.join(
                self.settings["sensors_location"], sensors[0].name, sensors[0].name + '.json')))
            print(str(sensors[0]))
            description_json = self.update_description_pins(description_json, sensors[0].dig_pins, sensors[0].anal_pins)
            ino_file = InoFile(sensors[0].name, FileIO.get_sensor_string(os.path.join(self.settings["sensors_location"],
                                                                                      sensors[0].name, sensors[0].name + ".ino")), description_json)
        except FileNotFoundError:
            # create ino object for the first sensor
            description_json = json.loads(FileIO.get_sensor_string(os.path.join(
                self.settings["projects"], sensors[0].name, sensors[0].name + '.json')))
            description_json = self.update_description_pins(description_json, sensors[0].dig_pins, sensors[0].anal_pins)
            ino_file = InoFile(sensors[0].name, FileIO.get_sensor_string(os.path.join(self.settings["projects"],
                                                                                      sensors[0].name, sensors[0].name + ".ino")), description_json)
        # create more ino files and combine the with the first one by one
        for i in range(1, len(sensors)):
            try:
                description_json1 = json.loads(FileIO.get_sensor_string(
                    os.path.join(self.settings["sensors_location"], sensors[i].name, sensors[i].name + '.json')))
                description_json1 = self.update_description_pins(description_json1, sensors[i].dig_pins, sensors[i].anal_pins)
                ino_file1 = InoFile(sensors[i].name, FileIO.get_sensor_string(
                    os.path.join(self.settings["sensors_location"], sensors[i].name, sensors[i].name + ".ino")), description_json1)
                ino_file.combine(ino_file1)
            except FileNotFoundError:
                description_json1 = json.loads(FileIO.get_sensor_string(
                    os.path.join(self.settings["projects"], sensors[i].name, sensors[i].name + '.json')))
                description_json1 = self.update_description_pins(description_json1, sensors[i].dig_pins,
                                                                 sensors[i].anal_pins)
                ino_file1 = InoFile(sensors[i].name, FileIO.get_sensor_string(
                    os.path.join(self.settings["projects"], sensors[i].name, sensors[i].name + ".ino")),
                                    description_json1)
                ino_file.combine(ino_file1)

        # add the combined experiment
        if name is not None:
            description_json['name'] = name
        exper_name = description_json['name']
        FileIO.add_folder(base_address=self.settings["projects"], name=exper_name, string_code=str(ino_file),
                          files=[self.settings['image']])
        FileIO.create_json(os.path.join(self.settings["projects"],
                                        exper_name, exper_name + ".json"), ino_file.get_description())
        return exper_name

    # this method receives a name of experiment to be executed along with a list of analog and digital
    # pins to be changed from default values (in case of empty lists, default values will be taken)
    # and a boolean for whether to read results (and a com number the arduino is connected to).
    # the method starts the appropriate experiment with the given parameters
    def activate(self, name, pins=None, com_number=None, frequency=None):
        if com_number is None:
            com_number = int(self.settings["port_COM"])
        if self.experiments is not None:
            self.stop(com_number)
        if name not in self.get_sensors():
            raise Exception("Error, sensor not found")
        if name + '.json' not in FileIO.get_sensors(os.path.join(self.settings["sensors_location"], name)):
            raise Exception("Error, sensor has no description file")
        description_json = json.loads(FileIO.get_sensor_string(os.path.join(self.settings["sensors_location"], name,
                                                                            name + '.json')))
        # initialize the ino file according to parameters
        # initialize the pins according to parameters
        ino_file = InoFile(name, FileIO.get_sensor_string(os.path.join(self.settings["sensors_location"], name,
                                                                       name + ".ino")), description_json)
        if pins is not None:
            for pin in pins:
                if ino_file.get_pin(pin['pin_name']) is None:
                    raise Exception("Error, no such pin in descriptions file")
                else:
                    ino_file.change_pin_power(pin['pin_name'], pin['power'])
                    ino_file.change_pin_number(pin['pin_name'], pin['number'])
        if frequency is not None:
            ino_file.change_frequency(frequency)
        # save the ino file and start the experiment
        FileIO.create_json(os.path.join(self.settings["sensors_location"], name, name + ".json"),
                           ino_file.get_description())
        FileIO.create_sensor(os.path.join(self.settings["sensors_location"], name, name + ".ino"),
                             str(ino_file))
        # start an experiment in a different thread and add the appropriate observers.
        # currently it also prints results to screen but in the future it will only be printing to a csv file
        exper = Experiment(name=name, settings=self.settings, read_result=ino_file.description["read_results"])
        self.experiments = exper
        exper.add_observer(CSVObserver(FileIO.get_free_name(self.settings['results'], exper.name)))
        # for printing to screen
        exper.add_observer(ConsoleObserver())
        try:
            thread = exper.start_experiment(com_number)
        except Exception as e:
            self.experiments = None
            # raise SystemError('arduino compilation failed, either no arduino compiler is installed or COM number is wrong')
            raise SystemError(e.args[0])
        return thread

    # this method is the same as activate but used for activating projects
    def activate_project(self, name, pins=None, com_number=None, frequency=None):
        if com_number is None:
            com_number = int(self.settings["port_COM"])
        if self.experiments is not None:
            self.stop(com_number)
        if name not in self.get_projects():
            raise SystemError("No project found")
        if name + '.json' not in FileIO.get_sensors(os.path.join(self.settings["projects"], name)):
            raise SystemError("no description file was found for this project")
        description_json = json.loads(FileIO.get_sensor_string(os.path.join(self.settings["projects"], name,
                                                                            name + '.json')))
        # initialize the ino file according to parameters
        # initialize the pins according to parameters
        ino_file = InoFile(name, FileIO.get_sensor_string(os.path.join(self.settings["projects"], name,
                                                                       name + ".ino")), description_json)
        if pins is not None:
            for pin in pins:
                if ino_file.get_pin(pin['pin_name']) is None:
                    raise Exception("Error, no such pin in descriptions file")
                else:
                    ino_file.change_pin_power(pin['pin_name'], pin['power'])
                    ino_file.change_pin_number(pin['pin_name'], pin['number'])
        if frequency is not None:
            ino_file.change_frequency(frequency)
        # save the ino file and start the experiment
        FileIO.create_json(os.path.join(self.settings["projects"], name, name + ".json"),
                           ino_file.get_description())
        FileIO.create_sensor(os.path.join(self.settings["projects"], name, name + ".ino"),
                             str(ino_file))
        # start an experiment in a different thread and add the appropriate observers.
        # currently it also prints results to screen but in the future it will only be printing to a csv file
        exper = Experiment(name=name, settings=self.settings, read_result=ino_file.description["read_results"])
        self.experiments = exper
        exper.add_observer(CSVObserver(FileIO.get_free_name(self.settings['results'], exper.name)))
        # for printing to screen
        exper.add_observer(ConsoleObserver())
        self.current_plot = PlotObserver()
        exper.add_observer(self.current_plot)
        try:
            thread = exper.start_experiment(com_number)
        except Exception as e:
            self.experiments = None
            #raise SystemError('arduino compilation failed, either no arduino compiler is installed or COM number is wrong')
            raise SystemError(str(e))
        return thread


class CmdMenu:
    """
    this class is the CMD interface of the program. it holds the menu and will be replaced by GUI
    """

    def __init__(self, settings_loc):
        self.menu = Menu(settings_loc)

    # this method is the main menu of the cmd interface. this will be replaced by the GUI later
    def main_menu(self):
        while True:
            option = input("choose command to be executed: ")
            if option == 'get sensors':
                print(self.menu.get_sensors())
            elif option == 'print results':
                print(self.menu.get_results_names())
            elif option == 'activate':
                print("experiments: {0}".format(str(self.menu.get_sensors())))
                exp = input("choose experiment/sensor to execute: ")
                if exp not in self.menu.get_sensors():
                    print("invalid sensor")
                    continue
                self.start_activation(Experiment(name=exp, settings=self.menu.settings))
            elif option == 'add sensor':
                image_loc = input("put the address of the image or NONE for default image")
                sensor_loc = input("put the address of the source code for the sensor")
                name = input("put the name of the sensors to be added")
                if image_loc == "NONE":
                    image_loc = None
                self.menu.add_sensor(name, sensor_loc, image_loc)
            elif option == "add description":
                name = input("enter sensor name to add description: ")
                self.menu.add_description(name, self.get_user_pins())
            elif option == 'stop':
                self.menu.stop(int(input("com number (-1 for default): ")))
            elif option == 'exit':
                break
            else:
                print('valid commands: ' + str(self.menu.options))

    # a method to initialize activation of an experiment, getting all necessary values
    def start_activation(self, exp):
        a_pins, d_pins = [], []
        read_result = False
        com_number = int(input("enter the port the arduino is connected to (-1 for default): "))
        if com_number == -1:
            com_number = None
        print("for the sensor: {0}\n the analog pins are:\n{1}\n and the digital pins are:\n{2}\n"
              .format(exp.name, exp.get_pin_names('analog'), exp.get_pin_names('digital')))
        if input("would you like to change analog pin param? (yes/no): ") == "yes":
            a_pins = self.change_pins(exp, 'analog')
        if input("would you like to change digital pin param? (yes/no): ") == "yes":
            d_pins = self.change_pins(exp, 'digital')
        if input("would you like to save results? (yes/no): ") == "yes":
            read_result = True
        self.menu.activate(exp.name, a_pins, d_pins, com_number)

    # changes pins depending on the pin type requested, returns a list of lists the user would like to change
    # in the given experiment. this method is used by start_activation
    @staticmethod
    def change_pins(exp, pin_type):
        pins = []
        while True:
            pin_name = input("enter pin name you would like to change (None for stopping): ")
            if pin_name == "None":
                break
            # if the pin is not in the appropriate list try again
            if pin_name not in exp.get_pin_names(pin_type):
                print("invalid name")
                continue
            power = input("select power (HIGH/LOW/NO): ")
            if power != "NO" and (power == "HIGH" or power == "LOW"):
                exp.change_pin_power(pin_name, power)
            frequency = input("select frequency (float/NO)")
            if frequency != "NO":
                exp.change_pin_frequency(pin_name, float(frequency))
            number = input("select number (int/NO)")
            if number != "NO":
                exp.change_pin_number(pin_name, int(number))
            # add the now changed pin to the list of pins to be changed in activation
            pins.append(exp.get_pin(pin_name))
        return pins

    # this is a helping function for setting a new description file
    def get_user_pins(self):
        user_pins = []
        while True:
            pin_name = input("please enter pin name (None to stop) ")
            if pin_name == "None":
                break
            pin_type = input("put pin type (analog/digital): ")
            pin_num = int(input("put pin number: "))
            power = input("input pin power (HIGH/LOW/default): ")
            if power == 'default':
                power = self.menu.settings["default_power"]
            frequency = input("enter frequency ")
            if frequency == 'default':
                frequency = self.menu.settings["default_frequency"]
            user_pins.append({"pin_name": pin_name, "power": power, "frequency": frequency, "number": pin_num,
                              "type": pin_type})
        return user_pins

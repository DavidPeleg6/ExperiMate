import json

# a list containing all needed values as viewed in examples.ino and location of print
segment_names = {"libraries": [], "pins : digital": [], "pins : analog": [], "frequency": [], "global": [], "setup": [],
                 "sleep for 1 sec": [], "loop start": [], "print statement": [], "loop end": [], "help functions": []}

json_format = {"name": "temp",
               "pins": [{"pin_name": "temp1", "power": "HIGH", "number": 8, "type": "digital"}],
               "frequency": 1000,
               "read_results": False,
               "results_num":  0}


# gets a string line and parses the data and number out of it as a tuple (name, data)
def get_data_from_line(line):
    split_line = line.split()
    for i in range(len(line.split())):
        if split_line[i + 1] == "=":
            return split_line[i], split_line[i + 2]


def change_data_from_line(line, data):
    split_line = line.split()
    for i in range(len(split_line)):
        if split_line[i + 1] == "=":
            split_line[i + 2] = str(data)
            return " ".join(split_line)


# get a list of strings each representing a function and parse it to a dictionary by name and function
def get_help_functions(func_list):
    functions = {}
    # if the list is empty
    if len(func_list.split("// ##")) <= 1:
        return
    for func in func_list.split("// ## "):
        temp_func = func.splitlines()
        functions[temp_func[0]] = temp_func[1:]
    return functions


class InoFile:
    """
    this class is an object representation of an arduino.ino file. its to_string method will return a string that
    can be saved into an ino file. it will receive a string representing a file to parse from. it will also create the
    description file (a string representation of it).
    """
    # get a sensor's arduino file and the sensors name
    def __init__(self, arduino_name, arduino_string, sensor_description=None):
        self.segments = {"libraries": [], "pins : digital": [], "pins : analog": [], "frequency": [], "global": [], "setup": [],
                 "sleep for 1 sec": [], "loop start": [], "print statement": [], "loop end": [], "help functions": []}

        self.parse_segments(arduino_string)
        if sensor_description is None:
            self.description = {"name": "temp",
                                "pins": [{"pin_name": "temp1", "power": "HIGH", "number": 8, "type": "digital"}],
                                "frequency": 1000, "read_results": False, "results_num":  0}
            self.parse_description(arduino_name)
        else:
            self.description = sensor_description
        self.change_frequency(self.description["frequency"])
        for pin in self.description["pins"]:
            self.change_pin_number(pin["pin_name"], pin["number"])

    def parse_description(self, sensor_name):
        self.description["name"] = sensor_name
        # reset the pins in the description and create a new pin list
        self.description["pins"] = []
        for line in self.segments["pins : digital"]:
            data_tuple = get_data_from_line(line)
            # TODO change to remove power
            print(data_tuple)
            if data_tuple is None:
                break
            self.description["pins"].append({"pin_name": data_tuple[0], "power": "HIGH", "number": data_tuple[1], "type": "digital"})
        # repeat for analog pins
        for line in self.segments["pins : analog"]:
            data_tuple = get_data_from_line(line)
            if data_tuple is None:
                break
            self.description["pins"].append({"pin_name": data_tuple[0], "power": "HIGH", "number": data_tuple[1], "type": "analog"})
        if len(self.segments["print statement"]) - 1 > 0:
            self.description["read_results"] = True
            self.description["results_num"] = len(self.segments["print statement"]) - 1

    # gets a file string and return it as segments
    def parse_segments(self, file_string):
        # assign segments to the dictionary
        for temp_segment in file_string.split("// **"):
            for key in self.segments.keys():
                if key in temp_segment:
                    self.segments[key].extend([line.rstrip() for line in temp_segment.splitlines()])
                    self.segments[key] = self.segments[key][1:]
                    break

    # combines this sensor with another one to create an experiment. gets a InoFile object and add it to itself
    def combine(self, other):
        # add libraries
        for library in other.segments["libraries"]:
            if library not in self.segments["libraries"]:
                self.segments["libraries"].append(library)
        # check no pins are being reused
        for other_pin in other.description["pins"]:
            for self_pin in self.description["pins"]:
                if other_pin["number"] == self_pin["number"] and other_pin["type"] == self_pin["type"]:
                    raise SystemError("you cant have 2 sensors with the same pin usage")
        # add the pins to self list
        self.segments["pins : digital"].extend(other.segments["pins : digital"])
        self.segments["pins : analog"].extend(other.segments["pins : analog"])
        # add the other global variables to the list
        self.segments["global"].extend(other.segments["global"])
        # take out all redundant lines that already appear in self and add the rest to self setup segment
        self.segments["setup"].extend([line for line in other.segments["setup"] if line not in self.segments["setup"]])
        # take out the head and append all the rest
        self.segments["loop start"].extend(other.segments["loop start"][1:])
        self.segments["print statement"].extend(other.segments["print statement"])
        # join the list into a string and send it for parsing if the list is not empty
        if other.segments["help functions"]:
            help_funcs = get_help_functions("".join(other.segments["help functions"]))
            self.segments["help functions"].extend([help_funcs[key] for key in help_funcs.keys() if key not in self.segments["help functions"]])
        # add other's description file
        self.combine_description(other)

    # combine the description of 2 ino objects
    def combine_description(self, other):
        # add others name to self
        self.description['name'] += (' ' + other.description['name'])
        # add other's pins to self
        self.description['pins'].extend(other.description['pins'])
        # frequency will remain as the first sensor
        # read results field will be determined if either one of the sensors has the field set to true
        if self.description['read_results'] or other.description['read_results']:
            self.description['read_results'] = True
        # update the amount of results given
        self.description['results_num'] += other.description['results_num']

    # return the the description dictionary
    def get_description(self):
        return self.description.copy()

    # returns a pin if its name is in the self description and None if its not in it
    def get_pin(self, name):
        for pin in self.description["pins"]:
            if pin["pin_name"] == name:
                return pin
        return None

    # TODO probably delete this = functionality might be taken out
    def change_pin_power(self, name, power):
        for pin in self.description["pins"]:
            if pin["pin_name"] == name:
                pin["power"] = power

    def change_frequency(self, frequency):
        self.description["frequency"] = int(frequency)
        self.segments["frequency"] = [change_data_from_line(self.segments["frequency"][0], frequency)]

    def change_pin_number(self, name, number):
        for pin in self.description["pins"]:
            if pin["pin_name"] == name:
                pin["number"] = number
        # find the pin in the digitals
        for i in range(len(self.segments["pins : digital"])):
            pin_data = get_data_from_line(self.segments["pins : digital"][i])
            # if the pin is in the names change its number
            if pin_data[0] == name:
                self.segments["pins : digital"][i] = change_data_from_line(self.segments["pins : digital"][i], number)
                return
        # find the pin in the analogs
        for i in range(len(self.segments["pins : digital"])):
            pin_data = get_data_from_line(self.segments["pins : analog"][i])
            # if the pin is in the names change its number
            if pin_data[0] == name:
                self.segments["pins : analog"][i] = change_data_from_line(self.segments["pins : analog"][i], number)

    # ths method overrides the to string method to return a printable object
    def __str__(self):
        printable = ''
        for key in self.segments.keys():
            printable += ("// ** " + key + "\n")
            printable += "\n".join(self.segments[key])
        return printable







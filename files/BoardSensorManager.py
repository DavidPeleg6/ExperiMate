class Board:

    def __init__(self, frequency, com_number=None, read_results=True, save_configuration=True):
        # frequency is given in Hz
        self.frequency = frequency
        self.dig_ports = [i + 1 for i in range(13)]
        self.anal_ports = [i + 1 for i in range(5)]
        self.com_number = com_number
        self.read_results = read_results
        self.save_configutarion = save_configuration
        self.sensors = []
        self.current_experiment = None
        self.current_result = None
        self.cur_name = ''

    def add_sensor_to_board(self, sensor):
        """ for when validation is added
        new_dig, new_anal = self.dig_ports.copy(), self.anal_ports.copy()
        for pin, num in sensor.dig_pins.items():
            new_dig.remove(num)
        for pin, num in sensor.anal_pins.items():
            new_anal.remove(num)
        self.dig_ports, self.anal_ports = new_dig, new_anal
        """
        self.sensors.append(sensor)

    def remove_sensor_from_board(self, sensor):
        """for when validation is added
        self.dig_ports.extend([num for pin, num in sensor.dig_pins.items()])
        self.dig_ports.sort()
        self.anal_ports.extend([num for pin, num in sensor.anal_pins.items()])
        self.anal_ports.sort()
        """
        self.sensors.remove(sensor)

    # swap an old sensor definition for a new one
    def update_sensor(self, old_sensor, new_sensor):
        self.sensors[self.sensors.index(old_sensor)] = new_sensor


    """ for when validation is added
    def update_port_num(self, old_num, num, digital_bool):
        if digital_bool:
            self.dig_ports.remove(old_num)
            self.dig_ports.append(num)
        else:
            self.anal_ports.remove(old_num)
            self.anal_ports.append(num)
    """


class Sensor:
    """ represents a sensor in the board """
    # gets sensor name, digital pin dictionary, analog pin dictionary
    def __init__(self, name, dig_pins, anal_pins):
        self.name = name
        self.dig_pins = dig_pins
        self.anal_pins = anal_pins

    def update_pin_num(self, name, new_num, digital_bool):
        if digital_bool:
            old_num = self.dig_pins[name]
            self.dig_pins[name] = new_num
        else:
            old_num = self.anal_pins[name]
            self.anal_pins[name] = new_num
        return old_num




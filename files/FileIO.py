import json
import os
import shutil


# get settings
def get_settings(settings_loc):
    if not os.path.exists(settings_loc):
        raise SystemError("settings file " + settings_loc + "could not be found")
    with open(settings_loc, 'r') as file:
        return json.loads(file.read())


# enumerates files in directory and returns the name + free number
def get_free_name(location, name):
    files = [f.split('.')[0] for f in os.listdir(location) if os.path.isfile(os.path.join(location, f))]
    if name not in files:
        return os.path.join(location, name)
    for i in range(1, len(files) + 2):
        if name + str(i) not in files:
            return os.path.join(location, name + str(i))
    raise SystemError("getting free name failed")


def create_json(location, json_file):
    with open(location, 'w') as file:
        file.write(json.dumps(json_file))


def get_sensors(sensors):
    return os.listdir(sensors)


def get_sensors_image(name):
    if not os.path.exists('../../sensors/' + name + '/' + name + '.jpg') or \
            not os.path.exists('../../sensors/' + name + '/' + name + '.png'):
        if not os.path.exists('../../sensors/' + name + '/default_img.jpg'):
            shutil.copyfile('images/' + 'default_img.jpg', '../../sensors/' + name + '/default_img.jpg')
        return '../../sensors/' + name + '/default_img.jpg'
    elif os.path.exists('../../sensors/' + name + '/' + name + '.jpg'):
        return '../../sensors/' + name + '/' + name + '.jpg'
    elif os.path.exists('../../sensors/' + name + '/' + name + '.png'):
        return '../../sensors/' + name + '/' + name + '.png'


# get a location and delete the entire sensor
def delete_folder(location):
    if not os.path.exists(location):
        raise SystemError("Error, could not find sensor in location " + location)
    shutil.rmtree(location, ignore_errors=True)


# delete a single file (used for delete description)
def delete_file(location):
    if not os.path.exists(location):
        return
        # raise SystemError("Error, could not find sensor in location " + location)
    os.remove(location)


# get a name (location) of string and returns a string representation of that sensor
def get_sensor_string(location):
    with open(location, 'r') as file:
        return file.read()


# creates a sensor from given code
def create_sensor(location, code):
    with open(location, 'w') as file:
        file.write(code)


# create folder with the name of the source code file and copy everything to it. method can get the code in a file
# or a string type but wont accept both missing
def add_folder(base_address, name, files, source_code=None, string_code=None):
    # get file name
    path = os.path.join(base_address, name)
    new_src_name = os.path.join(base_address, name, name + '.ino')
    if not os.path.exists(path):
        os.makedirs(path)
    if source_code is not None:
        shutil.move(source_code, new_src_name)
    elif string_code is not None:
        create_sensor(new_src_name, string_code)
    else:
        raise SystemError("no code to be applied (source_code/string_code)")
    for file in files:
        shutil.copy(src=file, dst=path)




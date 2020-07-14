from Menu import Menu
import time
from Menu import CmdMenu


# json file names
Settings = 'settings_file.json'
Settings2 = 'settings2.json'

# main
# menu = CmdMenu(settings_loc=Settings)
# thread = menu.main_menu()
menu = Menu(settings_loc=Settings)
menu.combine(['sonar', 'blink'])
menu.activate('sonar blink')
#menu.activate('blink')
#menu.activate('sonar')
#menu.activate('sonar', pins=[{"pin_name": "trigPin", "power": "HIGH", "number": 11, "type": "digital"}], frequency=100)
time.sleep(20)
menu.stop()
print("experiment started")


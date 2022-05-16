import winreg


class DllEdit:
    """docstring for DllEdit"""
    def __init__(self):
        self.default_value = '1200'
        #self.dll_path = "C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta/game/dota/bin/win64/client.dll"
    
    @property
    def dll_data(self):
        # Read bytes from .dll and covert them to readable format ansi
        file = open(self.dll_path, "rb")
        data = file.read()
        data = data.decode("ansi")
        file.close()
        return data
    
    @property
    def dll_path(self):
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        asubkey = winreg.OpenKey(aKey, 'Steam App 570')
        #print(winreg.QueryValueEx(asubkey, "DisplayName")[0])
        return winreg.QueryValueEx(asubkey, "InstallLocation")[0] + '/game/dota/bin/win64/client.dll'

    @property
    def current_distance(self):
        f_index = self.dll_data.find('r_propsmaxdist')
        return self.dll_data[f_index+16:f_index+20]

    def update_distance(self, new_value):
        # Do some stuff with data, as replacement of one string to another.
        #data = data.replace(search_value, new_value)
        old_data = self.dll_data
        f_index = old_data.find('r_propsmaxdist')
        new_data = old_data[:f_index+16] + new_value + old_data[f_index+20:]
        #print(data[f_index:f_index+25])

        # Encode back to bytes content of file
        new_data = new_data.encode("ansi")
        file = open(self.dll_path, "wb")
        file.write(new_data)
        file.close()

if __name__ == "__main__":
    de = DllEdit()
    print(f'Current distance: {de.current_distance}')
    new_distance = input('Set new distance: ')
    de.update_distance(new_distance)
    input(f'Done! New distance is {new_distance}. Press "Enter" to continue...')
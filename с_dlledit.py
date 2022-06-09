from itertools import chain
import winreg
from functools import cached_property


class DllEdit:
    """docstring for DllEdit"""

    def __init__(self):
        self.default_value = '1200'
        self.search_range = 30
        self.key_words = [
            'Maximum visible distance',
            'r_propsmaxdist', 
            'sv_noclipaccelerate',
        ]
        #self.dll_path = "C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta/game/dota/bin/win64/client.dll"

    @cached_property
    def dll_path(self):
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                              0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        asubkey = winreg.OpenKey(aKey, 'Steam App 570')
        #print(winreg.QueryValueEx(asubkey, "DisplayName")[0])
        # return "client_old.dll"
        return winreg.QueryValueEx(asubkey, "InstallLocation")[0] + '/game/dota/bin/win64/client.dll'

    @cached_property
    def dll_data(self):
        # Read bytes from .dll and covert them to readable format ansi
        file = open(self.dll_path, "rb")
        data = file.read()
        data = data.decode("ansi")
        file.close()
        return data

    @cached_property
    def indexes(self):
        result = {
            'start': 0,
            'end': 0
        }

        for key_word in self.key_words:
            w_index_start = self.dll_data.find(key_word)
            search_range = chain(range(-self.search_range, 0),
                                 range(len(key_word), self.search_range+len(key_word)))

            for i in search_range:
                s_index = w_index_start+i
                e_index = w_index_start+i+4
                pv = self.dll_data[s_index:e_index]
                if(pv.isdigit() and len(pv) == 4):
                    result['start'] = s_index
                    result['end'] = e_index

        return result

    @property
    def current_distance(self):
        result = self.dll_data[self.indexes['start']:self.indexes['end']]

        if len(result) != 4:
            raise Exception("Сan't get current distance :.(")

        return result

    def update_distance(self, new_value):
        # Do some stuff with data, as replacement of one string to another.
        new_data = self.dll_data[:self.indexes['start']] + \
            str(new_value) + self.dll_data[self.indexes['end']:]
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
    input(
        f'Done! New distance is {new_distance}. Press "Enter" to continue...')

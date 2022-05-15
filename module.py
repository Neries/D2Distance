dll_path = "C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta/game/dota/bin/win64/client.dll"
#dll_path = 'client.dll'
default_value = '1200'
search_value = default_value

def get_dll_data():
    # Read bytes from .dll and covert them to readable format ansi
    file = open(dll_path, "rb")
    data = file.read()
    data = data.decode("ansi")
    file.close()
    return data

def update_dll(data, new_value):
    # Do some stuff with data, as replacement of one string to another.
    #data = data.replace(search_value, new_value)
    f_index = data.find('r_propsmaxdist')
    data = data[:f_index+16] + new_value + data[f_index+20:]
    #print(data[f_index:f_index+25])

    # Encode back to bytes content of file
    data = data.encode("ansi")
    file = open(dll_path, "wb")
    file.write(data)
    file.close()

def get_current_distance(data):
    f_index = data.find('r_propsmaxdist')
    return data[f_index+16:f_index+20]


if __name__ == "__main__":
    print('Hi there!')
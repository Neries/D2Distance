import shutil
import os, sys
import PySimpleGUI as sg
from module import *

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

default_replace_value = '1375'

try:
    dll_data = get_dll_data()
    current_distance = get_current_distance(dll_data)
except Exception as e:
    sg.popup('Error', str(e))

sg.theme('DarkGreen3')   # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Current distance:', tooltip=f'Default is {default_value}'), sg.Text(current_distance, text_color='green', key='current_distance')],
            [sg.Text('Set new distance:'), sg.InputText(default_replace_value, size=(10, 1), key='new_maxdist')],
            [sg.Checkbox('Make reserve copy', key='make_reserve_copy')],
            [sg.Button('Edit'), sg.Button('Exit'), sg.Text('', text_color='green', key='out')]]


image_path = resource_path("app.ico")
print(image_path)
# Create the Window
window = sg.Window('D2Distance', layout, alpha_channel=0.9, icon=image_path)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break

    if event == 'Edit':
        new_maxdist = values['new_maxdist']
        out = {'text': '', 'text_color': ''}

        if new_maxdist.isnumeric() and len(new_maxdist) == 4:
            try:
                if values['make_reserve_copy']:
                    shutil.copyfile(dll_path, "client.dll-copy")

                update_dll(dll_data, new_maxdist)
                window['current_distance'].update(new_maxdist)
                out['text'] = '✔️Sucess'
                out['text_color'] = 'green'
            except Exception as e:
                out['text'] = '❌Error'
                out['text_color'] = 'red'
                sg.popup(out['text'], str(e))
        else:
            out['text'] = '⚠️ Wrong data!'
            out['text_color'] = 'orange'
            sg.popup(out['text'], f'New value must be a numeric and contain 4 digits.\nYou entered: {new_maxdist}', keep_on_top=True)

        window['out'].update(out['text'], text_color=out['text_color'])
        window['make_reserve_copy'].update(False)
        
    print('You entered ', values['new_maxdist'])

window.close()
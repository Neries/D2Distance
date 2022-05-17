import shutil
import PySimpleGUI as sg
from с_dlledit import DllEdit

default_replace_value = '1375'

sg.theme('DarkGreen3')   # Add a touch of color

try:
    de = DllEdit()
    cd = de.current_distance
except Exception as e:
    print(str(e))
    sg.popup('Error', str(e))

# All the stuff inside your window.
layout = [[sg.Text('Current distance:', tooltip=f'Default is {de.default_value}'), sg.Text(cd, text_color='green', key='current_distance')],
          #   [sg.Text('Set new distance:'), sg.InputText(default_replace_value, size=(10, 1), key='new_maxdist')],
          [sg.Text('Set new distance:'), sg.Slider((1000, 2000), cd, orientation='h',
                                                   key='new_maxdist', font='Courier 8', text_color='green')],
          [sg.Checkbox('Make reserve copy', key='make_reserve_copy')],
          [sg.Button('Save'), sg.Button('Exit'), sg.Text('', text_color='green', key='out')]]

# Create the Window
window = sg.Window('D2Distance', layout, alpha_channel=0.9, icon='app.ico')

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
        break

    if event == 'Save':
        new_maxdist = int(values['new_maxdist'])
        out = {'text': '', 'text_color': ''}

        try:
            if values['make_reserve_copy']:
                shutil.copyfile(de.dll_path, "client.dll-copy")

            de.update_distance(new_maxdist)
            window['current_distance'].update(new_maxdist)
            out['text'] = 'Success ✔️'
            out['text_color'] = 'green'
        except Exception as e:
            out['text'] = 'Error ❌'
            out['text_color'] = 'red'
            sg.popup(out['text'], str(e))

        window['out'].update(out['text'], text_color=out['text_color'])
        window['make_reserve_copy'].update(False)

    print('You entered ', values['new_maxdist'])

window.close()

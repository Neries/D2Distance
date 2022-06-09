import shutil
import PySimpleGUI as sg
from с_dlledit import DllEdit
import os

sg.theme('DarkGreen3')   # Add a touch of color

version = '0.4'

dist = {
    'min': 1000,
    'def': 1200,
    'opt': 1375,
    'max': 2000
}

try:
    de = DllEdit()
    cd = de.current_distance
except Exception as e:
    print(str(e))
    sg.popup('Error', str(e))

# All the stuff inside your window.
layout = [[ sg.Slider((dist['min'], dist['max']), cd, orientation='h', resolution=5, s = (28,None), border_width=5, tooltip='Set new distance',
                                                   key='new_maxdist', font='Courier 8', text_color='green')],
          [sg.Button('Min', tooltip=dist['min']), sg.Button('Default', tooltip=dist['def']), sg.Button('Optimal', tooltip=dist['opt']), sg.Button('Max', tooltip=dist['max'])],
          [sg.Checkbox('Make reserve copy', key='make_reserve_copy')],
          [sg.Button('Save'), sg.Button('Exit'), sg.Text('', text_color='green', key='out')]]


root = os.path.split(__file__)[0]
icon_path = os.path.join(root, 'app.ico')

# Create the Window
window = sg.Window(f'D2Distance | v{version}', layout, alpha_channel=0.9, icon=icon_path, resizable=True)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
        break
    
    if event == 'Min':
        window['new_maxdist'].update(dist['min'])
        
    if event == 'Default':
        window['new_maxdist'].update(dist['def'])
        
    if event == 'Optimal':
        window['new_maxdist'].update(dist['opt'])
        
    if event == 'Max':
        window['new_maxdist'].update(dist['max'])

    if event == 'Save':
        new_maxdist = int(values['new_maxdist'])
        out = {'text': '', 'text_color': ''}

        try:
            if values['make_reserve_copy']:
                shutil.copyfile(de.dll_path, "client.dll-copy")

            de.update_distance(new_maxdist)
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

import shutil
import PySimpleGUI as sg
import с_dlledit

default_replace_value = '1375'

try:
    de = с_dlledit.DllEdit()
except Exception as e:
    sg.popup('Error', str(e))

sg.theme('DarkGreen3')   # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Current distance:', tooltip=f'Default is {de.default_value}'), sg.Text(de.current_distance, text_color='green', key='current_distance')],
            [sg.Text('Set new distance:'), sg.InputText(default_replace_value, size=(10, 1), key='new_maxdist')],
            [sg.Checkbox('Make reserve copy', key='make_reserve_copy')],
            [sg.Button('Edit'), sg.Button('Exit'), sg.Text('', text_color='green', key='out')]]

# Create the Window
window = sg.Window('D2Distance', layout, alpha_channel=0.9, icon='app.ico')

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

                de.update_distance(new_maxdist)
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
import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--icon=app.ico',
    '--name=D2Distance',
    '--add-data=app.ico;.',
    '--onefile',
    '--clean',
    '--windowed'
])
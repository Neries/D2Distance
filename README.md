Create venv
`python -m venv venv`

Use venv:
Linux:
`source venv/bin/activate`
Windows:
`venv\Scripts\activate`

Install requirements
`pip install -r requirements.txt`

Create build
`python byild.py`
or
`pyinstaller --windowed -F main.py`
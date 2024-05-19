# JotPad

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-4B8BBE?style=for-the-badge&logo=tkinter&logoColor=white)](https://docs.python.org/3/library/tkinter.html)

## 📷 Screenshots

<!-- ![dark_mode](./screenshots/screenshot1.png) -->
<!-- ![syntax_mode](./screenshots/screenshot2.png) -->

<p align="center">
    <img height="500" src="./screenshots/screenshot2.png">
    <img height="500" src="./screenshots/screenshot1.png">
</p>

## ⚡️ Quick start

Install dependencies:

```python
pip3 install -r requirements.txt
```

```bash
make .
```

## Notes

- Create venv"

    ```bash
    # Create virtual env named venv
    # python3 for linux

    python -m venv venv

    # activate virutual env named venv
    # WINDOWS
    venv\Scripts\activate
    # Linux
    source venv/bin/activate
    ```

- Auto create requirements.txt

    ```bash
    # using pipreqs pkg
    # pipreqs /path/to/your/project
    pipreqs .

    # install dependencies (pip3 for linux)
    pip install -r requirements.txt
    ```

## 🗒️ ToDo

- [x] Add make file
- [x] Add requirements.txt
- [x] Add pyinstaller config file
- [x] Add .python-version
- [x] Use Chlorophyll for syntax highlighting
- [ ] add drag and drop to open files
- [ ] sense the file type on open and then auto select lexer
- [ ] a markdown viewer to view markdown files, and also an editor, like Marktext
- [ ] show path to the currently editing file
- [ ] tree view like vscode
- [ ] refactor into class based ui

## Ideas

- common pattenrs to add, TODO, DEBUG, REDO, FIXME, ERROR. These will be get highlighted
- <https://stackoverflow.com/questions/38594978/tkinter-syntax-highlighting-for-text-widget>
- <https://stackoverflow.com/a/77662152>

## How to use NSIS

- Install NSIS from official site (for windows)
- Open NSIS application, then click on "Compile NSI Script"
- Browse and select the *.nsi file

## Inspirations

- KDE Kate
- VS Code
- Notepad++
- Marktext
- Atom
- Gnome builder

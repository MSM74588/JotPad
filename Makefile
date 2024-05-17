.DEFAULT_GOAL := build

makespec:
	pyi-makespec --onefile --icon=icon.ico main.py

build: main.spec
	pyinstaller main.spec

clean:
	rd /s /q build
	rd /s /q dist


rebuild: clean build
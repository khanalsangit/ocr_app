@echo off
@echo [*] building python file from ./gui/ui/mainGUI.ui 
pyuic5 -x ./gui/ui/mainGUI.ui -o ./gui/pyUIdesign.py
@echo [+] file created
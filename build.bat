@echo off
@echo [*] building python file from ./gui/ui/mainGUI.ui 
pyrcc5 ./gui/ui/resources.qrc -o ./gui/resources_rc.py
pyuic5 -x ./gui/ui/mainGUI.ui -o ./gui/pyUIdesign.py
@echo [+] file created
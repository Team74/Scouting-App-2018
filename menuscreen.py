from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout

from widgetpresets import *

import mysql.connector #mysql --host=10.111.49.49 --user=jaga663 --password=chaos
import sqlite3

class MenuLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(MenuLayout, self).__init__()
        self.ipInputTextHint = ""

    def display(self):
        displist = []
        def appendLabel(text, sizeHint, color, widget=None, **kwargs):
            label = ColorLabel(text, sizeHint, color, **kwargs)
            if not widget: displist.append(label)
            else: widget.add_widget(label)
        def appendButton(text, sizeHint, color, bind, widget=None, **kwargs):
            button = ColorButton(text, sizeHint, color, **kwargs)
            button.bind(on_release=bind)
            if not widget: displist.append(button)
            else: widget.add_widget(button)
        # auton switch
        appendButton("Auton", halfHalf, grey, lambda x: self.switcher.switch("auton"))
        # teleop switch
        appendButton("Teleop", halfHalf, grey, lambda x: self.switcher.switch("teleop"))

        # login switch
        appendButton("Change team (data will be lost if not saved)", halfHalf, grey, lambda x: self.switcher.switch("login"))
        # layout for save and export buttons
        databaseLayout = StackLayout(size_hint=halfHalf)
        displist.append(databaseLayout)
        # save button
        appendButton("Save", wholeHalf, grey, self.switcher.robot.localSave, databaseLayout)
        # ip input text
        ipInput = TextInput(size_hint=quarterHalf, hint_text=self.ipInputTextHint)
        # export button
        appendButton("Export all", halfHalf, grey, lambda x: self.export(ipInput.text), databaseLayout)
        # mysql ip label
        appendLabel("mysql IP", quarterHalf, grey, databaseLayout)
        databaseLayout.add_widget(ipInput)


        # actually displaying everything
        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)

    def export(self, ip):
        for char in ip:
            if not char in "1234567890.":
                self.ipInputTextHint = "incorrect IP"
                self.display()
                return
        if not ip:
            self.ipInputTextHint = "enter IP here"
            self.display()
            return 
        mysqldb = mysql.connector.connect(user="jaga663", passwd="chaos", host=ip, database="scoutingdata")

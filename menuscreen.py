from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout

from widgetpresets import *
from robotclass import *

import mysql.connector #mysql --host=10.111.49.49 --user=jaga663 --password=chaos
import sqlite3

fairBlue = [28/255, 129/255, 201/255]

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
        appendButton("Auton", halfHalf, fairBlue, lambda x: self.switcher.switch("auton"))
        # teleop switch
        appendButton("Teleop", halfHalf, fairBlue, lambda x: self.switcher.switch("teleop"))

        # change team button
        appendButton("Change team (data will be lost if not saved)", (.5, .5), fairBlue, lambda x: self.switcher.switch("login"))

        # layout for save and export buttons
        databaseLayout = StackLayout(size_hint=(.5, .5))
        displist.append(databaseLayout)
        # save button
        appendButton("Save", (1 ,.5), fairBlue, self.switcher.robot.localSave, databaseLayout)
        # ip input text
        if self.ipInputTextHint:
            text = ""
        else:
            text = getIp()
        ipInput = TextInput(text=text, size_hint=(.25, .5), multiline=False, hint_text=self.ipInputTextHint)
        ipInput.bind(on_text_validate=lambda x: export(ipInput.text))
        # export button
        appendButton("Export all", (.5, .5), fairBlue, lambda x: export(ipInput.text), databaseLayout)
        # mysql ip label
        appendLabel("mysql IP", (.25, .5), fairBlue, databaseLayout)
        databaseLayout.add_widget(ipInput)


        # actually displaying everything
        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)

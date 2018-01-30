from kivy.app import App

from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.stacklayout import StackLayout

import os
import mysql.connector

class DisplayLayout(StackLayout):
    def __init__(self):
        super(DisplayLayout, self).__init__()
        self.displayMain("_")

    def displayMain(self, _):
        self.displist = []

        self.appendButton("switch data", (1, 1), self.displaySwitch)

        self.addAll()

    def displaySwitch(self, _):
        self.displist = []

        self.appendButton("back", (1, .05), self.displayMain)
        self.appendPicture("plots/switch.png", (1, .95))

        self.addAll()

    def appendButton(self, text, size_hint, bind):
        button = Button(text=text, size_hint=size_hint)
        button.bind(on_release=bind)
        self.displist.append(button)
    def appendPicture(self, source, size_hint):
        photo = Image(source=source, size_hint=size_hint, allow_stretch=True, keep_ratio=False)
        self.displist.append(photo)

    def addAll(self):
        self.clear_widgets()
        for widget in self.displist:
            self.add_widget(widget)

class MyApp(App):
    def build(self):
        return DisplayLayout()

if __name__ == "__main__":
    MyApp().run()

from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import Image

from plyer import camera
from widgetpresets import *
from robotclass import *
import os
import sqlite3
import time

class PhotoLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(PhotoLayout, self).__init__()
        self.displist = []

    def display(self):
        self.displist = []
        self.ifPhoto = ""

        self.appendButton("back", wholeFifth, grey, lambda x: self.switcher.switch("pitscouting main"))

        self.appendButton("Look at\nprevious photo.\n%s" % self.ifPhoto, halfFourFifth, grey, lambda x: self.photoDisplay())

        def takePicture(_):
            try:
                os.remove(self.switcher.robot.image)
            except Exception as error:
                pass
            pic = "/storage/sdcard0/%s.jpg" % (str(self.switcher.robot.teamNumber) + "_" + str(time.time()))
            camera.take_picture(pic, "")
            self.switcher.robot.image = pic


        self.appendButton("Take new\nphoto.", halfFourFifth, grey, takePicture)

        self.displayAll()

    def displayAll(self):
        self.clear_widgets()
        for widg in self.displist:
            self.add_widget(widg)

    def photoDisplay(self):
        self.displist = []

        self.appendButton("back", (1, .05), grey, self.back)
        self.appendPicture(self.switcher.robot.image, (1, .95))

        self.displayAll()

    def appendButton(self, text, size_hint, color, bind):
        button = Button(text=text, size_hint=size_hint)
        button.bind(on_release=bind)
        self.displist.append(button)
    def appendPicture(self, source, size_hint):
        photo = Image(source=source, size_hint=size_hint, allow_stretch=True, keep_ratio=False)
        self.displist.append(photo)
    def back(self, _):
        self.display()

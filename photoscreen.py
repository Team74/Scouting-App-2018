from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import Image

from plyer import camera
from widgetpresets import *
from robotclass import *
import os
import sqlite3

class PhotoLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(PhotoLayout, self).__init__()
        self.displist = []

    def display(self):
        self.displist = []
        self.ifPhoto = ""

        self.appendButton("back", wholeFifth, grey, lambda x: self.switcher.switch("pitscouting main"))

        self.appendButton("Look at\nprevious photo.\n%s" % self.ifPhoto, halfFourFifth, grey, lambda x: self.seePhoto())

        self.appendButton("Take new\nphoto.", halfFourFifth, grey, lambda _: self.newphoto())

        self.displayAll()

    def displayAll(self):
        self.clear_widgets()
        for widg in self.displist:
            self.add_widget(widg)

    def newphoto(self):
        if not '/storage/sdcard0/%s.jpg' % str(self.switcher.robot.teamNumber):
            os.remove('/storage/sdcard0/%s.jpg' % str(self.switcher.robot.teamNumber))
            camera.take_picture('/storage/sdcard0/%s.jpg' % str(self.switcher.robot.teamNumber))
            self.switcher.robot.image = '/storage/sdcard0/%s.jpg' % str(self.switcher.robot.teamNumber)
        else:
            camera.take_picture('/storage/sdcard0/%s.jpg' % str(self.switcher.robot.teamNumber))
            self.switcher.robot.image = '/storage/sdcard0/%s.jpg' % str(self.switcher.robot.teamNumber)w

    def photoDisplay(self):
        self.displist = []

        self.appendButton("back", (1, .05), grey, self.back)
        self.appendPicture(self.pic, (1, .95))

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


#picture = Image(source='photo')
    def seePhoto(self):
        try:
            self.ifPhoto = ""
            self.pic = '/storage/sdcard0/%s.jpg' % str(self.switcher.robot.teamNumber)
        except Exception as error:
            self.iifPhoto = "There is no\nphoto for this\nrobot"
            return
        self.photoDisplay()

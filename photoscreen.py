from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import Image

import time
from camera import *
from widgetpresets import *
from robotclass import *
import sqlite3

class PhotoLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(PhotoLayout, self).__init__()

    def display(self):
        displist = []
        def appendButton(text, sizeHint, color, bind, widget=None, **kwargs):
            button = ColorButton(text, sizeHint, color, **kwargs)
            button.bind(on_release=bind)
            if not widget: displist.append(button)
            else: widget.add_widget(button)
        self.ifPhoto = ""

        appendButton("back", wholefifth, grey, lambda x: self.switcher.switch("pitscouting main"))

        appendButton("Look at\nprevious photo.\n%s" % self.ifPhoto, halfWhole, grey, lambda x: self.seePhoto())

        appendButton("Take new\nphoto.", halfWhole, grey, lambda x: camera.take_picture('/storage/sdcard0/%s.jpg' % str(self.switcher.robot.teamNumber), ""))

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)
#picture = Image(source='photo')
    def seePhoto(self):
        try:
            self.ifPhoto = ""
            photo = Image(source = '/storage/sdcard0/%s.jpg' % str(self.switcher.robot.teamNumber))
        except Exception as error:
            self.ifPhoto = "There is no\nphoto for this\nrobot"
            return
        self.clear_widgets()
        self.add_widget(photo)

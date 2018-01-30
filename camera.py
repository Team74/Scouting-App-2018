from kivy.app import App #for the main app
from kivy.uix.floatlayout import FloatLayout #the UI layout
from kivy.uix.label import Label #a label to show information
from plyer import camera #object to read the camera
from robotclass import *

class UI(FloatLayout):
    def __init__(self, ScreenSwitcher, pic, **kwargs):
        super(UI, self).__init__(**kwargs)
        self.lblCam = Label(text = "Click to take a Picture.")
        self.add_widget(self.lblCam)
        self.switcher = ScreenSwitcher
        self.camera = pic
    def on_touch_down(self, e):
        camera.take_picture('/storage/sdcard0/%s.jpg' % str(self.switcher.robot.teamNumber), lambda x: self.done())

    def done(self, e):
        self.lblCam.text = e;
        self.camera.done()

class Camera(App):
    def __init__(self, ScreenSwitcher):
        self.switcher = ScreenSwitcher
        super(Camera, self).__init__()

    def build(self):
        ui = UI(self.switcher, self)
        return ui

    def done(self):
        self.parent.remove_widget(self)

    def on_pause(self):
        return true

    def on_resume(self):
        pass

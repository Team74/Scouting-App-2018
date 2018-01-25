from kivy.app import App #for the main app
from kivy.uix.floatlayout import FloatLayout #the UI layout
from kivy.uix.label import Label #a label to show information
from plyer import camera #object to read the camera

class UI(FloatLayout):
    def __init__(self, **kwargs):
        super(UI, self).__init__(**kwargs)
        self.lblCam = Label(text = "Click to take a Picture.")
        self.add_widget(self.lblCam)
    def on_touch_down(self, e):
        camera.take_picture('/storage/sdcard0/example.jpg', self.done)

    def done(self, e):
        self.lblCam.text = e;

class Camera(App):
    def build(self):
        ui = UI()
        return ui

    def on_pause(self):
        return true

    def on_resume(self):
        pass

Camera().run()

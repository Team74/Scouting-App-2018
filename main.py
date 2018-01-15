from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from menuscreen import MenuLayout
from loginscreen import LoginLayout
from teleopscreen import TeleopLayout

class ScreenSwitcher(BoxLayout):
    def __init__(self):
        super(ScreenSwitcher, self).__init__()
        self.currentScreen = LoginLayout(self)
        self.display()

    def display(self):
        self.clear_widgets
        self.add_widget(self.currentScreen)

class MyApp(App):
    def build(self):
        return ScreenSwitcher()

if __name__ == "__main__":
    MyApp().run()

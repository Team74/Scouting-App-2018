from kivy.app import App

from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.stacklayout import StackLayout

class DisplayLayout(StackLayout):
    def __init__(self):
        super(DisplayLayout, self).__init__()
        self.displayMain("")

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
        widget = Widget(size_hint=size_hint)
        widget.add_widget(Image(source=source))

    def addAll(self):
        self.clear_widgets()
        for widget in self.displist:
            self.add_widget(widget)

class MyApp(App):
    def build(self):
        return DisplayLayout()

if __name__ == "__main__":
    MyApp().run()

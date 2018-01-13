from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput

Builder.load_string("""
<ColorLabel>:
    text_size: self.size
    halign: "center"
    valign: "middle"
    canvas.before:
        Color:
            rgb: self.rgb
        BorderImage:
            source: "/colors/background.jpg"
            pos: self.pos
            size: self.size
        Rectangle:
            source: "/colors/background.jpg"
            pos: self.x + 1, self.y + 1
            size: self.width - 2, self.height - 2
<ColorButton>:
    text_size: self.size
    halign: "center"
    valign: "middle"
    canvas.before:
        Color:
            rgb: self.rgb
        BorderImage:
            source: "/colors/background.jpg"
            pos: self.pos
            size: self.size
""")

class ColorLabel(Label):
    def __init__(self, text, sizehint, color):
        self.rgb = color
        super(ColorLabel, self).__init__(text=str(text), size_hint=sizehint)

class ColorButton(Label):
    def __init__(self, text, sizehint, color):
        self.rgb = color
        super(ColorButton, self).__init__(text=str(text), size_hint=sizehint)

def normalLabel(text, color=[.5,.5,.5], height=.25):
    return ColorLabel(text, (.25, height), color)
def normalButton(text, color=[.5,.5,.5], height=.25):
    return ColorButton(text, (.25, height), color)
def normalTextInput(height=.25):
    return TextInput()

def smallLabel(text, color=[.5,.5,.5], height=.25):
    return ColorLabel(text, (.125, height), color)
def smallButton(text, color=[.5,.5,.5], height=.25):
    return ColorButton(text, (.125, height), color)

def bigLabel(text, color=[.5,.5,.5], height=.25):
    return ColorLabel(text, (.5, height), color)

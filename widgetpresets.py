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
        BorderImage:
            source: "/colors/background.jpg"
            pos: self.x - 1, self.y - 1
            size: self.width + 2, self.height + 2
        Color:
            rgb: self.rgb
        Rectangle:
            pos: self.pos
            size: self.size
<ColorButton>:
    text_size: self.size
    halign: "center"
    valign: "middle"
    background_normal: ""
    background_color: self.rgb
    canvas.before:
        BorderImage:
            source: "/colors/background.jpg"
            pos: self.x - 1, self.y - 1
            size: self.width + 2, self.height + 2
""") # uses BorderImage to outline every widget in white

class ColorLabel(Label):
    def __init__(self, text, sizehint, color):
        self.rgb = color
        super(ColorLabel, self).__init__(text=str(text), size_hint=sizehint)
        self.size = (self.width - 2, self.height - 2)

class ColorButton(Button):
    def __init__(self, text, sizehint, color):
        mutedColor = []
        for colorValue in color:
            mutedColor.append(colorValue-(30/255))
        print(mutedColor)
        self.rgb = mutedColor
        super(ColorButton, self).__init__(text=str(text), size_hint=sizehint)
        self.size = (self.width - 2, self.height - 2)

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
def bigButton(text, color=[.5,.5,.5], height=.25):
    return ColorButton(text, (.3, height), color)
def sLable(text, color=[.5,.5,.5], height=.125):
    return ColorLabel(text, (.3, height), color)

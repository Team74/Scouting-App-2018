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

""") # uses BorderImage and Rectangle to outline every widget in white

seaFoamGreen = [14/255, 201/255, 170/255]
darkMagenta = [171/255, 0/255, 117/255]
lightMagenta = [231/255, 58/255, 177/255]
fairBlue = [28/255, 129/255, 201/255]
lightOrange = [255/255, 150/255, 75/255]
red = [1, 0, 0]
tameRed = [200/255, 0, 0]
darkRed = [115/255, 0, 0]
green = [0, 1, 0]
tameGreen = [0, 200/255, 0]
black = [0, 0, 0]
grey = [.5, .5, .5]

class ColorLabel(Label):
    def __init__(self, text, sizehint, color, **kwargs):
        self.rgb = color
        super(ColorLabel, self).__init__(text=str(text), size_hint=sizehint, **kwargs)

class ColorButton(Button):
    def __init__(self, text, sizehint, color, **kwargs):
        mutedColor = []
        for colorValue in color:
            mutedColor.append(colorValue-(30/255))
        self.rgb = mutedColor+[1]
        super(ColorButton, self).__init__(text=str(text), size_hint=sizehint, **kwargs)

def quarterLabel(text, color=grey):
    return ColorLabel(text, (.25, .25), color)
def quarterButton(text, color=grey):
    return ColorButton(text, (.25, .25), color)

def eighthLabel(text, color=grey):
    return ColorLabel(text, (.125, .25), color)
def eighthButton(text, color=grey):
    return ColorButton(text, (.125, .25), color)

def fullLabel(text, color=grey):
    return ColorLabel(text, (1, .5), color)
def fullButton(text, color=grey):
    return ColorButton(text, (1, .5), color)
def halfLabel(text, color=grey):
    return ColorLabel(text, (.5, .5), color)
def halfButton(text, color=grey):
    return ColorButton(text, (.5, .5), color)

def quaterHalfButton(text, color=grey):
    return ColorButton(text, (.25, .5), color)

def tripleSideButton(text, color=grey):
    return ColorButton(text, (1/3, 1), color)
def tripleMiddleButton(text, color=grey):
    return ColorButton(text, (1/3, 1), color)

def bigLabel(text, color=grey):
    return ColorLabel(text, (.5, .25), color)
def bigButton(text, color=grey):
    return ColorButton(text, (.5, .25), color)

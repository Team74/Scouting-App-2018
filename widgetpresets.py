from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget

def normalLabel(text, height=.25):
    return Label(text=text, size_hint=(.25, height))
def normalButton(text=text, height=.25):
    return Button(text=text, size_hint=(.25, height))

def smallLabel(text, height=.25):
    return Label(text=text, size_hint=(.125, height))
def smallButton(text, height=.25):
    return Button(text=text, size_hint=(.125, height))

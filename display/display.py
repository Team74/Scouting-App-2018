from kivy.app import App

from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.core.window import Window

from widgetpresets import *
from robotclass import *
from datatable import DataViewLayout
import sqlite3
import os
import mysql.connector

class DisplayLayout(StackLayout):
    def __init__(self):
        super(DisplayLayout, self).__init__()
        self.displayMain("_")
        database = mysql.connector.connect(connection_timeout=1, user="jaga663", passwd="chaos", host="204.8.232.45", database="Scouting2018")
        cursor = database.cursor()
        cursor.execute("SELECT teamNumber, image FROM pitscoutingdata")
        currentDir = os.path.dirname(os.path.realpath(__file__))
        os.system("Rscript %s/boxplots.r" % currentDir)
        for data in cursor.fetchall():
            teamNumber = data[0]
            image = data[1]
            imageFile = open("%s/pitimages/%s.jpg" % (currentDir, teamNumber), "wb")
            imageFile.write(image)
            imageFile.close()
        database.close()

    def appendButton(self, text, size_hint, bind):
        button = Button(text=text, size_hint=size_hint)
        button.bind(on_release=bind)
        self.displist.append(button)
    def appendPicture(self, source, size_hint):
        photo = Image(source=source, size_hint=size_hint, allow_stretch=True, keep_ratio=False)
        self.displist.append(photo)
    def addAll(self):
        self.clear_widgets()
        for widget in self.displist:
            self.add_widget(widget)

    def displayMain(self, _):
        self.displist = []
        self.appendButton("switch data", halfHalf, self.displaySwitch)
        self.appendButton("data table", halfHalf, self.displayDataTable)
        self.appendButton("export", halfHalf, self.exportbutton)
        self.addAll()

    def displaySwitch(self, _):
        self.displist = []
        self.appendButton("back", (1, .05), self.displayMain)
        self.appendPicture("plots/switch.png", (1, .95))
        self.addAll()

    def displayDataTable(self, _):
        self.displist = []
        self.displist.append(DataViewLayout(self, "10.111.49.49"))
        self.addAll()

    def exportbutton(self, _):
        fh = open("hello.txt","w")
        sqlitedb = sqlite3.connect("displaydatabase.db") # sqlite database
        sqlitec = sqlitedb.cursor() # sqlite cursor
        sqlitec.execute("SELECT * FROM matchdata") # first upload all match data
        for row in sqlitec.fetchall():
            print (row)
            fh.write(\
            str(row[0])+","+\
            str(row[1])+","+\
            str(row[2])+","+\
            str(row[3])+","+\
            str(row[4])+","+\
            str(row[5])+","+\
            str(row[6])+","+\
            str(row[7])+","+\
            str(row[8])+","+\
            str(row[9])+","+\
            str(row[10])+","+\
            str(row[11])+","+\
            str(row[12])+","+\
            str(row[13])+","+\
            "\n"\
            )

        fh.close()


class MyApp(App):
    def build(self):
        return DisplayLayout()

if __name__ == "__main__":
    MyApp().run()

from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout

from widgetpresets import *

import mysql.connector #mysql --host=10.111.49.49 --user=jaga663 --password=chaos
import sqlite3

from PIL import Image

class MenuLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(MenuLayout, self).__init__()
        self.ipInputTextHint = ""

    def display(self):
        displist = []
        def appendLabel(text, sizeHint, color, widget=None, **kwargs):
            label = ColorLabel(text, sizeHint, color, **kwargs)
            if not widget: displist.append(label)
            else: widget.add_widget(label)
        def appendButton(text, sizeHint, color, bind, widget=None, **kwargs):
            button = ColorButton(text, sizeHint, color, **kwargs)
            button.bind(on_release=bind)
            if not widget: displist.append(button)
            else: widget.add_widget(button)
        # auton switch
        appendButton("Auton", halfHalf, grey, lambda x: self.switcher.switch("auton"))
        # teleop switch
        appendButton("Teleop", halfHalf, grey, lambda x: self.switcher.switch("teleop"))

        # change team button
        appendButton("Change team (data will be lost if not saved)", halfHalf, grey, lambda x: self.switcher.switch("login"))

        # layout for save and export buttons
        databaseLayout = StackLayout(size_hint=halfHalf)
        displist.append(databaseLayout)
        # save button
        appendButton("Save", wholeHalf, grey, self.switcher.robot.localSave, databaseLayout)
        # ip input text
        ipInput = TextInput(size_hint=quarterHalf, multiline=False, hint_text=self.ipInputTextHint)
        ipInput.bind(on_text_validate=lambda x: self.export(ipInput.text))
        # export button
        appendButton("Export all", halfHalf, grey, lambda x: self.export(ipInput.text), databaseLayout)
        # mysql ip label
        appendLabel("mysql IP", quarterHalf, grey, databaseLayout)
        databaseLayout.add_widget(ipInput)


        # actually displaying everything
        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)

    def export(self, ip):
        for char in ip: # testing if the ip is an actual ip and not a word
            if not char in "1234567890.":
                self.ipInputTextHint = "wait a minute\n\nthat's not an ip???///???!?"
                self.display()
                return
        if not ip: # testing if the ip actually exists
            self.ipInputTextHint = "enter IP here"
            self.display()
            return
        try: #TIMEOUT IS IN SECONDS, NOT MILLISECONDS
            mysqldb = mysql.connector.connect(connection_timeout=1, user="jaga663", passwd="chaos", host=ip, database="Scouting2018")
        except mysql.connector.errors.InterfaceError: # thrown when timeout hits or if the ip is incorrect
            self.ipInputTextHint = "incorrect IP"
            self.display()
            return

        mysqlc = mysqldb.cursor() # mysql cursor
        sqlitedb = sqlite3.connect("scoutingdatabase.db") # sqlite database
        sqlitec = sqlitedb.cursor() # sqlite cursor
        sqlitec.execute("SELECT * FROM matchdata") # first upload all match data
        for row in sqlitec.fetchall(): # see robotclass Robot.dumpData() for order of row
            mysqlc.execute("SELECT * FROM matchdata WHERE teamNumber=%s AND roundNumber=%s AND eventName=%s", row[:3])
            if mysqlc.fetchone(): # if a row similar to the one in the mysql database exists
                mysqlc.execute("""
                    UPDATE matchdata SET
                    scouter=%s, switch=%s, scale=%s, exchange=%s, climb=%s, notes=%s,
                    startingPosition=%s, attemptedSwitchSide=%s, autonSwitch=%s, autonScale=%s, autonExchange=%s
                    WHERE teamNumber=%s AND roundNumber=%s AND eventName=%s
                """, row[3:] + row[:3]) # overwrite instead of make a new one
            else: # if there was no row found
                mysqlc.execute("INSERT INTO matchdata VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", row) # make a new row
        sqlitec.execute("SELECT * FROM pitscoutingdata")
        for row in sqlitec.fetchall(): # see robotclass PitRobot.dumpData() for order of row
            try:
                row[7] = Image.open(row[7]) # TODO: fix this, make it work, so that it functions properly and doesn't break, throwing an error in the program and making people mad
            except FileNotFoundError:
                print("unable to find file %s" % row[7])

            mysqlc.execute("SELECT * FROM pitscoutingdata WHERE teamNumber=%s", (row[0],))
            if mysqlc.fetchone(): # if a row similar to the one in the mysql database exists
                mysqlc.execute("""
                    UPDATE pitscoutingdata SET
                    drivetrain=%s, groundPickup=%s, scaleCapability=%s, switchCapability=%s, exchangeCapability=%s, image=%s, notes=%s
                    WHERE teamNumber=%s
                """, row[2:] + (row[0],)) # replace instead of insert
            else: # if there was no match
                mysqlc.execute("INSERT INTO pitscoutingdata VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", row) # insert instead of replace
        mysqldb.commit()
        mysqldb.close()
        sqlitedb.close()

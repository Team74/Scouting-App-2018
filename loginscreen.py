from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.graphics.svg import Svg
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder

from widgetpresets import *
from robotclass import *
from qrcodes import generateRealQR, generateQR
#from webview import Wv
import sqlite3

Builder.load_string("""
<SvgWidget>:
    do_rotation: False

""")

class SvgWidget(Widget):
    def __init__(self, filename, **kwargs):
        super(SvgWidget, self).__init__(**kwargs)
        with self.canvas:
            svg = Svg(filename)
        self.size = 10000, 10000

class LoginLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(LoginLayout, self).__init__()
        self.round = 1
        self.last = ""
        self.ipInputTextHint = ""
        self.menuText = 'Teleop'
        self.QRRounds = 5

    def display(self):
        if not self.switcher.screens["dataview"].fromDataView == 1:
            if not (self.round-1) % 10 and self.round > 1:
                content = Button(text='Switch with your scouting partner.\n\n\n\n\n\n\n                 Tap to close.')
                popup = Popup(title='Time to switch.', content=content, auto_dismiss=False)
                content.bind(on_press=popup.dismiss)
                popup.open()
        database = sqlite3.connect("scoutingdatabase.db")
        cursor = database.cursor()
        cursor.execute("SELECT * FROM crash WHERE Exited=0")
        result = cursor.fetchone()
        if result:
            if not result[2] == "placeholder":
                self.switcher.robot = Robot(int(result[0]), int(result[1]), self.switcher.eventName, result[2])
                database.execute("UPDATE crash SET Exited=1")
                database.commit()
                database.close()
                self.scoutNumber = 0
                self.changer = 0
                self.menuText = 'Menu'
                database = sqlite3.connect("scoutingdatabase.db") # data calling from db
                cursor = database.cursor()
                cursor.execute("SELECT scouter FROM matchdata")
                for scouterData in cursor.fetchall():
                    if scouterData[0] == result[2]:
                        self.scoutNumber += 1
                self.switcher.switch("teleop")
            else:
                database.commit()
                database.close()
        else:
            database.commit()
            database.close()
        displist = []

        # scouter display
        scouterDisp = bigLabel("scouter", seaFoamGreen)
        displist.append(scouterDisp)
        # scouter input
        self.scouterInput = TextInput(text=str(self.last), multiline=False, size_hint=(.5, .25))
        displist.append(self.scouterInput)

        #row 2
        teamDisp = bigLabel("team", seaFoamGreen)
        displist.append(teamDisp)

        teamInput = TextInput(text=str(""), multiline=False, size_hint=(.5, .25))
        displist.append(teamInput)

        #row 3
        roundDisp = bigLabel("round", seaFoamGreen)
        displist.append(roundDisp)

        self.roundInput = TextInput(text=str(self.round), multiline=False, size_hint=quarterQuarter)
        displist.append(self.roundInput)

        roundDec = ColorButton("-", (.125, .25), seaFoamGreen)
        roundDec.bind(on_release=lambda x: self.changeRound(-1))
        displist.append(roundDec)

        roundInc = ColorButton("+", (.125, .25), seaFoamGreen)
        roundInc.bind(on_release=lambda x: self.changeRound(1))
        displist.append(roundInc)

        #row 4
        def pitScoutingSwitch(_):
            self.switcher.screens["pitscouting selecter"].query = ""
            self.switcher.switch("pitscouting selecter")
        pitScout = ColorButton("Pit Scouting", ((1/5), .25),fairBlue)
        pitScout.bind(on_release=pitScoutingSwitch)
        displist.append(pitScout)

        dataview = ColorButton('dataview', ((1/5), .25), fairBlue)
        dataview.bind(on_release=lambda x: self.switcher.switch("dataview"))
        displist.append(dataview)

        exportLayout = StackLayout(size_hint=(1/5, .25))
        displist.append(exportLayout)

        exportButton = ColorButton('Export All', (1, .5), fairBlue)
        exportLayout.add_widget(exportButton)

        if self.ipInputTextHint:
            text = ""
        else:
            text = getIp()
        ipInput = TextInput(text=text, multiline=False, size_hint=(1, .5))
        def exportBind(_):
            ipInput.hint_text = export(ipInput.text)
            ipInput.text = ""
        exportLayout.add_widget(ipInput)

        exportButton.bind(on_release=exportBind)

        QRLayout = StackLayout(size_hint=(1/5, .25))
        displist.append(QRLayout)

        QRExport = ColorButton("Export %s rounds with QR" % self.QRRounds, (1, .5), fairBlue)
        QRRoundInc = ColorButton("+", (.5, .5), fairBlue)
        QRRoundDec = ColorButton("-", (.5, .5), fairBlue)
        QRLayout.add_widget(QRExport)
        QRLayout.add_widget(QRRoundDec)
        QRLayout.add_widget(QRRoundInc)
        def QRChange(change):
            self.QRRounds += change
            QRExport.text = "Export %s rounds with QR" % self.QRRounds
        def QRBind(_):
            generateQR(int(self.roundInput.text), self.QRRounds)
            content = StackLayout()
            backButton = ColorButton("Back", (1, .2), fairBlue)
            content.add_widget(backButton)
            content.add_widget(SvgWidget("url.svg", size_hint=(1, .8)))
            #QRImage = Image(source="url.png", size_hint=(.8, .8), nocache=True)
            #QRImage.width = QRImage.height
            #content.add_widget(QRImage)
            #content.add_widget(Wv())
            popup = Popup(title='QR code', content=content, auto_dismiss=False)
            backButton.bind(on_press=popup.dismiss)
            popup.open()
        QRExport.bind(on_release=QRBind)
        QRRoundInc.bind(on_release=lambda _: QRChange(1))
        QRRoundDec.bind(on_release=lambda _: QRChange(-1))

        goButton = ColorButton("Go", (1/5, .25), fairBlue)
        def teleopSwitch(_):
            number = "1234567890"
            #checking to see if team number and round number are input correctly so we dont have data type mismatch in sql database
            tiCheck = False
            for char in teamInput.text:
                if char in number:
                    tiCheck = True
                    print("ticheck is true")
            if not tiCheck or not self.roundInput.text or not self.scouterInput.text or self.roundInput.text == "0": return
            self.switcher.robot = Robot(int("".join(char for char in teamInput.text if char in number)), int(self.roundInput.text), self.switcher.eventName, self.scouterInput.text)
            self.last = self.scouterInput.text
            self.round = int(self.roundInput.text) + 1
            self.scoutNumber = 0
            self.changer = 1
            self.switcher.screens["dataview"].fromDataView = 0
            self.menuText = 'Teleop'
            database = sqlite3.connect("scoutingdatabase.db") # data calling from db
            cursor = database.cursor()
            cursor.execute("SELECT scouter FROM matchdata")
            for scouterData in cursor.fetchall():
                if scouterData[0] == self.scouterInput.text:
                    self.scoutNumber += 1
            self.switcher.switch("auton")
        goButton.bind(on_release=teleopSwitch)
        displist.append(goButton)

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)

    def changeRound(self, change):
        if not self.roundInput.text: return
        for i in self.roundInput.text:
            if not i in "12344567890":
                return
        self.round = int(self.roundInput.text) + change
        if self.round <= 0:
            self.round = 1
        self.roundInput.text = str(self.round)

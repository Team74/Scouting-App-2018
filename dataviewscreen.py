from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

class DataViewLayout(StackLayout):
    def __init__(self, screenSwitcher):
        self.switcher = screenSwitcher
        super(DataViewLayout, self).__init__()

    def display(self):
        scrolllist = []
        displist = []

        searchBar = TextInput(size_hint=(.875,.1))
        displist.append(searchBar)

        back = ColorButton("Back", (.125, .1), darkblue)
        back.bind(on_release=lambda x: self.switcher.switch("login"))
        displist.append(back)

        eventList = ScrollView(size_hint=(1, None), size = (Window.width, Window.height-searchBar.height)) # make widgets and layouts for this
        displist.append(eventList) # corresponding with the variables
        eventListLayout = StackLayout(size_hint_y=None)
        eventListLayout.bind(minimum_height=eventListLayout.setter('height'))
        eventList.add_widget(eventListLayout)

        database = sqlite3.connect("scoutingdatabase.db") # data calling from db
        cursor = database.cursor()
        cursor.execute("SELECT * FROM matchdata")
        for teamData in cursor.fetchall():
            roundNumber = teamData[1]
            teamNumber = teamData[0]
            button = ColorButton("Round: %s, Team: %s" % (roundNumber, teamNumber), (1, None), darkblue)
            scrolllist.append(button)
            button.bind(on_release=self.dataViewSwitch)
        database.close()

        self.clear_widgets()
        for widget in displist:
            self.add_widget(widget)

    def dataViewSwitch(self, numberButton):
        buttonText = list(numberButton.text)
        roundNumber, teamNumber = buttonText.split(",")
        roundNumber = [x for x in roundNumber if x in "1234567890"]
        teamNumber = [x for x in teamNumber if x in "1234567890"]

        self.switcher.robot = Robot(numberButton.text)
        self.switcher.switch('')

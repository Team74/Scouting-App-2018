import sqlite3
import random
import robotclass

database = sqlite3.connect("scoutingdatabase.db")
database.execute("DELETE FROM matchdata")
database.commit()
database.close()

for team in [421, 6635, 1003]:
    for round in range(1,26):
        robot = robotclass.Robot(
            team,
            round,
            "datamaker",
            "datamaker",
            random.randint(0, 9),
            random.randint(0, 12),
            random.randint(0, 9),
            random.choice(["did not climb", "tried but failed", "levitated", "climbed"]),
            "datamaker",
            random.choice(["left", "middle", "right"]),
            random.choice(["left", "right"]),
            random.randint(0, 3),
            random.randint(0, 2),
            random.randint(0, 2)
        )
        robot.localSave("throwaway")

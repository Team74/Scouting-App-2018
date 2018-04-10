import sqlite3
import random
import robotclass

database = sqlite3.connect("scoutingdatabase.db")
database.execute("DELETE FROM matchdata")
database.commit()
database.close()

for team in [421]:
    for round in range(1,64):
        robot = robotclass.Robot(
            team,
            round,
            "datamaker",
            "datamaker",
            random.randint(0, 9),
            random.randint(0, 12),
            random.randint(0, 9),
            random.choice(["climbed", "didn't climb", "were assisted", "assisted +1", "assisted +2"]),
            "datamaker",
            random.choice(["left", "middle", "right"]),
            random.choice(["right", "left"]),
            random.randint(0, 3),
            random.randint(0, 2),
            random.randint(0, 2)
        )
        robot.localSave("_")

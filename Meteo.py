import random
import math

class Meteo():

    def __init__(self, heure):
        if heure > 20 or heure < 8:
            self.temp_ext = 10
        else:
            self.temp_ext = 19

    def upateTemps(self, heure):
        r = abs(math.pow(random.random() - 0.5, 6))
        if heure > 18 or heure < 8:
            self.temp_ext *= (1 - r)
        else:
            self.temp_ext *= (1 + r)

    def modifierMeteo(self):
        self.temp_ext = random.randint(0, 30)

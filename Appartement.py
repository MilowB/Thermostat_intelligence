import random

class Appartement():

    def __init__(self, w, perte, thermostat):
        self.thermostat = thermostat
        self.upper = False
        self.temp_int = 15
        self.temp_requise = 21
        #En Watt
        self.watt_chauffage = w
        self.chauffage_on = False
        #En Watt
        self.perte_isolation = perte

    #En Watt
    def getResultanteEnergie(self, temp_ext):
        ratio = 1
        if self.temp_int > temp_ext:
            ratio = -1
        res = self.perte_isolation * ratio
        #print("ratio : ", ratio, ", self.perte_isolation : ", self.perte_isolation, ", res : ", res)
        if self.chauffage_on:
            res = self.watt_chauffage - self.perte_isolation
        return res

    def besoinChauffage(self, hour):
        res = False
        self.temp_requise = self.thermostat.getRequireTemp("lundi", hour)
        #print(self.temp_requise)
        if self.temp_int > self.temp_requise:
            self.upper = True
        if self.temp_int < self.temp_requise and not self.upper:
            res = True
        elif self.temp_int >= self.temp_requise - 0.5 and self.temp_int < self.temp_requise and self.upper:
            res = False
        elif self.temp_int < self.temp_requise - 0.5:
            res = True
            self.upper = False
        return res

    def modifierTempRequise(self):
        self.temp_requise = random.randint(0, 30)

    
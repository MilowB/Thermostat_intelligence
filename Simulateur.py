from Meteo import *
from Appartement import *
import json

class Simulateur():

    def __init__(self, x, y, z, w, thermostat):
        self.heure = 0
        self.meteo = Meteo(self.heure)
        self.appartement = Appartement(w, 250, thermostat)
        self.x = x
        self.y = y
        self.z = z
        self.volume = x * y * z
        self.masse_vol_air = 1.225
        self.masse_air = self.volume * self.masse_vol_air
        self.capacite_cal_air = 1000
        self.q = 1
        self.watt_chauffage = w
        self.tick = 0.1

    def updateHeure(self):
        self.heure += self.tick
        if self.heure > 24:
            self.heure = 0

    def updateTemp(self):
        self.meteo.upateTemps(self.heure)
        if self.meteo.temp_ext != self.appartement.temp_int:
            ext = self.meteo.temp_ext
            inte = self.appartement.temp_int
            requis = self.appartement.temp_requise
            temp_convergence = None
            if self.appartement.chauffage_on:
                ratio_iso = self.appartement.perte_isolation / self.appartement.watt_chauffage
                diff = requis - ext
                requis += ratio_iso + diff
                self.q = self.masse_air * self.capacite_cal_air * (self.toKelvin(requis) - self.toKelvin(inte))
                temp_convergence = requis
            else:
                self.q = self.masse_air * self.capacite_cal_air * (self.toKelvin(ext) - self.toKelvin(inte))
                temp_convergence = ext
            energie = self.appartement.getResultanteEnergie(self.meteo.temp_ext)
            duree_chauffage = self.q / energie
            max_ratio = abs(temp_convergence - inte)
            if abs((60 * self.tick * 60) / duree_chauffage) > max_ratio:
                ratio = max_ratio * (duree_chauffage / abs(duree_chauffage))
            else:
                ratio = (60 * self.tick * 60)  / duree_chauffage
            #print("[Simulateur] ratio : ", ratio)
            delta = ratio * energie
            #print("[Simulateur] delta : ", delta)
            temp_finale =  delta / (self.masse_air * self.capacite_cal_air) + self.toKelvin(inte)
            self.appartement.temp_int = self.toCelsius(temp_finale)
            #print("[Simulateur] Q : ", self.q, ", temp_int : ", self.appartement.temp_int, ", temp_ext : ", self.meteo.temp_ext, ", heure : ", self.heure, ", chauffage : ", self.appartement.chauffage_on)
            #print("[Simulateur] temp_int : ", self.appartement.temp_int)

    def toCelsius(self, temp):
        return temp - 273.15

    def toKelvin(self, temp):
        return temp + 273.15

    def comportement(self, ite):

        #if ite % 240 == 0:
        #    self.appartement.modifierTempRequise()
        if ite % (240 * 7) == 0:
            self.meteo.modifierMeteo()
        if self.appartement.besoinChauffage(self.heure):
            self.appartement.chauffage_on = True
        elif not self.appartement.besoinChauffage(self.heure):
            self.appartement.chauffage_on = False

    def getStat(self):
        ext = self.meteo.temp_ext
        inte = self.appartement.temp_int
        req = self.appartement.temp_requise
        heure = self.heure
        chauffage = self.appartement.chauffage_on
        return json.dumps({"temp_ext": round(ext, 2), "temp_int": round(inte, 2), "temp_requise": round(req, 1), "heure": round(heure, 1), "chauffage": chauffage}, sort_keys=True)

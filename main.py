import matplotlib
import matplotlib.pyplot as plt
import json

from Simulateur import *

def main():
    print("Simulateur ON")
    # Data for plotting
    json_data = []
    temps = []
    temperature = []
    temperature_ext = []
    simulateur = Simulateur(4, 4, 2.5, 3000)
    cpt = 0
    #240 = 1 jour
    while cpt < 240 * 360 * 100:
        simulateur.updateHeure()
        simulateur.updateTemp()
        simulateur.comportement(cpt)
        temps.append(simulateur.heure)
        temperature.append(simulateur.appartement.temp_int)
        temperature_ext.append(simulateur.meteo.temp_ext)
        json_data.append(simulateur.getStat())
        cpt += 1

    fig, ax = plt.subplots()
    ax.plot(temps, temperature, label="temp intérieure")
    ax.plot(temps, temperature_ext, label="temp extérieure")
    ax.legend(loc='upper left')

    ax.set(xlabel='heure', ylabel='temperature',
        title='Température intérieure d\'une pièce de 16m² enregistrée heure par heure en fonction de la température extérieure')
    ax.grid()
    file = open("raw.json", "w") 
    file.write(json.dumps(json_data, indent=4))
    file.close() 
    plt.show()

    

if __name__ == "__main__":
    main()
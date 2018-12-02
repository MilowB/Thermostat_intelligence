import matplotlib
import matplotlib.pyplot as plt
import json

from Simulateur import *

def main():
    print("Traitement des données ON")
    with open("raw.json", "r") as f:
        knowledge = []
        found = False
        cpt = 0
        data = json.load(f)
        last_t_inte = 0
        t_inte = 0
        last_t_ext = 0
        t_ext = 0
        last_hour = 0
        hour = 0
        last_cpt = cpt
        for d in data:
            cpt += 1

            if json.loads(d)["chauffage"] and not found:
                last_t_inte = json.loads(d)["temp_int"]
                last_t_ext = json.loads(d)["temp_ext"]
                last_hour = json.loads(d)["heure"]
                last_cpt = cpt
                found = True
            elif not json.loads(d)["chauffage"] and last_cpt < cpt and found:
                t_inte = json.loads(d)["temp_int"]
                t_ext = json.loads(d)["temp_ext"]
                hour = json.loads(d)["heure"]
                #Format :
                #temp_ext, temp_ini, temp_fin, duree
                if last_t_inte != t_inte:
                    processed_hour = round(hour - last_hour, 1)
                    if processed_hour < 0:
                        processed_hour = round(round(24 - last_hour, 1) + round(hour, 1), 1)
                    if processed_hour < 6 and processed_hour > 0:
                        knowledge.append(str(round((t_ext + last_t_ext) / 2, 2)) + " " + str(last_t_inte) + " " + str(t_inte) + " " + str(processed_hour) + '\n')
                found = False
        file = open("data.csv", "w") 
        for k in knowledge:
            file.write(k)
        file.close() 
        
    

if __name__ == "__main__":
    main()
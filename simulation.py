import os, sys
import time

# Vérifie si l'environnement SUMO_HOME est défini
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:   
    sys.exit("Veuillez déclarer la variable d'environnement 'SUMO_HOME'")
    
# Importe les modules TraCI et les constantes de TraCI
import traci
import traci.constants

# Démarre SUMO avec la configuration osm.sumocfg et affiche la fenêtre graphique
sumoCmd = ["sumo-gui", "-c", "osm.sumocfg", "--start"]
traci.start(sumoCmd)


# Change l'affichage de la vue 0 de SUMO pour qu'elle corresponde au "monde réel"
traci.gui.setSchema("View #0", "real world")


# Compteur pour le nombre d'itérations de la boucle
j = 0

# Boucle principale qui dure 60 secondes
while(j<60):
    # Attend 0,5 secondes
    time.sleep(0.5)
    # Avance la simulation d'un pas
    traci.simulationStep()

    # Récupère la liste des IDs de tous les véhicules dans la simulation
    vehicles=traci.vehicle.getIDList()


    # Tous les 10 secondes...
    if (j%10)==0:
        # Pour chaque véhicule...
        for i in range(0,len(vehicles)): 
            # Définit le mode de vitesse du véhicule à 0
            traci.vehicle.setSpeedMode(vehicles[i],0)
            # Définit la vitesse du véhicule à 15 m/s
            traci.vehicle.setSpeed(vehicles[i],15)
            # Affiche la vitesse, l'émission de CO2, l'ID de l'arête et la distance totale parcourue du véhicule
            print("Vitesse ", vehicles[i], ": ",traci.vehicle.getSpeed(vehicles[i]), " m/s")
            print("Émission de CO2 ", vehicles[i], ": ", traci.vehicle.getCO2Emission(vehicles[i]), " mg/s")
            print("ID de l'arête du véhicule ", vehicles[i], ": ", traci.vehicle.getRoadID(vehicles[i]))
            print('Distance ', vehicles[i], ": ", traci.vehicle.getDistance(vehicles[i]), " m")
        
    # Incrémente le compteur de la boucle
    j = j+1

# Récupérer la liste des IDs des bords de la simulation
IDsOfEdges = traci.edge.getIDList()

# Afficher la liste des IDs des bords
print("IDs des bords:", IDsOfEdges)

# Récupérer la liste des IDs des junctions de la simulation
IDsOfJunctions = traci.junction.getIDList()

# Afficher la liste des IDs des junctions
print("IDs des junctions:", IDsOfJunctions)





# Fermer la connexion à la simulation
traci.close()
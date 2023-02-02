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
import math

# Démarre SUMO avec la configuration osm.sumocfg et affiche la fenêtre graphique
sumoCmd = ["sumo-gui", "-c", "osm.sumocfg", "--start"]
traci.start(sumoCmd)

# Change l'affichage de la vue 0 de SUMO pour qu'elle corresponde au "monde réel"
traci.gui.setSchema("View #0", "real world")

# identification du hub
latitude = 49.504600
longitude = 0.117550
hub = traci.simulation.convertGeo(latitude, longitude, True)
print("hub => x = ", hub[0], " y = ", hub[1])

# identification du cantine 1
latitude1 = 49.49447
longitude1 = 0.11338
cantine1 = traci.simulation.convertGeo(latitude1, longitude1, True)
print("Cantine 1 => x = ", cantine1[0], " y = ", cantine1[1])


def distance_entre_deux_points(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_junction_id_by_xy(x, y):
    voisin_distance = float('inf')
    voisin_junction = None

    for junction_id in traci.junction.getIDList():
        junction_x, junction_y = traci.junction.getPosition(junction_id)
        dist = distance_entre_deux_points(junction_x, junction_y, x, y)
        if dist < voisin_distance:
            voisin_distance = dist
            voisin_junction = junction_id

    return voisin_junction


# example usage
junction_hub = get_junction_id_by_xy(hub[0], hub[1])
print("Junction HUB:", junction_hub)
print(traci.junction.getPosition(junction_hub))
junction_cantine1 = get_junction_id_by_xy(cantine1[0], cantine1[1])
print("Junction Cantine1:", junction_cantine1)

#route1 = traci.simulation.findRoute(junction_hub , "-1099627053", "pt_vehicule")

#print("l'itinéraire le plus rapide entre les bords", route1)
# print(traci.edge.getIDList())

dis = traci.simulation.getDistance2D(latitude, longitude, latitude1, longitude1, True, False)

print("La distance entre deux positions est ", dis)

# routes = traci.route.getIDList()
# edges = traci.edge.getIDList()
#
# #creation de route 1
# route_id = "route1"
# edges = ["-1003929910", "-1028671518"]
# traci.route.add(route_id, edges)
# print("routes", traci.route.getIDList())
#
# #creation de vehicule 1
# vehicule_id = "ev1"
# route_id = "route1"
# traci.vehicle.add(vehicule_id, route_id)
# print("vehicule", traci.vehicle.getSpeed(vehicule_id))
#
#
# traci.simulation.findRoute()


# Compteur pour le nombre d'itérations de la boucle
j = 0

# Boucle principale qui dure 60 secondes
while (j < 60):
    # Attend 0,5 secondes
    time.sleep(0.5)
    # Avance la simulation d'un pas
    traci.simulationStep()

    # Récupère la liste des IDs de tous les véhicules dans la simulation
    vehicles = traci.vehicle.getIDList()

    # Tous les 10 secondes...
    if (j % 10) == 0:
        print("Liste des vehicules", traci.vehicle.getIDList())

# Fermer la connexion à la simulation
traci.close()

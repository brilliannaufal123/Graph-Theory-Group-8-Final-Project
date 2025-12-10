import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import math

# --- CONFIGURATION: HOSPITAL NAMES ---
hospital_names = {
    "UNA": "RS Universitas Airlangga",
    "ITS": "Medical Center ITS",
    "HAJ": "RSUD Haji Provinsi Jawa Timur"
}

hospitals = {
    "UNA": (-7.269874626602621, 112.7848445619724), 
    "ITS": (-7.29042166801988, 112.7928147461148),  
    "HAJ": (-7.283321335332439, 112.77968466250103) 
}

# --- HELPER: PRINT NAVIGATION ---
def print_route_details(graph, route):
    street_names = []
    for i in range(len(route) - 1):
        u, v = route[i], route[i+1]
        edge_data = graph.get_edge_data(u, v)[0]
        if 'name' in edge_data:
            name = edge_data['name']
            if isinstance(name, list): name = " / ".join(name)
            street_names.append(name)
            
    clean_names = []
    for name in street_names:
        if not clean_names or clean_names[-1] != name:
            clean_names.append(name)
            
    print("\n--- TURN BY TURN NAVIGATION ---")
    print(" -> ".join(clean_names))
    print("-------------------------------")

# --- SECTION 1: LOAD & PREPARE MAP ---
center_point = (-7.2797, 112.7975) 
print("Downloading map data...")
G = ox.graph_from_point(center_point, dist=3000, network_type='drive')

hospital_nodes = {}
for code, (lat, lon) in hospitals.items():
    node_id = ox.distance.nearest_nodes(G, X=lon, Y=lat)
    hospital_nodes[code] = node_id

G_proj = ox.project_graph(G)

# --- NEW: ADD SPEEDS AND TIME ---
print("Calculating road speeds and travel times...")
G_proj = ox.add_edge_speeds(G_proj) 
G_proj = ox.add_edge_travel_times(G_proj)

# --- SECTION 2: SIMULATION CONTROLS ---
# (Sama seperti sebelumnya, bisa dicopy dari kode Dijkstra/BFS jika mau simulasi macet)
# A* akan menghindari jalan macet jika travel_time tinggi.

# --- SECTION 3: USER INPUT ---
print("\n--- MANUAL LOCATION PICKER ---")
default_input = "-7.28, 112.79" 
user_input = input(f"Paste start coordinates (Lat, Lon) [Enter for default]: ")
if not user_input.strip(): user_input = default_input

clean_input = user_input.replace('(', '').replace(')', '').replace(' ', '')
lat_str, lon_str = clean_input.split(',')
start_lat, start_lon = float(lat_str), float(lon_str)

start_node = ox.distance.nearest_nodes(G, X=start_lon, Y=start_lat)

# --- SECTION 4: A* (A-STAR) ALGORITHM ---

# 1. Define Heuristic Function (Euclidean Distance)
# A* needs to guess the remaining distance to the target to be smart.
def dist_heuristic(u, v):
    # Access x and y coordinates from the graph nodes
    # Because G_proj is projected, x and y are in meters
    x1, y1 = G_proj.nodes[u]['x'], G_proj.nodes[u]['y']
    x2, y2 = G_proj.nodes[v]['x'], G_proj.nodes[v]['y']
    
    # Pythagorean theorem (Euclidean distance)
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def find_fastest_hospital_astar(graph, start_node, hospital_nodes):
    shortest_time = float('inf')
    best_hospital = None
    best_path = None

    print("\nCalculating A* Routes (Smartest Path)...")

    for code, target_node in hospital_nodes.items():
        try:
            # NetworkX A* Implementation
            # heuristic: the function to estimate distance
            # weight: still uses 'travel_time' for accuracy
            path = nx.astar_path(graph, start_node, target_node, 
                                 heuristic=dist_heuristic, 
                                 weight='travel_time')
            
            # Calculate total time for this path manually since astar_path only returns nodes
            current_time = nx.path_weight(graph, path, weight='travel_time')
            
            print(f" -> A* found path to {code} in {current_time:.1f} seconds")

            if current_time < shortest_time:
                shortest_time = current_time
                best_hospital = code
                best_path = path
                
        except nx.NetworkXNoPath:
            continue
            
    return best_hospital, shortest_time, best_path

best_hosp, time_sec, route = find_fastest_hospital_astar(G_proj, start_node, hospital_nodes)

if best_hosp:
    full_name = hospital_names[best_hosp]
    minutes = time_sec / 60
    
    print(f"\n========================================")
    print(f"A* RECOMMENDED DESTINATION: {full_name}")
    print(f"ESTIMATED TRAVEL TIME: {minutes:.1f} minutes")
    print(f"ALGORITHM: A* (Heuristic Search)")
    print(f"========================================")
    
    print_route_details(G_proj, route)

    print("Displaying map...")
    fig, ax = ox.plot_graph_route(G_proj, route, route_color='g', route_linewidth=6, node_size=0)
    plt.show()
else:
    print("\nCRITICAL ALERT: No hospitals are reachable!")
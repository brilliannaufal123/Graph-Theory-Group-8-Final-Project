import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

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

# Map Nodes (Lat/Lon)
hospital_nodes = {}
for code, (lat, lon) in hospitals.items():
    node_id = ox.distance.nearest_nodes(G, X=lon, Y=lat)
    hospital_nodes[code] = node_id

# Project to Meters
G_proj = ox.project_graph(G)

# --- NEW: ADD SPEEDS AND TIME ---
print("Calculating road speeds and travel times...")
# impute_missing=True fills in unknown speeds with defaults (e.g. 30km/h)
G_proj = ox.add_edge_speeds(G_proj) 
G_proj = ox.add_edge_travel_times(G_proj)

# --- SECTION 2: SIMULATION CONTROLS ---

def set_road_condition(graph, road_name_fragment, status):
    """
    Modifies the 'travel_time' of roads matching the name.
    Status: 'BLOCKED' (Inf), 'FLOODED' (3x slower), 'NORMAL' (No change)
    """
    count = 0
    for u, v, k, data in graph.edges(keys=True, data=True):
        if 'name' in data:
            names = data['name'] if isinstance(data['name'], list) else [data['name']]
            for name in names:
                if road_name_fragment.lower() in name.lower():
                    if status == 'BLOCKED':
                        data['travel_time'] = float('inf')
                    elif status == 'FLOODED':  # CHANGED FROM MUDDY
                        data['travel_time'] *= 3  # Slow down by 3x due to water depth
                    count += 1
    print(f"SIMULATION APPLIED: '{road_name_fragment}' is now {status} (Affected {count} segments)")

# --- *** CONTROL PANEL: EDIT THIS TO TEST *** ---

# Example 1: Total blockage (Bridge collapse / Landslide)
# set_road_condition(G_proj, "Jalan Arief Rahman Hakim", "BLOCKED")
# Example 2: Shallow water (Driveable but slow)
# set_road_condition(G_proj, "Jalan Raya Kertajaya Indah", "FLOODED")

# ------------------------------------------------

# --- SECTION 3: USER INPUT ---
print("\n--- MANUAL LOCATION PICKER ---")
user_input = input("Paste start coordinates (Lat, Lon): ")
clean_input = user_input.replace('(', '').replace(')', '').replace(' ', '')
lat_str, lon_str = clean_input.split(',')
start_lat, start_lon = float(lat_str), float(lon_str)

start_node = ox.distance.nearest_nodes(G, X=start_lon, Y=start_lat)

# --- SECTION 4: DIJKSTRA (WEIGHT = TIME) ---

def find_fastest_hospital(graph, start_node, hospital_nodes):
    shortest_time = float('inf')
    best_hospital = None
    best_path = None

    for code, target_node in hospital_nodes.items():
        try:
            # NOTE: weight='travel_time' (seconds) instead of 'length'
            time_seconds = nx.shortest_path_length(graph, start_node, target_node, weight='travel_time')
            
            if time_seconds < shortest_time:
                shortest_time = time_seconds
                best_hospital = code
                best_path = nx.shortest_path(graph, start_node, target_node, weight='travel_time')
        except nx.NetworkXNoPath:
            continue
            
    return best_hospital, shortest_time, best_path

best_hosp, time_sec, route = find_fastest_hospital(G_proj, start_node, hospital_nodes)

if best_hosp:
    full_name = hospital_names[best_hosp]
    minutes = time_sec / 60
    
    print(f"\n========================================")
    print(f"RECOMMENDED DESTINATION: {full_name}")
    print(f"ESTIMATED TRAVEL TIME: {minutes:.1f} minutes")
    print(f"========================================")
    
    print_route_details(G_proj, route)

    print("Displaying map...")
    fig, ax = ox.plot_graph_route(G_proj, route, route_color='b', route_linewidth=6, node_size=0)
    plt.show()
else:
    print("\nCRITICAL ALERT: No hospitals are reachable!")
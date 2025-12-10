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
    """
    Prints the street names for the generated route turn-by-turn.
    """
    street_names = []
    for i in range(len(route) - 1):
        u, v = route[i], route[i+1]
        # Get edge data (index 0 for multi-di-graph)
        edge_data = graph.get_edge_data(u, v)[0]
        if 'name' in edge_data:
            name = edge_data['name']
            if isinstance(name, list): name = " / ".join(name)
            street_names.append(name)
            
    # Remove consecutive duplicates for cleaner output
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
# Load the drive network within 3km of the center point
G = ox.graph_from_point(center_point, dist=3000, network_type='drive')

# Find nearest nodes for hospitals
hospital_nodes = {}
for code, (lat, lon) in hospitals.items():
    node_id = ox.distance.nearest_nodes(G, X=lon, Y=lat)
    hospital_nodes[code] = node_id

# Project graph to UTM (meters) for accurate calculations if needed
G_proj = ox.project_graph(G)

# --- NEW: ADD SPEEDS AND TIME ---
print("Calculating road speeds and travel times...")
# Even though BFS doesn't use time to find the path, we calculate it 
# so we can tell the user how long the BFS route actually takes.
G_proj = ox.add_edge_speeds(G_proj) 
G_proj = ox.add_edge_travel_times(G_proj)

# --- SECTION 2: SIMULATION CONTROLS (BFS ADAPTED) ---

def set_road_condition(graph, road_name_fragment, status):
    """
    Simulates road conditions.
    
    NOTE FOR BFS: 
    - BFS ignores edge weights (speed/time). 
    - To stop BFS from using a road (BLOCKED), we must REMOVE the edge entirely.
    - 'FLOODED' (slow traffic) implies no change for BFS, as it only counts hops.
    """
    edges_to_remove = []
    count = 0
    
    # Iterate through all edges to find matching street names
    for u, v, k, data in graph.edges(keys=True, data=True):
        if 'name' in data:
            names = data['name'] if isinstance(data['name'], list) else [data['name']]
            for name in names:
                if road_name_fragment.lower() in name.lower():
                    if status == 'BLOCKED':
                        edges_to_remove.append((u, v, k))
                        count += 1
                    elif status == 'FLOODED':
                        # Optional: You could update time here for the final report,
                        # but it won't change the path chosen by BFS.
                        data['travel_time'] = data.get('travel_time', 1) * 3
                        
    # Apply modifications
    if status == 'BLOCKED':
        graph.remove_edges_from(edges_to_remove)
        print(f"SIMULATION APPLIED: '{road_name_fragment}' is BLOCKED (Removed {count} segments)")
    elif status == 'FLOODED':
        print(f"WARNING: '{road_name_fragment}' is FLOODED. BFS algorithm ignores speed, so the route might still pass here.")

# --- *** CONTROL PANEL: EDIT THIS TO TEST *** ---

# Example 1: Total blockage (Edge removal)
# set_road_condition(G_proj, "Jalan Arief Rahman Hakim", "BLOCKED")

# Example 2: Flooding (No effect on BFS path selection, only affects estimated time)
# set_road_condition(G_proj, "Jalan Raya Kertajaya Indah", "FLOODED")

# ------------------------------------------------

# --- SECTION 3: USER INPUT ---
print("\n--- MANUAL LOCATION PICKER ---")
# Default coordinates for quick testing
default_input = "-7.28, 112.79"
user_input = input(f"Paste start coordinates (Lat, Lon) [Press Enter for default {default_input}]: ")

if not user_input.strip():
    user_input = default_input

clean_input = user_input.replace('(', '').replace(')', '').replace(' ', '')
lat_str, lon_str = clean_input.split(',')
start_lat, start_lon = float(lat_str), float(lon_str)

# Find the nearest node to the user's input
start_node = ox.distance.nearest_nodes(G, X=start_lon, Y=start_lat)

# --- SECTION 4: BFS ALGORITHM (UNWEIGHTED) ---

def calculate_actual_time(graph, path):
    """
    Helper function to sum up 'travel_time' for a given path.
    Used to show the user the duration, even though BFS didn't optimize for it.
    """
    total_time = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        edge_data = graph.get_edge_data(u, v)[0]
        total_time += edge_data.get('travel_time', 0)
    return total_time

def find_nearest_hospital_bfs(graph, start_node, hospital_nodes):
    """
    Finds the route with the FEWEST HOPS (Breadth-First Search).
    """
    min_hops = float('inf')
    best_hospital = None
    best_path = None

    print("\nCalculating BFS Routes (Fewest Hops)...")

    for code, target_node in hospital_nodes.items():
        try:
            # BFS Implementation: shortest_path with weight=None
            path = nx.shortest_path(graph, start_node, target_node, weight=None)
            
            # Metric: Hops (number of edges)
            hops = len(path) - 1
            
            print(f" -> Checking {hospital_names[code]}: {hops} road segments")

            if hops < min_hops:
                min_hops = hops
                best_hospital = code
                best_path = path
                
        except nx.NetworkXNoPath:
            continue
            
    return best_hospital, min_hops, best_path

# Execute BFS
best_hosp, hops_count, route = find_nearest_hospital_bfs(G_proj, start_node, hospital_nodes)

# --- SECTION 5: RESULT & VISUALIZATION ---
if best_hosp:
    full_name = hospital_names[best_hosp]
    
    # Calculate real-world time for the user's information
    real_time_sec = calculate_actual_time(G_proj, route)
    minutes = real_time_sec / 60
    
    print(f"\n========================================")
    print(f"BFS RECOMMENDED DESTINATION: {full_name}")
    print(f"METRIC (Fewest Hops): {hops_count} road segments")
    print(f"ESTIMATED TIME: {minutes:.1f} minutes") 
    print(f"NOTE: BFS chooses the path with fewer turns/segments, not necessarily the fastest.")
    print(f"========================================")
    
    print_route_details(G_proj, route)

    print("Displaying map...")
    # Plotting the route in red
    fig, ax = ox.plot_graph_route(G_proj, route, route_color='r', route_linewidth=6, node_size=0)
    plt.show()
else:
    print("\nCRITICAL ALERT: No hospitals are reachable from this location!")
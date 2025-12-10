# ============================================================================
# HOSPITAL DATASET
# ============================================================================

# Hospital codes (25 major hospitals in Surabaya)
nodes = [
    "DST", "SIL", "MYP", "PRS", "NHS",
    "BHY", "UNA", "HSU", "RSL", "MRN",
    "AUS", "RKZ", "BDH", "ONK", "ADH",
    "MTK", "RYL", "JMR", "ALR", "PHC",
    "SMS", "SBI", "GTR", "WYS", "SEM"
]

# Hospital full names
hospital_names = {
    "DST": "RSUD Dr. Soetomo",
    "SIL": "Siloam Hospitals Surabaya",
    "MYP": "Mayapada Hospital Surabaya",
    "PRS": "Premier Surabaya Hospital",
    "NHS": "National Hospital Surabaya",
    "BHY": "Bhayangkara Hospital Surabaya",
    "UNA": "Airlangga University Hospital",
    "HSU": "Husada Utama Hospital",
    "RSL": "Naval Hospital Dr. Ramelan",
    "MRN": "Marine Corps Hospital Gunungsari",
    "AUS": "Air Force Hospital dr. Soemitro",
    "RKZ": "St. Vincentius a Paulo Hospital",
    "BDH": "Bhakti Dharma Husada Hospital",
    "ONK": "Surabaya Oncology Hospital",
    "ADH": "Adi Husada Undaan Hospital",
    "MTK": "Mitra Keluarga Surabaya Hospital",
    "RYL": "Royal Hospital Surabaya",
    "JMR": "Jemursari Islamic Hospital",
    "ALR": "Al-Irsyad Hospital Surabaya",
    "PHC": "PHC Hospital Surabaya",
    "SMS": "Surabaya Medical Service Hospital",
    "SBI": "Surabaya International Hospital",
    "GTR": "Gotong Royong Hospital",
    "WYS": "Wiyung Sejahtera Hospital",
    "SEM": "Sejahtera Medical Hospital"
}

# Hospital tiers (for priority routing)
hospital_tiers = {
    "DST": "Top-Tier", "SIL": "Top-Tier", "MYP": "Top-Tier", 
    "PRS": "Top-Tier", "NHS": "Top-Tier",
    "BHY": "Upper-Tier", "UNA": "Upper-Tier", "HSU": "Upper-Tier", 
    "RSL": "Upper-Tier", "MRN": "Upper-Tier", "AUS": "Upper-Tier",
    "RKZ": "Upper-Tier", "BDH": "Upper-Tier", "ONK": "Upper-Tier",
    "ADH": "Middle-Tier", "MTK": "Middle-Tier", "RYL": "Middle-Tier",
    "JMR": "Middle-Tier", "ALR": "Middle-Tier", "PHC": "Middle-Tier",
    "SMS": "Lower Middle-Tier", "SBI": "Lower Middle-Tier", 
    "GTR": "Lower Middle-Tier", "WYS": "Lower Middle-Tier", 
    "SEM": "Lower Middle-Tier"
}

inf = float('inf')

# ============================================================================
# ADJACENCY MATRIX (ROAD NETWORK)
# Distance in minutes between hospitals/locations
# You can modify this matrix based on real Google Maps data
# ============================================================================

graph = [
    # DST  SIL  MYP  PRS  NHS  BHY  UNA  HSU  RSL  MRN  AUS  RKZ  BDH  ONK  ADH  MTK  RYL  JMR  ALR  PHC  SMS  SBI  GTR  WYS  SEM
    [ 0.0, 15.0, 18.0, inf, 12.0, 20.0, 8.0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf],  # 0 DST
    [15.0,  0.0, 10.0, 22.0, inf, inf, inf, 25.0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf],  # 1 SIL
    [18.0, 10.0,  0.0, 14.0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf],  # 2 MYP
    [ inf, 22.0, 14.0,  0.0, 16.0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 30.0, inf, inf, inf, inf, inf],  # 3 PRS
    [12.0, inf, inf, 16.0,  0.0, 18.0, 10.0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf],  # 4 NHS
    [20.0, inf, inf, inf, 18.0,  0.0, 15.0, inf, inf, inf, 25.0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf],  # 5 BHY
    [ 8.0, inf, inf, inf, 10.0, 15.0,  0.0, 12.0, 14.0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf],  # 6 UNA
    [ inf, 25.0, inf, inf, inf, inf, 12.0,  0.0, 20.0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf],  # 7 HSU
    [ inf, inf, inf, inf, inf, inf, 14.0, 20.0,  0.0, 22.0, 18.0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf],  # 8 RSL
    [ inf, inf, inf, inf, inf, inf, inf, inf, 22.0,  0.0, 16.0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf],  # 9 MRN
    [ inf, inf, inf, inf, inf, 25.0, inf, inf, 18.0, 16.0,  0.0, 28.0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf],  # 10 AUS
    [ inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 28.0,  0.0, 20.0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf],  # 11 RKZ
    [ inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 20.0,  0.0, 15.0, 18.0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf],  # 12 BDH
    [ inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 15.0,  0.0, 12.0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf],  # 13 ONK
    [ inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 18.0, 12.0,  0.0, 22.0, inf, inf, inf, inf, inf, inf, inf, inf, inf],  # 14 ADH
    [ inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 22.0,  0.0, 14.0, 25.0, inf, inf, inf, inf, inf, inf, inf],  # 15 MTK
    [ inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 14.0,  0.0, 18.0, 20.0, inf, inf, inf, inf, inf, inf],  # 16 RYL
    [ inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 25.0, 18.0,  0.0, 16.0, inf, inf, 30.0, inf, inf, inf],  # 17 JMR
    [ inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 20.0, 16.0,  0.0, 22.0, inf, inf, inf, inf, inf],  # 18 ALR
    [ inf, inf, inf, 30.0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 22.0,  0.0, 28.0, inf, inf, inf, inf],  # 19 PHC
    [ inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 28.0,  0.0, 20.0, 25.0, inf, inf],  # 20 SMS
    [ inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 30.0, inf, inf, 20.0,  0.0, 18.0, inf, inf],  # 21 SBI
    [ inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 25.0, 18.0,  0.0, 22.0, inf],  # 22 GTR
    [ inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 22.0,  0.0, 20.0],  # 23 WYS
    [ inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 20.0,  0.0]   # 24 SEM
]

# ============================================================================
# ROAD STATUS (FOR DISASTER SIMULATION)
# Modify this to simulate flooded or blocked roads
# Format: (from_index, to_index): status
# Status: "OPEN", "FLOODED" (3x time), "BLOCKED" (infinite time)
# ============================================================================

road_status = {}  # Empty means all roads are OPEN by default

def set_road_status(from_node, to_node, status):
    """Set road status for disaster simulation"""
    i = nodes.index(from_node)
    j = nodes.index(to_node)
    road_status[(i, j)] = status
    road_status[(j, i)] = status  # Bidirectional

def get_effective_distance(i, j, base_distance):
    """Get effective distance considering road status"""
    if base_distance == inf or base_distance == 0.0:
        return base_distance
    
    status = road_status.get((i, j), "OPEN")
    
    if status == "BLOCKED":
        return inf
    elif status == "FLOODED":
        return base_distance * 3.0  # 3x penalty for flooded roads
    else:
        return base_distance

# ============================================================================
# DIJKSTRA'S ALGORITHM IMPLEMENTATION
# ============================================================================

def dijkstra(graph, start_node_index):
    """
    Implementation of Dijkstra's Algorithm using an Adjacency Matrix.
    
    Args:
        graph: 2D adjacency matrix (list of lists)
        start_node_index: Index of the starting node
    
    Returns:
        distances: List of shortest distances from start to each node
        previous_nodes: List of parent nodes for path reconstruction
    """
    num_nodes = len(graph)
    
    # Initialize data structures
    distances = [inf] * num_nodes
    visited = [False] * num_nodes
    previous_nodes = [-1] * num_nodes
    
    # Distance from start to itself is 0
    distances[start_node_index] = 0
    
    # Main Dijkstra loop
    for _ in range(num_nodes):
        # Find unvisited node with minimum distance
        min_dist = inf
        u = -1
        
        for i in range(num_nodes):
            if not visited[i] and distances[i] < min_dist:
                min_dist = distances[i]
                u = i
        
        # If no reachable unvisited node found, break
        if u == -1:
            break
        
        # Mark current node as visited
        visited[u] = True
        
        # Relax edges: update distances to neighbors
        for v in range(num_nodes):
            base_dist = graph[u][v]
            
            # Check if edge exists (not infinity and not self-loop)
            if base_dist > 0 and base_dist != inf and not visited[v]:
                # Get effective distance considering road status
                effective_dist = get_effective_distance(u, v, base_dist)
                
                if effective_dist != inf:
                    new_dist = distances[u] + effective_dist
                    
                    # Update if we found a shorter path
                    if new_dist < distances[v]:
                        distances[v] = new_dist
                        previous_nodes[v] = u
    
    return distances, previous_nodes

# ============================================================================
# PATH RECONSTRUCTION
# ============================================================================

def get_path(previous_nodes, node_names, start_index, end_index):
    """
    Reconstruct the path from start to end using parent pointers.
    
    Args:
        previous_nodes: List of parent indices from Dijkstra
        node_names: List of node names
        start_index: Starting node index
        end_index: Ending node index
    
    Returns:
        String representation of the path, or "No path" if unreachable
    """
    path = []
    current_index = end_index
    
    # Backtrack from end to start
    while current_index != -1:
        path.append(node_names[current_index])
        current_index = previous_nodes[current_index]
    
    # Reverse to get path from start to end
    path.reverse()
    
    # Check if valid path exists
    if path[0] == node_names[start_index]:
        return " -> ".join(path)
    else:
        return "No path"

# ============================================================================
# MAIN PROGRAM
# ============================================================================

def main():
    """Main program execution"""
    
    print("="*90)
    print("DIJKSTRA'S ALGORITHM - HOSPITAL EVACUATION ROUTING SYSTEM")
    print("GROUP 8: Resilient Routing for Disaster-Proof Hospital Access")
    print("="*90)
    print()
    
    # ========================================================================
    # CONFIGURATION SECTION - MODIFY HERE
    # ========================================================================
    
    # Set starting location (emergency site)
    start_hospital = "UNA"  # Change this to any hospital code
    
    # Simulate disaster conditions (optional)
    # Uncomment and modify these lines to simulate road damage:
    
    # set_road_status("DST", "SIL", "FLOODED")   # Road is flooded (3x time)
    # set_road_status("MYP", "PRS", "BLOCKED")   # Road is completely blocked
    # set_road_status("UNA", "HSU", "FLOODED")   # Another flooded road
    
    # ========================================================================
    
    # Get index of starting hospital
    try:
        start_index = nodes.index(start_hospital)
    except ValueError:
        print(f"ERROR: Hospital code '{start_hospital}' not found in database.")
        print(f"Available codes: {', '.join(nodes)}")
        return
    
    # Run Dijkstra's algorithm
    print(f"Starting Location: {start_hospital} - {hospital_names[start_hospital]}")
    print(f"Tier: {hospital_tiers[start_hospital]}")
    print()
    
    # Display any active road restrictions
    if road_status:
        print("⚠️  ACTIVE ROAD RESTRICTIONS:")
        displayed = set()
        for (i, j), status in road_status.items():
            if (i, j) not in displayed and (j, i) not in displayed:
                print(f"   {nodes[i]} <-> {nodes[j]}: {status}")
                displayed.add((i, j))
                displayed.add((j, i))
        print()
    
    distances, prev_nodes = dijkstra(graph, start_index)
    
    # Display results
    print("="*90)
    print(f"{'Hospital Code':<15} | {'Hospital Name':<40} | {'Distance (min)':<15} | {'Route'}")
    print("-"*90)
    
    for i in range(len(nodes)):
        # Skip the starting hospital itself
        if i == start_index:
            continue
        
        hospital_code = nodes[i]
        hospital_name = hospital_names[hospital_code]
        distance = distances[i]
        
        if distance == inf:
            distance_str = "Not Reachable"
            path_str = "-"
        else:
            distance_str = f"{distance:.1f}"
            path_str = get_path(prev_nodes, nodes, start_index, i)
        
        # Add tier indicator
        tier = hospital_tiers[hospital_code]
        hospital_display = f"{hospital_name} [{tier}]"
        
        print(f"{hospital_code:<15} | {hospital_display:<40} | {distance_str:<15} | {path_str}")
    
    print("="*90)
    
    # Find nearest reachable top-tier hospital
    print("\n🏥 RECOMMENDED EVACUATION DESTINATIONS:")
    print("-"*90)
    
    tier_priority = ["Top-Tier", "Upper-Tier", "Middle-Tier", "Lower Middle-Tier"]
    
    for tier in tier_priority:
        tier_hospitals = [(i, distances[i]) for i in range(len(nodes)) 
                         if i != start_index and hospital_tiers[nodes[i]] == tier 
                         and distances[i] != inf]
        
        if tier_hospitals:
            # Sort by distance
            tier_hospitals.sort(key=lambda x: x[1])
            
            print(f"\n{tier} Hospitals:")
            for rank, (idx, dist) in enumerate(tier_hospitals[:3], 1):  # Show top 3
                code = nodes[idx]
                name = hospital_names[code]
                path = get_path(prev_nodes, nodes, start_index, idx)
                print(f"  {rank}. {code} - {name}")
                print(f"     Distance: {dist:.1f} minutes")
                print(f"     Route: {path}")
    
    print("\n" + "="*90)
    print("ALGORITHM COMPLETED SUCCESSFULLY")
    print("="*90)

if __name__ == "__main__":
    main()
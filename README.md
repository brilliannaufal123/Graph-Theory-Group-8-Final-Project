# Resilient Routing: Disaster-Proof Hospital Access System

| Name | NRP | Class |
| ---  | --- | --- |
| Bismantaka Revano Dirgantara | 5025241075 | IUP |
| Naufal Bintang Brillian | 5025241168 | IUP |
| Stephanie Gabriella Adiseputra | 5025241081 | IUP |


## 1. Project Overview
Indonesia is highly susceptible to floods and infrastructure failure, which often isolates communities from critical healthcare. Standard GPS systems calculate routes based on static maps, failing to account for sudden disasters like flash floods or collapsed bridges.

**Resilient Routing** is a Python-based Decision Support System (DSS) that models the Surabaya ITS/Sukolilo area as a dynamic graph. Unlike standard navigation, this system allows operators to simulate road failures in real-time and calculates the safest, fastest evacuation route to the nearest of three major hospitals.

## 2. Key Features
* **Real-World Data:** Utilizes `osmnx` to fetch live street network data from OpenStreetMap.
* **Time-Based Routing:** Calculates routes based on estimated travel time (seconds), not just distance.
* **Disaster Simulation:** Allows operators to mark specific roads as:
    * **FLOODED:** Increases travel time by 3x (simulating driving through water).
    * **BLOCKED:** Sets travel time to Infinity (road is impassable).
* **Multi-Target Analysis:** Automatically runs Dijkstra’s Algorithm to three different hospitals simultaneously and selects the best destination based on current road conditions.

## 3. Hospital Targets
The system evaluates routes to these three facilities:
1.  **RS UNAIR:** RS Universitas Airlangga (North-West)
2.  **ITS Medical Center:** Internal Campus Clinic (Central)
3.  **RSUD Haji:** General Hospital (South-West)

## 4. How It Works (Technical Explanation)

### A. Graph Construction
The system downloads the road network for a 3km radius around ITS Surabaya.
* **Nodes ($V$):** Intersections and locations.
* **Edges ($E$):** Roads connecting them.
* **Weights ($W$):** We convert road length into **Travel Time** using estimated speed limits.

### B. The Disaster Logic
Before routing, the system applies a modifier function `set_road_condition(Graph, StreetName, Status)`.
Mathematically, the weight of an edge $e$ is modified as:

$$
W_{new}(e) =
\begin{cases}
W_{original}(e) & \text{if Status = NORMAL} \\
W_{original}(e) \times 3 & \text{if Status = FLOODED} \\
\infty & \text{if Status = BLOCKED}
\end{cases}
$$

### C. The Routing Algorithm
The system uses **Dijkstra’s Algorithm** to find the shortest path from the user's location ($S$).
1.  It calculates $D_{UNA} = \text{Dijkstra}(S, \text{RS UNAIR})$
2.  It calculates $D_{ITS} = \text{Dijkstra}(S, \text{ITS Med Center})$
3.  It calculates $D_{HAJ} = \text{Dijkstra}(S, \text{RSUD Haji})$
4.  It compares the results:
    $$\text{Best Destination} = \min(D_{UNA}, D_{ITS}, D_{HAJ})$$

This ensures that if the road to the closest hospital (geographically) is blocked, the system automatically reroutes the ambulance to the next best hospital that is actually reachable.

### IMAGE EXAMPLE:

<img width="846" height="919" alt="image" src="https://github.com/user-attachments/assets/7fa4748a-6204-487e-85dc-bf58cdfecf3f" />

(pointing to Medical Center ITS)

## 5. Requirements & Installation
Ensure you have Python installed. Install the required libraries:

```bash
pip install osmnx networkx matplotlib scipy scikit-learn
```
## 6. How to Run & Test

1.  **Run the script:**
    ```bash
    python dijkstra.py
    OR
    python bfs.py
    OR
    python astar.py
    ```

2.  **Configure Disasters (Optional):**
    Open the script and edit the `CONTROL PANEL` section to simulate disasters:
    ```python
    # Example: Block the main highway
    set_road_condition(G_proj, "Jalan Raya Kertajaya Indah", "BLOCKED")
    ```

3.  **Input Location:**
    When prompted, paste coordinates from Google Maps.
    * *Test Coordinate (Inside ITS):* `-7.2824, 112.7954`

## 7. Example Scenarios

### Scenario A: Normal Conditions
* **Input:** User is at ITS Library.
* **Status:** All roads Open.
* **Result:** System routes to **Medical Center ITS** (1.7 mins) via the main gate.

### Scenario B: The "Muddy" Road
* **Input:** User is at ITS Library.
* **Status:** "Jalan Arief Rahman Hakim" is **FLOODED**.
* **Result:** The main route is now too slow. The system reroutes the user to **RSUD Haji** (2.3 mins) because the highway is faster than the flooded main gate.

### Scenario C: Total Lockdown
* **Input:** User is at ITS Library.
* **Status:** Main Highway (Kertajaya) and Main Gate (Arief Rahman) are **BLOCKED**.
* **Result:** System finds a "rat path" (*jalan tikus*) through the residential area (Jalan Gebang Lor) to bypass the blockage, proving the system's resilience.

## 8. Code Implementation Details (dijkstra.py)

This section explains the logic behind the `dijkstra.py` script, breaking down how the graph theory concepts are applied in Python.

### A. Library Imports
```python
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
```
* **osmnx:** The core library used to download real-world street networks from OpenStreetMap and convert them into graph objects.
* **networkx:** The mathematical engine that performs the graph algorithms (Dijkstra, Shortest Path).
* **matplotlib:** Used to visualize the final result (the map and the route line).

### B. Configuration & Helper Functions
```python
hospital_names = { ... }
hospitals = { "UNA": (-7.269, 112.784), ... }

def print_route_details(graph, route):
    # ... (extracts street names from edge data)
```
* **Dataset:** We define dictionaries to map hospital codes (e.g., "UNA") to their human-readable names and real-world Latitude/Longitude coordinates.
* **Navigation Helper:** The print_route_details function takes the list of Node IDs returned by Dijkstra and looks up the name attribute of the Edges connecting them. This converts a mathematical path (Node 1 -> Node 2) into human instructions ("Jalan Raya ITS -> Jalan Kertajaya").

### C. Map Loading & Node Mapping
```python
center_point = (-7.2797, 112.7975)
G = ox.graph_from_point(center_point, dist=3000, network_type='drive')

for code, (lat, lon) in hospitals.items():
    node_id = ox.distance.nearest_nodes(G, X=lon, Y=lat)
    hospital_nodes[code] = node_id
```
* **Graph Creation:** We download the driveable road network within a 3km radius of ITS.
* **Nodes:** Intersections.
* **Edges:** Roads.
* **Nearest Node Mapping:** Graph algorithms cannot work with raw GPS coordinates (floats). We must "snap" the hospital coordinates to the nearest actual intersection (Node ID) on the map using ox.distance.nearest_nodes.

### D. Graph Projection & Weight Calculation
```python
G_proj = ox.project_graph(G)
G_proj = ox.add_edge_speeds(G_proj) 
G_proj = ox.add_edge_travel_times(G_proj)
```
* **Projection:** We convert the graph from Latitude/Longitude (degrees) to UTM (meters). This is essential for accurate distance measurement.
* **Time Calculation:** Standard Dijkstra uses distance. To support "Fastest Time," we calculate the time required to traverse every edge: $$\text{Travel Time} = \frac{\text{Length (meters)}}{\text{Speed Limit (m/s)}}$$ This creates a new attribute 'travel_time' on every edge.

### E. Disaster Simulation Logic
```python
def set_road_condition(graph, road_name_fragment, status):
    # Iterates through all edges to find matching road names
    if status == 'BLOCKED':
        data['travel_time'] = float('inf')
    elif status == 'FLOODED':
        data['travel_time'] *= 3
```
This function is the core of the Decision Support System.
1. It scans every road segment in the graph.
2. If a road name matches the input (e.g., "Jalan Raya ITS"), it modifies the edge weight:
* **BLOCKED:** Sets time to Infinity. Dijkstra will never select an infinite edge.
* **FLOODED:** Multiplies time by 3. Dijkstra will only select this if the detour is 3x longer than the flooded path.

### F. The Multi-Target Routing Algorithm
```python
def find_fastest_hospital(graph, start_node, hospital_nodes):
    shortest_time = float('inf')
    
    for code, target_node in hospital_nodes.items():
        time = nx.shortest_path_length(..., weight='travel_time')
        
        if time < shortest_time:
            shortest_time = time
            best_hospital = code
            best_path = ...
```
This block executes the routing strategy:
1. It iterates through all 3 hospitals.
2. It runs Dijkstra's Algorithm for each one, using 'travel_time' as the weight.
3. It compares the results. If the path to RSUD Haji is 180 seconds, but the path to Medical Center ITS is 600 seconds (due to floods), it automatically selects RSUD Haji as the best_hospital.

### G. Execution & Visualization
```python
# User Input Processing
start_node = ox.distance.nearest_nodes(...)

# Run Algorithm
best_hosp, time, route = find_fastest_hospital(...)

# Visualization
ox.plot_graph_route(G_proj, route, route_color='b', ...)
```
* **User Input:** Converts the pasted text string into float coordinates and snaps them to a Start Node.
* **Plotting:** Uses matplotlib to render the map background (black) and overlays the calculated optimal route (blue line).

## 9. Code Implementation Details (bfs.py)

This section details the logic behind the `bfs.py` script. Unlike the Dijkstra implementation which focuses on time, this script focuses on topological simplicity (number of turns/segments).

### A. Library Imports
```python
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
```

- **osmnx & networkx**: The core libraries used for graph construction and algorithmic processing.
- **matplotlib**: Used to visualize the route (rendered in Red for BFS to distinguish from Dijkstra's Blue).

### B. Configuration & Helper Functions
```
hospital_names = { ... }
hospitals = { "UNA": (-7.269, 112.784), ... }

def print_route_details(graph, route):
    # ... (extracts street names from edge data)
```
- **Dataset**: We define the same dictionaries as the Dijkstra script to map hospital codes to coordinates. This ensures consistency across all experiments.
- **Navigation Helper**: The `print_route_details` function converts the list of Node IDs returned by BFS into human-readable street names.

### C. Map Loading & Graph Preparation
```
center_point = (-7.2797, 112.7975)
G = ox.graph_from_point(center_point, dist=3000, network_type='drive')
G_proj = ox.project_graph(G)

# Note: Speeds are calculated ONLY for reporting, not for routing
G_proj = ox.add_edge_travel_times(G_proj)
```
- **Graph Creation**: We download the same 3km radius network around ITS.
- **The Difference**: While we still calculate `travel_time` attributes using `add_edge_travel_times`, BFS does not use them for decision making. They are calculated solely to show the user "how long" the BFS path would actually take in the real world (usually highlighting its inefficiency).

### D. Disaster Logic (Topology vs. Weights)
```
def set_road_condition(graph, road_name_fragment, status):
    if status == 'BLOCKED':
        graph.remove_edges_from(edges_to_remove)
    elif status == 'FLOODED':
        print("WARNING: BFS ignores speed, route might pass here.")
```
This function highlights the fundamental limitation of BFS in disaster scenarios:

1 - **BLOCKED (Edge Removal)**: BFS ignores edge weights (infinity doesn't stop it). To simulate a blockage in BFS, we must physically remove the edge from the graph topology ($E' = E - \{e_{blocked}\}$). <br>
2 - **FLOODED (Ignored)**: Since BFS treats every road as "1 Hop," it cannot process the concept of a "slow" road. The script issues a warning, but the algorithm will likely still route through the flood if it is the shortest path by segment count.

### E. The BFS Routing Algorithm
```
def find_nearest_hospital_bfs(graph, start_node, hospital_nodes):
    min_hops = float('inf')
    
    for code, target_node in hospital_nodes.items():
        # Key Difference: weight=None for Unweighted Search
        path = nx.shortest_path(graph, start_node, target_node, weight=None)
        hops = len(path) - 1
        
        if hops < min_hops:
            min_hops = hops
            best_hospital = code
```

This is the core algorithmic difference:

- **Unweighted Search**: We call `nx.shortest_path` with `weight=None`.
- **The Metric**: The "cost" is defined strictly by the number of edges (Hops).
- **Logic**: A 5km highway (1 edge) and a 100m alleyway (1 edge) are treated as identical costs.


### F. Execution & Post-Calculation
```
# 1. Run BFS
best_hosp, hops_count, route = find_nearest_hospital_bfs(...)

# 2. Calculate actual time for user reference
real_time_sec = calculate_actual_time(G_proj, route)

# 3. Visualization
ox.plot_graph_route(..., route_color='r')
```

- **Post-Processing**: Since BFS doesn't optimize for time, we run a custom helper function `calculate_actual_time` after the route is found. This sums up the travel times of the chosen path segments to demonstrate the difference between "Simplest Path" and "Fastest Path" to the user.
- **Visualization**: The route is plotted in Red to visually differentiate it from the optimal Dijkstra/A* path.


## 10. Code Implementation Details (astar.py)

This section explains the logic behind the `astar.py` script. A* is an "informed" search algorithm that improves upon Dijkstra by using a heuristic to estimate the remaining distance to the goal, allowing it to search more efficiently.

### A. Library Imports
```
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import math
```
- **math**: This is the key addition compared to the other scripts. We use `math` to calculate the square root required for the Euclidean distance (Pythagorean theorem).
- **osmnx, networkx, matplotlib**: Standard graph and visualization libraries.

### B. Map Loading & Graph Projection
```
center_point = (-7.2797, 112.7975)
G = ox.graph_from_point(center_point, dist=3000, network_type='drive')
G_proj = ox.project_graph(G)

# Speeds are crucial for A* (g-score)
G_proj = ox.add_edge_speeds(G_proj) 
G_proj = ox.add_edge_travel_times(G_proj)
```
- **Projecting** *($x, y$)*: The `ox.project_graph(G)` step is absolutely critical for A*. It converts the coordinate system from Degrees (Lat/Lon) to Meters (UTM).
- It's beacuse the heuristic function needs to calculate distance in meters. If we didn't project the graph, the Pythagorean theorem would calculate distance in "degrees," which would break the algorithm.

### C. The Heuristic Function (Euclidean Distance)
```
def dist_heuristic(u, v):
    # Access x and y coordinates (in meters) from the graph nodes
    x1, y1 = G_proj.nodes[u]['x'], G_proj.nodes[u]['y']
    x2, y2 = G_proj.nodes[v]['x'], G_proj.nodes[v]['y']
    
    # Pythagorean theorem
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
```

This function is the "brain" of A*.
1 - **Input**: It takes the current node u and the target node v (the hospital).
2 - **Logic**: It calculates the straight-line distance ("as the crow flies") using the standard distance formula: $d = \sqrt{(x_1-x_2)^2 + (y_1-y_2)^2}$.
3 - **Result**: This value ( $h(n)$ ) allows the algorithm to prioritize roads that geographically lead towards the hospital, rather than exploring in all directions like Dijkstra.

### D. The A* Routing Algorithm
```
def find_fastest_hospital_astar(graph, start_node, hospital_nodes):
    shortest_time = float('inf')
    
    for code, target_node in hospital_nodes.items():
        # A* Implementation:
        # heuristic: The function we defined above
        # weight: 'travel_time' (actual cost to drive)
        path = nx.astar_path(graph, start_node, target_node, 
                             heuristic=dist_heuristic, 
                             weight='travel_time')
        
        # Calculate exact time cost
        current_time = nx.path_weight(graph, path, weight='travel_time')
```

- **Dual Metrics**: The algorithm minimizes $f(n) = g(n) + h(n)$.
   - `weight='travel_time'` represents $g(n)$ (the actual time spent driving so far).
   - `heuristic=dist_heuristic` represents $h(n)$ (the estimated distance remaining).
- **Optimization**: This ensures we find the fastest path (like Dijkstra) but explore fewer unnecessary nodes (efficiency).

### E. Execution & Visualization
```
# 1. Run A*
best_hosp, time_sec, route = find_fastest_hospital_astar(...)

# 2. Visualization
ox.plot_graph_route(G_proj, route, route_color='g', ...)
```

- **Output**: The system prints the estimated travel time in minutes.
- **Visualization**: The optimal route is plotted in Green ('g') to distinguish the "Smart Path" (A*) from the "Shortest Path" (Dijkstra - Blue) and the "Simplest Path" (BFS - Red).

---

## Comparative Analysis: BFS vs. Dijkstra vs. A*

To validate the reliability of the **Resilient Routing System**, we implemented and tested three fundamental Graph Theory algorithms under identical simulated disaster conditions. The goal was to determine which algorithm offers the best balance between computational speed, path safety, and optimality.

### 1. Algorithm Behavior Overview

| Metric | **Breadth-First Search (BFS)** | **Dijkstra's Algorithm** | **A* (A-Star) Search** |
| :--- | :--- | :--- | :--- |
| **Graph Type** | Unweighted | Weighted ($W_{time}$) | Weighted ($W_{time}$) + Heuristic |
| **Optimization Goal** | Fewest Hops (Edges) | Lowest Travel Time | Lowest Travel Time (Greedy) |
| **Disaster Awareness** | ❌ **Fails** (Ignores Weights) | ✅ **Success** (Respects Penalties) | ✅ **Success** (Respects Penalties) |
| **Complexity** | $O(V + E)$ | $O((V + E) \log V)$ | Optimized $O((V + E) \log V)$ |
| **Verdict** | **Unsafe for Navigation** | **Reliable Standard** | **Best for Scalability** |

### 2. Critical Analysis of Results

#### A. The "Blindness" of BFS
Breadth-First Search treats the map as a **Topological Graph**, ignoring physical distances and speed limits.
* **The Flaw:** In our simulation, BFS consistently selected "Rat Paths" (*jalan tikus*) through residential areas (e.g., *Jalan Gebang*).
* **Why it failed:** BFS considers a 5km highway and a 500m alleyway as equal cost (1 Edge). It prefers a path with 5 intersections through a slow neighborhood over a path with 10 intersections on a fast highway.
* **Safety Risk:** Crucially, BFS **ignored the `FLOODED` status**. Since it does not read edge weights, it routed the ambulance through deep water simply because that path had fewer turns.

#### B. The Accuracy of Dijkstra
Dijkstra's Algorithm treats the map as a **Weighted Graph**, where $W(e) = \text{Travel Time}$.
* **The Logic:** It explores all directions uniformly from the source until the target is found.
* **Disaster Handling:** When we simulated a flood on *Jalan Arief Rahman Hakim* (multiplying weight by 3), Dijkstra correctly calculated that the "longer" route via the Ring Road (MERR) was actually faster in seconds.
* **Conclusion:** It guarantees the mathematically optimal path relative to the road conditions.

#### C. The Efficiency of A* (A-Star)
A* is an extension of Dijkstra that uses a **Heuristic Function** to prioritize search direction.
* **The Formula:**
    $$f(n) = g(n) + h(n)$$
    Where:
    * $g(n)$: Actual travel time from the start node.
    * $h(n)$: **Euclidean Distance** from node $n$ to the Hospital (Target).
* **The Result:** In our tests, A* produced the **exact same path** as Dijkstra but explored significantly fewer nodes. By using the coordinate distance as a compass, it ignored roads moving away from the hospital.

### 3. Case Study Simulation

**Scenario:** Traveling from *ITS Library* to *RS UNAIR*.
* **Road Condition:** Main road (*Jl. Kertajaya*) is heavily congested (High Travel Time). Residential road (*Jl. Gebang*) is short but slow.

**Result Comparison:**
1.  **BFS Route:** Takes *Jl. Gebang* (Residential).
    * *Reasoning:* "It only has 4 turns."
    * *Outcome:* **8.5 Minutes** (Too slow for emergency).
2.  **Dijkstra / A-star Route:** Takes *Jl. Dr. Ir. H. Soekarno* (MERR).
    * *Reasoning:* "Even though it has 12 intersections, the speed limit is 60km/h."
    * *Outcome:* **4.2 Minutes** (Optimal).

### 4. Final Conclusion
While **BFS** is useful for network connectivity checks, it is dangerous for emergency routing due to its inability to process variable edge weights (disasters).

**A* (A-Star) is the superior choice** for this Decision Support System. It combines the safety guarantees of Dijkstra which is accurately avoiding blocked and flooded roads with the computational efficiency required for real-time decision-making in a large-scale urban graph.

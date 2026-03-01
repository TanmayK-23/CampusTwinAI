import networkx as nx

campus_graph = nx.Graph()
# Add edges with 'time' (minutes) as weight
campus_graph.add_edge("Gate1", "MB_Block", weight=3)
campus_graph.add_edge("MB_Block", "Hostel", weight=5)
campus_graph.add_edge("Hostel", "Canteen", weight=2)
campus_graph.add_edge("Canteen", "Biotech_Block", weight=4)
campus_graph.add_edge("Biotech_Block", "TP1", weight=3)
campus_graph.add_edge("TP1", "TP2", weight=2)
campus_graph.add_edge("TP2", "Auditorium", weight=3)
campus_graph.add_edge("Auditorium", "Ground", weight=4)
campus_graph.add_edge("Ground", "Gate1", weight=5)
# Cross paths
campus_graph.add_edge("MB_Block", "Canteen", weight=3)
campus_graph.add_edge("Gate1", "Auditorium", weight=6)

def optimize_route(current_stop: str, target_stops: list[str]) -> dict:
    """
    Given the current stop and a list of target stops with high demand,
    calculate the shortest path covering them. For simplicity in demo,
    we find the shortest path from current to the closest target, etc.
    """
    if not target_stops:
        return {"route": [], "total_time": 0, "delay_reduction_pct": 0}
        
    route = [current_stop]
    total_time = 0
    
    unvisited = target_stops.copy()
    current = current_stop
    
    while unvisited:
        # Find closest unvisited target using Dijkstra
        closest_target = None
        min_dist = float('inf')
        path_to_closest = []
        
        for tgt in unvisited:
            try:
                # networkx generic dijkstra
                path = nx.shortest_path(campus_graph, current, tgt, weight='weight')
                dist = nx.shortest_path_length(campus_graph, current, tgt, weight='weight')
                if dist < min_dist:
                    min_dist = dist
                    closest_target = tgt
                    path_to_closest = path
            except nx.NetworkXNoPath:
                continue
                
        if not closest_target: break
        
        # Add path (excluding start node to prevent duplication)
        route.extend(path_to_closest[1:])
        total_time += min_dist
        current = closest_target
        unvisited.remove(closest_target)
        
    # Standard complete round robin path takes roughly 20 mins. Calculate reduction.
    base_time = 24  # static naive round trip assumption
    savings = max(0, base_time - total_time)
    delay_reduction_pct = round((savings / base_time) * 100) if base_time > 0 else 0
        
    return {
        "suggested_route": route,
        "total_time_mins": total_time,
        "expected_delay_reduction_pct": delay_reduction_pct
    }

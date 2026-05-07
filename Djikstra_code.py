import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

edges = [
    ("Warehouse", "Area1", {"distance": 4, "traffic": 2}),
    ("Warehouse", "Area2", {"distance": 6, "traffic": 5}),
    ("Area1", "Area3", {"distance": 3, "traffic": 1}),
    ("Area2", "Area3", {"distance": 2, "traffic": 3}),
    ("Area3", "Customer1", {"distance": 5, "traffic": 2}),
    ("Area2", "Customer2", {"distance": 7, "traffic": 4}),
    ("Area1", "Customer2", {"distance": 6, "traffic": 2}),
    
    ("Area3", "Customer3", {"distance": 4, "traffic": 3}),
    ("Area2", "Customer3", {"distance": 5, "traffic": 2}),
    
    ("Area1", "Customer4", {"distance": 3, "traffic": 3}),
    ("Area3", "Customer4", {"distance": 6, "traffic": 2})
]

for u, v, w in edges:
    distance = w["distance"]
    traffic = w["traffic"]
    total_weight = distance + traffic

    G.add_edge(u, v, weight=total_weight, distance=distance, traffic=traffic)

print("Available locations:", list(G.nodes()))

start = input("Enter start location: ")
destinations_input = input("Enter destinations (comma separated): ")
destinations = [d.strip() for d in destinations_input.split(",")]

current = start
full_path = []
total_cost = 0
total_distance = 0
all_path_edges = []

while destinations:
    shortest = None
    shortest_path = None
    min_cost = float('inf')

    for dest in destinations:
        path = nx.shortest_path(G, source=current, target=dest, weight='weight')
        cost = nx.shortest_path_length(G, source=current, target=dest, weight='weight')

        if cost < min_cost:
            min_cost = cost
            shortest = dest
            shortest_path = path

    full_path.extend(shortest_path[:-1])
    total_cost += min_cost

    path_edges = list(zip(shortest_path, shortest_path[1:]))
    all_path_edges.extend(path_edges)

    total_distance += sum(G[u][v]["distance"] for u, v in path_edges)

    current = shortest
    destinations.remove(shortest)

full_path.append(current)

print("Full Delivery Path:", full_path)
print("Total Cost:", total_cost)
print("Total Distance:", total_distance, "km")

speed = 40
eta = total_distance / speed

print("Estimated Time:", round(eta, 2), "hours")

pos = nx.spring_layout(G)

nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000)

nx.draw_networkx_edges(G, pos, edgelist=all_path_edges, edge_color='red', width=3)

edge_labels = {}
for u, v, data in G.edges(data=True):
    d = data["distance"]
    t = data["traffic"]
    edge_labels[(u, v)] = f"{d}+{t}"

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show() 
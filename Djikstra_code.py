import networkx as nx
import matplotlib.pyplot as plt
import random
from itertools import permutations

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


for u, v, data in G.edges(data=True):
      dynamic_traffic = random.randint(1, 5)

data['traffic'] = dynamic_traffic
data['weight'] = data['distance'] + dynamic_traffic

print("Available locations:", list(G.nodes()))

start = input("Enter start location: ")
destinations_input = input("Enter destinations (comma separated): ")
destinations = [d.strip() for d in destinations_input.split(",")]

best_order = None
best_cost = float('inf')
best_full_path = []
best_path_edges = []
best_total_distance = 0

# Try all possible delivery orders
for order in permutations(destinations):

    current = start
    total_cost_temp = 0
    total_distance_temp = 0
    full_path_temp = []
    path_edges_temp = []

    possible = True

    for dest in order:

        try:
            path = nx.shortest_path(
                G,
                source=current,
                target=dest,
                weight='weight'
            )

            cost = nx.shortest_path_length(
                G,
                source=current,
                target=dest,
                weight='weight'
            )

        except:
            possible = False
            break

        full_path_temp.extend(path[:-1])

        total_cost_temp += cost

        path_edges = list(zip(path, path[1:]))
        path_edges_temp.extend(path_edges)

        total_distance_temp += sum(
            G[u][v]["distance"]
            for u, v in path_edges
        )

        current = dest

    full_path_temp.append(current)

    if possible and total_cost_temp < best_cost:
        best_cost = total_cost_temp
        best_order = order
        best_full_path = full_path_temp
        best_path_edges = path_edges_temp
        best_total_distance = total_distance_temp

print("Best Delivery Order:", best_order)
print("Optimized Delivery Path:", best_full_path)
print("Minimum Total Cost:", best_cost)
print("Total Distance:", best_total_distance, "km")

speed = 40
eta = best_total_distance / speed

print("Estimated Time:", round(eta, 2), "hours")

pos = nx.spring_layout(G)

nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000)

nx.draw_networkx_edges(G, pos, edgelist=best_path_edges, edge_color='red', width=3)

edge_labels = {}
for u, v, data in G.edges(data=True):
    d = data["distance"]
    t = data["traffic"]
    edge_labels[(u, v)] = f"{d}+{t}"

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show() 
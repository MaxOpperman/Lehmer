import copy
import math
from argparse import Namespace
from typing import List

import networkx as nx
from matplotlib import pyplot as plt

from pathmarker import PathMarker
from permutation_graphs import start_perm, defect


def visualize(dict_graph, dict_inv) -> (nx.Graph(), dict):
    graph = nx.Graph()
    partite_counts = dict.fromkeys(set(dict_inv.values()), 0)

    # give the nodes their positions
    for node, k_partite in dict_inv.items():
        graph.add_node(node, pos=(k_partite, partite_counts[k_partite]))
        # keep track of the Y-axis value based on the number of nodes with the arity counts
        partite_counts[k_partite] += 1

    # draw the edges
    for perm1, values in dict_graph.items():
        for perm2 in values:
            graph.add_edge(perm1, perm2, color='k')

    return graph, nx.get_edge_attributes(graph, 'color')


def find_path_colors(edge_colors: dict, graph: nx.Graph(), cli_args: Namespace, signature: List[int]) -> (list, list):
    """
     Finds the coloring if a possibly imperfect Hamiltonian path exits
    """
    h_nodes, spur_origins, spur_destinations = lehmer_path(copy.deepcopy(graph), cli_args, signature)
    # Color the edges
    for ind in range(len(h_nodes) - 1):
        if (h_nodes[ind], h_nodes[ind + 1]) in edge_colors:
            edge_colors[(h_nodes[ind], h_nodes[ind + 1])] = 'r'
        if (h_nodes[ind + 1], h_nodes[ind]) in edge_colors:
            edge_colors[(h_nodes[ind + 1], h_nodes[ind])] = 'r'
    # Color the nodes
    if cli_args.color:
        node_colors = ['green' if node in spur_origins else 'red' if node in spur_destinations else
                       'blue' if node in h_nodes else 'skyblue' for node in graph.nodes()]
    else:
        node_colors = ['green' if node in spur_origins else 'red' if node in spur_destinations else 'skyblue'
                       for node in graph.nodes()]
    return node_colors, edge_colors.values()


def plot_graph(graph: nx.Graph, n_color: list, e_color: list):
    plt.figure(figsize=(19, 38))
    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw(
        graph,
        pos,
        with_labels=True,
        edge_color=e_color,
        node_color=n_color,
        node_size=500,
        font_size=10,
        font_weight='bold',
    )

    path_marker = PathMarker(graph, pos, e_color, n_color)

    # Register click event handler
    def onclick(event):
        if event.inaxes is not None:
            x, y = event.xdata, event.ydata
            node = None
            edge = None
            for n, (xp, yp) in pos.items():
                if (x - xp) ** 2 + (y - yp) ** 2 < 0.01:  # Check if the click is close to a node
                    node = n
                    break
            if node is None:
                # Check if the click is close to an edge
                for u, v in graph.edges():
                    x1, y1 = pos[u]
                    x2, y2 = pos[v]
                    # Calculate the distance from the click to the edge
                    dist = point_to_line_distance(x, y, x1, y1, x2, y2)
                    if dist < 0.01:  # Click is close to the edge
                        edge = (u, v)
                        break
            if node is not None:
                path_marker.toggle_node(node)
                path_marker.update_plot(nx, plt)
            elif edge is not None:
                path_marker.toggle_edge(edge)
                path_marker.update_plot(nx, plt)

    # Register key press event handler
    def onkeypress(event):
        if event.key == 'c':
            path_marker.reset_colors()
            path_marker.update_plot(nx, plt)

    plt.gcf().canvas.mpl_connect('button_press_event', onclick)
    plt.gcf().canvas.mpl_connect('key_press_event', onkeypress)

    plt.axis('off')
    plt.show()


def point_to_line_distance(x, y, x1, y1, x2, y2):
    # Calculate the dot product of the vectors (x - x1, y - y1) and (x2 - x1, y2 - y1)
    dot_product = (x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)

    # Calculate the square of the length of the line segment
    line_length_squared = (x2 - x1) ** 2 + (y2 - y1) ** 2

    # Parameter t is the proportion of the projection of the point onto the line
    t = max(0, min(1, dot_product / line_length_squared))

    # Calculate the closest point on the line segment to the point (x, y)
    closest_x = x1 + t * (x2 - x1)
    closest_y = y1 + t * (y2 - y1)

    # Calculate the distance between the closest point and the point (x, y)
    distance = math.sqrt((x - closest_x) ** 2 + (y - closest_y) ** 2)

    return distance


def is_stutter_permutation(perm, max_arity):
    """
     Returns whether the permutation is a stutter permutation
     Always returns False when the permutation has the maximum arity in the graph
    """
    if max_arity:
        return False
    # Iterate over pairs of elements
    for i in range(1, len(perm), 2):
        # Check if the pair satisfies the condition
        if perm[i] != perm[i - 1]:
            return False
    return True


def lehmer_path(graph: nx.Graph(), cli_args: Namespace, signature: List[int]):
    # Step 1: Set node tally at 1
    node_tally = 1
    # Step 2: Set spur tally at 0
    spur_tally = 0
    spur_origins = []
    stutters = []
    # Step 3: The first node becomes B
    b = start_perm(signature)

    interchanges = [b]  # Store interchange digits

    # Step 4: If there is no path leaving B, go to Step 16
    while list(graph.neighbors(b)):
        # Step 5: Among the nodes connected to B of least multiplicity, select the node N of least serial number
        # TODO This doesn't work because sometimes stutter permutations are chosen as part of the actual path
        connected_nodes = list(graph.neighbors(b))
        # Get the minimum number of connections among the connected nodes
        min_conn = min([len(list(graph.neighbors(node))) for node in connected_nodes])
        # Filter the connected nodes to include only those with the minimum number of connections
        # In case of a tie, smaller serial number
        node = min([node for node in connected_nodes if len(list(graph.neighbors(node))) == min_conn])

        # Step 6: If the multiplicity of N is 1, go to Step 12
        if graph.degree(node) == 1:
            # Step 12: Store interchange digit from B to N in the next two storage places
            interchanges.append(node)
            if graph.number_of_edges() > 1:
                # Step 13: Spur tally plus 1 replaces spur tally
                spur_tally += 1
                # add nodes to path and list of spurs
                interchanges.append(b)
                spur_origins.append(b)
                stutters.append(node)
            # Step 14: Disconnect B and N
            graph.remove_edge(b, node)
            # Step 15: Go to Step 10
            node_tally += 1
            # Then go back to Step 4
            continue

        # Step 7: Store interchange digit from B to N in next storage place
        interchanges.append(node)
        # Step 8: Disconnect B from all connecting nodes, thus reducing by 1 the multiplicity of each such node
        for neighbors in list(graph.neighbors(b)):  # Use list() to create a copy of the list before iterating
            graph.remove_edge(b, neighbors)

        # Step 9: N becomes B
        b = node
        # Step 10: Node tally plus 1 replaces node tally
        node_tally += 1

        # Step 11: Go to step 4

    # Step 16: Output initial marks, spur and node tallies, and list of interchange digits
    if cli_args.verbose:
        if len(spur_origins) != len(stutters):
            print("Spur origins:", spur_origins)
            print("Stutters:", stutters)
        else:
            print("Spur origin -> stutter:")
            for i in range(len(spur_origins)):
                print("Spur {}:".format(i), spur_origins[i], "->", stutters[i])
        if node_tally < graph.number_of_nodes():
            print("Node Tally:", node_tally, "and path length:", len(interchanges))
            print("!!!!! INCORRECT PATH; MISSING", graph.number_of_nodes() - node_tally, "NODES !!!!!")
        else:
            print("Node Tally:", node_tally, "which is CORRECT! And path length:", len(interchanges))
        if spur_tally > 0 and spur_tally != defect(signature):
            print("Spur Tally:", spur_tally)
            print("!!!!! INCORRECT NUMBER OF SPURS; FOUND", spur_tally, "BUT ONLY", max(defect(signature), 0),
                  "IS CORRECT !!!!!")
        else:
            print("Spur Tally:", spur_tally, "which is CORRECT!")

    # Step 17: Halt
    return interchanges, spur_origins, stutters

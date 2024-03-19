import argparse
import copy
import random
from itertools import permutations
import math
from collections import Counter
from functools import reduce

import networkx as nx
import matplotlib.pyplot as plt

from pathmarker import PathMarker


def visualize(perm_inversions, color):
    graph = nx.Graph()
    # keep track of the Y-axis value based on the number of nodes with the arity counts
    partite_counts = dict.fromkeys(set(perm_inversions.values()), 0)

    for node, k_partite in perm_inversions.items():
        graph.add_node(node, pos=(k_partite, partite_counts[k_partite]))
        # change the Y-axis value
        partite_counts[k_partite] += 1

    # Add edges between permutations that can be transformed into each other by a single neighbor swap
    perms = list(perm_inversions.keys())
    for i in range(len(perms)):
        for j in range(i + 1, len(perms)):
            perm1, perm2 = perms[i], perms[j]
            inv_diff = abs(perm_inversions[perm1] - perm_inversions[perm2])
            if inv_diff == 1 and can_neighbor_swap(perm1, perm2):
                graph.add_edge(perm1, perm2, color='k')

    edge_colors = nx.get_edge_attributes(graph, 'color')
    return color, edge_colors, graph, partite_counts


def find_path(edge_colors, graph, ham, lehmer, verbose, parity_diff, permutations_dict, arities, spurs):
    """
     Either finds a perfect Hamiltonian Path or a Lehmer path (Hamiltonian Path with spurs) or returns empty arrays
    """
    hamiltonian_nodes, spur_origins, stutters = [], [], []
    if ham or lehmer is not None:
        if ham:
            if verbose:
                print("Computing Hamiltonian path...")
            hamiltonian_nodes = hamilton(graph, [])
            prev_paths = [hamiltonian_nodes]
            print(hamiltonian_nodes)
            while hamiltonian_nodes is not None:
                hamiltonian_nodes = hamilton(graph, prev_paths)
                prev_paths.append(hamiltonian_nodes)
                print(hamiltonian_nodes)
        if lehmer is not None:
            hamiltonian_nodes, spur_origins, stutters = lehmer_path(copy.deepcopy(graph), verbose, permutations_dict, arities, parity_diff, lehmer, spurs)
        if hamiltonian_nodes is not None:
            for ind in range(len(hamiltonian_nodes) - 1):
                if (hamiltonian_nodes[ind], hamiltonian_nodes[ind + 1]) in edge_colors:
                    edge_colors[(hamiltonian_nodes[ind], hamiltonian_nodes[ind + 1])] = 'r'
                if (hamiltonian_nodes[ind + 1], hamiltonian_nodes[ind]) in edge_colors:
                    edge_colors[(hamiltonian_nodes[ind + 1], hamiltonian_nodes[ind])] = 'r'
    return hamiltonian_nodes, spur_origins, stutters


def plot_graph(color, edge_colors, graph, hamiltonian_nodes, spur_origins, stutters):
    plt.figure(figsize=(19, 38))
    pos = nx.get_node_attributes(graph, 'pos')
    if color:
        node_colors = ['green' if node in spur_origins else 'olive' if node in stutters else
                       'deeppink' if node in hamiltonian_nodes else 'skyblue' for node in graph.nodes()]
    else:
        node_colors = ['green' if node in spur_origins else 'olive' if node in stutters else 'skyblue'
                       for node in graph.nodes()]
    nx.draw(
        graph,
        pos,
        with_labels=True,
        edge_color=edge_colors.values(),
        node_color=node_colors,
        node_size=500,
        font_size=10,
        font_weight='bold',
        # width=4,
    )

    path_marker = PathMarker(graph, pos, edge_colors.values(), node_colors)

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


def can_neighbor_swap(perm1, perm2):
    """
    Check if two permutations can be transformed into each other by a single neighbor swap.
    """
    index = 0
    neighbor_swaps = 0
    while index < len(perm1) - 1:
        if perm1[index] != perm2[index]:
            if perm1[index+1] != perm2[index+1] and perm1[index] == perm2[index+1] and perm2[index] == perm1[index+1]:
                neighbor_swaps += 1
                index += 1
            else:
                return False
        index += 1
    return neighbor_swaps == 1


# from https://gist.github.com/mikkelam/ab7966e7ab1c441f947b
def hamilton(G, excluded_paths=None):
    if excluded_paths is None:
        excluded_paths = []

    F = [(G, [list(G.nodes())[0]])]
    n = G.number_of_nodes()
    while F:
        graph, path = F.pop()
        confs = []
        neighbors = (node for node in graph.neighbors(path[-1])
                     if node != path[-1])  # exclude self loops
        for neighbor in neighbors:
            conf_p = path[:]
            conf_p.append(neighbor)
            conf_g = nx.Graph(graph)
            conf_g.remove_node(path[-1])
            confs.append((conf_g, conf_p))
        for g, p in confs:
            if len(p) == n:
                if p not in excluded_paths:
                    return p
            else:
                F.append((g, p))
    return None


def lehmer_path(graph, verbose, perm_inversions, arities, parity_diff, strat, spurs):
    # Step 1: Set node tally at 1
    node_tally = 1
    # Step 2: Set spur tally at 0
    spur_tally = 0
    spur_origins = []
    stutters = []
    # Step 3: The first node becomes B
    b = list(graph.nodes())[0]
    max_arity = max(arities.keys())

    interchanges = [b]  # Store interchange digits

    # Step 4: If there is no path leaving B, go to Step 16
    while list(graph.neighbors(b)):
        # Step 5: Pick the next node
        node = use_strategy(arities, b, graph, perm_inversions, strat, not verbose)
        # Update the arities dictionary to reflect the decreasing count of nodes with each arity
        arities[perm_inversions[node]] -= 1

        # Step 6: If the multiplicity of N is 1, go to Step 12
        if graph.degree(node) == 1 or (is_stutter_permutation(node, perm_inversions[node], max_arity) and spurs):
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
            if spurs:
                for neighbors in list(graph.neighbors(node)):
                    graph.remove_edge(node, neighbors)
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
    if verbose:
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
        if spur_tally > 0 and spur_tally != parity_diff - 1:
            print("Spur Tally:", spur_tally)
            print("!!!!! INCORRECT NUMBER OF SPURS; FOUND", spur_tally, "BUT ONLY", max(parity_diff - 1, 0),
                  "IS CORRECT !!!!!")
        else:
            print("Spur Tally:", spur_tally, "which is CORRECT!")
    # print("Path:", interchanges)

    # Step 17: Halt
    return interchanges, spur_origins, stutters


# Define the strategies
strategies = {
    0: "Among the nodes connected to B of least multiplicity, select the node N of least serial number",
    1: "First pick nodes of which less nodes with that #inversions are available, then the smallest serial number node",
    2: "First pick nodes of which less nodes with that #inversions are available, then apply Lehmer's strategy",
    3: "First pick nodes with larger multiplicity, then pick the first node with the smallest serial number as before",
    4: "First pick the node with the least multiplicity, upon a tie choose the one with the largest serial number",
    5: "First pick nodes with larger multiplicity upon a tie choose the one with the largest serial number",
}


def use_strategy(arities, b, graph, perm_inversions, strategy, verbose):
    """
     Compute the next node based on the strategy provided
    :return: the next node for the Lehmer Path according to the given strategy
    """
    connected_nodes = list(graph.neighbors(b))
    # Lehmer's Original Strategy:
    # Among the nodes connected to B of least multiplicity, select the node N of least serial number
    if strategy == 0:
        # This doesn't work because sometimes stutter permutations are chosen as part of the actual path
        # Get the minimum number of connections among the connected nodes
        num_connections = [len(list(graph.neighbors(node))) for node in connected_nodes]
        min_connections = min(num_connections)
        if verbose:
            print(b, arities, [n for n in connected_nodes], [perm_inversions[n] for n in connected_nodes],
                  [arities[perm_inversions[n]] for n in connected_nodes])
        # Filter the connected nodes to include only those with the minimum number of connections
        min_connection_nodes = [node for node in connected_nodes if len(list(graph.neighbors(node))) == min_connections]
        # In case of a tie, smaller serial number
        node = min(min_connection_nodes)
    # Arity strategy:
    # First pick nodes of which less nodes with that arity are available, then pick the smallest serial number node
    elif strategy == 1:
        # This doesn't work since sometimes the last node (e.g. case of 0^4,1^6), there are stutter permutations being
        # skipped on the far right
        min_arity = min([arities[perm_inversions[n]] for n in connected_nodes])
        min_arities = [k for k, v in arities.items() if v == min_arity]
        if verbose:
            print(b, arities, [n for n in connected_nodes], [perm_inversions[n] for n in connected_nodes],
                  [arities[perm_inversions[n]] for n in connected_nodes])
        # Filter the connected nodes to include only those with the minimum arity
        min_arity_nodes = [node for node in connected_nodes if perm_inversions[node] in min_arities]
        if verbose:
            print(b, min_arity_nodes, min_arity, arities)
        # In case of a tie, smaller serial number
        node = min(min_arity_nodes)
    # Arity strategy & Lehmer combined:
    # First pick nodes of which less nodes with that arity are available, then apply Lehmer's strategy
    elif strategy == 2:
        #
        min_arity = min([arities[perm_inversions[n]] for n in connected_nodes])
        min_arities = [k for k, v in arities.items() if v == min_arity]
        if verbose:
            print(b, arities, [n for n in connected_nodes], [perm_inversions[n] for n in connected_nodes],
                  [arities[perm_inversions[n]] for n in connected_nodes])
        # Filter the connected nodes to include only those with the minimum arity
        min_arity_nodes = [node for node in connected_nodes if perm_inversions[node] in min_arities]
        # Get the minimum number of connections among the connected nodes
        num_connections = [len(list(graph.neighbors(node))) for node in min_arity_nodes]
        min_connections = min(num_connections)
        # Filter the connected nodes to include only those with the minimum number of connections
        min_connection_nodes = [node for node in connected_nodes if len(list(graph.neighbors(node))) == min_connections]
        if verbose:
            print(b, num_connections, min_connection_nodes, min_arity_nodes, min_arity, arities)
        # In case of a tie, smaller serial number
        node = min(min_connection_nodes)
    # First pick nodes with larger multiplicity, then pick the first node with the smallest serial number as before
    elif strategy == 3:
        # Get the minimum number of connections among the connected nodes
        num_connections = [len(list(graph.neighbors(node))) for node in connected_nodes]
        max_connections = max(num_connections)
        if verbose:
            print(b, arities, [n for n in connected_nodes], [perm_inversions[n] for n in connected_nodes],
                  [arities[perm_inversions[n]] for n in connected_nodes])
        # Filter the connected nodes to include only those with the minimum number of connections
        max_connection_nodes = [node for node in connected_nodes if len(list(graph.neighbors(node))) == max_connections]
        if verbose:
            print(b, num_connections, max_connection_nodes, arities)
        # In case of a tie, smaller serial number
        node = min(max_connection_nodes)
    # First pick the node with the least multiplicity, upon a tie choose the one with the largest serial number
    elif strategy == 4:
        # Get the minimum number of connections among the connected nodes
        num_connections = [len(list(graph.neighbors(node))) for node in connected_nodes]
        min_connections = min(num_connections)
        if verbose:
            print(b, arities, [n for n in connected_nodes], [perm_inversions[n] for n in connected_nodes],
                  [arities[perm_inversions[n]] for n in connected_nodes])
        # Filter the connected nodes to include only those with the minimum number of connections
        min_connection_nodes = [node for node in connected_nodes if len(list(graph.neighbors(node))) == min_connections]
        # In case of a tie, larger serial number
        node = max(min_connection_nodes)
    # Opposite Lehmer:
    # First pick nodes with larger multiplicity, then pick the first node with the largest serial number
    elif strategy == 5:
        # Get the minimum number of connections among the connected nodes
        num_connections = [len(list(graph.neighbors(node))) for node in connected_nodes]
        max_connections = max(num_connections)
        if verbose:
            print(b, arities, [n for n in connected_nodes], [perm_inversions[n] for n in connected_nodes],
                  [arities[perm_inversions[n]] for n in connected_nodes])
        # Filter the connected nodes to include only those with the minimum number of connections
        max_connection_nodes = [node for node in connected_nodes if len(list(graph.neighbors(node))) == max_connections]
        if verbose:
            print(b, num_connections, max_connection_nodes, arities)
        # In case of a tie, smaller serial number
        node = max(max_connection_nodes)
    else:
        node = random.choice(list(graph.neighbors(b)))
    return node


def is_stutter_permutation(perm, inversions, max_arity):
    """
     Returns whether the permutation is a stutter permutation
     Always returns False when the permutation has the maximum arity in the graph
    """
    if max_arity == inversions:
        return False
    # Iterate over pairs of elements
    for i in range(1, len(perm), 2):
        # Check if the pair satisfies the condition
        if perm[i] != perm[i - 1]:
            return False
    return True


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


def compute_parity(perms):
    """
    Compute the parity of the number of inversions for each permutation in a list.
    """
    parity_dict = {}
    even_count, odd_count = 0, 0
    for perm in perms:
        inv = count_inversions(perm)
        parity_dict[perm] = inv
        if inv % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
    return parity_dict, even_count, odd_count


def count_inversions(perm):
    """
    Count the number of inversions in a permutation.
    """
    inversions = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                inversions += 1
    return inversions


def count_permutations(inp):
    # Count occurrences of each character
    char_counts = Counter(inp)

    # Calculate factorial of counts and multiply them together
    total_factorial = reduce(lambda x, y: x * y, (math.factorial(count) for count in char_counts.values()), 1)

    return math.factorial(len(inp))/total_factorial


def print_unique_permutations(input_str):
    # Generate all permutations of the input string
    perm = permutations(input_str)

    # Use a set to store unique permutations
    unique_permutations_set = set()

    # Use a list to store the order of generated permutations
    unique_permutations_list = []

    # Iterate over all permutations
    for p in perm:
        perm_str = ''.join(p)
        # Check if the permutation has not been printed before
        if perm_str not in unique_permutations_set:
            unique_permutations_set.add(perm_str)
            unique_permutations_list.append(perm_str)
    return unique_permutations_list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lehmer_strategy_help = "Default: random choices\r\n"
    for key, val in strategies.items():
        lehmer_strategy_help += f"{key}: {val}\r\n"
    parser = argparse.ArgumentParser(description='Helper tool to find paths through permutation neighbor swap graphs.')
    parser.add_argument('-p', '--permutation', type=str, help='Input permutation string')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('-m', '--hamiltonian', action='store_true', help='Print all possible perfect Hamiltonian Paths')
    parser.add_argument('-l', '--lehmer', type=int, choices=strategies.keys(), default=-1,
                        help=f'Select a strategy for finding a path: {lehmer_strategy_help}')
    parser.add_argument('-s', '--spur', action='store_true', help='Automatically recognize stutters as spurs')
    parser.add_argument('-g', '--graph', action='store_true', help='Show the NetworkX neighbor swap graph')
    parser.add_argument('-c', '--color', action='store_true', help='Color the nodes in the Hamiltonian Path')

    args = parser.parse_args()

    if args.permutation:
        print(f"Number of permutations generated by '{args.permutation}' are: {count_permutations(args.permutation)}")
        permutations = print_unique_permutations(args.permutation)
        if args.verbose:
            print(permutations)
        parities, even, odd = compute_parity(permutations)
        # Print each unique permutation in the order they were generated
        print("Computed all {} permutations of which {} are even and {} odd".format(len(parities), even, odd))
        print(f"Using strategy: {strategies[args.lehmer]}")
        if args.graph or args.hamiltonian:
            node_color, edge_color, perm_graph, arity_counts = visualize(parities, args.color)
            h_path, spurs_orig, spurs_dest = find_path(
                edge_color, perm_graph, args.hamiltonian, args.lehmer, args.verbose, even-odd, parities, arity_counts, args.spur,
            )
            if args.graph:
                plot_graph(node_color, edge_color, perm_graph, h_path, spurs_orig, spurs_dest)
    else:
        print("Please provide a permutation string using the -p or --permutation option.")


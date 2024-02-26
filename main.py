import argparse
from itertools import permutations
import math
from collections import Counter
from functools import reduce

import mplcursors as mplcursors
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm

from pathmarker import PathMarker


def visualize(perm_inversions, show_graph, ham, verbose):
    graph = nx.Graph()
    partite_counts = dict.fromkeys(set(perm_inversions.values()), 0)

    for node, k_partite in perm_inversions.items():
        graph.add_node(node, pos=(k_partite, partite_counts[k_partite]))
        partite_counts[k_partite] += 1

    # Add edges between permutations that can be transformed into each other by a single neighbor swap
    permutations = list(perm_inversions.keys())
    for i in range(len(permutations)):
        for j in range(i + 1, len(permutations)):
            perm1, perm2 = permutations[i], permutations[j]
            inv_diff = abs(perm_inversions[perm1] - perm_inversions[perm2])
            if inv_diff == 1 and can_neighbor_swap(perm1, perm2):
                graph.add_edge(perm1, perm2, color='k')

    colors = nx.get_edge_attributes(graph, 'color')
    if ham:
        if verbose:
            print("Computing Hamiltonian path...")
        hamiltonian_nodes = hamilton(graph, verbose)
        print("There exists a Hamiltonian path in the graph:", hamiltonian_nodes)
        if hamiltonian_nodes is not None:
            for ind in range(len(hamiltonian_nodes) - 1):
                if (hamiltonian_nodes[ind], hamiltonian_nodes[ind+1]) in colors:
                    colors[(hamiltonian_nodes[ind], hamiltonian_nodes[ind+1])] = 'r'
                if (hamiltonian_nodes[ind+1], hamiltonian_nodes[ind]) in colors:
                    colors[(hamiltonian_nodes[ind+1], hamiltonian_nodes[ind])] = 'r'

    if show_graph:
        plt.figure(figsize=(19, 38))
        pos = nx.get_node_attributes(graph, 'pos')
        nx.draw(
            graph,
            pos,
            with_labels=True,
            edge_color=colors.values(),
            node_color='skyblue',
            node_size=500,
            font_size=10,
            font_weight='bold',
        )

        path_marker = PathMarker(graph, pos)

        # Register click event handler
        def onclick(event):
            if event.inaxes is not None:
                x, y = event.xdata, event.ydata
                node = None
                for n, (xp, yp) in pos.items():
                    if (x - xp) ** 2 + (y - yp) ** 2 < 0.01:  # Check if the click is close to a node
                        node = n
                        break
                if node is not None:
                    path_marker.toggle_node(node)
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
def hamilton(G, verb):
    F = [(G, [list(G.nodes())[0]])]
    n = G.number_of_nodes()
    if verb:
        pbar = tqdm(total=math.factorial(len(F)))
    else:
        pbar = None
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
                return p
            else:
                F.append((g, p))
        if verb:
            pbar.update(1)
    if verb:
        pbar.close()
    return None


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
    parser = argparse.ArgumentParser(description='Count permutations of a given input string.')
    parser.add_argument('-p', '--permutation', type=str, help='Input permutation string')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('-m', '--hamiltonian', action='store_true', help='Check if a Hamiltonian Path Exists')
    parser.add_argument('-g', '--graph', action='store_true', help='Show the NetworkX neighbor swap graph')

    args = parser.parse_args()

    if args.permutation:
        print(f"Number of permutations generated by '{args.permutation}' are: {count_permutations(args.permutation)}")
        permutations = print_unique_permutations(args.permutation)
        if args.verbose:
            print(permutations)
        parities, even, odd = compute_parity(permutations)
        # Print each unique permutation in the order they were generated
        print("Computed all {} permutations of which {} are even and {} odd".format(len(parities), even, odd))
        if args.graph or args.hamiltonian:
            visualize(parities, args.graph, args.hamiltonian, args.verbose)
    else:
        print("Please provide a permutation string using the -p or --permutation option.")


import copy
import math
from argparse import Namespace

import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.backend_bases import KeyEvent, MouseEvent

from core.figure_generation_files.pathmarker import PathMarker
from core.helper_operations.permutation_graphs import (
    defect,
    multiset,
    total_path_motion,
)


def visualize(
    dict_graph: dict[str, set[str]], dict_inv: dict[tuple, int]
) -> tuple[nx.Graph, dict]:
    """
    Visualizes a graph based on the given dictionary adjacency matrix.\n
    The inversion dictionary is used to determine the position of each node in the visualization.
    The number of inversions of a node is represented by the number of elements that appear out of order in the permutation.
    Two elements are considered out of order if the left element is strictly greater than the right element (the elements are not necessarily adjacent).

    Args:
        dict_graph (dict[str, set[str]]): A dictionary representing the graph, where each key is a node and the corresponding value is a set of adjacent nodes.
        dict_inv (dict[tuple, int]): A dictionary mapping nodes to their respective number of inversions.

    Returns:
        tuple[nx.Graph, dict]: A tuple containing the graph object and a dictionary of edge colors.
    """
    graph = nx.Graph()
    partite_counts = dict.fromkeys(set(dict_inv.values()), 0)

    # give the nodes their positions
    for node, k_partite in dict_inv.items():
        # rename node to be a string without the commas
        graph.add_node(
            "".join(map(str, node)), pos=(k_partite, partite_counts[k_partite])
        )
        # keep track of the Y-axis value based on the number of nodes with the arity counts
        partite_counts[k_partite] += 1

    # draw the edges
    for perm1, values in dict_graph.items():
        for perm2 in values:
            graph.add_edge(perm1, perm2, color="k")

    return graph, nx.get_edge_attributes(graph, "color")


def find_path_colors(
    edge_colors: dict, graph: nx.Graph, cli_args: Namespace, signature: list[int]
) -> tuple[list[str], list[str]]:
    """
    Determines the colors of a Lehmer path in a neighbor-swap graph. The Lehmer path is computed using the ``lehmer_path`` function.
    Uses whether the CLI arguments specify coloring or not.
    If coloring is enabled, the nodes and edges are colored based on the Lehmer path (possibly with spurs).
    If coloring is disabled, the nodes and edges are colored based on whether they are spurs or not.

    Args:
        edge_colors (dict):
            A dictionary representing which edges are colored red (because they are in the Lehmer path), or black (rest).
            The keys are tuples of nodes and the values are the color of the edge.
        graph (nx.Graph): The networx graph to find the coloring for.
        cli_args (Namespace): Command-line arguments. Contains the color flag, which activates coloring of the Lehmer path if `True`.
        signature (list[int]): The signature of the permutations (for the Lehmer path)

    Returns:
        tuple[list[str], list[str]]:
            A tuple containing the nodes and edges colors as lists of strings where the strings represent the colors.
            The order of the colors corresponds to the order of the nodes and edges in the graph.
    """
    h_nodes, spur_bases, spur_destinations = lehmer_path(
        copy.deepcopy(graph), cli_args, signature
    )
    # Color the edges
    for ind in range(len(h_nodes) - 1):
        if (h_nodes[ind], h_nodes[ind + 1]) in edge_colors:
            edge_colors[(h_nodes[ind], h_nodes[ind + 1])] = "r"
        if (h_nodes[ind + 1], h_nodes[ind]) in edge_colors:
            edge_colors[(h_nodes[ind + 1], h_nodes[ind])] = "r"
    # Color the nodes
    if cli_args.color:
        node_colors = [
            (
                "orange"
                if node in spur_bases
                else (
                    "olive"
                    if node in spur_destinations
                    else "deeppink" if node in h_nodes else "skyblue"
                )
            )
            for node in graph.nodes()
        ]
    else:
        node_colors = [
            (
                "orange"
                if node in spur_bases
                else "olive" if node in spur_destinations else "skyblue"
            )
            for node in graph.nodes()
        ]
    return node_colors, edge_colors.values()


def plot_graph(graph: nx.Graph, n_color: list[str], e_color: list[str]) -> None:
    """
    Plot a graph using NetworkX and Matplotlib.

    Args:
        graph (nx.Graph): The graph to be plotted.
        n_color (list[str]): List of colors for nodes. The order corresponds to the order of the nodes in the graph.
        e_color (list[str]): List of colors for edges. The order corresponds to the order of the edges in the graph.

    Returns:
        None
    """
    plt.figure(figsize=(19, 38))
    pos = nx.get_node_attributes(graph, "pos")
    nx.draw(
        graph,
        pos,
        with_labels=True,
        edge_color=e_color,
        node_color=n_color,
        node_size=1000,
        font_size=10,
        font_weight="bold",
        # width=4,
    )

    path_marker = PathMarker(graph, pos, e_color, n_color)

    # Register click event handler
    def onclick(event: MouseEvent) -> None:
        """
        Handles the click event of the plot. Toggles the color of nodes and edges based on the click.
        Finds the nearest node or edge to the click and toggles the color of the node or edge.

        Args:
            event (MouseEvent): The onclick event object.

        Returns:
            None
        """
        if event.inaxes is not None:
            x, y = event.xdata, event.ydata
            node = None
            edge = None
            for n, (xp, yp) in pos.items():
                if (x - xp) ** 2 + (
                    y - yp
                ) ** 2 < 0.01:  # Check if the click is close to a node
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
                if event.button == 3:  # Right mouse click
                    path_marker.toggle_right_mark_node(node)
                else:  # Left mouse click
                    path_marker.toggle_node(node)
                path_marker.update_plot(nx, plt)
            elif edge is not None:
                path_marker.toggle_edge(edge)
                path_marker.update_plot(nx, plt)

    # Register key press event handler
    def onkeypress(event: KeyEvent) -> None:
        """
        Reset the colors of the path marker and update the plot. This is triggered when the **C** key is pressed.

        Args:
            event (KeyEvent): The key press event object.

        Returns:
            None
        """
        if event.key == "c":
            path_marker.reset_colors()
            path_marker.update_plot(nx, plt)

    plt.gcf().canvas.mpl_connect("button_press_event", onclick)
    plt.gcf().canvas.mpl_connect("key_press_event", onkeypress)

    plt.axis("off")
    plt.show()


import math


def point_to_line_distance(
    x: float, y: float, x1: float, y1: float, x2: float, y2: float
) -> float:
    """
    Calculates the shortest distance between a point `(x, y)` and a line segment defined by two points `(x1, y1)` and `(x2, y2)`.
    We will say that the click is close to the edge if the distance is less than 0.01.

    Args:
        x (float): The x-coordinate of the clicked point.
        y (float): The y-coordinate of the clicked point.
        x1 (float): The x-coordinate of the first point defining the line segment.
        y1 (float): The y-coordinate of the first point defining the line segment.
        x2 (float): The x-coordinate of the second point defining the line segment.
        y2 (float): The y-coordinate of the second point defining the line segment.

    Returns:
        float: The shortest distance between the point and the line segment.
    """
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


def is_stutter_permutation(perm: str, max_arity: bool = False) -> bool:
    """
    Returns whether the permutation is a stutter permutation.
    Always returns False when the permutation has the maximum arity in the graph.
    This is used to determine whether to automatically recognize stutters as spurs in a variation on Lehmer's algorithm.

    Args:
        perm (str): The permutation to check
        max_arity (bool, optional): Whether the permutation has the maximum arity in the graph

    Returns:
        bool: `True` if the permutation is a stutter permutation, `False` otherwise.
    """
    if max_arity:
        return False
    # Iterate over pairs of elements
    for i in range(1, len(perm), 2):
        # Check if the pair satisfies the condition
        if perm[i] != perm[i - 1]:
            return False
    return True


def lehmer_path(
    graph: nx.Graph, cli_args: Namespace, signature: list[int]
) -> tuple[list, list, list]:
    """
    Implementation Lehmer's permutations by adjacent interchanges algorithm

    Args:
        graph (nx.Graph): The neighbor-swap graph
        cli_args (Namespace): Command line arguments
        signature (list[int]): The permutation signature

    Returns:
        tuple[list, list, list]: A tuple containing the Lehmer path, spur bases, and spur tips

    References:
        - D. H. Lehmer. Permutation by Adjacent Interchanges. Technical Report 2, 1965.
    """
    # Step 1: Set node tally at 1
    node_tally = 1
    # Step 2: Set spur tally at 0
    spur_tally = 0
    spur_bases = []
    spur_tips = []
    # Step 3: The first node becomes B
    b = "".join(map(str, multiset(signature)))

    interchanges = [b]  # Store interchange digits

    # Step 4: If there is no path leaving B, go to Step 16
    while list(graph.neighbors(b)):
        # Step 5: Among the nodes connected to B of least multiplicity, select the node N of least serial number
        connected_nodes = list(graph.neighbors(b))
        # Get the minimum number of connections among the connected nodes
        min_conn = min([len(list(graph.neighbors(node))) for node in connected_nodes])
        # Filter the connected nodes to include only those with the minimum number of connections
        # In case of a tie, smaller serial number
        node = min(
            [
                node
                for node in connected_nodes
                if len(list(graph.neighbors(node))) == min_conn
            ]
        )

        # Step 6: If the multiplicity of N is 1, go to Step 12
        if graph.degree(node) == 1:
            # Step 12: Store interchange digit from B to N in the next two storage places
            interchanges.append(node)
            if graph.number_of_edges() > 1:
                # Step 13: Spur tally plus 1 replaces spur tally
                spur_tally += 1
                # add nodes to path and list of spurs
                interchanges.append(b)
                spur_bases.append(b)
                spur_tips.append(node)
            # Step 14: Disconnect B and N
            graph.remove_edge(b, node)
            # Step 15: Go to Step 10
            node_tally += 1
            # Then go back to Step 4
            continue

        # Step 7: Store interchange digit from B to N in next storage place
        interchanges.append(node)
        # Step 8: Disconnect B from all connecting nodes, thus reducing by 1 the multiplicity of each such node
        for neighbors in list(
            graph.neighbors(b)
        ):  # Use list() to create a copy of the list before iterating
            graph.remove_edge(b, neighbors)

        # Step 9: N becomes B
        b = node
        # Step 10: Node tally plus 1 replaces node tally
        node_tally += 1

        # Step 11: Go to step 4

    # Step 16: Output initial marks, spur and node tallies, and list of interchange digits
    if cli_args.verbose:
        if len(spur_bases) != len(spur_tips):
            print("Spur origins:", spur_bases)
            print("Stutters:", spur_tips)
        else:
            print("Spur origin -> stutter:")
            for i in range(len(spur_bases)):
                print(
                    f"Spur {i}: {tuple([int(x) for x in spur_bases[i]])} -> {tuple([int(x) for x in spur_tips[i]])}"
                )
        if node_tally < graph.number_of_nodes():
            print(f"Node Tally: {node_tally} and path length: {len(interchanges)}")
            print(
                f"Incorrect path, missing {graph.number_of_nodes() - node_tally} nodes"
            )
        else:
            print(
                f"Node Tally: {node_tally} which is correct. The path length is {len(interchanges)}"
            )
        if spur_tally > 0 and spur_tally != defect(signature) + 1:
            print(f"Spur Tally: {spur_tally}")
            print(
                f"The number of spurs is not optimal. Found {spur_tally} but expected {max(defect(signature) - 1, 0)}"
            )
        else:
            print(f"Spur Tally: {spur_tally} is optimal!")
        print(f"Total Lehmer motion {total_path_motion(interchanges)}")

    # Step 17: Halt
    return interchanges, spur_bases, spur_tips

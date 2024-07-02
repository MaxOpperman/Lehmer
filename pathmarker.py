from matplotlib import pyplot as plt
import networkx as nx


class PathMarker:
    """
    A class that represents a path marker for a graph. This is used as a class since we want to keep track of one instance of a graph.
    This instance is used to keep track of the marked nodes and edges in the graph.
    Note we can mark nodes with left-click and right-click. Marked nodes and edges are drawn in royalblue color,
    while right-click marked nodes are drawn in darkturquoise color.

    Note:
        - Both nodes and edges can be marked with left-click.
        - Only nodes can be right-click marked. Edges cannot!

    Attributes:
        graph (nx.Graph): The networkx graph object.
        pos (dict): The position of the nodes in the graph. The keys are the nodes and the values are the positions.
        marked_nodes (set): A set of marked nodes. Starts empty.
        right_marked_nodes (set): A set of right-click marked nodes. Starts empty.
        marked_edges (set): A set of marked edges. Starts empty.
        edge_colors (list):
            A list of colors for the edges. Is black by default.
            If a Lehmer path is highlighted, the edge colors are changed to red.
        node_colors (list):
            A list of colors for the nodes. Is lightblue by default.
            If a Lehmer path is highlighted, the graph has the following colors:\n
            - Orange for the spur bases
            - Olive for the spur tips
            - Deeppink for the other visited nodes
            - Lightblue for the unvisited nodes
    """

    def __init__(self, graph: nx.Graph, pos: dict, default_edges: list, default_nodes: list):
        self.graph = graph
        self.pos = pos
        self.marked_nodes = set()
        self.right_marked_nodes = set()
        self.marked_edges = set()
        self.edge_colors = default_edges
        self.node_colors = default_nodes

    def mark_node(self, node):
        """
        Marks a node.

        Args:
            node: The node to be marked.
        """
        if node not in self.marked_nodes:
            self.marked_nodes.add(node)

    def right_mark_node(self, node):
        """
        Marks a node with a right-click.

        Args:
            node: The node to be right-click marked.
        """
        if node not in self.right_marked_nodes:
            self.right_marked_nodes.add(node)

    def un_right_mark_node(self, node):
        """
        Unmarks a right-click marked node.

        Args:
            node: The node to be unmarked.
        """
        if node in self.right_marked_nodes:
            self.right_marked_nodes.remove(node)

    def unmark_node(self, node):
        """
        Unmarks a node.

        Args:
            node: The node to be unmarked.
        """
        if node in self.marked_nodes:
            self.marked_nodes.remove(node)

    def toggle_node(self, node):
        """
        Toggles the marking of a node.

        Args:
            node: The node to be toggled.
        """
        if node in self.right_marked_nodes:
            self.un_right_mark_node(node)
        if node in self.marked_nodes:
            self.unmark_node(node)
        else:
            self.mark_node(node)

    def toggle_right_mark_node(self, node):
        """
        Toggles the right-click marking of a node. If the node is already right-click marked, it will be unmarked and vice versa.

        Args:
            node: The node to be toggled.
        """
        if node in self.marked_nodes:
            self.unmark_node(node)
        if node in self.right_marked_nodes:
            self.un_right_mark_node(node)
        else:
            self.right_mark_node(node)

    def mark_edge(self, edge):
        """
        Marks an edge.

        Args:
            edge: The edge to be marked.
        """
        if edge not in self.marked_edges:
            self.marked_edges.add(edge)

    def unmark_edge(self, edge):
        """
        Unmarks an edge.

        Args:
            edge: The edge to be unmarked.
        """
        if edge in self.marked_edges:
            self.marked_edges.remove(edge)

    def toggle_edge(self, edge):
        """
        Toggles the marking of an edge. If the edge is already marked, it will be unmarked and vice versa.

        Args:
            edge: The edge to be toggled.
        """
        if edge in self.marked_edges:
            self.unmark_edge(edge)
        else:
            self.mark_edge(edge)

    def reset_colors(self):
        """
        Clears the sets of marked nodes and edges. This is to reset the colors of the graph.
        """
        self.marked_nodes.clear()
        self.marked_edges.clear()


    def update_plot(self, nx: nx.Graph, plt_instance: plt):
        """
        Updates the plot with the marked nodes and edges. Draws it in the matplotlib pyplot instance.
        Marked nodes and edges are drawn in royalblue color.
        For right-click marked nodes, they are drawn in darkturquoise color.

        Args:
            nx (nx.Graph): The networkx graph object.
            plt_instance (plt): The matplotlib pyplot instance.
        """
        plt_instance.clf()
        nx.draw(
            self.graph,
            self.pos,
            with_labels=True,
            node_color=self.node_colors,
            node_size=1000,
            font_size=10,
            font_weight="bold",
            edge_color=self.edge_colors,
            # width=4,
        )

        # Draw marked nodes in color
        nx.draw_networkx_nodes(
            self.graph,
            self.pos,
            nodelist=self.marked_nodes,
            node_color="royalblue",
            node_size=900,
        )

        # Draw right click marked nodes in color
        nx.draw_networkx_nodes(
            self.graph,
            self.pos,
            nodelist=self.right_marked_nodes,
            node_color="darkturquoise",
            node_size=900,
        )

        # Draw marked edges in color
        nx.draw_networkx_edges(
            self.graph,
            self.pos,
            edgelist=self.marked_edges,
            edge_color="royalblue",
            width=3,
        )

        plt_instance.title("Permutation Inversions Graph")
        plt_instance.draw()

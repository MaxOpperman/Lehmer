class PathMarker:
    """
    A class that represents a path marker for a graph.

    Attributes:
        graph (object): The graph object.
        pos (dict): A dictionary containing the positions of the nodes in the graph.
        default_edges (list): A list of default edge colors.
        default_nodes (list): A list of default node colors.
        marked_nodes (set): A set of marked nodes.
        right_marked_nodes (set): A set of right-click marked nodes.
        marked_edges (set): A set of marked edges.
        edge_colors (list): A list of edge colors.
        node_colors (list): A list of node colors.
    """

    def __init__(self, graph, pos, default_edges, default_nodes):
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
        Toggles the right-click marking of a node.

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
        Toggles the marking of an edge.

        Args:
            edge: The edge to be toggled.
        """
        if edge in self.marked_edges:
            self.unmark_edge(edge)
        else:
            self.mark_edge(edge)

    def reset_colors(self):
        """
        Resets the marked nodes and edges to their default colors.
        """
        self.marked_nodes.clear()
        self.marked_edges.clear()

    def is_node_marked(self, node):
        """
        Checks if a node is marked.

        Args:
            node: The node to be checked.

        Returns:
            bool: True if the node is marked, False otherwise.
        """
        return node in self.marked_nodes

    def is_edge_marked(self, edge):
        """
        Checks if an edge is marked.

        Args:
            edge: The edge to be checked.

        Returns:
            bool: True if the edge is marked, False otherwise.
        """
        return edge in self.marked_edges

    def update_plot(self, nx, plt):
        """
        Updates the plot with the marked nodes and edges.

        Args:
            nx: The networkx module.
            plt: The matplotlib.pyplot module.
        """
        plt.clf()
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

        plt.title("Permutation Inversions Graph")
        plt.draw()

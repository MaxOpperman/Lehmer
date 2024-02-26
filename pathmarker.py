class PathMarker:
    def __init__(self, graph, pos, default_edges, default_nodes):
        self.graph = graph
        self.pos = pos
        self.marked_nodes = set()
        self.marked_edges = set()
        self.edge_colors = default_edges
        self.node_colors = default_nodes

    def mark_node(self, node):
        if node not in self.marked_nodes:
            self.marked_nodes.add(node)

    def unmark_node(self, node):
        if node in self.marked_nodes:
            self.marked_nodes.remove(node)

    def toggle_node(self, node):
        if node in self.marked_nodes:
            self.unmark_node(node)
        else:
            self.mark_node(node)

    def mark_edge(self, edge):
        if edge not in self.marked_edges:
            self.marked_edges.add(edge)

    def unmark_edge(self, edge):
        if edge in self.marked_edges:
            self.marked_edges.remove(edge)

    def toggle_edge(self, edge):
        if edge in self.marked_edges:
            self.unmark_edge(edge)
        else:
            self.mark_edge(edge)

    def reset_colors(self):
        self.marked_nodes.clear()
        self.marked_edges.clear()

    def is_node_marked(self, node):
        return node in self.marked_nodes

    def is_edge_marked(self, edge):
        return edge in self.marked_edges

    def update_plot(self, nx, plt):
        plt.clf()
        nx.draw(
            self.graph,
            self.pos,
            with_labels=True,
            node_color=self.node_colors,
            node_size=500,
            font_size=10,
            font_weight='bold',
            edge_color=self.edge_colors,
        )

        # Draw marked nodes in red
        nx.draw_networkx_nodes(self.graph, self.pos, nodelist=self.marked_nodes, node_color='blue', node_size=500)

        # Draw marked edges in green
        nx.draw_networkx_edges(self.graph, self.pos, edgelist=self.marked_edges, edge_color='blue', width=4)

        plt.title('Permutation Inversions Graph')
        plt.draw()

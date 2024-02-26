class PathMarker:
    def __init__(self, graph, pos):
        self.graph = graph
        self.pos = pos
        self.marked_nodes = set()
        self.marked_edges = set()

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

    def reset_colors(self):
        self.marked_nodes.clear()
        self.marked_edges.clear()

    def is_node_marked(self, node):
        return node in self.marked_nodes

    def update_plot(self, nx, plt):
        plt.clf()
        nx.draw(self.graph, self.pos, with_labels=True, node_color='skyblue', node_size=500, font_size=10, font_weight='bold', edge_color='gray')

        # Draw marked nodes in red
        nx.draw_networkx_nodes(self.graph, self.pos, nodelist=self.marked_nodes, node_color='red', node_size=500)

        # Draw marked edges in red
        nx.draw_networkx_edges(self.graph, self.pos, edgelist=self.marked_edges, edge_color='red', width=2)

        plt.title('Permutation Inversions Graph')
        plt.draw()

import networkx as nx

# Create an empty graph with no nodes or edges
G = nx.graph()

# Add one node
G.add_node(1)

# Add a list of nodes
G.add_nodes_from([2, 3])

# Or add any nbunch of nodes
# Nbunch = iterable container of nodes that is not itself a node in the graph (e.g. a list, set, graph, file, etc.)
H = nx.path_graph(10)
G.add_nodes_from(H)
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import os
import random

def load_graph_from_txt(file_path):
    """Loads graph data from the specified TXT file."""
    G = nx.DiGraph() # Use DiGraph for directed edges
    edges_data = []
    nodes = set()
    print(f"Loading graph from: {file_path}")
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split()
                if len(parts) == 3:
                    try:
                        u, v, p = int(parts[0]), int(parts[1]), float(parts[2])
                        nodes.add(u)
                        nodes.add(v)
                        # Add edge with probability as 'weight' attribute
                        G.add_edge(u, v, weight=p)
                        edges_data.append({'u': u, 'v': v, 'prob': p})
                    except ValueError:
                        print(f"Warning: Skipping line with invalid format: '{line}'")
                else:
                     print(f"Warning: Skipping line with incorrect number of parts: '{line}'")

    except FileNotFoundError:
        print(f"Error: Input file not found at '{file_path}'")
        return None, None, None

    print(f"Loaded {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    return G, list(nodes), edges_data

def plot_graph_with_traps(G, nodes, edges_data, output_filename="graph_plot_traps.png"):
    """Plots the graph highlighting specific node roles and trap structure."""
    if not G:
        print("Cannot plot an empty graph.")
        return

    # --- Define Node Groups based on dataset_5.txt structure ---
    main_nodes = [n for n in nodes if 0 <= n <= 14]
    distributor_node = [n for n in nodes if n == 15]
    bad_seed_nodes = [n for n in nodes if 16 <= n <= 18]
    trap_nodes = [n for n in nodes if 19 <= n <= 21]
    good_seed_nodes = [n for n in nodes if 22 <= n <= 24]

    # --- Layout ---
    print("Calculating layout...")
    # Spring layout can be sensitive, use a fixed seed
    # You might need to adjust k and iterations for better visualization
    pos = nx.spring_layout(G, k=0.6, iterations=150, seed=50) # Increased iterations
    print("Layout calculated.")

    # --- Drawing ---
    plt.figure(figsize=(20, 16)) # Larger figure size

    # Draw nodes with distinct styles
    node_size_main = 350
    node_size_good = 500
    node_size_dist = 700
    node_size_bad = 600
    node_size_trap = 550

    nx.draw_networkx_nodes(G, pos, nodelist=main_nodes, node_color='lightblue', node_size=node_size_main, label='Main Component (M0-14)')
    nx.draw_networkx_nodes(G, pos, nodelist=good_seed_nodes, node_color='lightgreen', node_size=node_size_good, label='Good Seeds (G22-24)')
    nx.draw_networkx_nodes(G, pos, nodelist=distributor_node, node_color='purple', node_size=node_size_dist, label='Distributor (D15)')
    nx.draw_networkx_nodes(G, pos, nodelist=bad_seed_nodes, node_color='orange', node_size=node_size_bad, label='Bad Seeds (B16-18)')
    nx.draw_networkx_nodes(G, pos, nodelist=trap_nodes, node_color='salmon', node_size=node_size_trap, label='Spider Trap (T19-21)')

    # Draw edges with varying thickness based on probability (weight)
    min_width = 0.1
    max_width = 4.0
    edge_widths = []
    edge_list_filtered = []
    for edge in edges_data:
         u, v = edge['u'], edge['v']
         # Ensure edge exists in the graph object (handles potential inconsistencies)
         if G.has_edge(u, v):
             edge_list_filtered.append((u,v))
             prob = G[u][v]['weight'] # Get weight directly from graph object
             edge_widths.append(min_width + prob * (max_width - min_width))

    nx.draw_networkx_edges(G, pos, edgelist=edge_list_filtered, width=edge_widths, alpha=0.4, edge_color='gray', arrowsize=10, node_size=node_size_main) # Use node_size to adjust arrow start/end

    # --- Highlight Critical Paths ---
    # 1. Distributor -> Bad Seeds
    d_to_b_edges = [(u, v) for u, v in G.edges() if u in distributor_node and v in bad_seed_nodes]
    nx.draw_networkx_edges(G, pos, edgelist=d_to_b_edges, width=max_width*1.1, alpha=0.9, edge_color='purple', style='dashed', arrowsize=15, node_size=node_size_dist)

    # 2. Bad Seeds -> Trap Entry
    b_to_trap_edges = [(u, v) for u, v in G.edges() if u in bad_seed_nodes and v == 19] # Assuming 19 is trap entry
    nx.draw_networkx_edges(G, pos, edgelist=b_to_trap_edges, width=max_width*1.1, alpha=0.9, edge_color='darkorange', style='dashed', arrowsize=15, node_size=node_size_bad)

    # 3. Within Trap Edges
    trap_internal_edges = [(u, v) for u, v in G.edges() if u in trap_nodes and v in trap_nodes]
    nx.draw_networkx_edges(G, pos, edgelist=trap_internal_edges, width=max_width*0.8, alpha=0.8, edge_color='red', arrowsize=12, node_size=node_size_trap)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')

    # --- Final Plot Adjustments ---
    plt.title("Graph Visualization Highlighting Trap Structure (dataset_5.txt)", fontsize=18)
    plt.xlabel(f"Layout: spring_layout (k=0.6, iterations=150, seed=50)")
    plt.legend(scatterpoints=1, loc='upper left')
    plt.axis('off')
    plt.tight_layout()

    # Save the plot
    try:
        plt.savefig(output_filename, dpi=300)
        print(f"Graph plot saved to '{output_filename}'")
    except Exception as e:
        print(f"Error saving plot: {e}")

    # Display the plot
    plt.show()

# --- Main execution block ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load graph data from TXT and plot using NetworkX, highlighting traps."
    )
    parser.add_argument(
        "input_file",
        help="Path to the input graph TXT file (e.g., dataset_5.txt)"
    )
    parser.add_argument(
        "-o", "--output",
        default="graph_plot_traps.png",
        help="Optional: Path for the output PNG image file."
    )

    args = parser.parse_args()

    # Load the graph
    graph, node_list, edge_list_data = load_graph_from_txt(args.input_file)

    # Plot the graph if loaded successfully
    if graph:
        plot_graph_with_traps(graph, node_list, edge_list_data, args.output)
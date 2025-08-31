import numpy as np
import networkx as nx
import argparse

def get_sorted_nodes(DATASET, N):

    dataset = np.loadtxt(DATASET)
    n_nodes = int(max(dataset[:, 0].max(), dataset[:, 1].max()) + 1)

    graph = nx.DiGraph()

    for i in range(0, dataset.shape[0]):
        if((dataset[i][0] == dataset[i][1])):
            continue
        else:
            graph.add_edge(int(dataset[i][0]), int(dataset[i][1]), weight = float(dataset[i][2]))

    pagerank_outputs = nx.pagerank(graph.reverse(), weight = 'weight', alpha = 0.65, max_iter = 100)

    sorted_pagerank = sorted(pagerank_outputs.items(), key = lambda kv: (kv[1], kv[0]), reverse = True)[:N]

    best_nodes = [x[0] for x in sorted_pagerank]

    return best_nodes

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'PageRank')
    parser.add_argument('dataset_path')
    parser.add_argument('output_path', help="Path to store the output seed nodes")
    parser.add_argument('k', type=int, help="Number of top nodes to select")

    args = parser.parse_args()

    DATASET_PATH = args.dataset_path
    OUTPUT_PATH = args.output_path
    N_NODES = int(args.k)

    seeds = get_sorted_nodes(DATASET_PATH, N_NODES)

    write_seeds = [str(x) + '\n' for x in seeds]
    file2 = open(OUTPUT_PATH, 'w')
    file2.writelines(write_seeds[:N_NODES])
    file2.close()
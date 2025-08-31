#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <set>
#include <map>
#include <queue>
#include <random>
#include <unordered_set>

using namespace std;

class RandomNumberGenerator {
public:
    RandomNumberGenerator() : rng(0), dist(0.0, 1.0) {}
    double extractNumber() { return dist(rng); }
private:
    mt19937 rng;
    uniform_real_distribution<double> dist;
};

struct Graph {
    map<long, vector<long>> adjList;
    map<pair<long, long>, double> probs;
    void addEdge(long src, long dst) {
        adjList[src].push_back(dst);
        //adjList[dst].push_back(src);
    }
};

Graph loadGraph(const string &fileName) {
    Graph graph;
    ifstream file(fileName);
    string line;
    long nnodes = 0, nedges = 0;
    double prob;
    vector<pair<long, long>> edges;
    map<pair<long, long>, double> probs;
    while (getline(file, line)) {
        istringstream iss(line);
        if (line[0] == '#') {
            iss.ignore(1); // Skip "# Nodes: "
            iss >> nnodes;
            iss >> nedges;
            cout << "Nodes: " << nnodes << " Edges: " << nedges << endl;
        } else {
            long src, dst;
            if (iss >> src >> dst >> prob) {
                edges.emplace_back(src, dst);
                probs[{src, dst}] = prob;
            }
        }
    }
    file.close();
    for (const auto &edge : edges) {
        graph.addEdge(edge.first, edge.second);
    }
    graph.probs = move(probs);
    return graph;
}

vector<long> loadSeedSet(const string &seedFileName){
  ifstream file(seedFileName);
  string line;
  int nlines = 0;
  vector<long> seedSet;
  while (getline(file, line)){
    istringstream iss(line);
    long node;
    iss >> node;
    seedSet.emplace_back(node);
    nlines++;
  }
  cout << "Found " << nlines << " nodes in the seed set.\n";
  file.close();
  return seedSet;
}

double random_sim(Graph &graph, map<pair<long, long>, double> &probs, const vector<long> &seedSet, long iters = 100) {
    RandomNumberGenerator rng;
    double infectionSpread = 0.0;
    for (long i = 0; i < iters; i++) {
        queue<long> Q;
        unordered_set<long> infectedNodes(seedSet.begin(), seedSet.end());
        for (long node : seedSet) {
            Q.push(node);
        }
        while (!Q.empty()) {
            long node = Q.front();
            Q.pop();
            for (long neighbor : graph.adjList[node]) {
                if (infectedNodes.count(neighbor)) continue;
                if (rng.extractNumber() > probs[{node, neighbor}]) continue;
                infectedNodes.insert(neighbor);
                Q.push(neighbor);
            }
        }
        infectionSpread += (double)infectedNodes.size() / iters;
    }
    return infectionSpread;
}


int main(int argc, char* argv[]) {
    if (argc < 3) {
        cerr << "Usage: " << argv[0] << " <graph_file> <seed_file>" << endl;
        return 1;
    }
    string fileName = argv[1];
    string seedFileName = argv[2];
    Graph graph = loadGraph(fileName);
    cout << "Graph loaded\n";
    vector<long> seedSet = loadSeedSet(seedFileName);
    cout << "Seed set loaded\n";
    double infection = random_sim(graph, graph.probs, seedSet, 100);
    cout << "Spread: " << infection << endl;
    return 0;
}


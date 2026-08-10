#!/usr/bin/env python3
"""
Custom Network Density & Graph-Theoretic Analyzer.
Calculates density, clustering coefficients, average path length, and eigenvector centrality
across excavations and synthesis essays, flagging isolated nodes and topological bottlenecks.
"""

import os
import re
import math
import sys

class DensityAnalyzer:
    def __init__(self, root_dir):
        self.root_dir = os.path.abspath(root_dir)
        self.nodes = [] # List of relative paths like 'excavations/stack-machines.md'
        self.adj = {} # Node -> list of other nodes (directed edges)
        self.undirected_adj = {} # Node -> set of neighbor nodes (undirected edges)

    def scan_network(self):
        """Scans directories and parses links to build the network graph."""
        # Find all relevant md files
        target_dirs = ['excavations', 'synthesis']
        md_files = []
        for d in target_dirs:
            dir_path = os.path.join(self.root_dir, d)
            if not os.path.exists(dir_path):
                continue
            for file in os.listdir(dir_path):
                if file.endswith(".md") and file not in ("README.md", "excavation-template.md"):
                    rel_path = f"{d}/{file}"
                    md_files.append(rel_path)
                    self.nodes.append(rel_path)

        # Initialize adjacencies
        for node in self.nodes:
            self.adj[node] = []
            self.undirected_adj[node] = set()

        # Regex to find links: [text](relative_path)
        link_pattern = re.compile(r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)')

        for node in self.nodes:
            file_abs_path = os.path.join(self.root_dir, node)
            file_dir = os.path.dirname(file_abs_path)

            if not os.path.exists(file_abs_path):
                continue

            with open(file_abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            matches = link_pattern.findall(content)
            for text, link in matches:
                clean_link = link.split('#')[0].split('?')[0].strip()
                if not clean_link or clean_link.startswith(("http", "mailto", "ftp", "/")):
                    continue

                # Resolve relative link
                target_abs = os.path.abspath(os.path.join(file_dir, clean_link))
                target_rel = os.path.relpath(target_abs, self.root_dir)

                if target_rel in self.nodes and target_rel != node:
                    if target_rel not in self.adj[node]:
                        self.adj[node].append(target_rel)
                    # For undirected graph
                    self.undirected_adj[node].add(target_rel)
                    self.undirected_adj[target_rel].add(node)

    def calculate_density(self) -> float:
        """Calculates directed graph density: E / (V * (V - 1))"""
        v = len(self.nodes)
        if v <= 1:
            return 0.0
        e = sum(len(neighbors) for neighbors in self.adj.values())
        return e / (v * (v - 1))

    def calculate_clustering_coefficients(self) -> dict:
        """Calculates undirected local clustering coefficient for each node and network average."""
        coefficients = {}
        for node in self.nodes:
            neighbors = list(self.undirected_adj[node])
            k = len(neighbors)
            if k <= 1:
                coefficients[node] = 0.0
                continue

            # Count edges between neighbors
            edges_between_neighbors = 0
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    n1, n2 = neighbors[i], neighbors[j]
                    if n2 in self.undirected_adj[n1]:
                        edges_between_neighbors += 1

            possible_edges = k * (k - 1) // 2
            coefficients[node] = edges_between_neighbors / possible_edges if possible_edges > 0 else 0.0

        # Network average
        avg_cc = sum(coefficients.values()) / len(self.nodes) if self.nodes else 0.0
        return {"local": coefficients, "average": avg_cc}

    def calculate_average_path_length(self) -> float:
        """Calculates the average shortest path length across all reachable node pairs (undirected)."""
        total_dist = 0
        pairs_count = 0

        for start_node in self.nodes:
            # BFS to find shortest path to all other nodes
            distances = {start_node: 0}
            queue = [start_node]
            head = 0

            while head < len(queue):
                curr = queue[head]
                head += 1
                curr_dist = distances[curr]

                for neighbor in self.undirected_adj[curr]:
                    if neighbor not in distances:
                        distances[neighbor] = curr_dist + 1
                        queue.append(neighbor)
                        total_dist += curr_dist + 1
                        pairs_count += 1

        return total_dist / pairs_count if pairs_count > 0 else 0.0

    def calculate_eigenvector_centrality(self) -> dict:
        """Calculates eigenvector centrality using power iteration (undirected) with a self-loop damping."""
        v = len(self.nodes)
        if v == 0:
            return {}

        # Initialize all centralities to 1 / sqrt(V)
        centrality = {node: 1.0 / math.sqrt(v) for node in self.nodes}

        # Power iteration
        iterations = 150
        tolerance = 1e-6

        for _ in range(iterations):
            next_centrality = {}
            for node in self.nodes:
                # 0.1 self-loop, 0.9 neighbors to prevent bipartite oscillations
                neighbor_sum = sum(centrality[neighbor] for neighbor in self.undirected_adj[node])
                next_centrality[node] = centrality[node] * 0.1 + neighbor_sum * 0.9

            # Normalize using L2 norm
            l2_norm = math.sqrt(sum(val**2 for val in next_centrality.values()))
            if l2_norm == 0:
                break

            # Update and check convergence
            diff = 0.0
            for node in self.nodes:
                normalized_val = next_centrality[node] / l2_norm
                diff += abs(normalized_val - centrality[node])
                centrality[node] = normalized_val

            if diff < tolerance:
                break

        return centrality

    def get_isolated_or_underlinked_nodes(self, threshold=2) -> list:
        """Identifies nodes with degree <= threshold."""
        flagged = []
        for node in self.nodes:
            deg = len(self.undirected_adj[node])
            if deg <= threshold:
                flagged.append((node, deg))
        return sorted(flagged, key=lambda x: x[1])

    def generate_report(self):
        """Prints a comprehensive topological network report."""
        print("\n" + "=" * 60)
        print("         GRAPH-THEORETIC KNOWLEDGE NETWORK ANALYSIS")
        print("=" * 60)
        print(f"  Total Network Nodes: {len(self.nodes)}")
        total_edges = sum(len(neighbors) for neighbors in self.adj.values())
        print(f"  Total Directed Edges: {total_edges}")

        density = self.calculate_density()
        print(f"  Network Density:     {density:.4f}")

        cc_data = self.calculate_clustering_coefficients()
        print(f"  Average Clustering:  {cc_data['average']:.4f}")

        avg_path = self.calculate_average_path_length()
        print(f"  Average Path Length: {avg_path:.4f} hops")

        centrality = self.calculate_eigenvector_centrality()
        top_central = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        print("\n--- Top 5 Most Central Lineages / Essays (Eigenvector Centrality) ---")
        for rank, (node, score) in enumerate(top_central, 1):
            print(f"  {rank}. {node} ({score:.4f})")

        underlinked = self.get_isolated_or_underlinked_nodes()
        print("\n--- Under-linked / Isolated Nodes (Degree <= 2) ---")
        if not underlinked:
            print("  None! The network has flawless cohesive density and topological integration.")
        else:
            for node, deg in underlinked:
                print(f"  • {node} (Links: {deg})")
        print("=" * 60 + "\n")

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    analyzer = DensityAnalyzer(repo_root)
    analyzer.scan_network()
    analyzer.generate_report()

if __name__ == "__main__":
    main()

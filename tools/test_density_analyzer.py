import os
import pytest
from density_analyzer import DensityAnalyzer

def test_density_analyzer_structure(tmp_path):
    """Test that DensityAnalyzer correctly parses mock md files and computes metrics."""
    # Create temporary structure with mock files
    excavations = tmp_path / "excavations"
    synthesis = tmp_path / "synthesis"
    excavations.mkdir()
    synthesis.mkdir()

    # Create mock md files
    f1 = excavations / "stack-machines.md"
    f2 = excavations / "ternary.md"
    f3 = synthesis / "spatial-computing.md"

    f1.write_text("[ternary](../excavations/ternary.md) and [spatial](../synthesis/spatial-computing.md)")
    f2.write_text("[stack](../excavations/stack-machines.md)")
    f3.write_text("[stack](../excavations/stack-machines.md)")

    analyzer = DensityAnalyzer(str(tmp_path))
    analyzer.scan_network()

    # 3 nodes: stack-machines.md, ternary.md, spatial-computing.md
    assert len(analyzer.nodes) == 3
    assert "excavations/stack-machines.md" in analyzer.nodes
    assert "excavations/ternary.md" in analyzer.nodes
    assert "synthesis/spatial-computing.md" in analyzer.nodes

    # Stack-machines links to ternary and spatial-computing
    assert "excavations/ternary.md" in analyzer.adj["excavations/stack-machines.md"]
    assert "synthesis/spatial-computing.md" in analyzer.adj["excavations/stack-machines.md"]

    # Verify density: 4 directed links (stack->ternary, stack->spatial, ternary->stack, spatial->stack)
    # Possible directed links: 3 * 2 = 6
    # Density should be 4/6 = 0.666...
    density = analyzer.calculate_density()
    assert pytest.approx(density) == 4.0 / 6.0

    # Verify clustering coefficient
    # In undirected graph:
    # Neighbors of stack: {ternary, spatial}
    # Edge between neighbors: none. So CC for stack = 0.
    # Ternary has neighbor {stack}. CC = 0.
    # Spatial has neighbor {stack}. CC = 0.
    # Average Clustering Coefficient = 0.0
    cc_data = analyzer.calculate_clustering_coefficients()
    assert cc_data["average"] == 0.0

    # Verify average path length
    # Shortest paths in undirected graph:
    # stack <-> ternary: 1
    # stack <-> spatial: 1
    # ternary <-> spatial (via stack): 2
    # Total undirected pairs: 6 (stack-ternary, stack-spatial, ternary-spatial, and symmetric)
    # Total distance: 1+1+2 + 1+1+2 = 8
    # Average path length = 8 / 6 = 1.3333
    avg_path = analyzer.calculate_average_path_length()
    assert pytest.approx(avg_path) == 8.0 / 6.0

    # Verify eigenvector centrality returns values for all nodes
    centrality = analyzer.calculate_eigenvector_centrality()
    assert len(centrality) == 3
    assert centrality["excavations/stack-machines.md"] > centrality["excavations/ternary.md"]

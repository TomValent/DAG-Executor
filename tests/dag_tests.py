import numpy as np

from dag_processor.DAG import DAG
from dag_processor.executor import Executor
from dag_processor.node import Node
from errors.duplicate_node_error import DuplicateNodeError
from errors.node_deps_error import NodeDependenciesError


def _merge_and_print_stats_action(inputs):
    """Merge raw and normalized stats and print them."""

    print("Raw Stats:", inputs["compute_raw_stats"])
    print("Normalized Stats:", inputs["compute_normalized_stats"])
    return {
        "raw_stats": inputs["compute_raw_stats"],
        "normalized_stats": inputs["compute_normalized_stats"]
    }


def test_from_pdf():
    """Test case provided by the assignment."""

    dag = DAG()

    dag.add_node(Node(
        name="generate_random_data",
        dependencies=[],
        action=lambda inputs: np.random.randint(1, 100, size=(1000, 5))
    ))

    dag.add_node(Node(
        name="compute_raw_stats",
        dependencies=["generate_random_data"],
        action=lambda inputs: {
            "min": np.min(inputs["generate_random_data"]),
            "max": np.max(inputs["generate_random_data"]),
            "mean": np.mean(inputs["generate_random_data"]),
            "std": np.std(inputs["generate_random_data"])
        }
    ))

    dag.add_node(Node(
        name="normalize_array",
        dependencies=["generate_random_data"],
        action=lambda inputs: (
            (inputs["generate_random_data"] - np.min(inputs["generate_random_data"])) /
            (np.max(inputs["generate_random_data"]) - np.min(inputs["generate_random_data"]))
        )
    ))

    dag.add_node(Node(
        name="compute_normalized_stats",
        dependencies=["normalize_array"],
        action=lambda inputs: {
            "min": np.min(inputs["normalize_array"]),
            "max": np.max(inputs["normalize_array"]),
            "mean": np.mean(inputs["normalize_array"]),
            "std": np.std(inputs["normalize_array"])
        }
    ))

    dag.add_node(Node(
        name="merge_and_print_stats",
        dependencies=["compute_raw_stats", "compute_normalized_stats"],
        action=_merge_and_print_stats_action
    ))

    executor = Executor(dag)
    results = executor.run()

    assert "generate_random_data" in results
    assert "compute_raw_stats" in results
    assert "normalize_array" in results
    assert "compute_normalized_stats" in results
    assert "merge_and_print_stats" in results

    assert results["generate_random_data"].shape == (1000, 5)
    assert results["normalize_array"].shape == (1000, 5)

    raw_stats = results["compute_raw_stats"]
    assert "min" in raw_stats and "max" in raw_stats
    assert "mean" in raw_stats and "std" in raw_stats

    normalized_stats = results["compute_normalized_stats"]
    assert "min" in normalized_stats and "max" in normalized_stats
    assert "mean" in normalized_stats and "std" in normalized_stats


def test_seven_nodes():
    """Test case with more complex dependencies."""

    dag = DAG()

    dag.add_node(Node(
        name="generate_data",
        dependencies=[],
        action=lambda inputs: np.random.randn(1000, 5)
    ))

    dag.add_node(Node(
        name="add_noise",
        dependencies=["generate_data"],
        action=lambda inputs: inputs["generate_data"] +
                              np.random.normal(0, 0.1, inputs["generate_data"].shape)
    ))

    dag.add_node(Node(
        name="compute_mean_std",
        dependencies=["add_noise"],
        action=lambda inputs: np.array([
            inputs["add_noise"].mean(axis=0),
            inputs["add_noise"].std(axis=0)
        ])
    ))

    dag.add_node(Node(
        name="compute_correlation",
        dependencies=["add_noise"],
        action=lambda inputs: np.corrcoef(inputs["add_noise"].T)
    ))

    dag.add_node(Node(
        name="normalize_features",
        dependencies=["add_noise", "compute_mean_std"],
        action=lambda inputs: (
            (inputs["add_noise"] - inputs["compute_mean_std"][0]) /
            inputs["compute_mean_std"][1]
        )
    ))

    dag.add_node(Node(
        name="pca_reduce",
        dependencies=["normalize_features", "compute_correlation"],
        action=lambda inputs: (
            inputs["normalize_features"] @
            np.linalg.eig(inputs["compute_correlation"])[1][:, :2]
        )
    ))

    dag.add_node(Node(
        name="summary_report",
        dependencies=["pca_reduce"],
        action=lambda inputs: np.array([
            inputs["pca_reduce"].mean(axis=0),
            inputs["pca_reduce"].std(axis=0)
        ])
    ))

    executor = Executor(dag)
    results = executor.run()

    assert results["generate_data"].shape == (1000, 5)
    assert results["add_noise"].shape == (1000, 5)
    assert results["compute_mean_std"].shape == (2, 5)
    assert results["compute_correlation"].shape == (5, 5)
    assert results["normalize_features"].shape == (1000, 5)
    assert results["pca_reduce"].shape == (1000, 2)
    assert results["summary_report"].shape == (2, 2)


def test_unmet_dependencies():
    """Test that executor raises error when dependencies are unmet. Should raise NodeDependenciesError."""

    dag = DAG()

    dag.add_node(Node(
        name="node_a",
        dependencies=[],
        action=lambda inputs: np.array([1, 2, 3])
    ))

    # Node B depends on non-existent node "missing_node"
    dag.add_node(Node(
        name="node_b",
        dependencies=["missing_node"],
        action=lambda inputs: inputs["missing_node"] * 2
    ))

    executor = Executor(dag)

    try:
        executor.run()
        assert False, "Expected NodeDependenciesError to be raised"
    except NodeDependenciesError as e:
        assert "node_b" in str(e)
        assert "missing_node" in str(e)


def test_duplicate_nodes():
    dag = DAG()

    dag.add_node(Node(
        name="node_a",
        dependencies=[],
        action=lambda inputs: np.array([1, 2, 3])
    ))

    try:
        dag.add_node(Node(
            name="node_a",
            dependencies=[],
            action=lambda inputs: np.array([1, 2, 3])
        ))
        assert False, "Expected DuplicateNodeError to be raised"
    except DuplicateNodeError as e:
        assert "node_a" in str(e)

import numpy as np

from concurrent.futures import ThreadPoolExecutor

from dag_processor.DAG import DAG
from dag_processor.node import Node
from errors.node_deps_error import NodeDependenciesError


class Executor:
    """Class for executing DAG nodes in parallel using Kahn's algorithm."""

    def __init__(self, dag):
        """Executor constructor. Requires DAG object."""

        self.dag = dag


    def run(self):
        """
        Execute all nodes in the DAG using Kahn's algorithm.

        1. Find all nodes with no remaining dependencies
        2. Run them in parallel
        3. Remove completed nodes from others' remaining_deps
        4. Repeat until all nodes are processed
        """

        results: dict[str, np.ndarray] = {}

        while True:
            nodes_to_run = []

            for node in self.dag.get_nodes():
                if len(node.get_remaining_dependencies()) == 0 and not node.is_passed():
                    nodes_to_run.append(node)

            if not nodes_to_run:
                # check if there are nodes that didn't run at all and exit
                for node in self.dag.get_nodes():
                    if not node.is_passed():
                        raise NodeDependenciesError(node.get_name(), node.get_dependencies())

                # the good ending
                print(f"All nodes processed.")
                break

            print(f"Starting stage: {[n.get_name() for n in nodes_to_run]}")

            with ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(
                        node.run,
                        {dep: results[dep] for dep in node.get_dependencies()}
                    ): node
                    for node in nodes_to_run
                }
                # Collect all results first
                for future, node in futures.items():
                    results[node.get_name()] = future.result()
                    node.set_passed()
                    print(f"Finished node: {node.get_name()}.")

                # Remove dependencies after all nodes have completed
                for future, node in futures.items():
                    self.dag.pop_from_deps(node.get_name())

        return results

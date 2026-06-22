from dag_processor.node import Node


class DAG:
    """
    Class representing a DAG data structure. Contains list of nodes an methods for adding nodes and removing
    dependencies.
    """

    def __init__(self):
        """Initialize the DAG object."""

        self._nodes: list = []


    def add_node(self, node):
        """Add a node to the DAG object."""

        self._nodes.append(node)


    def pop_from_deps(self, dep: str):
        """Remove a dependency for all nodes after the dependency is satisfied."""

        for node in self._nodes:
            if dep in node.get_remaining_dependencies():
                node.remove_from_remaining_dependencies(dep)


    def get_nodes(self):
        """Return a list of all nodes in the DAG object."""

        return self._nodes

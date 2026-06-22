from dag_processor.node import Node
from errors.duplicate_node_error import DuplicateNodeError


class DAG:
    """
    Class representing a DAG data structure. Contains list of nodes an methods for adding nodes and removing
    dependencies.
    """

    def __init__(self):
        """Initialize the DAG object."""

        self._nodes: list = []


    def add_node(self, node: Node) -> None:
        """
        Add a node to the DAG object. If not exists already.

        :param node: node to add.
        """

        if any(n.get_name() == node.get_name() for n in self._nodes):
            raise DuplicateNodeError(f"Node '{node.get_name()}' already exists in the DAG.")

        self._nodes.append(node)


    def pop_from_deps(self, dep: str) -> None:
        """
        Remove a dependency for all nodes after the dependency is satisfied.

        :param dep: name of the dependency to remove.
        """

        for node in self._nodes:
            if dep in node.get_remaining_dependencies():
                node.remove_from_remaining_dependencies(dep)


    def get_nodes(self) -> list:
        """Return a list of all nodes in the DAG object."""

        return self._nodes

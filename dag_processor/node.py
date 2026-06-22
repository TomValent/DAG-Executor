from typing import Callable, Any

import numpy as np


class Node:
    """
    Represents a node in the DAG. It contains a name, list of dependendies, action to perform, and its state.
    Class stores all dependencies (used to fetch results from the executor) and remaining dependencies to be satisfied
    (used by Kahn's algorithm to track when node is ready to run).
    """

    def __init__(self, name: str, dependencies: list, action: Callable[[dict[str, np.ndarray]], Any]):
        """
        Node constructor.

        :param name: name of the action this node represents, must be unique in a DAG.
        :param dependencies: list of dependencies for this node.
        :param action: function that takes a dict of input arrays and returns a result.
        """

        self._name: str = name
        self._dependencies: list = list(dependencies)
        self._remaining_deps: list = list(dependencies)
        self._action: Callable[[dict[str, np.ndarray]], Any] = action
        self._passed: bool = False


    def run(self, inputs: dict[str, np.ndarray]) -> Any:
        """Execute this node's action with the provided inputs."""

        return self._action(inputs)


    def get_name(self) -> str:
        """Return the name of the node."""

        return self._name


    def get_dependencies(self) -> list:
        """Return a list of all dependencies for this node."""

        return self._dependencies


    def get_remaining_dependencies(self) -> list:
        """Return a list of all dependencies for this node."""

        return self._remaining_deps


    def remove_from_remaining_dependencies(self, node_name: str) -> None:
        """Return a list of all dependencies for this node."""

        self._remaining_deps.remove(node_name)


    def set_passed(self) -> None:
        """Set this node's passed status."""

        self._passed = True


    def is_passed(self) -> bool:
        """Return True if the node is passed, False otherwise."""

        return self._passed

class NodeDependenciesError(RuntimeError):
    """Raised when a node has unmet dependencies."""

    def __init__(self, node_name: str, unmet_dependencies: list[str]):
        """
        Constructor providing custom error message.

        :param node_name: name of the node.
        :param unmet_dependencies: list of unmet dependencies of the node.
        """

        super().__init__(f"Node {node_name} dependencies {unmet_dependencies} unmet.")

class NodeDependenciesError(RuntimeError):
    """Raised when a node has unmet dependencies."""

    def __init__(self, node_name, unmet_dependencies):
        """Constructor providing custom error message."""

        super().__init__(f"Node {node_name} dependencies {unmet_dependencies} unmet.")

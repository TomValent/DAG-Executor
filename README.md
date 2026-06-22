## DAG Executor

A lightweight Python implementation of a DAG (Directed Acyclic Graph) executor with parallel execution support.

### Structure

```
root/
├── dag_processor/
│   ├── DAG.py              # DAG data structure
│   ├── executor.py         # Executor with parallel execution
│   └── node.py             # Node definition
├── errors/
│   └── node_deps_error.py  # Custom exception
└── tests/
    └── dag_tests.py
```

### Requirements

- Python 3.10+
- NumPy
- Pytest

### Usage

```pycon
python from dag_processor.DAG import DAG
from dag_processor.executor import Executor
from dag_processor.node import Node
import numpy as np

dag = DAG()

dag.add_node(Node(
    name="node_name",
    dependencies=[],
    action=lambda inputs: np.random.randn(1000, 5)
))

dag.add_node(Node(
    ...
))

...

executor = Executor(dag)
results = executor.run()
```

### How It Works

The executor uses Kahn's algorithm to determine execution order:

1. Find all nodes with no remaining dependencies
2. Execute them in parallel using ThreadPoolExecutor
3. Once completed, remove them from other nodes' dependencies
4. Repeat until all nodes are processed
5. If nodes remain unprocessed after the loop, a cycle is detected and NodeDependenciesError is raised


### Running Tests

```bash
  python -m pytest tests/
```

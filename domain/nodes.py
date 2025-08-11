from abc import ABC, abstractmethod
from typing import Dict, List


class Node(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def call(self, arg1: str, arg2: str) -> Dict:
        pass


class ExampleNode(Node):
    name = "example-node"
    title = "Node Title"
    description = "Node Description"

    def call(self, arg1: str, arg2: str, arg3: int) -> Dict:
        # Plugin logic here
        return {"arg1": arg1, "arg2": arg2, "arg3": arg3}


class SentimentNode(Node):
    name = "sentiment-node"
    title = "Sentiment Analysis"
    description = "Analyze text sentiment"

    def call(self, arg1: str, arg2: str) -> Dict:
        # Plugin logic here
        return {"sentiment": "positive", "score": 0.8}


def get_all_nodes(nodes: List[Node]) -> Dict[str, Node]:
    all_nodes = {}
    for node in nodes:
        node_name = getattr(node, "name", None)
        if node_name:
            if node_name in all_nodes:
                print(f" Warning: Duplicate node name '{node_name}' found")
            all_nodes[node_name] = node
            print(f"Registered node: {node_name}")

    return all_nodes

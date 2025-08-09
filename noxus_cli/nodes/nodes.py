from abc import ABC, abstractmethod
from typing import Dict


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

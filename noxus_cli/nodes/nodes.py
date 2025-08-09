from typing import Dict
from abc import ABC, abstractmethod


class Node(ABC):
    @abstractmethod
    def call(self, arg1: str, arg2: str) -> Dict:
        pass


class ExampleNode(Node):
    title = "Node Title"
    description = "Node Description"

    def call(self, arg1: str, arg2: str, arg3: int) -> Dict:
        # Plugin logic here
        return {"arg1": arg1, "arg2": arg2, "arg3": arg3}


class SentimentNode(Node):
    title = "Sentiment Analysis"
    description = "Analyze text sentiment"

    def call(self, arg1: str, arg2: str) -> Dict:
        # Plugin logic here
        return {"sentiment": "positive", "score": 0.8}

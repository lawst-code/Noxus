from abc import ABC, abstractmethod
from typing import List

from .nodes import ExampleNode, Node, SentimentNode


class Plugin(ABC):
    @abstractmethod
    def nodes(self) -> List[Node]:
        pass


class SentimentPlugin(Plugin):
    title = "Sentiment Plugin"

    def nodes(self):
        return [SentimentNode(), ExampleNode()]

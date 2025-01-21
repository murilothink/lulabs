from abc import ABC, abstractmethod
from typing import List
from models.user import User

class DataProcessor(ABC):
    @abstractmethod
    def process(self, lines: List[str]) -> List[User]:
        pass

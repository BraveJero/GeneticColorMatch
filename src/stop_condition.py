from abc import ABC, abstractmethod


class StopCondition(ABC):
    @abstractmethod
    def __call__(self):
        pass

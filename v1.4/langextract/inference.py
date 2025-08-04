
import abc
from collections.abc import Iterator, Sequence
import dataclasses
from typing import Any

@dataclasses.dataclass(frozen=True)
class ScoredOutput:
    score: float | None = None
    output: str | None = None

class InferenceOutputError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class BaseLanguageModel(abc.ABC):
    def __init__(self, constraint=None):
        self._constraint = constraint

    @abc.abstractmethod
    def infer(self, batch_prompts: Sequence[str], **kwargs) -> Iterator[Sequence[ScoredOutput]]:
        pass

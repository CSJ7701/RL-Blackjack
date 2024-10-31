from enum import Enum
from typing import Iterator

class Action(Enum):
    HIT = "hit"
    STAND = "stand"

    @classmethod
    def all_actions(cls) -> Iterator['Action']:
        """
        Returns an iterator over all possible actions.
        """
        return iter(cls)

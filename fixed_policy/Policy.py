from Actions import Action
from typing import Dict, Tuple

class Policy:
    def __init__(self, cutoff: int):
        self.cutoff = cutoff
        self.state_values = Dict[Tuple[int,int,bool],float]
        # State values are a dict that associates (agent_hand, dealer_hand, usable_ace) with an value between 0 and 1.


    def chooseAction(self, hand: int) -> Action:
        """
        Takes a hand value and returns the action to take
        """
        if hand < self.cutoff:
            return Action.HIT
        return Action.STAND

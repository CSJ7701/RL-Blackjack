from Actions import Action
from typing import Dict, Tuple

class MonteCarlo:
    def __init__(self):
        # Dictionary to hold the "best" action for each state
        # States defined as a tuple - (agent hand value, dealer card)
        # Values are actions, initially set to "HIT" for simplicity

        self.policy: Dict[Tuple[int,int],Dict[Action,int]] = {}
        self.state_count: Dict[Tuple[int,int],int] = {} # Counts the number of times a state has been visited. For discounting?

    def initialize_state(self, state: Tuple[int,int]) -> None:
        """
        Initialize a state with a default action.
        :param state: Tuple with agents hand value and dealers hand value.
        """
        if state not in self.policy:
            self.policy[state] = {Action.HIT: 0}

    def update_policy(self, state: Tuple[int,int], action: Action, value: int) -> None:
        """
        Update policy manually. Changes the action for a given state.
        :param state: Tuple with agent and dealers' hand values
        :param action: The action to update for this state.
        :param value: The value to assign the action
        """
        self.initialize_state(state)
        self.policy[state] = {action: value}
        

    def get_best_action(self, state: Tuple[int,int]) -> Action:
        """
        Find the best known action for the given state, based on the list.
        :param state: State. Tuple of agent's hand value and dealer's visible hand.
        :return: The 'best' action for this state.
        """
        self.initialize_state(state)

        # This is somewhat arcane, but should return the Action with the highest value.
        # Based on the dict structure I use, where policy is a Dict that looks like:
        # Policy = {
        #            (agent_hand,dealer_hand): {
        #                                        Action: Value
        #                                      }
        #          }

        return max(self.policy[state].items(), key=lambda k: k[1])[0]

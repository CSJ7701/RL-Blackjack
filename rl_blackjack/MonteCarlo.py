from Actions import Action
from typing import Dict, Tuple

class MonteCarlo:
    def __init__(self):
        # Dictionary to hold the "best" action for each state
        # States defined as a tuple - (agent hand value, dealer card)
        # Values are actions, initially set to "HIT" for simplicity

        self.policy: Dict[Tuple[int,int],Action] = {}
        self.state_count: Dict[Tuple[int,int],int] = {} # Counts the number of times a state has been visited. For discounting?

    def initialize_state(self, agent_value: int, dealer_card: int) -> None:
        """
        Initialize a state with a default action.
        ... Explain later?
        :param agent_value: Total hand value of the agent.
        :param dealer_card: The dealer's visible card value.
        """

        state = (agent_value, dealer_card)
        if state not in self.policy:
            self.policy[state] = Action.HIT

    def update_policy(self, agent_value: int, dealer_card: int, best_action: Action) -> None:
        """
        Update policy manually. Changes the action for a given state.
        :param agent_value: Total hand value for the agent.
        :param dealer_card: The dealers visible card.
        :param best_action: The action that is 'best' for this state.
        """
        state = (agent_value, dealer_card)
        self.initialize_state(agent_value,dealer_card)
        self.policy[state] = best_action

    def get_best_action(self, agent_value: int, dealer_card: int) -> Action:
        """
        Find the best known action for the given state, based on the list.
        :param agent_value: Total value of the agent's hand.
        :param dealer_card: The dealers visible card value.
        :return: The 'best' action for this state.
        """
        state = (agent_value, dealer_card)
        self.initialize_state(agent_value, dealer_card)
        return self.policy[state]

import os
import pickle
from random import random, choice
from Actions import Action
from typing import Dict, Tuple

class MonteCarlo:
    def __init__(self):
        # Dictionary to hold the "best" action for each state
        # States defined as a tuple - (agent hand value, dealer card)
        # Values are actions, initially set to "HIT" for simplicity

        self.policy: Dict[Tuple[int,int],Dict[Action,float]] = {}
        self.actions: Dict[Tuple[int,int],Action] = {}
        self.state_count: Dict[Tuple[Tuple[int,int],Action],int] = {} # Counts the number of times a state has been visited. For discounting?

    def initialize_state(self, state: Tuple[int,int]) -> None:
        """
        Initialize a state with a default action.
        :param state: Tuple with agents hand value and dealers hand value.
        """
        if state not in self.policy:
            self.policy[state] = {Action.HIT: 0, Action.STAND: 0}
        if (state, Action.HIT) not in self.state_count:
            self.state_count[state,Action.HIT] = 0
        if (state, Action.STAND) not in self.state_count:
            self.state_count[state,Action.STAND] = 0

    def update(self, state: Tuple[int,int], action: Action, reward: int) -> None:
        """
        Update policy manually. Changes the action for a given state.
        :param state: Tuple with agent and dealers' hand values
        :param action: The action to update for this state.
        :param value: The value to assign the action
        """
        self.initialize_state(state)
        self.state_count[state,action] += 1
        # print(state)
        # print(action)
        action_value = self.policy[state][action]
        action_count = self.state_count[state,action]
        self.policy[state][action] = action_value+(reward-action_value)/action_count


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

    def update_actions(self, epsilon: float) -> None:
        """
        Use the given state/value actions (self.policy) to populate a fixed policy associating states with actions.
        """
        for state in self.policy.keys():
            if random() < epsilon:
                best_action = self.get_best_action(state)
                possible_actions = [action for action in Action if action != best_action]
                action = choice(possible_actions) if possible_actions else best_action
            else:
                action = self.get_best_action(state)
            self.actions[state] = action

    def get_policy(self, state: Tuple[int,int]) -> Action:
        """
        Return the on-policy action defined in the current policy (self.actions).
        If there is no known on-policy action, hit.
        :param state: The agent's current state.
        """
        if state not in self.actions.keys():
            return Action.HIT
        else:
            return self.actions[state]

    def save(self, filename: str) -> None:
        """
        Save the policy to a .MonteCarlo file.
        :param filename: Base filename (without extension) to save to.
        """
        full_filename = f"{filename}.MonteCarlo"
        with open(full_filename, 'wb') as f:
            pickle.dump(self.policy, f)
            pickle.dump(self.actions,f)
        print(f"Policy saved to {full_filename}")

    def load(self, filename: str) -> None:
        """
        Load the policy from a .MonteCarlo file.
        :param filename: Name of the file to load (without extension).
        """
        full_filename = f"{filename}.MonteCarlo"

        if not os.path.exists(full_filename):
            print(f"File {full_filename} not found. Policy not loaded.")
            return
        with open(full_filename, 'rb') as f:
            self.policy = pickle.load(f)
            self.actions = pickle.load(f)
        print(f"Policy loaded from {full_filename}")
        

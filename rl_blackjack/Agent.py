from typing import Tuple
from Actions import Action
from MonteCarlo import MonteCarlo
from random import random, choice

class Agent:
    def __init__(self, policy: MonteCarlo, epsilon: float = 0.2):
        self.hand = []
        self.policy = policy
        self.epsilon = epsilon # Probability of exploration

    def receiveCard(self, card: str) -> None:
        """
        Add a card to the agent's hand.
        """
        self.hand.append(card)

    def calculateHand(self) -> int:
        """
        Calculate and return the value of the agent's hand.
        """
        value = 0
        aces = 0

        for card in self.hand:
            if card == 'A':
                aces += 1
                value += 11
            else:
                value += int(card)

        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return value

    def playTurn(self, state: Tuple[int,int]) -> None:
        if random() < self.epsilon:
            # exclude the best action if possible
            best_action = self.policy.get_best_action(state)
            possible_actions = [action for action in Action if action != best_action]
            action = choice(possible_actions) if possible_actions else best_action
        else:
            action = self.policy.get_best_action(state)

    def resetHand(self) -> None:
        """
        Clear the agent's hand for a new round.
        """
        self.hand = []


if __name__ == "__main__":
    policy = MonteCarlo()
    agent = Agent(policy)
    agent.receiveCard("5")
    agent.receiveCard("8")
    print("Agent's hand:", agent.hand)
    print("Hand value:", agent.calculateHand())

    agent_hand = agent.calculateHand()
    dealer_hand = 5 # placeholder
    state = (agent_hand,dealer_hand)

    agent.playTurn(state)
    agent.resetHand()
    print("Hand after reset:", agent.hand)

from typing import Tuple
from Policy import Policy

class Agent:
    def __init__(self, cutoff: int = 20):
        self.policy = Policy(cutoff)
        self.hand = []
        self.states = []
        self.usable_ace = False

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
            self.usable_ace = True
        return value

    def stateUpdate(self, dealer_hand: int) -> None:
        """
        Takes the dealer's hand and uses it to update the current state.
        :param dealer_hand: The integer value of the dealer's visible card.
        """
        state: Tuple[int,int,bool]
        current_hand = self.calculateHand()
        usable_ace = self.usable_ace
        state = (current_hand, dealer_hand, usable_ace)
        self.states.append(state)

    def rewardUpdate(self, reward: int) -> None:
        # receive reward from Table class
        # pass reward to policy to update all states in this episode.
        ...

    def playTurn(self) -> None:
        # Call policy to return the action to take.
        ...

    def reset(self) -> None:
        """
        Clear the Agent's hand and reset parameters for a new episode.
        """
        self.hand = []
        self.states = []
        self.usable_ace = False

                

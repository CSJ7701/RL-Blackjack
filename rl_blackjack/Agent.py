from typing import Tuple
from Actions import Action
from MonteCarlo import MonteCarlo
from random import random, choice

## TODO: agent never adds 'stand' to stateActions

class Agent:
    def __init__(self, policy: MonteCarlo, name: str = "Agent", epsilon: float = 0.2, win_reward: int = 1, loss_reward: int = -1, draw_reward: int = 0):
        self.name = name
        self.hand = []
        self.states = []
        self.stateActions = []
        self.policy = policy
        self.epsilon = epsilon # Probability of exploration
        self.win_reward = win_reward
        self.loss_reward = loss_reward
        self.draw_reward = draw_reward

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

    def playTurn(self, dealer_hand: int) -> Action:
        state = (self.calculateHand(), dealer_hand)
        self.stateUpdate(dealer_hand)
        if random() < self.epsilon:
            # exclude the best action if possible
            best_action = self.policy.get_best_action(state)
            possible_actions = [action for action in Action if action != best_action]
            action = choice(possible_actions) if possible_actions else best_action
        else:
            action = self.policy.get_best_action(state)
        self.stateActions.append(action) # Keep track of the actions taken, in order
        return action

    def stateUpdate(self, dealer_hand: int) -> None:
        """
        Takes dealer's hand and updates current state.
        :param dealer_hand: Integer value of the dealer's visible card.
        """
        state = Tuple[int,int]
        current_hand = self.calculateHand()
        state = (current_hand, dealer_hand)
        if state not in self.states:
            self.states.append(state)

    def rewardUpdate(self, reward: int) -> None:
        """
        Receive a reward from the table class, and use it to update every state/action pair in this hand.
        :param reward: The reward from win/loss/draw in this hand.
        """
        # print(f"States: {self.states}")
        # print(f"Actions: {self.stateActions}")
        # for state, action in zip(self.states, self.stateActions):
            # print(f"State: {state} with action {action} = {reward}")
        # print(self.policy.state_count)
        for state, action in zip(self.states, self.stateActions):
            self.policy.update(state, action, reward)

    def reset(self) -> None:
        """
        Clear the agent's hand for a new round.
        """
        self.hand = []
        self.states = []
        self.stateActions = []


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

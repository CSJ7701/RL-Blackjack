class Agent:
    def __init__(self):
        self.hand = []

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

    def playTurn(self) -> None:
        ...

    def resetHand(self) -> None:
        """
        Clear the agent's hand for a new round.
        """
        self.hand = []


if __name__ == "__main__":
    agent = Agent()
    agent.receiveCard("5")
    agent.receiveCard("8")
    print("Agent's hand:", agent.hand)
    print("Hand value:", agent.calculateHand())
    
    agent.playTurn()
    agent.resetHand()
    print("Hand after reset:", agent.hand)

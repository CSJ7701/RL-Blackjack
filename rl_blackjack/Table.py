from Agent import Agent
from Dealer import Dealer
from Shoe import Shoe

class Table:
    def __init__(self, shoe: Shoe, dealer: Dealer):
        """
        Initialize the table with a shoe and a dealer.
        """
        self.agents: list[Agent] = []
        self.shoe = shoe
        self.dealer = dealer
        self.current_turn = 0

    def add(self, agent:Agent) -> None:
        """
        Add an agent to the table.
        """
        self.agents.append(agent)

    def dealInitial(self) -> None:
        """
        Dealer deals to the table.
        """
        for agent in self.agents:
            self.dealer.deal(agent)
            self.dealer.deal(agent)
        # Dealer draws last
        self.dealer.drawInitial()

    def playTurns(self) -> None:
        """
        Each agent takes a turn, then the dealer plays.
        """

        for agent in self.agents:
            agent.playTurn()

        # After all the agents have played
        self.dealer.playTurn()

    def reset(self) -> None:
        """
        Reset the table for a new round.
        """
        self.current_turn = 0
        for agent in self.agents:
            agent.resetHand()
        self.dealer.reset()

if __name__ == "__main__":
    # Set up the components
    shoe = Shoe()
    dealer = Dealer(shoe)
    table = Table(shoe, dealer)

    # Add agents to the table
    table.add(Agent())
    table.add(Agent())

    # Deal initial cards
    table.dealInitial()

    # Print each agent's initial hand
    for i, agent in enumerate(table.agents):
        print(f"Agent {i+1} initial hand:", agent.hand)
    print(f"Dealer initial hand: {dealer.checkHand()}\n")

    # Agents and dealer play their turns
    table.playTurns()

    # Show final hands and values
    print("Dealer's final hand: ", "Value:", dealer.calculateHand()," | ", dealer.hand)
    for i, agent in enumerate(table.agents):
        print(f"Agent {i+1}'s final hand:", "Value:", agent.calculateHand()," | ", agent.hand)


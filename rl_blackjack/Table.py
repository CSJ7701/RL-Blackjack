from Actions import Action
from Agent import Agent
from Dealer import Dealer
from MonteCarlo import MonteCarlo
from Shoe import Shoe
from tqdm import tqdm
from typing import List

class Table:
    def __init__(self, shoe: Shoe, dealer: Dealer):
        """
        Initialize the table with a shoe and a dealer.
        """
        self.agents: List[Agent] = []
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

    def playEpisode(self) -> None:
        """
        Each agent takes a turn, then the dealer plays.
        """
        dealer_hand_full = self.dealer.calculateHand()
        dealer_hand_hide = self.dealer.calculateHand(True)
        initial_winners = [agent for agent in self.agents if agent.calculateHand() == 21]
        for agent in self.agents:
            agent.stateUpdate(dealer_hand_hide)
        if dealer_hand_full == 21:
            for agent in self.agents:
                if agent in initial_winners:
                    agent.rewardUpdate(agent.draw_reward)
                else:
                    agent.rewardUpdate(agent.loss_reward)
            return
        elif initial_winners:
            for agent in initial_winners:
                agent.rewardUpdate(agent.win_reward)
            return

        for agent in self.agents:
            action=Action.HIT
            while action != Action.STAND:
                action = agent.playTurn(dealer_hand_hide)
                if action == Action.HIT:
                    self.dealer.deal(agent)
                    agent.stateUpdate(dealer_hand_hide)
                    if agent.calculateHand() > 21:
                        agent.rewardUpdate(agent.loss_reward)
                        break
            agent.stateUpdate(dealer_hand_hide)

        if any(agent.calculateHand() <= 21 for agent in self.agents):
            self.dealer.playTurn()

        dealer_hand_final = self.dealer.calculateHand()
        for agent in self.agents:
            agent.stateUpdate(dealer_hand_final)
            agent_hand = agent.calculateHand()
            if agent_hand > 21:
                agent.rewardUpdate(agent.loss_reward)
            elif dealer_hand_final > 21 or agent_hand > dealer_hand_final:
                agent.rewardUpdate(agent.win_reward)
            elif agent_hand == dealer_hand_final:
                agent.rewardUpdate(agent.draw_reward)
            else:
                agent.rewardUpdate(agent.loss_reward)

                
    def reset(self) -> None:
        """
        Reset the table for a new round.
        """
        self.current_turn = 0
        self.shoe.reset()
        for agent in self.agents:
            agent.reset()
        self.dealer.reset()

if __name__ == "__main__":
    # Set up the components
    shoe = Shoe()
    dealer = Dealer(shoe)
    table = Table(shoe, dealer)
    policy = MonteCarlo()

    # Add agents to the table
    table.add(Agent(policy, epsilon=0.5))

    episode_count=10
    generation_count = 10
    for generation in range(generation_count):
        policy.update_actions(0.5)
        for _ in range(episode_count):
            table.dealInitial()

            # Print each agent's initial hand
            for i, agent in enumerate(table.agents):
                print(f"Agent {i+1} initial hand:", agent.hand)
            print(f"Dealer initial hand: {dealer.checkHand()}\n")

            table.playEpisode()

            # Show final hands and values
            print("Dealer's final hand: ", "Value:", dealer.calculateHand()," | ", dealer.hand)
            for i, agent in enumerate(table.agents):
                print(f"Agent {i+1}'s final hand:", "Value:", agent.calculateHand()," | ", agent.hand)
                #print(agent.policy.policy)
            table.reset()

    #print(policy.policy)

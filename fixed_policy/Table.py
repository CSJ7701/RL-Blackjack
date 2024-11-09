from typing import List
from Actions import Action
from Agent import Agent
from Dealer import Dealer
from Policy import Policy
from Shoe import Shoe
from Visualizer import BlackjackPolicyVisualizer
from tqdm import tqdm

class Table:
    def __init__(self, shoe: Shoe, dealer:Dealer):
        """
        Initialize the table with a shoe and a dealer.
        """
        self.agents: List[Agent] = [] 
        self.shoe = shoe
        self.dealer = dealer

    def reset(self) -> None:
        for agent in self.agents:
            agent.reset()
        self.dealer.reset()
        self.shoe.reset()


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

    def playEpisodeOld(self) -> None:
        """
        Each agent takes a turn, then the dealer plays.
        """
        # Check whether there is an initial win
        # Logic is somewhat skewed here for simplicity.
        # Multiple agents can "win" if multiple agents have 21.
        # If an agent AND the dealer have 21, then it is a draw.
        for agent in self.agents:
            agent.stateUpdate(self.dealer.calculateHand(True))
            if agent.calculateHand() == 21:
                if self.dealer.calculateHand(False) == 21:
                    # Draw if 
                    agent.rewardUpdate(agent.draw_reward)
                else:
                    agent.rewardUpdate(agent.win_reward)

            ## If no one won, each agent takes their turn, then the dealer takes their turn.
            else:
                action = Action.HIT
                while action != Action.STAND:
                    # Agent updates state every time it plays a turn.
                    action = agent.playTurn(self.dealer.calculateHand(False))
                    if action == Action.HIT:
                        self.dealer.deal(agent)
                # Agent has chosen to stand
                agent_hand = agent.calculateHand()
                if agent_hand > 21:
                    agent.rewardUpdate(agent.loss_reward)
                elif agent_hand == 21:
                    agent.rewardUpdate(agent.win_reward)
                else: # If score is less than 21, find the closest to 21 
                    # If the current highest score is undefined
                    if not self.episode_winner:
                        self.episode_winner = agent
                    if agent.calculateHand() > self.episode_winner.calculateHand():
                        self.episode_winner = agent
                    self.episode_queue.append(agent)

    def playEpisode(self) -> None:
        """
        Play a single round of blackjack with all agents and the dealer.
        """
        dealer_hand_full = self.dealer.calculateHand()
        dealer_hand_hide = self.dealer.calculateHand(True)
        initial_winners = [agent for agent in self.agents if agent.calculateHand() == 21]
        
        # Update every agent's initial state
        for agent in self.agents:
            agent.stateUpdate(dealer_hand_hide)

        # If dealer has initial blackjack
        if dealer_hand_full ==  21:
            for agent in self.agents:
                if agent in initial_winners:
                    agent.rewardUpdate(agent.draw_reward)
                else:
                    agent.rewardUpdate(agent.loss_reward)
            return # End the episode, since the dealer has blackjack.
        elif initial_winners:
            # Case: Some agents have blackjack and the dealer does not
            for agent in initial_winners:
                agent.rewardUpdate(agent.win_reward)
            return # End the episode, since we have winners

        # If there is no initial blackjack, each agent takes a turn.
        for agent in self.agents:
            action = Action.HIT
            while action != Action.STAND:
                action = agent.playTurn(dealer_hand_hide)
                if action == Action.HIT:
                    self.dealer.deal(agent)
                    agent.stateUpdate(dealer_hand_hide)
                    if agent.calculateHand() > 21:
                        agent.rewardUpdate(agent.loss_reward)
                        break # No further action, agent busted
            agent.stateUpdate(dealer_hand_hide)

        # Dealers turn ONLY if an agent has not busted
        if any(agent.calculateHand() <= 21 for agent in self.agents):
            self.dealer.playTurn()

        dealer_hand_final = self.dealer.calculateHand()
        for agent in self.agents:
            agent.stateUpdate(dealer_hand_final)
            agent_hand = agent.calculateHand()
            if agent_hand > 21: # Agent busts
                agent.rewardUpdate(agent.loss_reward)
            elif dealer_hand_final > 21 or agent_hand > dealer_hand_final:
                # Logic issue. Any agent with a hand higher than dealer will win.
                agent.rewardUpdate(agent.win_reward)
            elif agent_hand == dealer_hand_final:
                agent.rewardUpdate(agent.draw_reward)
            else:
                agent.rewardUpdate(agent.loss_reward)


if __name__ == "__main__":
    shoe = Shoe()
    dealer = Dealer(shoe)
    table = Table(shoe, dealer)

    agent = Agent()

    table.add(agent)


    episode_count=500000
    for _ in tqdm(range(episode_count), desc="Running Episodes...", bar_format="{desc} ({n_fmt} of {total_fmt})"):
        table.dealInitial()
        table.playEpisode()
        table.reset()

   # print(agent.policy.state_values)
   # print(len(agent.policy.state_values))

    visualizer = BlackjackPolicyVisualizer(state_values = agent.policy.state_values)
    visualizer.plot_state_values(usable_ace_p=True)

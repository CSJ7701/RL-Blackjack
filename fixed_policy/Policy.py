from Actions import Action
from typing import Dict, Tuple
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from PIL import Image


class Policy:
    def __init__(self, cutoff: int):
        self.cutoff = cutoff
        self.state_values: Dict[Tuple[int,int,bool],float] = {}
        self.state_counts: Dict[Tuple[int,int,bool],int] = {}
        # State values are a dict that associates (agent_hand, dealer_hand, usable_ace) with an value between 0 and 1.


    def chooseAction(self, hand: int) -> Action:
        """
        Takes a hand value and returns the action to take
        """
        if hand < self.cutoff:
            return Action.HIT
        return Action.STAND


    def update(self, state: Tuple[int,int,bool], reward: int) -> None:
        """
        Updates the state_values dictionary with a running average for the given state and reward.
        """
        # Insert entry into self.state_values with state as key and reward as value.
        # If this is the first time we have visited a state, simply insert the reward as the dict value.
        # If we have visited this state before, reward should be a running average.
        if state in self.state_values:
            # Update visit count
            self.state_counts[state] += 1
            # Compute new average
            self.state_values[state] += (reward - self.state_values[state]) / self.state_counts[state]
        else:
            # First visit to this state
            self.state_values[state] = reward
            self.state_counts[state] = 1

    def stateValuePlot(self, usable_ace_p: bool, save_path = None):

        # Filter states based on usable_ace_p
        filtered_states = {(agent, dealer): score for (agent, dealer, ace), score in self.state_values.items() if ace == usable_ace_p}

        # Lists for filtered data
        agent_hands = np.array([state[0] for state in filtered_states.keys()])
        dealer_hands = np.array([state[1] for state in filtered_states.keys()])
        scores = np.array(list(filtered_states.values()))

        # 3d plot
        fig = plt.figure()
        ax = fig.add_subplot(111,projection = '3d')

        # Plotting the 3d surface
        ax.plot_trisurf(agent_hands, dealer_hands, scores, cmap="viridis", edgecolor="none")

        # Limits
        # These values come from the example in my RL textbook.
        ax.set_xlim(12,21)
        ax.set_ylim(1,11)
        
        # Labels
        ax.set_xlabel("Agent Hand")
        ax.set_ylabel("Dealer Hand")
        ax.set_zlabel("Score")

        if save_path:
            plt.savefig(save_path)
            print(f"Plot saved to {save_path}")

            image = Image.open(save_path + ".png")
            image.show()
        else:
            plt.show()

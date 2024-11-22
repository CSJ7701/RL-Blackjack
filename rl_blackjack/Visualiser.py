import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from Shoe import Shoe
from Agent import Agent
from Dealer import Dealer
from MonteCarlo import MonteCarlo
from Table import Table

class Visualizer:
    def __init__(self, generation_count, episode_count, epsilon, save_path="training_visualization.mp4"):
        self.generation_count = generation_count
        self.episode_count = episode_count
        self.epsilon = epsilon
        self.save_path = save_path

        # Initialize win rates and generations
        self.win_rates = []
        self.generations = []

        # Set up the plot
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], label="Win Rate")
        self.ax.set_xlim(0, generation_count)
        self.ax.set_ylim(0, 1)
        self.ax.set_title("Agent Win Rate Over Generations")
        self.ax.set_xlabel("Generation")
        self.ax.set_ylabel("Win Rate")
        self.ax.legend()

        # Set up the blackjack environment
        self.shoe = Shoe()
        self.dealer = Dealer(self.shoe)
        self.table = Table(self.shoe, self.dealer)
        self.policy = MonteCarlo()
        self.agent = Agent(self.policy)
        self.table.add(self.agent)

    def update_plot(self, generation, win_rate):
        """Update data and redraw the plot."""
        self.generations.append(generation)
        self.win_rates.append(win_rate)
        self.line.set_data(self.generations, self.win_rates)

    def play_generation(self, generation):
        """Simulates a generation and computes the win rate."""
        print(f"Starting generation {generation + 1}...")
        self.policy.update_actions(self.epsilon)
        wins = 0

        for _ in range(self.episode_count):
            self.table.dealInitial()
            self.table.playEpisode()  # Assume this returns the winner

            agent_val = self.agent.calculateHand()
            dealer_val = self.dealer.calculateHand()

            if agent_val > 21:
                wins += 0
            elif dealer_val > 21:
                wins += 1
            elif agent_val > dealer_val:
                wins += 1
            elif agent_val < dealer_val:
                wins += 0
            else:
                wins += 0.5
            self.table.reset()

        win_rate = wins / self.episode_count
        print(f"Generation {generation + 1} complete. Win rate: {win_rate:.2f}")
        return win_rate

    def save_animation(self):
        """Save the animation to a file."""
        def animate(frame):
            win_rate = self.play_generation(frame)
            self.update_plot(frame + 1, win_rate)
            return self.line,

        ani = FuncAnimation(
            self.fig, animate, frames=self.generation_count, interval=200, blit=True
        )
        ani.save(self.save_path, writer="ffmpeg")
        print(f"Visualization saved to {self.save_path}")


# Example usage
if __name__ == "__main__":
    # Total number of generations
    generation_count = 1000
    
    # Number of episodes per generation
    episode_count = 100000

    # Exploration rate
    epsilon = 0.05

    save_path = "training_visualization.mp4"  # File to save the animation

    visualizer = Visualizer(generation_count, episode_count, epsilon, save_path)
    visualizer.save_animation()

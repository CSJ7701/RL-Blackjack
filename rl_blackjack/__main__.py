import argparse
from collections import deque
import os
from Shoe import Shoe
from Dealer import Dealer
from Table import Table
from Agent import Agent
from Actions import Action
from MonteCarlo import MonteCarlo
from pprint import pprint

def train_agent(episode_count: int, generation_count: int, epsilon: float, save_policy_name: str) -> None:
    shoe=Shoe()
    dealer=Dealer(shoe)
    table=Table(shoe,dealer)
    policy=MonteCarlo()

    if os.path.exists(f"{save_policy_name}.MonteCarlo"):
        policy.load(save_policy_name)

    table.add(Agent(policy))

    for generation in range(generation_count):
        print(f"Starting generation {generation+1}...")
        policy.update_actions(epsilon)
        for _ in range(episode_count):
            table.dealInitial()
            table.playEpisode()
            table.reset()
        print(f"Generation {generation+1} complete.")

    policy.save(save_policy_name)
    print(f"Training complete. Policy saved as '{save_policy_name}.MonteCarlo'")

def evaluate_agent(episodes:int, policy_name: str = None) -> None:
    shoe = Shoe()
    dealer=Dealer(shoe)
    table=Table(shoe, dealer)
    policy = MonteCarlo()

    if policy_name:
        policy.load(policy_name)
        print(f"Loaded policy from {policy_name}.MonteCarlo")
    agent = Agent(policy)
    table.add(agent)

    # Track Stats
    wins = 0
    losses = 0
    draws = 0
    win_rates = []
    running_win_rate = []

    window_size = 1000
    recent_results = deque(maxlen=window_size)

    print(f"\nEvaluating agent over {episodes} episodes...")

    for episode in range(episodes):
        table.dealInitial()
        table.playEpisode()

        agent_val = agent.calculateHand()
        dealer_val = dealer.calculateHand()

        if agent_val > 21:
            losses += 1
            recent_results.append(0)
        elif dealer_val > 21:
            wins += 1
            recent_results.append(1)
        elif agent_val > dealer_val:
            wins += 1
            recent_results.append(1)
        elif agent_val < dealer_val:
            losses += 1
            recent_results.append(0)
        else:
            draws += 1
            recent_results.append(0.5)

        # Calculate instantaneous win rate
        current_win_rate = (wins / (episode + 1))*100
        win_rates.append(current_win_rate)

        # Running Avg with window
        if episode < window_size:
            running_avg = sum(recent_results) / len(recent_results) * 100
        else:
            running_avg = sum(recent_results) / window_size * 100
        running_win_rate.append(running_avg)

        table.reset()

        # Progress update every 10% of episodes
        if (episode + 1) % (episodes // 10) == 0:
            print(f"Completed {episode+1}/{episodes} episodes...")
            print(f"Current running win rate (last {window_size} episodes): {running_avg:.1f}%")

    # Final win statistics
    total_games = wins+losses+draws
    win_rate = (wins/total_games)*100
    loss_rate = (losses/total_games)*100
    draw_rate = (draws/total_games)*100
    final_running_avg = sum(recent_results) / len(recent_results) * 100

    print("\n===== Final Statistics =====")
    print(f"Total Games: {total_games}")
    print(f"Wins: {wins} ({win_rate:.1f}%)")
    print(f"Losses: {losses} ({loss_rate:.1f}%)")
    print(f"Draws: {draws} ({draw_rate:.1f}%)")
    print(f"Final {window_size}-episode running win rate: {final_running_avg:.1f}%")

    #print(agent.policy.policy)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a Blackjack RL simulation or interactive game.")
    parser.add_argument("--train", type=int, help="Train a new agent with the specified number of episodes.")
    parser.add_argument("--eval", type=int, help="Evaluate an agent over the specified number of episodes.")
    parser.add_argument("--policy", type=str, help="Policy filename base (without extension) for saving or loading.")
    parser.add_argument("--inspect", type=str, help="Policy filename to inspect.")
    parser.add_argument("--gen", type=int, help="Number of generations to run. Default 50.")
    parser.add_argument("--epsilon", type=float, help="Probability of choosing a random action. Defualt 0.05 (5%).")
    args = parser.parse_args()

    if args.gen:
        generations = args.gen
    else:
        generations = 50

    if args.epsilon:
        epsilon = args.epsilon
    else:
        epsilon = 0.05
        
    if args.train:
        if not args.policy:
            print("Please provide a policy name with --policy to save the training results.")
        else:
            print(generations)
            print(epsilon)
            train_agent(args.train, generations, epsilon, args.policy)
    elif args.eval:
        evaluate_agent(args.eval, args.policy)
    elif args.inspect:
        policy = MonteCarlo()
        policy.load(args.inspect)
        pprint(policy.actions)
    else:
        print("Please specify --train or --play along with necessary arguments.")

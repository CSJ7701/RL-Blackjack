import numpy as np
import plotly.graph_objects as go

class BlackjackPolicyVisualizer:
    def __init__(self, state_values):
        # Store the dictionary of state values
        self.state_values = state_values

    def plot_state_values(self, usable_ace_p: bool):
        # Filter states based on usable_ace_p value
        filtered_states = {(agent, dealer): score for (agent, dealer, ace), score in self.state_values.items() if ace == usable_ace_p}

        # Prepare lists for the filtered data
        agent_hands = np.array([state[0] for state in filtered_states.keys()])
        dealer_hands = np.array([state[1] for state in filtered_states.keys()])
        scores = np.array(list(filtered_states.values()))

        # Create a Plotly 3D scatter plot
        fig = go.Figure(data=[go.Mesh3d(
            x=agent_hands,
            y=dealer_hands,
            z=scores,
            opacity=0.5,
            colorscale="Viridis"
        )])

        # Set labels and title
        fig.update_layout(
            scene=dict(
                xaxis_title='Agent Hand',
                yaxis_title='Dealer Hand',
                zaxis_title='Score'
            ),
            title="3D Plot of Blackjack Policy State Values"
        )

        # Show the interactive plot
        fig.show()

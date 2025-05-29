import pickle
import random
import numpy as np


class SARSA:
    def __init__(self, env, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.1):
        self.env = env
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.epsilon_decay = epsilon_decay  # Decay rate for epsilon
        self.min_epsilon = min_epsilon  # Minimum epsilon value
        self.q_table = {}  # Q-table for storing state-action values

    def state_to_key(self, state):
        if isinstance(state, np.ndarray):
            return tuple(state.flatten())
        elif isinstance(state, (list, tuple)):
            return tuple(self.state_to_key(s) for s in state)
        elif isinstance(state, dict):
            return tuple((k, self.state_to_key(v)) for k, v in sorted(state.items()))
        else:
            return (state,)

    def get_action(self, state):
        state_key = self.state_to_key(state)
        if random.uniform(0, 1) < self.epsilon:
            return self.env.action_space.sample()
        else:
            state_actions = self.q_table.get(state_key, {})
            if not state_actions:
                return self.env.action_space.sample()
            return max(state_actions, key=state_actions.get)

    def decay_epsilon(self):
        """
        Decay epsilon after each episode to balance exploration and exploitation.
        """
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def train(self, num_episodes=1000):
        """
        Train the agent using SARSA. It updates the Q-values for state-action pairs based on the rewards received
        and the Q-value of the next state-action pair.
        :param num_episodes: Number of episodes to train the agent for.
        :return: Q-table with learned state-action values.
        """
        for episode in range(num_episodes):
            state = self.env.reset()[0]
            state_key = self.state_to_key(state)
            action = self.get_action(state)
            done = False

            while not done:
                next_state, reward, terminated, truncated, _ = self.env.step(action)
                done = terminated or truncated
                next_state_key = self.state_to_key(next_state)
                next_action = self.get_action(next_state)

                # Inicializa os dicionários se necessário
                if state_key not in self.q_table:
                    self.q_table[state_key] = {}
                if action not in self.q_table[state_key]:
                    self.q_table[state_key][action] = 0.0
                if next_state_key not in self.q_table:
                    self.q_table[next_state_key] = {}
                if next_action not in self.q_table[next_state_key]:
                    self.q_table[next_state_key][next_action] = 0.0

                # Atualiza a Q-table com a fórmula SARSA
                old_value = self.q_table[state_key][action]
                next_value = self.q_table[next_state_key][next_action]
                self.q_table[state_key][action] = old_value + self.alpha * (reward + self.gamma * next_value - old_value)

                state_key = next_state_key
                action = next_action

            self.decay_epsilon()

        return self.q_table

    def test(self, num_episodes=100):
        """
        Run the environment using the learned policy to evaluate performance.
        :param num_episodes: Number of episodes to run for testing.
        """
        self.set_epsilon_to_min()
        total_rewards = []

        for episode in range(num_episodes):
            state = self.env.reset()[0]
            done = False
            episode_reward = 0

            while not done:
                action = self.get_action(state)
                next_state, reward, terminated, truncated, _ = self.env.step(action)
                done = terminated or truncated
                episode_reward += reward
                state = next_state

            total_rewards.append(episode_reward)

        avg_reward = np.mean(total_rewards)
        print(f"Recompensa média durante o teste: {avg_reward}")

    def save_q_table(self, filename='models/sarsa.pkl'):
        """
        Save the Q-table to a file using pickle.
        :param filename: Name of the file to save the Q-table to.
        """
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filename='models/sarsa.pkl'):
        """
        Load the Q-table from a file using pickle.
        :param filename: Name of the file to load the Q-table from.
        """
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)

    def set_epsilon_to_min(self):
        """
        Set epsilon to its minimum value to focus on exploitation.
        """
        self.epsilon = self.min_epsilon

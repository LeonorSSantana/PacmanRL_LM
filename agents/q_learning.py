import pickle
import random
import numpy as np



class QLearning:
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
            # Recursively convert elements inside list/tuple
            return tuple(self.state_to_key(s) for s in state)
        elif isinstance(state, dict):
            # Recursively convert dict items
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
        Train the agent using Q-learning. It updates the Q-values for state-action pairs based on the rewards received.
        :param num_episodes: Number of episodes to train the agent for.
        :return: Q-table with learned state-action values.
        """
        for episode in range(num_episodes):
            obs = self.env.reset()
            state = obs[0] if isinstance(obs, tuple) else obs
            state_key = self.state_to_key(state)

            done = False

            while not done:
                action = self.get_action(state)

                next_state, reward, terminated, truncated, _ = self.env.step(action)
                next_state_key = self.state_to_key(next_state)
                done = terminated or truncated

                if state_key not in self.q_table:
                    self.q_table[state_key] = {}
                if action not in self.q_table[state_key]:
                    self.q_table[state_key][action] = 0.0
                if next_state_key not in self.q_table:
                    self.q_table[next_state_key] = {}

                next_max = max(self.q_table[next_state_key].values()) if self.q_table[next_state_key] else 0.0
                old_value = self.q_table[state_key][action]
                self.q_table[state_key][action] = old_value + self.alpha * (reward + self.gamma * next_max - old_value)

                state = next_state
                state_key = next_state_key

            self.decay_epsilon()

        return self.q_table

    def test(self, num_episodes=100, load_model=True):
        """
        Run the environment using the learned policy to evaluate performance.
        :param num_episodes: Number of episodes to run for testing.
        """
        if load_model:
            try:
                self.load_q_table()
                print("[INFO] Q-table carregada com sucesso.")
                print(f"[DEBUG] Tamanho da Q-table: {len(self.q_table)}")
            except FileNotFoundError:
                print("[WARNING] Ficheiro de Q-table não encontrado. A testar com Q-table vazia.")

        self.epsilon = 0.0
        total_rewards = []
        collected_pellets_all = []

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
            collected_pellets = 30 - self.env.remaining_pellets
            collected_pellets_all.append(collected_pellets)

        avg_reward = np.mean(total_rewards)
        avg_collected = np.mean(collected_pellets_all)
        print(f"Recompensa média durante o teste: {round(avg_reward,2)}")
        print(f"Média de pellets recolhidas durante o teste: {(avg_collected)}")


    def save_q_table(self, filename='models/q_learning_solution.pkl'):
        """
        Save the Q-table to a file using pickle.
        :param filename: Name of the file to save the Q-table to.
        """
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filename='models/q_learning_solution.pkl'):
        """
        Load the Q-table from a file using pickle.
        :param filename:
        """
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)

    def set_epsilon_to_min(self):
        """
        Set epsilon to its minimum value to focus on exploitation.
        """
        self.epsilon = self.min_epsilon

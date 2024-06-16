import pickle


class QLearning:
    def __init__(self, env, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.1):
        self.env = env
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.epsilon_decay = epsilon_decay  # Decay rate for epsilon
        self.min_epsilon = min_epsilon  # Minimum epsilon value
        self.q_table = {}  # Q-table for storing state-action values

    def get_action(self, state):
        pass

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
        pass

    def test(self, num_episodes=100):
        """
        Run the environment using the learned policy to evaluate performance.
        :param num_episodes: Number of episodes to run for testing.
        """
        pass

    def save_q_table(self, filename='models/q_learning.pkl'):
        """
        Save the Q-table to a file using pickle.
        :param filename: Name of the file to save the Q-table to.
        """
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filename='models/q_learning.pkl'):
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

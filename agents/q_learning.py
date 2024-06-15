import numpy as np
import random
import pickle


class QLearning:
    def __init__(self, env, alpha=0.1, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.1):
        self.env = env
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.epsilon_decay = epsilon_decay  # Decay rate for epsilon
        self.min_epsilon = min_epsilon  # Minimum epsilon value
        self.q_table = {}  # Q-table for storing state-action values

    def get_state(self):
        # Convert the agent's position and direction into a tuple representing the state
        state = (self.env.agent_pos, self.env.agent_dir)
        return state

    def get_action(self, state):
        # Epsilon-greedy action selection
        if random.uniform(0, 1) < self.epsilon:
            return self.env.action_space.sample()  # Explore: select a random action
        else:
            # Exploit: select the action with max Q-value for the current state
            q_values = self.q_table.get(state, [0] * self.env.action_space.n)
            return np.argmax(q_values)

    def update_q_table(self, state, action, reward, next_state):
        # Initialize Q-values for the states if they are not present in the Q-table
        if state not in self.q_table:
            self.q_table[state] = [0] * self.env.action_space.n
        if next_state not in self.q_table:
            self.q_table[next_state] = [0] * self.env.action_space.n

        # Q-learning update rule
        old_value = self.q_table[state][action]
        next_max = max(self.q_table[next_state])
        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        self.q_table[state][action] = new_value

    def decay_epsilon(self):
        # Decay epsilon after each episode to reduce exploration over time
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def train(self, num_episodes=1000):
        self.env.reset()
        for episode in range(num_episodes):
            state = self.get_state()
            done = False
            total_reward = 0

            while not done:
                action = self.get_action(state)
                obs, reward, terminated, truncated, _ = self.env.step(action)
                next_state = self.get_state()

                # Update Q-values
                self.update_q_table(state, action, reward, next_state)

                state = next_state
                total_reward += reward

                if terminated or truncated:
                    self.env.reset()
                    done = True

            # Decay epsilon after each episode
            self.decay_epsilon()

            print(f"Episode {episode + 1}/{num_episodes}, Total Reward: {total_reward}, Epsilon: {self.epsilon}")

    def save_q_table(self, filename='q_table.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filename='q_table.pkl'):
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)
